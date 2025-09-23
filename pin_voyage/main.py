import uvicorn
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    message: str


@app.get("/", tags=[], response_model=Item)
def home():
    return {"message": "Hello World!"}


@app.post("/", tags=[], response_model=Item)
def post_item(item: Item):
    return {"message": item.message}


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
    uvicorn.run("pin_voyage.main:app", host="0.0.0.0", port=8000, reload=True)
