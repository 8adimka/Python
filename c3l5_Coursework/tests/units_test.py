from units import get_posts_all, get_comments_all, get_posts_by_user, get_comments_by_post_id, search_for_posts, get_post_by_pk
import pytest, json

# Параметры для тестирования функции search_for_posts
word_params = ['ржавые', 'класс', 'привет']
@pytest.mark.parametrize("query", word_params)
def test_search_for_posts(query):
    # Проверяем, что функция возвращает ожидаемый результат
    assert search_for_posts(query) == search_for_posts(query)

def test_get_posts_all():
    with open('/home/v/Python/c3l5_Coursework/static/data/posts.json', 'r', encoding="utf-8") as file:
        posts = json.load(file)
    assert get_posts_all() == posts

def test_get_comments_all():
    with open('/home/v/Python/c3l5_Coursework/static/data/comments.json', 'r', encoding="utf-8") as file:
        comments = json.load(file)
    assert get_comments_all() == comments

@pytest.mark.parametrize("username", ["john_doe", "jane_doe"])
def test_get_posts_by_user(username):
    posts = get_posts_by_user(username)
    assert all(post['username'] == username for post in posts)

@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_comments_by_post_id(post_id):
    comments = get_comments_by_post_id(post_id)
    assert all(comment['post_id'] == post_id for comment in comments)

@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_post_by_pk(post_id):
    post = get_post_by_pk(post_id)
    assert post['pk'] == post_id

