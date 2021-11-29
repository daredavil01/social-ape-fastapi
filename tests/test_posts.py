from calendar import c
from fastapi import status
from typing import List
import pytest

from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert res.status_code == status.HTTP_200_OK
    assert len(posts_list) == len(test_posts)


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/8888")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert res.status_code == status.HTTP_200_OK
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title
    assert post.Post.owner_id == test_posts[0].owner_id


@pytest.mark.parametrize("title, content, published",
                         [("Awsome new title", "new content", True),
                          ("Best new title", "newest content", False),
                          ("Very best new title", "The newest content", False)])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.owner_id == test_user["id"]
    assert created_post.published == published
    assert created_post.id is not None


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "Awsome new title", "content": "new content"})
    created_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == "Awsome new title"
    assert created_post.content == "new content"
    assert created_post.owner_id == test_user["id"]
    assert created_post.published == True
    assert created_post.id is not None


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "Awsome new title", "content": "new content"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_post_unauthorized_user(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_delete_post_not_exist(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/8888")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_other_user_post(authorized_client, test_user,  test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_post(authorized_client, test_user, test_posts):
    res = authorized_client.put(
        f"/posts/{test_posts[0].id}", json={"title": "New title", "content": "New content", "id": test_posts[0].id})
    updated_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_200_OK
    assert updated_post.title == "New title"
    assert updated_post.content == "New content"
    assert updated_post.owner_id == test_user["id"]
    assert updated_post.id == test_posts[0].id


def test_update_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.put(
        f"/posts/{test_posts[3].id}", json={"title": "New title", "content": "New content", "id": test_posts[3].id})
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_unauthenticated_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}", json={"title": "New title", "content": "New content", "id": test_posts[0].id})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.put(
        f"/posts/8888", json={"title": "New title", "content": "New content", "id": test_posts[0].id})
    assert res.status_code == status.HTTP_404_NOT_FOUND
