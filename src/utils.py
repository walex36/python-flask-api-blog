from flask_jwt_extended import get_jwt_identity
from src.hello import User, db
from http import HTTPStatus
from functools import wraps

def required_role(role_name):
    def decorator(f):
            @wraps(f)
            def wrapperd(*args, **kwargs):
                user_id = get_jwt_identity()
                user = db.get_or_404(User, user_id)
                
                if user.role.name != role_name:
                    return {"message": "Permission denied"}, HTTPStatus.FORBIDDEN
                
                return f(*args, **kwargs)
            return wrapperd
    return decorator