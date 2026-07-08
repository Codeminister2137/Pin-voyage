from datetime import datetime

import pytest
from geoalchemy2.shape import from_shape
from shapely.geometry import Point as ShapelyPoint

from pin_voyage.models import Point
from pin_voyage.schemas import PointCreate, PointResponse, PointUpdate


def test_point_create_accepts_required_coordinates():
    point = PointCreate(
        name="Library",
        description=None,
        created_by="alice",
        geom_lat=52.2297,
        geom_lon=21.0122,
    )

    assert point.geom_lat == pytest.approx(52.2297)
    assert point.geom_lon == pytest.approx(21.0122)


def test_point_update_allows_omitted_coordinates():
    point_update = PointUpdate(name="Library", description=None, created_by=None)

    assert point_update.geom_lat is None
    assert point_update.geom_lon is None


def test_point_response_converts_model_geometry_to_coordinates():
    created_at = datetime(2026, 1, 2, 3, 4, 5)
    point = Point(
        id=10,
        name="Observation deck",
        description="City view",
        created_by="bob",
        created_at=created_at,
        geom=from_shape(ShapelyPoint(14.4208, 50.088), srid=4326),
    )

    response = PointResponse.model_validate(point)

    assert response.id == 10
    assert response.name == "Observation deck"
    assert response.description == "City view"
    assert response.created_by == "bob"
    assert response.created_at == created_at
    assert response.geom_lon == pytest.approx(14.4208)
    assert response.geom_lat == pytest.approx(50.088)
