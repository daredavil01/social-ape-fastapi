from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

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


@ app.post('/posts')
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1, 10000000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@ app.get('/posts/{post_id}')
def get_post(post_id: int):
    return {"post_detail": find_post(post_id)}
