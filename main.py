from fastapi import FastAPI

from api.v1 import user, news
from db.base import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(news.router)


@app.get("/")
def home():
    return {"detail": "Welcome to NewsStream!"}
