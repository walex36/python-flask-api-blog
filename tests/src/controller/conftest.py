import pytest
from app import create_app, db, User, Role

@pytest.fixture
def app():
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def access_token(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    
    user = User(username="test", password="test", role_id=1)
    db.session.add(user)
    db.session.commit()
    
    result = client.post("/auth/login", json={"username": user.username, "password": user.password})
    return result.json["access_token"]