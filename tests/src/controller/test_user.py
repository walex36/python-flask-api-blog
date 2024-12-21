from http import HTTPStatus
from app import User, Role, db
from sqlalchemy import select


def test_get_user_success(client):
    # Arrange
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    
    user = User(username="test", password="test", role_id=1)
    db.session.add(user)
    db.session.commit()
     
    # Act
    response = client.get(f"/users/{user.id}")
    
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"id": user.id, "username": user.username}
    
def test_get_user_not_found(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    
    user_id = 1
     
    response = client.get(f"/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    
def test_create_user_success(client, access_token):
    # Arrange
    role_id = db.session.query(Role).filter(Role.name == "admin").first().id
    payload = {"username": "test1", "password": "test1", "role_id": role_id}
    
    # Act
    response = client.post("/users/", json=payload, headers={"Authorization": f"Bearer {access_token}"})
    
    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'message': 'User created!'}
    assert db.session.query(User).count() == 2
    
def test_list_users_success(client, access_token):
    # Arrange
    user = db.session.query(User).filter(User.username == "test").first()
    
    # Act
    response = client.get("/users/", headers={"Authorization": f"Bearer {access_token}"})
    
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"users": [{"id": user.id, "username": user.username, "role": {"id": user.role.id, "name": user.role.name}}]}