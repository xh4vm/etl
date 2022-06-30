from typing import Any, Iterator, Optional
from pydantic import BaseModel
from psycopg2.extras import DictCursor

from .state import BaseState


class Extractor:

    def __init__(self, cursor : DictCursor, state : BaseState, chunk_size : int = 100):
        self.cursor : DictCursor = cursor
        self.state : BaseState = state
        self.chunk_size : int = chunk_size

    def get_some_raw_data(self, schema : BaseModel, fields : set = None, where_statement : Optional[str] = None, in_statement : Optional[list[str]] = None) -> list[tuple[Any]]:
        where = f'WHERE {where_statement} IN {in_statement}'\
            if where_statement is not None and in_statement is not None \
            else '1 = 1'
        
        fields = schema.__fields_set__ if fields is None else fields
        query : str = (
            f'SELECT {", ".join(fields)} FROM {schema._meta.model}'
            f'{where}'
        )
        self.cursor.execute(query)
        
        return self.cursor.fetchmany(size=self.chunk_size)
