import json


def get_posts_all():
    with open ('/home/v/Python/c3l5_Coursework/static/data/posts.json', 'r', encoding="utf-8") as file:
        posts = json.load(file)
        return posts
    
def get_comments_all():
    with open ('/home/v/Python/c3l5_Coursework/static/data/comments.json', 'r', encoding="utf-8") as file:
        comments = json.load(file)
        return comments


def get_posts_by_user(user_name):
    posts = get_posts_all()
    user_posts = [post for post in posts if post['poster_name'].lower() == user_name.lower()]
    return user_posts

# print (get_posts_by_user('Leo'))

    #  – возвращает посты определенного пользователя. Функция должна возвращать пустой список, если у нет постов, у которых указан автором этот пользователь. 

def get_comments_by_post_id(post_id):
    posts = get_posts_all()
    comments = get_comments_all()
    # try:
    for post in posts:
        if post['pk'] == int(post_id):
            post_comments = [comment for comment in comments if comment['post_id'] == int(post_id)]
            return post_comments
    # except ValueError as e:
    #     print (f"Post with this ID - {post_id} not find")
    raise ValueError (f"Post with this ID - {post_id} not find")

# print (get_comments_by_post_id(8))
# print (get_comments_by_post_id(2))
# print (get_comments_by_post_id(82))
    #  – возвращает комментарии определенного поста. Функция должна вызывать ошибку ValueError
    #  если такого поста нет и пустой список, если у поста нет комментов.

def search_for_posts(query):
    query = query.lower()
    posts = get_posts_all()
    comments = get_comments_all()
    post_list = [post for post in posts if query in post['content'].lower()]
    for comment in comments:
        if query in comment['comment'].lower():
            for post in posts:
                if post['pk'] == comment['post_id']:
                    if post not in post_list:
                        post_list.append(post)
    return post_list
# print (search_for_posts ('ржавые'))
# print (search_for_posts('класс'))

    #  – возвращает список постов по ключевому слову

def get_post_by_pk(pk):
    posts = get_posts_all()
    for post in posts:
        if post['pk'] == pk:
            return post
    raise ValueError (f"Post with this ID - {pk} not find")
    #  – возвращает один пост по его идентификатору. Функция должна вызывать ошибку `ValueError` если такого поста нет.

# print (get_post_by_pk (1))
