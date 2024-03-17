from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from src.brd.test.database import engine, SessionLocal, Base
from src.brd.test.models import Item
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


Base.metadata.create_all(engine)

app = FastAPI()

origins = [
    "*",
    "http://localhost",
    "http://localhost:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    s: str = ""
    s = "<b>Ввод данных</b><form><input type='text'/></form>"
    return s


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


class ItemRequest(BaseModel):
    name: str
    description: str
    price: float
    tax: float


@app.post("/insert/")
async def insert_data(item_request: ItemRequest):
    item = Item(
        name=item_request.name,
        description=item_request.description,
        price=item_request.price,
        tax=item_request.tax
    )

    # Сохранение объекта в базе данных
    session = SessionLocal()
    session.add(item)
    session.commit()

    # Возврат сохраненного объекта

    return item


@app.get("/inserted/")
async def inserted():
    s = SessionLocal()
    r = s.query(Item).all()
    return r


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    s = SessionLocal()
    s.query(Item).filter(Item.id == item_id).delete()
    s.commit()
    print("delete item: ", item_id)
    return


@app.delete("/delete_items/")
async def delete_item(items):
    print("delete item: ", items)
    return

'''
@app.post("/items/")
async def create_item(item: Item, db: Session = Depends(SessionLocal)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
'''
