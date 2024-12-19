from flask import Blueprint, request
from src.hello import User, db
from http import HTTPStatus, HTTPMethod
from flask_jwt_extended import create_access_token
from sqlalchemy import select

app = Blueprint('auth', __name__, url_prefix='/auth')

@app.route("/login", methods=[HTTPMethod.POST])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    user = db.session.execute(select(User).where(User.username == username)).scalar_one_or_none()
    
    if user is None or user.password != password:
        return {"message": "Bad username or password"}, HTTPStatus.UNAUTHORIZED
    
    access_token = create_access_token(identity=str(user.id))
    return {'access_token': access_token}, HTTPStatus.OK