from fastapi import FastAPI, APIRouter

from .models import Base
from .database import engine
from .routers import post, user

Base.metadata.create_all(bind=engine)

app = FastAPI()


@ app.get('/')
def root():
    return {"message": "Hello World !!!"}


app.include_router(post.router)
app.include_router(user.router)
