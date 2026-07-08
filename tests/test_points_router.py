import pytest
from fastapi import HTTPException, status

from pin_voyage.exceptions import PointNotFoundException
from pin_voyage.points_crud import router as router_module
from pin_voyage.schemas import PointCreate, PointUpdate


class RecordingRepository:
    def __init__(self, db):
        self.db = db

    def list(self):
        return ["point-1", "point-2"]

    def get_by_id(self, point_id):
        return {"id": point_id}

    def create(self, payload):
        return {"payload": payload}

    def update(self, point_id, payload):
        return {"id": point_id, "payload": payload}

    def delete(self, point_id):
        return {"deleted": point_id}


class MissingPointRepository(RecordingRepository):
    def get_by_id(self, point_id):
        raise PointNotFoundException(f"Point {point_id} not found")


def test_list_points_delegates_to_repository(monkeypatch):
    monkeypatch.setattr(router_module, "PointRepository", RecordingRepository)

    assert router_module.list_points(db=object()) == ["point-1", "point-2"]


def test_get_point_delegates_to_repository(monkeypatch):
    monkeypatch.setattr(router_module, "PointRepository", RecordingRepository)

    assert router_module.get_point(7, db=object()) == {"id": 7}


def test_get_point_maps_not_found_exception_to_http_404(monkeypatch):
    monkeypatch.setattr(router_module, "PointRepository", MissingPointRepository)

    with pytest.raises(HTTPException) as exc_info:
        router_module.get_point(7, db=object())

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Point 7 not found"


def test_create_points_delegates_to_repository(monkeypatch):
    monkeypatch.setattr(router_module, "PointRepository", RecordingRepository)
    payload = PointCreate(
        name="Cafe",
        description=None,
        created_by="alice",
        geom_lat=52.1,
        geom_lon=21.0,
    )

    assert router_module.create_points(payload, db=object()) == {"payload": payload}


def test_update_point_delegates_to_repository(monkeypatch):
    monkeypatch.setattr(router_module, "PointRepository", RecordingRepository)
    payload = PointUpdate(name="Cafe", description=None, created_by="alice")

    assert router_module.update_point(3, payload, db=object()) == {
        "id": 3,
        "payload": payload,
    }


def test_delete_point_delegates_to_repository(monkeypatch):
    monkeypatch.setattr(router_module, "PointRepository", RecordingRepository)

    assert router_module.delete_point(3, db=object()) == {"deleted": 3}
