from units import (
    get_posts_all,
    get_comments_all,
    get_posts_by_user,
    get_comments_by_post_id,
    search_for_posts,
    get_post_by_pk,
)
import pytest
import json
import os

# Динамические пути к данным
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(BASE_DIR, "../static/data/posts.json")
COMMENTS_FILE = os.path.join(BASE_DIR, "../static/data/comments.json")


def test_get_posts_all():
    with open(POSTS_FILE, 'r', encoding="utf-8") as file:
        posts_data = json.load(file)
    posts = get_posts_all()
    # Сравниваем количество постов
    assert len(posts) == len(posts_data)
    # Сравниваем содержимое полей первого поста
    assert posts[0].pk == posts_data[0]["pk"]
    assert posts[0].poster_name == posts_data[0]["poster_name"]


def test_get_comments_all():
    with open(COMMENTS_FILE, 'r', encoding="utf-8") as file:
        comments_data = json.load(file)
    comments = get_comments_all()
    # Сравниваем количество комментариев
    assert len(comments) == len(comments_data)
    # Сравниваем содержимое полей первого комментария
    assert comments[0].pk == comments_data[0]["pk"]
    assert comments[0].post_id == comments_data[0]["post_id"]


@pytest.mark.parametrize("username", ["john_doe", "Jane_Doe"])
def test_get_posts_by_user(username):
    posts = get_posts_by_user(username)
    # Проверяем, что все посты принадлежат указанному автору
    assert all(post.poster_name.lower() == username.lower() for post in posts)


@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_comments_by_post_id(post_id):
    comments = get_comments_by_post_id(post_id)
    # Проверяем, что все комментарии принадлежат указанному посту
    assert all(comment.post_id == post_id for comment in comments)


@pytest.mark.parametrize("query", ["ржавые", "класс", "привет"])
def test_search_for_posts(query):
    results = search_for_posts(query)
    # Проверяем, что в содержимом постов или комментариев встречается запрос
    for post in results:
        assert query in post.content.lower() or any(
            query in comment.comment.lower() for comment in get_comments_all()
        )


@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_post_by_pk(post_id):
    post = get_post_by_pk(post_id)
    # Проверяем, что найденный пост имеет правильный ID
    assert post.pk == post_id


@pytest.mark.parametrize("invalid_post_id", [999, -1, "abc"])
def test_get_post_by_pk_invalid(invalid_post_id):
    with pytest.raises(ValueError):
        get_post_by_pk(invalid_post_id)


@pytest.mark.parametrize("invalid_post_id", [999, -1, "abc"])
def test_get_comments_by_post_id_invalid(invalid_post_id):
    with pytest.raises(ValueError):
        get_comments_by_post_id(invalid_post_id)

