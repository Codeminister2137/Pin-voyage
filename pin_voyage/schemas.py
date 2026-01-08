from typing import Self

from geoalchemy2.shape import to_shape
from datetime import datetime
from pydantic import BaseModel, model_validator
from pin_voyage.models import Point


class PointCreate(BaseModel):
    name: str | None
    description: str | None
    created_by: str | None
    geom_lat: float
    geom_lon: float


class PointResponse(PointCreate):
    id: int
    created_at: datetime | None

    @model_validator(mode="before")
    @classmethod
    def convert_coords(cls, point_obj: Point) -> Self:
        geom = getattr(point_obj, "geom")
        geom_point = to_shape(geom)
        point_obj.geom_lon = geom_point.x
        point_obj.geom_lat = geom_point.y

        return point_obj

    model_config = {
        # This is equivalent to orm_mode=True
        "from_attributes": True
    }


class PointUpdate(PointResponse):
    @model_validator(mode="before")
    @classmethod
    def convert_coords(cls, point_obj: Point) -> Self:
        # this is a dummy method to prevent wrong dictionary operations
        return point_obj


class PointList(BaseModel):
    id: int
    name: str | None
    description: str | None
