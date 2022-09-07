-- Так как мы считаем что тут база одна целая то можно контролировать целостность данных на уровне БД через ограничения.
-- Postgres использует блокировку всей таблицы поэтому в курсе за валидацию данных отвечает сервис, а не хранилище, так что везде TEXT

CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work
(
    id            uuid PRIMARY KEY,
    title         TEXT NOT NULL,
    description   TEXT,
    creation_date DATE,
    rating        FLOAT,
    type          TEXT NOT NULL,
    created       timestamp with time zone,
    modified      timestamp with time zone
);

DROP INDEX content.film_work_creation_date_idx;
CREATE INDEX film_work_creation_date_idx ON content.film_work_ (creation_date);

CREATE TABLE IF NOT EXISTS content.person
(
    id        uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created   timestamp with time zone,
    modified  timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work
(
    id           uuid PRIMARY KEY,
    film_work_id uuid NOT NULL references content.film_work_ (id) on delete cascade on update cascade,
    person_id    uuid NOT NULL references content.person (id) on delete cascade on update cascade,
    role         TEXT NOT NULL,
    created      timestamp with time zone
);

DROP INDEX content.film_work_person_idx;
CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id);

CREATE TABLE IF NOT EXISTS content.genre
(
    id          uuid PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT,
    created     timestamp with time zone,
    modified    timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work
(
    id           uuid PRIMARY KEY,
    film_work_id uuid NOT NULL references content.film_work_ (id) on delete cascade on update cascade,
    genre_id     uuid NOT NULL references content.genre (id) on delete cascade on update cascade,
    role         TEXT NOT NULL,
    created      timestamp with time zone
);

DROP INDEX content.film_work_genre_idx;
CREATE UNIQUE INDEX film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id, role);



