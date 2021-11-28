from typing import List
from fastapi import status, HTTPException
from fastapi.params import Depends
from fastapi.routing import APIRouter
from starlette.responses import Response
from ..database import SessionLocal, get_db

from .. import models, schemas


router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)


@ router.get('/', response_model=List[schemas.Post])
def get_posts(db: SessionLocal = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@ router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: SessionLocal = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@ router.get('/{post_id}', response_model=schemas.Post)
def get_post(post_id: int, db: SessionLocal = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return post


@ router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: SessionLocal = Depends(get_db)):
    post = db.query(models.Post).filter(
        models.Post.id == post_id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ router.put('/{post_id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(post_id: int, updated_post: schemas.CreatePost, db: SessionLocal = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

    post_query.update(
        updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()