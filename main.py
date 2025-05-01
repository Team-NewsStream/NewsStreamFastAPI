from fastapi import FastAPI

from api.v1 import user, news, scheduler
from db.base import Base, pool

app = FastAPI()

Base.metadata.create_all(bind=pool)

app.include_router(user.router)
app.include_router(news.router)
app.include_router(scheduler.router)


@app.get("/")
def home():
    return {"detail": "Welcome to NewsStream!"}
