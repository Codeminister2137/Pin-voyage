from fastapi import APIRouter, HTTPException, status, Depends
from geoalchemy2.shape import from_shape
from sqlalchemy import select
from sqlalchemy.orm import Session

from shapely.geometry import Point as ShapelyPoint
from pin_voyage.database import get_db
from pin_voyage.models import Point
from pin_voyage.schemas import PointCreate, PointResponse, PointList, PointUpdate

router = APIRouter(prefix="/points", tags=["points"])


@router.get("/", response_model=list[PointList])
def list_points(db: Session = Depends(get_db)):
    return db.execute(select(Point)).scalars().all()


@router.get("/{point_id}", response_model=PointResponse)
def get_point(point_id: int, db: Session = Depends(get_db)):
    point = db.execute(select(Point).where(Point.id == point_id)).scalars().first()
    if not point:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Point not found")
    else:
        return point


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



@router.patch("/{point_id}", response_model=PointResponse)
def update_point(
    point_id: int,
    payload: PointUpdate,
    db: Session = Depends(get_db),
):
    point = db.get(Point, point_id)
    if not point:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Point not found",
        )

    data = payload.model_dump(exclude_unset=True)
    if not data["geom"]:
        if data["geom_lon"] or data["geom_lat"]:
            if data["geom_lon"] and data["geom_lat"]:

                shape = ShapelyPoint(data["geom_lon"], data["geom_lat"])
                point.geom = from_shape(shape, srid=4326)

            else:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTI,
                    detail="Both geom_lat and geom_lon must be provided to update geomet",
            )
    # --- Generic field updates ---
    for field, value in data.items():
        setattr(point, field, value)


    db.commit()
    db.refresh(point)
    return point



@router.delete("/{point_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_point(point_id: int, db: Session = Depends(get_db)):
    point = db.get(Point, point_id)
    if not point:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Point not found")

    db.delete(point)
    db.commit()
    return None
