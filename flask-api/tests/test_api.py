# tests/test_api.py
import os
import tempfile
import pytest
from app import create_app
from extensions import db as _db
from models import User, Item
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ["JWT_SECRET_KEY"] = "test-jwt-secret"
    app = create_app()
    client = app.test_client()

    # create tables
    with app.app_context():
        _db.create_all()
        # create a test user
        user = User(username="testuser", password=generate_password_hash("pass"))
        _db.session.add(user)
        _db.session.commit()
    yield client

    # teardown
    with app.app_context():
        _db.session.remove()
        _db.drop_all()
    os.close(db_fd)
    os.remove(db_path)

def get_token(client):
    rv = client.post("/auth/login", json={"username": "testuser", "password": "pass"})
    assert rv.status_code == 200
    return rv.get_json()["access_token"]

def test_index(client):
    rv = client.get("/")
    assert rv.status_code == 200

def test_items_crud(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    # create
    rv = client.post("/api/items", json={"name": "item1"}, headers=headers)
    assert rv.status_code == 201
    data = rv.get_json()
    assert data["name"] == "item1"

    item_id = data["id"]
    # get
    rv = client.get(f"/api/items/{item_id}", headers=headers)
    assert rv.status_code == 200
    # update
    rv = client.put(f"/api/items/{item_id}", json={"name": "item-1-updated"}, headers=headers)
    assert rv.status_code == 200
    assert rv.get_json()["name"] == "item-1-updated"
    # list
    rv = client.get("/api/items", headers=headers)
    assert rv.status_code == 200
    # delete
    rv = client.delete(f"/api/items/{item_id}", headers=headers)
    assert rv.status_code == 200
