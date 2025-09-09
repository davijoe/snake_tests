from db import save_user

def test_save_user(mocker):
    # Mock sqlite3.connect to avoid real database operations
    mock_conn = mocker.patch("db.sqlite3.connect")
    mock_cursor = mock_conn.return_value.cursor.return_value

    # Call function
    save_user("Alice", 30)

    # Assert
    mock_conn.assert_called_once_with("users.db")
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30)
    )