import pytest

from pin_voyage import database


class FakeSession:
    def __init__(self):
        self.closed = False
        self.committed = False
        self.rolled_back = False

    def close(self):
        self.closed = True

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True


def test_get_db_commits_and_closes_session(monkeypatch):
    session = FakeSession()
    monkeypatch.setattr(database, "Session", lambda: session)

    db_generator = database.get_db()

    assert next(db_generator) is session
    with pytest.raises(StopIteration):
        next(db_generator)

    assert session.committed is True
    assert session.rolled_back is False
    assert session.closed is True


def test_get_db_rolls_back_closes_and_reraises_on_error(monkeypatch):
    session = FakeSession()
    monkeypatch.setattr(database, "Session", lambda: session)
    db_generator = database.get_db()
    error = RuntimeError("database failure")

    assert next(db_generator) is session
    with pytest.raises(RuntimeError, match="database failure"):
        db_generator.throw(error)

    assert session.committed is False
    assert session.rolled_back is True
    assert session.closed is True
