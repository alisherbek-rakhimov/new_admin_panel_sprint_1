from dataclasses import dataclass, fields
from dataclasses import field
from abc import ABC
import uuid
from datetime import datetime, date


# from enum import Enum


# @dataclass
# class AbstractDataclass(ABC):
#     def __new__(cls, *args, **kwargs):
#         if cls == AbstractDataclass or cls.__bases__[0] == AbstractDataclass:
#             raise TypeError("Cannot instantiate abstract class.")
#         return super().__new__(cls)


# class TimeStampedMixin(AbstractDataclass):


# class UUIDMixin(AbstractDataclass):


# class PostInitMixin(AbstractDataclass):


@dataclass(slots=True)
class Person:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    full_name: str = field(default='')
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())

    @staticmethod
    def attrs() -> str:
        return 'id, full_name, created, modified'

    @staticmethod
    def table():
        return 'person'

    @staticmethod
    def attr_placeholders():
        return ', '.join(['%s'] * 4)

    def __post_init__(self):
        for field in fields(self):
            if getattr(self, field.name) is None:
                setattr(self, field.name, field.default)


@dataclass(slots=True)
class Filmwork:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    title: str = field(default='')
    description: str = field(default='')
    creation_date: datetime = field(default=date.today())
    rating: float = field(default=0.0)
    type: str = field(default='')
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())

    @staticmethod
    def attrs() -> str:
        return 'id, title, description, creation_date, rating, type, created, modified'

    @staticmethod
    def table():
        return 'film_work'

    @staticmethod
    def attr_placeholders():
        return ', '.join(['%s'] * 8)

    def __post_init__(self):
        for field in fields(self):
            if getattr(self, field.name) is None:
                setattr(self, field.name, field.default)


@dataclass(slots=True)
class Genre:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = field(default='')
    description: str = field(default='')
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())

    @staticmethod
    def attrs() -> str:
        return 'id, name, description, created, modified'

    @staticmethod
    def table():
        return 'genre'

    @staticmethod
    def attr_placeholders():
        return ', '.join(['%s'] * 5)

    def __post_init__(self):
        for field in fields(self):
            if getattr(self, field.name) is None:
                setattr(self, field.name, field.default)


# class Role(Enum):
#     actor = 'actor'
#     producer = 'producer'
#     director = 'director'


@dataclass(slots=True)
class PersonFilmwork:
    film_work_id: uuid.uuid4
    person_id: uuid.uuid4
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    role: str = field(default='')
    created_at: datetime = field(default=datetime.now())

    @staticmethod
    def attrs() -> str:
        return 'film_work_id, person_id, id, role, created'

    @staticmethod
    def table():
        return 'person_film_work'

    @staticmethod
    def attr_placeholders():
        return ', '.join(['%s'] * 5)

    def __post_init__(self):
        for field in fields(self):
            if getattr(self, field.name) is None:
                setattr(self, field.name, field.default)


@dataclass(slots=True)
class GenreFilmwork:
    film_work_id: uuid.uuid4
    genre_id: uuid.uuid4
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default=datetime.now())

    @staticmethod
    def attrs() -> str:
        return 'film_work_id, genre_id, id, created'

    @staticmethod
    def table():
        return 'genre_film_work'

    @staticmethod
    def attr_placeholders():
        return ', '.join(['%s'] * 4)

    def __post_init__(self):
        for field in fields(self):
            if getattr(self, field.name) is None:
                setattr(self, field.name, field.default)


def dataclass_factory(cls):
    def factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return cls(**d)

    return factory

# def filmwork_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return Filmwork(**d)
#
#
# def person_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return Person(**d)
#
#
# def genre_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return Genre(**d)
#
#
# def person_filmwork_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return PersonFilmwork(**d)
#
#
# def genre_filmwork_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return GenreFilmwork(**d)
