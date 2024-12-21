from src.app import ma
from src.models import Role

class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Role
        
    id = ma.auto_field()
    name = ma.auto_field()