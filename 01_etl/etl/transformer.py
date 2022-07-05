from typing import Any, Iterator, Optional, Union

from schema import FilmWorkModelIntoES


class Transformer:
    def _get_short_persons(self, persons: Optional[list[dict[str, Any]]]) -> Union[Iterator[str], tuple]:
        '''Метод разворачивания словарей с персонами в массив имен'''
        return (person['name'] for person in persons) if persons is not None else ()

    def transform(self, raw_data: Iterator[tuple[Any]]) -> Iterator[FilmWorkModelIntoES]:
        '''Метод для преобразования сырых данных из бд в модель'''

        for row in raw_data:
            directors_names = self._get_short_persons(row['directors'])

            yield FilmWorkModelIntoES(
                id=row['id'],
                title=row['title'],
                description=row['description'],
                imdb_rating=row['rating'],
                genre=row['genres'],
                director=', '.join(directors_names),
                actors_names=self._get_short_persons(row['actors']),
                writers_names=self._get_short_persons(row['writers']),
                actors=row['actors'],
                writers=row['writers'],
            ), str(row['updated_at'])
