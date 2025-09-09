from db import Database
import pytest

@pytest.fixture
def db():
    database = Database()
    yield database # Provide the fixture instance
    database.data.clear()  # Cleanup after test

def test_add_user(db):
    db.add_user(1, "Alice")
    assert db.get_user(1) == "Alice"

def test_add_existing_user(db):
    db.add_user(1, "Alice")
    with pytest.raises(ValueError, match="User already exists"):
        db.add_user(1, "Bob")

def test_delete_user(db):
    db.add_user(1, "Alice")
    db.delete_user(1)
    assert db.get_user(1) is None