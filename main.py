from fastapi import FastAPI

from api.v1 import user
from db.base import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
