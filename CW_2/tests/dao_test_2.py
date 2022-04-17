import pytest
import app


class TestAPI:

    def test_get_response_all_posts(self):
        """ Проверяем статус вьюшки """
        response = app.app.test_client().get('/api/posts/')
        assert response.status_code == 200

    def test_get_all_posts_is_list(self):
        """Проверяем тип получаемого объекта. Что это список"""
        response = app.app.test_client().get('/api/posts/')
        assert type(response.json) == list, 'Не list'

    def test_get_all_posts_is_keys(self):
        """Пробегаемся по первым 3 постам и проверяем их ключи
        Так же проверяем у них значения по ключу pic - что там всё ОК"""
        allowed_keys = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count",
                        "pk", 'comments', 'comments_count'}

        response = app.app.test_client().get('/api/posts/')
        posts_list = response.json
        assert len(posts_list) > 0, "Пустой JSON"
        for post in posts_list[:3]:
            post_keys = set(post.keys())
            assert post_keys == allowed_keys, f"Ключи {post_keys} не соответствуют ожидаемым"
            assert post['pic'] != None, 'Отсутствует картинка'
            assert len(post['pic']) > 3, 'Очень короткий URL картинки'
            assert type(post['pic']) is str, 'URL картинки не является строкой'

    def test_get_response_one_post(self):
        """ Проверяем статус вьюшки """
        response = app.app.test_client().get('/api/posts/1')
        assert response.status_code == 200

    def test_get_one_post_is_dict(self):
        """Проверяем тип получаемого объекта. Что это словарь"""
        response = app.app.test_client().get('/api/posts/1')
        assert type(response.json) is dict, f'{response} не является словарём'

    def test_get_one_post_is_keys(self):
        """ Проверяем ключи API поста. Проверяем ключ pic что там все ОК """
        allowed_keys = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count",
                        "pk", 'comments', 'comments_count'}

        response = app.app.test_client().get('/api/posts/1')
        post_keys = response.json.keys()
        post_dict = response.json
        assert post_keys == allowed_keys, f"Ключи {post_keys} не соответствуют ожидаемым"
        assert post_dict['pic'] is not None, 'Отсутствует картинка'
        assert len(post_dict['pic']) > 3, 'Очень короткий URL картинки'
        assert type(post_dict['pic']) is str, 'URL картинки не является строкой'