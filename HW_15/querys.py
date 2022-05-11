DATABASE_SOURCE = 'animal.db'
CREATE_QUERIES = f"""
    CREATE TABLE types (
        id_type integer PRIMARY KEY AUTOINCREMENT,
        type text
    );

    CREATE TABLE breeds (
        id_breed integer PRIMARY KEY AUTOINCREMENT,
        breed text
    );

    CREATE TABLE color1 (
        id_color integer PRIMARY KEY AUTOINCREMENT,
        color1 text
    );

       CREATE TABLE color2 (
        id_color integer PRIMARY KEY AUTOINCREMENT,
        color2 text
    );

    CREATE TABLE outcome_subtypes (
        id_outcome_subtype integer PRIMARY KEY AUTOINCREMENT,
        outcome_subtype text
    );

    CREATE TABLE outcome_types (
        id_outcome_type integer PRIMARY KEY AUTOINCREMENT,
        outcome_type text
    );

    CREATE TABLE animals_new (
        id integer PRIMARY KEY AUTOINCREMENT,
        age_upon_outcome varchar(10),
        animal_id varcar(10),
        name varchar(32),
        id_type integer,
        id_breed integer,
        id_color1 integer,
        id_color2 integer,
        date_of_birth datetime,
        id_outcome_subtype text,
        id_outcome_type text,
        outcome_month integer,
        outcome_year integer,
        FOREIGN KEY(id_type) REFERENCES types(id_type) ON DELETE SET NULL ON UPDATE CASCADE,
        FOREIGN KEY(id_breed) REFERENCES breeds(id_breed) ON DELETE SET NULL ON UPDATE CASCADE,
        FOREIGN KEY(id_color1) REFERENCES color1(id_color) ON DELETE SET NULL ON UPDATE CASCADE,
        FOREIGN KEY(id_color2) REFERENCES color2(id_color) ON DELETE SET NULL ON UPDATE CASCADE,
        FOREIGN KEY(id_outcome_subtype) REFERENCES outcome_subtypes(id_outcome_subtype) ON DELETE SET NULL ON UPDATE CASCADE,
        FOREIGN KEY(id_outcome_type) REFERENCES outcome_types(id_outcome_type) ON DELETE SET NULL ON UPDATE CASCADE
    );
"""

MIGRATE_SECOND = f"""
INSERT INTO types (type)
SELECT DISTINCT animals.animal_type
FROM animals;
INSERT INTO breeds (breed)
SELECT DISTINCT animals.breed
FROM animals;
INSERT INTO color1 (color1)
SELECT DISTINCT animals.color1
FROM animals;
INSERT INTO color2 (color2)
SELECT DISTINCT animals.color1
FROM animals;
INSERT INTO outcome_subtypes (outcome_subtype)
SELECT DISTINCT animals.outcome_subtype
FROM animals;
INSERT INTO outcome_subtypes (outcome_subtype)
SELECT DISTINCT animals.outcome_subtype
FROM animals;
INSERT INTO outcome_types (outcome_type)
SELECT DISTINCT animals.outcome_type
FROM animals;
"""

MIGRATE_JOIN = f"""
INSERT INTO animals_new (age_upon_outcome, animal_id, id_type, name, id_breed, id_color1, id_color2, date_of_birth,
                        id_outcome_subtype, id_outcome_type, outcome_month, outcome_year)

SELECT animals.age_upon_outcome, animals.animal_id, types.id_type, animals.name, breeds.id_breed, 
color1.id_color, color2.id_color, animals.date_of_birth, outcome_subtypes.id_outcome_subtype, 
outcome_types.id_outcome_type, animals.outcome_month, animals.outcome_year
FROM animals       
LEFT JOIN types ON types.type = animals.animal_type
LEFT JOIN breeds ON breeds.breed = animals.breed
LEFT JOIN color1 ON color1.color1 = animals.color1
LEFT JOIN color2 ON color2.color2 = animals.color2
LEFT JOIN outcome_subtypes ON outcome_subtypes.outcome_subtype = animals.outcome_subtype
LEFT JOIN outcome_types ON outcome_types.outcome_type = animals.outcome_type
"""