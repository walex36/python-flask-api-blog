from flask import Blueprint, request
from src.models import User, db
from http import HTTPStatus, HTTPMethod
from flask_jwt_extended import create_access_token
from sqlalchemy import select
from src.app import bcrypt

app = Blueprint('auth', __name__, url_prefix='/auth')

def _check_password(password_hash, password_raw):
    return bcrypt.check_password_hash(password_hash, password_raw)

@app.route("/login", methods=[HTTPMethod.POST])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    user = db.session.execute(select(User).where(User.username == username)).scalar_one_or_none()
    
    if user is None or not _check_password(user.password, password):
        return {"message": "Bad username or password"}, HTTPStatus.UNAUTHORIZED
    
    access_token = create_access_token(identity=str(user.id))
    return {'access_token': access_token}, HTTPStatus.OK