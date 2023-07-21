from typing import List, Optional

from parser.base import AbstractCommandSequence
from pydantic import BaseModel

from parser.Huawei._regex import (
    BGP_NEIGHBOR,
)


class HuaweiBgpPeer(BaseModel):
    neighbor: str
    state: str


class HuaweiBgpPeers(AbstractCommandSequence):
    total_number_of_peers: Optional[int]
    peers_in_down_state: Optional[int]
    peers: List[HuaweiBgpPeer]

    def __getitem__(self, i: int):
        return self.peers.__getitem__(i)

    def __len__(self) -> int:
        return len(self.peers)

    def __iter__(self):
        return iter(self.peers)

    @classmethod
    def parse(cls, output: str) -> 'HuaweiBgpPeers':
        peers = [peer.groupdict()
                 for peer in BGP_NEIGHBOR.finditer(output)]
        return cls.parse_obj({
            'peers': peers,
        })
