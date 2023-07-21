from abc import ABC
from abc import abstractmethod
from collections.abc import Sequence

from pydantic import BaseModel


class AbstractCommand(ABC, BaseModel):

    @classmethod
    @abstractmethod
    def parse(cls, output: str):
        raise NotImplementedError


class AbstractCommandSequence(Sequence, AbstractCommand):

    @abstractmethod
    def __getitem__(self, i: int):
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError
