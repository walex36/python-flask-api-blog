from flask import Blueprint, request
from src.hello import Post, db
from http import HTTPStatus, HTTPMethod
from sqlalchemy import inspect

app = Blueprint('post', __name__, url_prefix='/posts')


@app.route("/", methods=[HTTPMethod.GET, HTTPMethod.POST])
def handler_post():
    if request.method == HTTPMethod.GET:
        return {"posts": _list_posts()}, HTTPStatus.OK
    elif request.method == HTTPMethod.POST:
        _create_post()
        return {"messsage": "Post created!"}, HTTPStatus.CREATED

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
    return [
        {
         "id": post.id, 
         "author_id": post.author_id, 
         "created": post.created, 
         "title": post.title, 
         "body": post.body,
        } for post in posts
    ]

def _post_by_id(post_id):
    post = db.get_or_404(Post, post_id)
    return {
        "id": post.id, 
        "author_id": post.author_id, 
        "created": post.created, 
        "title": post.title, 
        "body": post.body,
    }

def _create_post():
    data = request.json
    post = Post(
        author_id = data["author_id"],
        title = data["title"],
        body = data["body"],
    )
    db.session.add(post)
    db.session.commit()

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