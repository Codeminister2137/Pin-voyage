from geoalchemy2 import Geometry
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text, DateTime, func
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Point(Base):
    __tablename__ = "points"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    created_by: Mapped[str | None] = mapped_column(Text)
    geom: Mapped[str] = mapped_column(Geometry(geometry_type="POINT", srid=4326))
