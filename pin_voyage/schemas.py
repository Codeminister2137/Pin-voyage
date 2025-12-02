from pydantic import BaseModel


class PointCreate(BaseModel):
    name: str | None
    description: str | None
    created_by: str
    geom_lat: float
    geom_lon: float
