from typing import Optional
from fastapi import FastAPI, responses, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

from starlette.responses import Response

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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
    return{"data": my_posts}


@ app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1, 10000000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@ app.get('/posts/{post_id}')
def get_post(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return {"post_detail": post}


@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
