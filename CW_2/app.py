from flask import Flask, request, render_template, jsonify
from posts_dao import PostsDAO
# Импортируем логирование
import logging

# Включаем логирование
logging.basicConfig(encoding='utf-8', level=logging.INFO)

dao = PostsDAO()
app = Flask(__name__)


@app.route('/')
def get_main_page():
    """ Вьюшка главной страницы """
    posts_list = dao.get_main_page()
    return render_template('index.html', posts_list=posts_list)


@app.route('/posts/<int:post_id>/')
def get_post_by_id(post_id):
    """ Вьюшка страницы 1 поста (по ID) """
    single_post_dict = dao.get_post_by_pk(post_id)  # Словарь с данными по ОДНОМУ посту
    return render_template('post.html', post=single_post_dict)


@app.route('/search/')  # http://127.0.0.1:5000/search/?s=еда
def get_search():
    """ Вьюшка страницы поиска """
    search_str = request.args.get('s')
    logging.info(f'Поисковая фраза: {search_str}')

    post_list = dao.get_post_by_keyword(search_str)[:10]
    logging.info(f'Поисковый список: {post_list}')
    search_count = len(post_list)

    return render_template('search.html', post_list=post_list, scount=search_count)


@app.route('/users/<string:username>/')
def get_posts_by_user(username):
    """ Вьюшка страницы автора """
    user_posts = dao.get_posts_by_user(username)
    return render_template('user-feed.html', posts=user_posts)


@app.route('/api/posts/')
def get_posts_json_api():
    """ Вьюшка API endpoint - полный список постов в json """
    posts_list = dao.get_posts_for_json()
    return jsonify(posts_list)


@app.route('/api/posts/<int:post_id>')
def get_post_json_api(post_id):
    """ Вьюшка API endpoint - возвращает json для одного поста """
    post = dao.get_post_by_pk(post_id)
    return jsonify(post)


app.config['JSON_AS_ASCII'] = False

if __name__ == '__main__':
    app.run()
