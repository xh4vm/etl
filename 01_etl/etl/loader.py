import logging
from asyncio.log import logger
from typing import Iterator, Optional

import backoff
from config import BACKOFF_CONFIG, ElasticsearchSettings
from elasticsearch import Elasticsearch, helpers
from schema import FilmWorkModelIntoES, Schema
from state import BaseState


def es_conn_is_alive(es_conn: Elasticsearch) -> bool:
    '''Функция для проверки работоспособности Elasticsearch'''
    try:
        return es_conn.ping()
    except Exception:
        return False


class ElasticsearchLoader:
    logger = logging.getLogger(__name__)

    def __init__(
        self,
        settings: ElasticsearchSettings,
        state: BaseState,
        es_conn: Optional[Elasticsearch] = None,
        chunk_size: int = 100,
    ) -> None:
        self._settings = settings
        self._state = state
        self._es_conn = es_conn
        self.chunk_size = chunk_size

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def _reconnection(self) -> Elasticsearch:
        if self._es_conn is not None:
            self._es_conn.close()

        return Elasticsearch(
            [
                (
                    f'{self._settings.protocol}://{self._settings.user}:{self._settings.password}'
                    f'@{self._settings.host}:{self._settings.port}'
                )
            ]
        )

    @property
    def es_conn(self):
        if self._es_conn is None or not es_conn_is_alive(self._es_conn):
            self._es_conn = self._reconnection()
        return self._es_conn

    def _load_wrapper(
        self, data: Iterator[tuple[FilmWorkModelIntoES, str]], index: str
    ) -> Iterator[FilmWorkModelIntoES]:
        down_limit = None
        i = 0

        for movie, updated_at in data:
            down_limit = updated_at
            i += 1

            movie_dict = movie.dict()
            movie_dict['_id'] = movie.id
            yield movie_dict

            if i % self.chunk_size == 0:
                self.logger.debug(r'i % chunk_size =' + updated_at)
                self._state.set(f'down_limit_{Schema.film_work}', down_limit)

        if down_limit is not None:
            self.logger.debug(r'flushed with =' + updated_at)
            self._state.set(f'down_limit_{Schema.film_work}', down_limit)

    def load(self, data: Iterator[tuple[FilmWorkModelIntoES, str]], index: str) -> None:
        movies: Iterator[FilmWorkModelIntoES] = self._load_wrapper(data, index)

        lines, _ = helpers.bulk(client=self.es_conn, actions=movies, index=index)

        logger.info(f'STATE - {self._state.get(f"down_limit_{Schema.film_work}")}')
        if lines == 0:
            logger.info('Nothing to update for index %s', index)
        else:
            logger.info('%s lines saved for index %s', lines, index)
