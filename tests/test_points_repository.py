import pytest
from fastapi import HTTPException, status
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Point as ShapelyPoint

from pin_voyage.models import Point
from pin_voyage.points_crud.repository import PointRepository
from pin_voyage.schemas import PointCreate, PointUpdate


class FakeScalarResult:
    def __init__(self, value):
        self.value = value

    def all(self):
        return self.value

    def first(self):
        return self.value


class FakeExecuteResult:
    def __init__(self, value):
        self.value = value

    def scalars(self):
        return FakeScalarResult(self.value)


class FakeSession:
    def __init__(self, point=None, execute_value=None):
        self.point = point
        self.execute_value = execute_value
        self.added = []
        self.deleted = []
        self.commits = 0
        self.refreshes = []

    def add(self, point):
        self.added.append(point)

    def commit(self):
        self.commits += 1

    def delete(self, point):
        self.deleted.append(point)

    def execute(self, statement):
        self.last_statement = statement
        return FakeExecuteResult(self.execute_value)

    def get(self, model, point_id):
        self.get_args = (model, point_id)
        return self.point

    def refresh(self, point):
        self.refreshes.append(point)


def make_point(
    *,
    point_id: int = 1,
    name: str | None = "Museum",
    description: str | None = "Open daily",
    created_by: str | None = "alice",
    lon: float = 19.0402,
    lat: float = 47.4979,
) -> Point:
    return Point(
        id=point_id,
        name=name,
        description=description,
        created_by=created_by,
        geom=from_shape(ShapelyPoint(lon, lat), srid=4326),
    )


def test_get_by_id_returns_first_matching_point():
    point = make_point()
    repo = PointRepository(FakeSession(execute_value=point))

    assert repo.get_by_id(1) is point


def test_get_by_id_raises_when_point_does_not_exist():
    repo = PointRepository(FakeSession(execute_value=None))

    with pytest.raises(Exception, match="Point not found"):
        repo.get_by_id(404)


def test_create_persists_point_with_expected_shape():
    session = FakeSession()
    repo = PointRepository(session)
    payload = PointCreate(
        name="Park",
        description="Green space",
        created_by="alice",
        geom_lon=21.0122,
        geom_lat=52.2297,
    )

    point = repo.create(payload)

    assert point in session.added
    assert session.commits == 1
    assert session.refreshes == [point]
    assert point.name == "Park"
    assert point.description == "Green space"
    geom = to_shape(point.geom)
    assert geom.x == pytest.approx(21.0122)
    assert geom.y == pytest.approx(52.2297)


def test_update_raises_http_404_when_point_does_not_exist():
    repo = PointRepository(FakeSession(point=None))
    payload = PointUpdate(name=None, description=None, created_by=None)

    with pytest.raises(HTTPException) as exc_info:
        repo.update(404, payload)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Point not found"


def test_update_changes_fields_and_preserves_existing_lon_for_lat_only_update():
    point = make_point(name="Old name", description="Old description")
    session = FakeSession(point=point)
    repo = PointRepository(session)
    payload = PointUpdate(
        name="New name",
        description="New description",
        created_by="bob",
        geom_lat=48.8566,
    )

    updated = repo.update(1, payload)

    assert updated is point
    assert point.name == "New name"
    assert point.description == "New description"
    assert point.created_by == "bob"
    geom = to_shape(point.geom)
    assert geom.x == pytest.approx(19.0402)
    assert geom.y == pytest.approx(48.8566)
    assert session.commits == 1
    assert session.refreshes == [point]


def test_delete_removes_existing_point():
    point = make_point()
    session = FakeSession(point=point)
    repo = PointRepository(session)

    assert repo.delete(1) is None
    assert session.deleted == [point]
    assert session.commits == 1


def test_delete_raises_http_404_when_point_does_not_exist():
    repo = PointRepository(FakeSession(point=None))

    with pytest.raises(HTTPException) as exc_info:
        repo.delete(404)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Point not found"


def test_list_returns_all_points():
    points = [make_point(point_id=1), make_point(point_id=2)]
    repo = PointRepository(FakeSession(execute_value=points))

    assert repo.list() == points
