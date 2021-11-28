from typing import Optional, List
from fastapi import FastAPI, status, HTTPException
from fastapi.params import Depends
from starlette.responses import Response
from . import models, schemas
from .database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost', database='social-ape', user='postgres', password='12345', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection successfull!!!")
#         break
#     except Exception as e:
#         print("Connecting to database failed!")
#         print("Error:", e)
#         time.sleep(2)


@ app.get('/')
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}


@ app.get('/posts', response_model=List[schemas.Post])
def get_posts(db: SessionLocal = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@ app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: SessionLocal = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@ app.get('/posts/{post_id}', response_model=schemas.Post)
def get_post(post_id: int, db: SessionLocal = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return post


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


@ app.put('/posts/{post_id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(post_id: int, updated_post: schemas.CreatePost, db: SessionLocal = Depends(get_db)):
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

    return post_query.first()
