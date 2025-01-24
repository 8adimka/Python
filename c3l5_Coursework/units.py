import json
import os

# Динамические пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(BASE_DIR, 'static', 'data', 'posts.json')
COMMENTS_FILE = os.path.join(BASE_DIR, 'static', 'data', 'comments.json')
BOOKMARKS_FILE = os.path.join(BASE_DIR, 'static', 'data', 'bookmarks.json')

class Post:
    def __init__(self, poster_name, poster_avatar, pic, content, views_count, likes_count, pk, hashtags):
        self.poster_name = poster_name
        self.poster_avatar = poster_avatar
        self.pic = pic
        self.content = content
        self.views_count = views_count
        self.likes_count = likes_count
        self.pk = pk
        self.hashtags = hashtags


    def __repr__(self):
        return f"Post(id={self.pk}, author={self.poster_name})"

class Comment:
    def __init__(self, post_id, commenter_name, comment, pk):
        self.post_id = post_id
        self.commenter_name = commenter_name
        self.comment = comment
        self.pk = pk

    def __repr__(self):
        return f"Comment(id={self.pk}, post_id={self.post_id})"

def get_posts_all():
    try:
        with open(POSTS_FILE, 'r', encoding="utf-8") as file:
            posts_data = json.load(file)
            
            for post in posts_data:
                # Разделяем текст в 'content' на список слов
                content_list = post['content'].split()
                
                # Отбираем хэштеги
                hashtags = ' '.join([word for word in content_list if word.startswith('#')])
                
                # Убираем хэштеги из текста
                content = ' '.join([word for word in content_list if not word.startswith('#')])
                
                # Обновляем словарь поста
                post['hashtags'] = hashtags
                post['content'] = content
            
            # Преобразуем в список объектов Post
            posts = [Post(**data) for data in posts_data]
            return posts

    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Error reading posts: {e}")

def get_comments_all():
    try:
        with open(COMMENTS_FILE, 'r', encoding="utf-8") as file:
            comments_data = json.load(file)
            comments = [Comment(**data) for data in comments_data]
            return comments
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Error reading comments: {e}")

def get_posts_by_user(user_name):
    posts = get_posts_all()
    user_posts = [post for post in posts if post.poster_name.lower() == user_name.lower()]
    return user_posts

def get_comments_by_post_id(post_id):
    posts = get_posts_all()
    comments = get_comments_all()
    for post in posts:
        if post.pk == int(post_id):
            post_comments = [comment for comment in comments if comment.post_id == int(post_id)]
            return post_comments
    raise ValueError(f"Post with this ID - {post_id} not found")

def search_for_posts(query):
    query = query.lower()
    posts = get_posts_all()
    comments = get_comments_all()
    post_list = [post for post in posts if query in post.content.lower()]
    for comment in comments:
        if query in comment.comment.lower():
            for post in posts:
                if post.pk == comment.post_id:
                    if post not in post_list:
                        post_list.append(post)
    return post_list

def get_post_by_pk(id):
    posts = get_posts_all()
    for post in posts:
        if post.pk == id:
            return post
    raise ValueError(f"Post with this ID - {id} not found")

def load_bookmarks():
    """Загружает закладки из файла."""
    try:
        with open(BOOKMARKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_bookmarks(bookmarks):
    """Сохраняет закладки в файл."""
    with open(BOOKMARKS_FILE, "w", encoding="utf-8") as file:
        json.dump(bookmarks, file, ensure_ascii=False, indent=4)

def delete_bookmark(post_id):
    bookmarks = load_bookmarks()
    for bookmark in bookmarks:
        if bookmark['post_id'] == post_id:
            bookmarks.remove(bookmark)
    save_bookmarks(bookmarks)

def get_bookmarks_by_post_id(post_id):
    bookmarks = load_bookmarks()
    for bookmark in bookmarks:
        if bookmark['post_id'] == post_id:
            return bookmark
    return None
            
