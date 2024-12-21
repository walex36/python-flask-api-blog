from flask import Blueprint, request
from src.models import db, User
from src.utils import required_role
from http import HTTPStatus, HTTPMethod
from flask_jwt_extended import jwt_required
from src.app import bcrypt
from src.views.user_view import UserSchema, CreateUserSchema
from marshmallow import ValidationError

app = Blueprint('user', __name__, url_prefix='/users')

def _create_user():  
    user_schema = CreateUserSchema()
    try:
        data = user_schema.load(request.json)
    except ValidationError as err:
        return err.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    user = User(
            username=data["username"], 
            password=bcrypt.generate_password_hash(data["password"]), 
            role_id=data["role_id"])
    db.session.add(user)
    db.session.commit()
    return {"message": "User created!"}, HTTPStatus.CREATED


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars().all()
    
    users_schema = UserSchema(many=True)
    return users_schema.dump(users)
    


@app.route('/', methods=[HTTPMethod.GET, HTTPMethod.POST])
@jwt_required()
@required_role("admin")
def handler_user():   
    if request.method == "POST":
        return _create_user()
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