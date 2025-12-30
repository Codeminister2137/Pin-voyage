from fastapi import APIRouter
from fastapi import Depends
from geoalchemy2.shape import from_shape
from sqlalchemy import select
from sqlalchemy.orm import Session

from shapely.geometry import Point as ShapelyPoint
from pin_voyage.database import get_db
from pin_voyage.models import Point
from pin_voyage.schemas import PointCreate, PointResponse, PointList

router = APIRouter(prefix="/points", tags=["points"])


@router.get("/", response_model=list[PointList])
def list_points(db: Session = Depends(get_db)):
    return db.execute(select(Point)).scalars().all()


@router.get("/{id}", response_model=PointResponse)
def get_point(point_id: int, db: Session = Depends(get_db)):
    return db.execute(select(Point).where(Point.id == point_id)).scalars().first()


@router.post("/", response_model=PointResponse)
def create_points(payload: PointCreate, db: Session = Depends(get_db)):
    shape = ShapelyPoint(payload.geom_lon, payload.geom_lat)
    point = Point(
        name=payload.name,
        description=payload.description,
        geom=from_shape(shape, srid=4326),
    )
    db.add(point)
    db.commit()
    db.refresh(point)

    return point
