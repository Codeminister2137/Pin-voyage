from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from pin_voyage.database import get_db
from pin_voyage.schemas import PointCreate, PointResponse, PointList, PointUpdate
from pin_voyage.points_crud.repository import PointRepository
from pin_voyage.exceptions import PointNotFoundException

router = APIRouter(prefix="/points", tags=["points"])


@router.get("/", response_model=list[PointList])
def list_points(db: Session = Depends(get_db)):
    points_repo = PointRepository(db)
    return points_repo.list()


@router.get("/{point_id}", response_model=PointResponse)
def get_point(point_id: int, db: Session = Depends(get_db)):
    points_repo = PointRepository(db)
    try:
        return points_repo.get_by_id(point_id)
    except PointNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=PointResponse)
def create_points(payload: PointCreate, db: Session = Depends(get_db)):
    points_repo = PointRepository(db)
    return points_repo.create(payload)


@router.patch("/{point_id}", response_model=PointResponse)
def update_point(
    point_id: int,
    payload: PointUpdate,
    db: Session = Depends(get_db),
):
    points_repo = PointRepository(db)
    return points_repo.update(point_id, payload)


@router.delete("/{point_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_point(point_id: int, db: Session = Depends(get_db)):
    points_repo = PointRepository(db)
    return points_repo.delete(point_id)
