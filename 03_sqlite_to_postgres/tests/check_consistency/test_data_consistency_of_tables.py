from my_dataclasses import (Filmwork, Genre, GenreFilmwork, Person,
                            PersonFilmwork)


def test_film_work(loaders):
    sqlite_loader, postgres_loader = loaders

    sqlite_data = sqlite_loader.load_one_table(Filmwork, as_dataclass=False)
    pg_data = postgres_loader.load_one_table(Filmwork)

    sqlite_loader.close_conn()
    postgres_loader.close_conn()

    assert sqlite_data == pg_data


def test_genre(loaders):
    sqlite_loader, postgres_loader = loaders

    sqlite_data = sqlite_loader.load_one_table(Genre, as_dataclass=False)
    pg_data = postgres_loader.load_one_table(Genre)

    sqlite_loader.close_conn()
    postgres_loader.close_conn()

    assert sqlite_data == pg_data


def test_person(loaders):
    sqlite_loader, postgres_loader = loaders

    sqlite_data = sqlite_loader.load_one_table(Person, as_dataclass=False)
    pg_data = postgres_loader.load_one_table(Person)

    sqlite_loader.close_conn()
    postgres_loader.close_conn()

    assert sqlite_data == pg_data


def test_genre_film_work(loaders):
    sqlite_loader, postgres_loader = loaders

    sqlite_data = sqlite_loader.load_one_table(GenreFilmwork, as_dataclass=False)
    pg_data = postgres_loader.load_one_table(GenreFilmwork)

    sqlite_loader.close_conn()
    postgres_loader.close_conn()

    assert sqlite_data == pg_data


def test_person_film_work(loaders):
    sqlite_loader, postgres_loader = loaders

    sqlite_data = sqlite_loader.load_one_table(PersonFilmwork, as_dataclass=False)
    pg_data = postgres_loader.load_one_table(PersonFilmwork)

    sqlite_loader.close_conn()
    postgres_loader.close_conn()

    assert sqlite_data == pg_data
