from flask import Blueprint, request
from src.hello import User, db
from http import HTTPStatus

app = Blueprint('user', __name__, url_prefix='/users')


def _create_user():
    data = request.json
    user = User(username=data["username"], password=data["password"])
    db.session.add(user)
    db.session.commit()

def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars().all()
    return [
        {"id": user.id, "username": user.username} for user in users
    ]


@app.route('/', methods=["GET", "POST"])
def handler_user():
    if request.method == "POST":
        _create_user()
        return {"message": "User created!"}, HTTPStatus.CREATED
    else:
        return {"users":  _list_users()}, HTTPStatus.OK
        

@app.route('/<int:user_id>', methods=["GET", "PATCH", "DELETE"])
def handler_user_id(user_id):
    if request.method == "GET":
        user = db.get_or_404(User, user_id)
        return {"id": user.id, "username": user.username}, HTTPStatus.OK
    elif request.method == "PATCH":
        data = request.json

        if "username" in data:
            user.username = data["username"]

        if "password" in data:
            user.password = data["password"]

        user = db.get_or_404(User, user_id)
        db.session.commit()

        return {"id": user.id, "username": user.username}, HTTPStatus.OK
    else:
        user = db.get_or_404(User, user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted!"}, HTTPStatus.OK