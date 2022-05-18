from flask import Flask, jsonify
import logging
import sqlite3
from querys import DATABASE_SOURCE, CREATE_QUERIES, MIGRATE_SECOND, MIGRATE_JOIN
# Включаем логирование
logging.basicConfig(encoding='utf-8', level=logging.INFO)

app = Flask(__name__)


def get_sqlite_query(query, base=DATABASE_SOURCE, is_script=False):
    with sqlite3.connect(base) as connection:
        cursor = connection.cursor()
        if is_script:
            cursor.executescript(query)
        else:
            cursor.execute(query)


def get_all_by_id(id):
    query = """ 

SELECT 
    animals_new.id,
    animals_new.age_upon_outcome,
    animals_new.animal_id,
    animals_new.name,
    types."type",
    breeds.breed,
    color1.color1,
    color2.color2,
    animals_new.date_of_birth,
    outcome_types.outcome_type,
    outcome_subtypes.outcome_subtype,
    animals_new.outcome_month,
    animals_new.outcome_year

    FROM animals_new

    LEFT JOIN types ON animals_new.id_type = types.id_type
    LEFT JOIN breeds ON animals_new.id_breed = breeds.id_breed
    LEFT JOIN color1 ON animals_new.id_color1 = color1.id_color
    LEFT JOIN color2 ON animals_new.id_color2 = color2.id_color
    LEFT JOIN outcome_types ON animals_new.id_outcome_type = outcome_types.id_outcome_type
    LEFT JOIN outcome_subtypes ON animals_new.id_outcome_subtype = outcome_subtypes.id_outcome_subtype

    WHERE id == '{id}'
"""

    raw = get_sqlite_query(query, is_script=False)
    result_dict = {'id': raw[0][0], 'age_upon_outcome': raw[0][1], 'animal_id': raw[0][2],
                   'name': raw[0][3], 'id_type': raw[0][4], 'id_breed': raw[0][5], 'id_color1': raw[0][6],
                   'id_color2': raw[0][7], 'date_of_birth': raw[0][8][0:10], 'id_outcome_subtype': raw[0][9],
                   'id_outcome_type': raw[0][10], 'outcome_month': raw[0][11], 'outcome_year': raw[0][12]}
    return result_dict


@app.route('/<id>/')
def get_all_by_id(id):
    """ Эдпоинт выводящий инфу по ID. """
    logging.info(f'Ищем по ID: {id}')
    animal = get_all_by_id(id)

    logging.info(f'Функция поиска вернула: {animal}')
    return jsonify(animal)


app.config['JSON_AS_ASCII'] = False

if __name__ == '__main__':
    app.run(debug=True)

get_sqlite_query(CREATE_QUERIES, is_script=True)

get_sqlite_query(MIGRATE_SECOND, is_script=True)

get_sqlite_query(MIGRATE_JOIN, is_script=False)