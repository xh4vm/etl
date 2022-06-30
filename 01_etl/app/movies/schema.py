from datetime import date, datetime
from typing import Optional
import uuid
from pydantic import BaseModel

from .models import FilmWork, FilmWorkType, Genre, GenreFilmWork, Person, PersonFilmWork, PersonFilmWorkRole


SCHEMA = 'content'

class UUIDModelMixin(BaseModel):
    id : uuid.UUID


class TimeStampedModelMixin(BaseModel):
    created_at : Optional[datetime] = None
    updated_at : Optional[datetime] = None


class GenreModel(BaseModel, UUIDModelMixin, TimeStampedModelMixin):
    name : str
    description : str

    class Meta:
        model = Genre._meta.db_table


class FilmWorkModel(BaseModel, UUIDModelMixin, TimeStampedModelMixin):
    title : str
    description : Optional[str] = None
    creation_date : Optional[date] = None
    file_path : Optional[str] = None
    rating : Optional[float] = None
    type : FilmWorkType = FilmWorkType.MOVIE

    class Meta:
        model = FilmWork._meta.db_table


class GenreFilmWorkModel(BaseModel, UUIDModelMixin):
    film_work : FilmWorkModel
    genre : GenreModel
    created_at : Optional[datetime] = None

    class Meta:
        model = GenreFilmWork._meta.db_table


class PersonModel(BaseModel, UUIDModelMixin, TimeStampedModelMixin):
    full_name : str

    class Meta:
        model = Person._meta.db_table


class PersonFilmWorkModel(BaseModel, UUIDModelMixin, TimeStampedModelMixin):
    film_work : FilmWorkModel
    person : PersonModel
    role : PersonFilmWorkRole
    created_at : Optional[datetime] = None

    class Meta:
        model = PersonFilmWork._meta.db_table
