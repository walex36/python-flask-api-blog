from src.app import ma
from marshmallow import fields
from src.models import Post

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True
        

class CreatePostSchema(ma.Schema):
    author_id = fields.Integer(required=True)
    title = fields.String(required=True)
    body = fields.String(required=True)