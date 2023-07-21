from typing import List, Optional

from parser.base import AbstractCommandSequence
from pydantic import BaseModel
from parser.utils import opt_search

from parser.Juniper._regex import (
    BFD_SESSION,
    BFD_NUMBER_SESSION,
)


class BfdPeer(BaseModel):
    bfd_peer: str
    state: str


class BfdPeers(AbstractCommandSequence):
    total_number_of_peers: Optional[int]
    bfd_peers: List[BfdPeer]

    def __getitem__(self, i: int):
        return self.bfd_peers.__getitem__(i)

    def __len__(self) -> int:
        return len(self.bfd_peers)

    def __iter__(self):
        return iter(self.bfd_peers)

    @classmethod
    def parse(cls, output: str) -> 'BfdPeers':
        peers = [peer.groupdict()
                 for peer in BFD_SESSION.finditer(output)]
        return cls.parse_obj({
            'total_number_of_peers': opt_search(BFD_NUMBER_SESSION, output),
            'bfd_peers': peers,
        })
