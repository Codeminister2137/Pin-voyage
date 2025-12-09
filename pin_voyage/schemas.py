from typing import Self

from pydantic import BaseModel


class PointCreate(BaseModel):
    name: str | None
    description: str | None
    created_by: str
    geom_lat: float
    geom_lon: float


class PointResponse(PointCreate):
    id: int
    created_at: str | None

    @classmethod
    def model_validate(cls, data) -> Self:
        print("HERE")
        return super().model_validate(
            {
                "id": data.id,
                "name": data.name,
                "description": data.description,
                "created_by": data.created_by,
            }
        )

    model_config = {
        # This is equivalent to orm_mode=True
        "from_attributes": True
    }
