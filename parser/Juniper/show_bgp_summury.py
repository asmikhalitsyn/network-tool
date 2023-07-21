from typing import List, Optional

from parser.base import AbstractCommandSequence
from pydantic import BaseModel
from parser.utils import opt_search

from parser.Juniper._regex import (
    BGP_NUMBER_DOWN_PEERS,
    BGP_TOTAL_NUMBER_OF_PEERS,
    BGP_PEER
)


class BgpPeer(BaseModel):
    peer: str
    state: str


class BgpPeers(AbstractCommandSequence):
    total_number_of_peers: Optional[int]
    peers_in_down_state: Optional[int]
    peers: List[BgpPeer]

    def __getitem__(self, i: int):
        return self.peers.__getitem__(i)

    def __len__(self) -> int:
        return len(self.peers)

    def __iter__(self):
        return iter(self.peers)

    @classmethod
    def parse(cls, output: str) -> 'BgpPeers':
        peers = [peer.groupdict()
                 for peer in BGP_PEER.finditer(output)]
        return cls.parse_obj({
            'peers_in_down_state': opt_search(BGP_NUMBER_DOWN_PEERS, output),
            'total_number_of_peers': opt_search(BGP_TOTAL_NUMBER_OF_PEERS, output),
            'peers': peers,
        })
