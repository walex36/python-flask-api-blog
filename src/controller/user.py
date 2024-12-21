from flask import Blueprint, request
from src.models import db, User
from src.utils import required_role
from http import HTTPStatus, HTTPMethod
from flask_jwt_extended import jwt_required

app = Blueprint('user', __name__, url_prefix='/users')

def _create_user():
    data = request.json
    user = User(username=data["username"], password=data["password"], role_id=data["role_id"])
    db.session.add(user)
    db.session.commit()


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars().all()
    return [
        {
         "id": user.id, 
         "username": user.username,
         "role": {
             "id": user.role.id,
             "name": user.role.name
             }
         } for user in users
    ]


@app.route('/', methods=[HTTPMethod.GET, HTTPMethod.POST])
@jwt_required()
@required_role("admin")
def handler_user():   
    if request.method == "POST":
        _create_user()
        return {"message": "User created!"}, HTTPStatus.CREATED
    elif request.method == "GET":
        return {"users":  _list_users()}, HTTPStatus.OK
    else:
        return {"message": "Method not allowed"}, HTTPStatus.METHOD_NOT_ALLOWED
        

@app.route('/<int:user_id>', methods=[HTTPMethod.GET, HTTPMethod.PATCH, HTTPMethod.DELETE])
def handler_user_id(user_id):
    if request.method == HTTPMethod.GET:
        user = db.get_or_404(User, user_id)
        return {"id": user.id, "username": user.username}, HTTPStatus.OK
    elif request.method == HTTPMethod.PATCH:
        data = request.json

        if "username" in data:
            user.username = data["username"]

        if "password" in data:
            user.password = data["password"]

        user = db.get_or_404(User, user_id)
        db.session.commit()

        return {"id": user.id, "username": user.username}, HTTPStatus.OK
    elif request.method == HTTPMethod.DELETE:
        user = db.get_or_404(User, user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted!"}, HTTPStatus.OK
    else:
        return {"message": "Method not allowed"}, HTTPStatus.METHOD_NOT_ALLOWED