from typing import List, Optional
from fastapi import status, HTTPException
from fastapi.params import Depends
from fastapi.routing import APIRouter
from starlette.responses import Response
from ..database import SessionLocal, get_db

from .. import models, schemas, ooath2


router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)


@ router.get('/', response_model=List[schemas.Post])
def get_posts(db: SessionLocal = Depends(get_db), current_user: schemas.UserOut = Depends(ooath2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@ router.get('/user', response_model=List[schemas.Post])
def get_user_posts(db: SessionLocal = Depends(get_db), current_user: schemas.UserOut = Depends(ooath2.get_current_user)):
    posts = db.query(models.Post).filter(
        models.Post.owner_id == current_user.id).all()
    return posts


@ router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: SessionLocal = Depends(get_db), current_user: int = Depends(ooath2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@ router.get('/{post_id}', response_model=schemas.Post)
def get_post(post_id: int, db: SessionLocal = Depends(get_db), current_user: int = Depends(ooath2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return post


@ router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: SessionLocal = Depends(get_db), current_user: int = Depends(ooath2.get_current_user)):
    post_query = db.query(models.Post).filter(
        models.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not the owner of this post")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ router.put('/{post_id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(post_id: int, updated_post: schemas.CreatePost, db: SessionLocal = Depends(get_db), current_user: int = Depends(ooath2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not the owner of this post")

    post_query.update(
        updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
