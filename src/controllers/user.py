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
    """User handler admin.
    ---
    get:
      summary: List users
      description: List users
      tags:
        - User
      responses:
        200:
          description: Users successfully found
          content:
            application/json:
              schema:
                type: object
                properties:
                  users:
                    type: array
                    items:
                      type: object
                      properties:
                        username:
                          type: string
                        role_id:
                          type: integer
    post:
      summary: Create a user
      description: Create a user
      tags:
        - User
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateUserSchema
      responses:
        201:
          description: User successfully created
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "User created!"
        422:
          description: Validation error
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "Validation error"
                  errors:
                    type: array
                    items:
                      type: object
                      properties:
                        username:
                          type: array
                          items:
                            type: string
                            example: ["Username is required"]
                        password:
                          type: array
                          items:
                            type: string
                            example: ["Password is required"]
                        role_id:
                          type: array
                          items:
                            type: string
                            example: ["Role ID is required"]
        401:
          description: Unauthorized
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "Unauthorized"
        403:
          description: Forbidden
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "Forbidden"
    """
    if request.method == "POST":
        return _create_user()
    elif request.method == "GET":
        return {"users":  _list_users()}, HTTPStatus.OK
    else:
        return {"message": "Method not allowed"}, HTTPStatus.METHOD_NOT_ALLOWED
        

@app.route('/<int:user_id>', methods=[HTTPMethod.GET, HTTPMethod.PATCH, HTTPMethod.DELETE])
def handler_user_id(user_id):
    """User handler by id.
    ---
    get:
      summary: Get a user
      description: Get a user
      tags:
        - User
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
          required: true
          description: User ID
      responses:
        200:
          description: User successfully found
          content:
            application/json:
              schema: UserSchema
        404:
          description: User not found
    patch:
      summary: Update a user
      description: Update a user
      tags:
        - User
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
          required: true
          description: User ID
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                password:
                  type: string
                role_id:
                  type: integer
      responses:
        200:
          description: User successfully updated
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                  username:
                    type: string
        404:
          description: User not found
    delete:
      summary: Delete a user
      description: Delete a user
      tags:
        - User
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
          required: true
          description: User ID
      responses:
        200:
          description: User successfully deleted
        404:
          description: User not found
    """
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