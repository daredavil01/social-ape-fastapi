from typing import Optional
from fastapi import FastAPI, responses, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor

from starlette.responses import Response

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


@ app.get('/')
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}


@ app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return{"data": posts}


@ app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return{"data": new_post}


@ app.get('/posts/{post_id}')
def get_post(post_id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return {"post_detail": post}


@ app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING * """, (post_id,))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ app.put('/posts/{post_id}', status_code=status.HTTP_200_OK)
def update_post(post_id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, post_id))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {post_id} not found")
    return {"data": updated_post}
