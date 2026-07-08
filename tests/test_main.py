from sqlalchemy import text

from pin_voyage.main import Item, delete_item, home, ping, put_item


class FakeDb:
    def __init__(self, error: Exception | None = None):
        self.error = error
        self.executed_statement = None

    def execute(self, statement):
        self.executed_statement = statement
        if self.error:
            raise self.error


def test_home_returns_hello_world_message():
    assert home() == {"message": "Hello World!"}


def test_put_item_echoes_message():
    assert put_item(Item(message="hello")) == {"message": "hello"}


def test_delete_item_returns_success_message():
    assert delete_item(123) == {"message": "successfully deleted"}


def test_ping_executes_database_probe():
    db = FakeDb()

    assert ping(db) == {"ping": "pong"}
    assert str(db.executed_statement) == str(text("SELECT 1"))


def test_ping_returns_error_message_when_database_probe_fails():
    response = ping(FakeDb(error=RuntimeError("connection refused")))

    assert response == {"error": "connection refused"}
