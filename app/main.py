from typing import Optional
from fastapi import FastAPI, status, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from sqlalchemy.sql.functions import mode
from starlette.responses import Response

from . import models
from .database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='social-ape', user='postgres', password='12345', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successfull!!!")
        break
    except Exception as e:
        print("Connecting to database failed!")
        print("Error:", e)
        time.sleep(2)


my_posts = [{"title": "apple", "content": "sweet", "id": 1}]


def find_post(id: int) -> Optional[dict]:
    for post in my_posts:
        if post["id"] == id:
            return post
    return None


@app.get('/sqlalchemy')
def test_posts(db: SessionLocal = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@ app.get('/')
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}


@ app.get('/posts')
def get_posts(db: SessionLocal = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@ app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: SessionLocal = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return{"data": new_post}


@ app.get('/posts/{post_id}')
def get_post(post_id: int, db: SessionLocal = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return {"post_detail": post}


@ app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: SessionLocal = Depends(get_db)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING * """, (post_id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(
        models.Post.id == post_id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ app.put('/posts/{post_id}', status_code=status.HTTP_200_OK)
def update_post(post_id: int, updated_post: Post, db: SessionLocal = Depends(get_db)):
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, post_id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

    post_query.update(
        updated_post.dict(), synchronize_session=False)
    db.commit()

    return {"data": post_query.first()}
