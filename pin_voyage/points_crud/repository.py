from fastapi import HTTPException, status
from geoalchemy2.shape import from_shape
from sqlalchemy import select
from sqlalchemy.orm import Session

from shapely.geometry import Point as ShapelyPoint
from pin_voyage.models import Point
from pin_voyage.schemas import PointCreate, PointResponse, PointList, PointUpdate


class PointRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, point_id: int) -> PointResponse:
        point = (
            self.db.execute(select(Point).where(Point.id == point_id)).scalars().first()
        )
        if not point:
            raise Exception("Point not found")
        else:
            return point

    def create(self, payload: PointCreate):
        shape = ShapelyPoint(payload.geom_lon, payload.geom_lat)
        point = Point(
            name=payload.name,
            description=payload.description,
            geom=from_shape(shape, srid=4326),
        )
        self.db.add(point)
        self.db.commit()
        self.db.refresh(point)

        return point

    def update(self, point_id: int, payload: PointUpdate):
        point = self.db.get(Point, point_id)
        if not point:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Point not found",
            )
        data = payload.model_dump(exclude_unset=True)
        geom_lon, geom_lat = data.pop("geom_lon", None), data.pop("geom_lat", None)
        print(geom_lon, geom_lat)
        if geom_lon or geom_lat:
            point_response = PointResponse.model_validate(point)
            if geom_lon is not None and geom_lat is None:
                geom_lat = point_response.geom_lat
            if geom_lon is None and geom_lat is not None:
                geom_lon = point_response.geom_lon
            shape = ShapelyPoint(geom_lon, geom_lat)
            point.geom = from_shape(shape, srid=4326)

        # --- Generic field updates ---
        for field, value in data.items():
            setattr(point, field, value)

        self.db.commit()
        self.db.refresh(point)
        return point

    def delete(self, point_id: int):
        point = self.db.get(Point, point_id)
        if not point:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Point not found"
            )

        self.db.delete(point)
        self.db.commit()
        return None

    def list(self) -> PointList:
        return self.db.execute(select(Point)).scalars().all()
