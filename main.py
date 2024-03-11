from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from src.brd.test.database import engine, SessionLocal, Base
from src.brd.test.models import Item

Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/insert/")
async def insert_data():
    item = Item(
        id=2,
        name="Test2",
        description="Test Desc2",
        price=123.55,
        tax=0.22
    )
    s = SessionLocal()
    s.add(item)
    s.commit()
    r = s.query(Item).first()
    return r


@app.get("/inserted/")
async def inserted():
    s = SessionLocal()
    r = s.query(Item).all()
    return r

'''
@app.post("/items/")
async def create_item(item: Item, db: Session = Depends(SessionLocal)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
'''
