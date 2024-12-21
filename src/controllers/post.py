from flask import Blueprint, request
from src.models import db, Post
from http import HTTPStatus, HTTPMethod
from src.views.post_view import PostSchema, CreatePostSchema
from marshmallow import ValidationError

app = Blueprint('post', __name__, url_prefix='/posts')


@app.route("/", methods=[HTTPMethod.GET, HTTPMethod.POST])
def handler_post():
    if request.method == HTTPMethod.GET:
        return {"posts": _list_posts()}, HTTPStatus.OK
    elif request.method == HTTPMethod.POST:
        return _create_post()

@app.route("/<int:post_id>", methods=[HTTPMethod.PATCH, HTTPMethod.DELETE, HTTPMethod.GET])
def handler_post_by_id(post_id):
    match request.method:
        case HTTPMethod.GET:
            post = _post_by_id(post_id)
            return post, HTTPStatus.OK
        case HTTPMethod.PATCH:
            _update_post(post_id)
            return {"message": "Post updated!"}, HTTPStatus.OK
        case HTTPMethod.DELETE:
            _delete_post(post_id)
            return {"message": "Post deleted!"}, HTTPStatus.OK
        case _:
            pass


def _list_posts():
    query = db.select(Post)
    posts = db.session.execute(query).scalars().all()
    posts_schema = PostSchema(many=True)
    return posts_schema.dump(posts)

def _post_by_id(post_id):
    post = db.get_or_404(Post, post_id)
    post_schema = PostSchema()
    return post_schema.dump(post)

def _create_post():
    create_post_schema = CreatePostSchema()
    try:
        data = create_post_schema.load(request.json)
    except ValidationError as err:
        return err.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    post = Post(
        author_id = data["author_id"],
        title = data["title"],
        body = data["body"],
    )
    db.session.add(post)
    db.session.commit()
    return {"messsage": "Post created!"}, HTTPStatus.CREATED

def _update_post(post_id):
    data = request.json
    post = db.get_or_404(Post, post_id)

    mapper = ["title", "body"]
    for column in mapper:
        if column in data:
            setattr(post, column, data[column])

    db.session.commit()

def _delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()