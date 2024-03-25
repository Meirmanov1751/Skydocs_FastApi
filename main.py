from fastapi import FastAPI, Body, File, UploadFile

from src.brd.test.database import engine, SessionLocal, Base
from src.brd.test.router import router as router_brd_test
from fastapi.middleware.cors import CORSMiddleware


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

app.include_router(router_brd_test)

@app.get("/")
async def root():
    s: str = ""
    s = "<b>Ввод данных</b><form><input type='text'/></form>"
    return s


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}




