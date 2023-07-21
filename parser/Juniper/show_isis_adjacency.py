from typing import List

from parser.base import AbstractCommandSequence
from pydantic import BaseModel

from parser.Juniper._regex import ISIS_ADJACENCY


class IsisInterface(BaseModel):
    interface: str
    state: str


class IsisInterfaces(AbstractCommandSequence):
    isis_interface: List[IsisInterface]

    def __getitem__(self, i: int):
        return self.isis_interface.__getitem__(i)

    def __len__(self) -> int:
        return len(self.isis_interface)

    def __iter__(self):
        return iter(self.isis_interface)

    @classmethod
    def parse(cls, output: str) -> 'IsisInterfaces':
        interfaces = [interface.groupdict()
                      for interface in ISIS_ADJACENCY.finditer(output)]
        return cls.parse_obj({'isis_interface': interfaces})
