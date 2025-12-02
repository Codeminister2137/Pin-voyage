import uvicorn
from fastapi import FastAPI, WebSocket, Depends
from geoalchemy2.shape import from_shape
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from shapely.geometry import Point as ShapelyPoint
from pin_voyage.database import get_db
from pin_voyage.models import Point
from pin_voyage.schemas import PointCreate

app = FastAPI()


class Item(BaseModel):
    message: str


@app.get("/ping-db")
def ping(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"ping": "pong"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/", tags=[], response_model=Item)
def home():
    return {"message": "Hello World!"}


@app.post("/", tags=[])
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

    return {"message": point.id}


@app.put("/", tags=[], response_model=Item)
def put_item(item: Item):
    return {"message": item.message}


@app.delete("/{item_id}", tags=[], response_model=Item)
def delete_item(item_id: int):
    return {"message": "successfully deleted"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        await websocket.send_text(f"Received: {data}")


if __name__ == "__main__":
    uvicorn.run("pin_voyage.main:app", host="0.0.0.0", port=8001, reload=True)
