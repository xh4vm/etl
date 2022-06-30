from abc import ABCMeta, abstractmethod
from typing import Any


class BaseState:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self) -> dict[str, Any]:
        '''Получение состояния'''

    @abstractmethod
    def set(self) -> None:
        '''Установка состояния'''
