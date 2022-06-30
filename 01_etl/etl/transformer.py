from typing import Any, Iterator
from pydantic import BaseModel

from .extractor import Extractor


class Transformer:

    def __init__(self, extractor : Extractor):
        self.extractor = extractor

    def transform_some_data(self, schema : BaseModel, data : list[tuple[Any]]) -> Iterator[BaseModel]:
        for row in data:
            yield schema(*row)
