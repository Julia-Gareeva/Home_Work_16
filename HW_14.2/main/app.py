from flask import Flask, jsonify
import sqlite3


def main():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['DEBUG'] = True

    def db_connect(query):
        """Подключение к БД netflix"""
        connection = sqlite3.connect('netflix.db')
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result

    @app.route('/movie/<title>/')
    def search_by_title(title):
        """Шаг 1. Поиск по названию самого свежего."""
        query = f"""
            SELECT 
              title, 
              country, 
              release_year, 
              listed_in AS genre, 
              description
            FROM netflix
            WHERE title = '{title}'
            ORDER BY release_year DESC 
            LIMIT 1 """

        response = db_connect(query)
        if len(response) > 0:
            response = response[0]
            response_json = {
              'title': response[0],
              'country': response[1],
              'release_year': response[2],
              'genre': response[3],
              'description': response[4]
            }
            return jsonify(response_json)
        """Индекс списка вне допустимого диапазона."""
        return "Такого фильма/сериала нет в базе данных."

    @app.route('/movie/<int:start>/to/<int:end>')
    def search_by_period(start, end):
        """Шаг 2. Поиск по диапазону лет выпуска."""
        query = f"""
            SELECT title, 
              release_year
            FROM netflix 
            WHERE release_year BETWEEN '{start}' AND '{end}'
            ORDER BY release_year
            LIMIT 100 """

        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'release_year': film[1],
            })
        return jsonify(response_json)

    @app.route('/rating/<group>')
    def search_by_rating(group):
        """Шаг 3. Поиск по рейтингу.
        Определенные группы: для детей - children; для семейного просмотра - family; для взрослых - adult"""
        levels = {
            'children': ['G'],
            'family': ['G', 'PG', 'PG-13'],
            'adult': ['R', 'NC-17'],
        }
        if group in levels:
            level = f'\", \"'.join(levels[group])
            level = f'\"{level}\"'
        else:
            return jsonify([])

        query = f"""
            SELECT 
              title,
              rating,
              description
            FROM netflix 
            WHERE rating IN ({level}) """
        print(query)

        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'rating': film[1],
                'description': film[2].strip(),
            })
        return jsonify(response_json)

    @app.route('/genre/<genre>/')
    def search_by_genre(genre):
        """Шаг 4. Функция, которая возвращает 10 самых свежих фильмов по определенному жанру."""
        query = f"""
            SELECT title,
              description
            FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC 
            LIMIT 10 """

        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
              'title': film[0].strip(),
              'description': film[1].strip()
            })
        return jsonify(response_json)

    def get_actors(name1, name2):
        """Шаг 5. Функция, которая получает имена двух актеров.
        И возвращает список тех, кто играет с ними в паре больше 2 раз."""
        query = f"""
            SELECT "cast"
            FROM netflix
            WHERE "cast" LIKE '%{name1}%' 
            AND "cast" LIKE '%{name2}%' """

        response = db_connect(query)
        actors = []
        for cast in response:
            actors.extend(cast[0].split(', '))
        result = []
        for a in actors:
            if a not in [name1, name2]:
                if actors.count(a) > 2:
                    result.append(a)
        result = set(result)
        return result
    print(get_actors(name1='Jack Black', name2='Dustin Hoffman'))

    def get_films(type_film, release_year, genre):
        """Шаг 6. Функция, с помощью которой можно искать картины по определенным:
        типу (фильмы или сериалы), году их выпуска и их жанру."""
        query = f"""
            SELECT title,
                description,
                "type"
            FROM netflix
            WHERE "type" = '{type_film}'
                AND release_year  = '{release_year}'
                AND listed_in LIKE '%{genre}%' """

        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'description': film[1],
                'type': film[2],
            })
        return response_json

    print(get_films(type_film='Movie', release_year='2016', genre='Dramas'))

    app.run() # debug=True


if __name__ == '__main__':
    main()