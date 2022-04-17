import json
from pprint import pprint
from config import *


class PostsDAO:

    def __init__(self):
        self.posts_list = None
        self.comments_list = None
        self.tags_list = None

    def load_posts(self):
        """Метод загружает файл с постами и сохраняет их в поле объекта"""
        with open(POSTS_JSON, 'r', encoding='utf-8') as file:
            self.posts_list = json.load(file)

    def load_comments(self):
        """Метод загружает файл с комментами и сохраняет их в поле объекта"""
        with open(COMMENTS_JSON, 'r', encoding='utf-8') as file:
            self.comments_list = json.load(file)

    def get_posts(self):
        """Метод загружает данные по постам в поле объекта и возвращает список словарей с постами """
        self.load_posts()

    def get_comments(self):
        """ Метод загружает данные по комментам в поле объекта и возвращает список словарей с комментами"""
        self.load_comments()

    def get_all(self):
        """Метод обновляет поля объекта данными с Json посты и комменты"""
        self.get_posts()
        self.get_comments()

    def get_posts_by_user(self, user_name):
        """ Метод обновляет поле с постами, а потом возвращает список словарей постов конкретного пользователя """
        user_posts_list = []
        self.get_posts()
        for post in self.posts_list:
            if post['poster_name'] == user_name:
                post_pk = post['pk']
                post = self.get_post_by_pk(post_pk)
                user_posts_list.append(post)
        return user_posts_list

    def get_comments_by_post_id(self, post_id):
        """ Метод обновляет поле с комментами, а потом возвращает комменты принадлежащие конкретному посту"""
        comments_list = []
        self.get_comments()
        for comment in self.comments_list:
            if comment['post_id'] == post_id:
                comments_list.append(comment)
        return comments_list

    def get_count_comments_for_post(self, post_id):
        """ Метод вытаскивает все комменты к конкретному посту в переменную в виде списка и возвращает его длину """
        all_posts_comments = self.get_comments_by_post_id(post_id)
        return len(all_posts_comments)

    def get_post_by_keyword(self, keyword):
        """Метод обновляет поле с постами, а потом возвращает пост с искомыми словами в тексте поста"""
        post_list = []
        self.get_posts()
        for post in self.posts_list:
            if keyword.lower() in post['content'].lower():
                post = self.get_post_by_pk(post['pk'])
                post_list.append(post)
        return post_list[:10]

    def get_post_by_pk(self, pk):
        """Метод обновляет поле с постами, а потом возвращает СЛОВАРЬ поста по его ID
        Добавляет данные: количество комментов, тексты комментов в виде списка"""
        self.get_all()
        for post in self.posts_list:
            if post['pk'] == pk:
                post['comments'] = self.get_comments_by_post_id(pk)
                post['comments_count'] = self.get_count_comments_for_post(pk)
                return post

    def get_posts_for_json(self):
        """Метод обновляет поле с постами. Потом проходит по нему, и формирует новый список
        в который добавляет полную инфу о каждом посте, включая данные с json с комментарии"""
        self.get_posts()
        posts_list = []
        for post in self.posts_list:
            posts_list.append(self.get_post_by_pk(post['pk']))
        return posts_list

    def get_main_page(self):
        """Метод берет исходный json с постами и добавляет туда ключ comments_count
         с количеством комментов для каждого поста для вывода вьюшки главной страницы """
        self.get_all()
        posts_list = []
        for post in self.posts_list:
            post_id = post['pk']
            comments_count = self.get_count_comments_for_post(post_id)
            post['comments_count'] = comments_count
            posts_list.append(post)
        return posts_list

    def get_all_tags(self):
        """Метод обходит все посты и возвращает список тэгов в поле self.tags_list DAO """
        self.get_posts()
        for post in self.posts_list:
            content = post['content'].lower()
            if '#' in content:
                content_list = content.split(' ')
                tags_list = []
                for word in content_list:
                    """
                    Сплитануть лишнее
                    Если слово содержит тэг добавить в список tags_list
                    Записать результат в поле self.tags_list
                    """
                    pass
