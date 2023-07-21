from typing import List, Union, Optional
import dataclasses

from parser.Juniper._regex import (
    VPN_TABLE,
    PREFIX,
    NEXT_HOP,
    NEXT_HOP_NULL,
    METRIC,
    LOCALPREF,
    MED,
    FROM_NEIGHBOR,
    AS_PATH,
    PROTOCOL_AND_AD

)
from parser.utils import opt_search


@dataclasses.dataclass(frozen=True)
class NextHopNull:
    next_hop: str

    def __str__(self):
        return str(self.next_hop)

    def __repr__(self):
        return str(self.next_hop)


@dataclasses.dataclass(frozen=True)
class NextHop:
    next_hop: str

    def __str__(self):
        return str(self.next_hop)

    def __repr__(self):
        return str(self.next_hop)


@dataclasses.dataclass(frozen=True)
class RouteAttribute:
    table: str
    prefix: str
    metric: Optional[int]
    ip_neighbor: Optional[str]
    as_path: Optional[str]
    med: Optional[int]
    localpref: Optional[int]
    next_hop: List[Union[NextHop, NextHopNull]]

    @property
    def diff_key(self):
        return self.table, self.prefix, self.ip_neighbor


@dataclasses.dataclass(frozen=True)
class RouteTablesBgp:
    routes: List[RouteAttribute]

    def __getitem__(self, i: int):
        return self.routes.__getitem__(i)

    def __len__(self) -> int:
        return len(self.routes)

    def __iter__(self):
        return iter(self.routes)

    @classmethod
    def parse(cls, output: str):
        routing_tables = VPN_TABLE.split(output)
        routing_headers = VPN_TABLE.finditer(output)
        routes_list = []
        for idx, routing_header in enumerate(routing_headers, start=1):
            if idx % 2 != 0:
                vrf_table_name = routing_tables[idx]
            else:
                routing_information = routing_tables[idx]
                prefix_tables = PREFIX.split(routing_information)
                for idx_, prefix_header in enumerate(PREFIX.finditer(routing_information), start=1):
                    delta = prefix_tables[idx_ * 2]
                    neighbor_table = PROTOCOL_AND_AD.split(delta)
                    for idx__ in range(1, len(neighbor_table)):
                        bgp_information = neighbor_table[idx__]
                        if NEXT_HOP.search(bgp_information):
                            nh_list = [NextHop(**obj_match.groupdict())
                                       for obj_match in NEXT_HOP.finditer(bgp_information)]
                        elif NEXT_HOP_NULL.search(delta):
                            nh_list = [NextHopNull(**obj_match.groupdict())
                                       for obj_match in NEXT_HOP_NULL.finditer(bgp_information)]
                        routes_list.append(RouteAttribute(**{
                            'table': vrf_table_name,
                            **prefix_header.groupdict(),
                            'localpref': opt_search(LOCALPREF, bgp_information),
                            'med': opt_search(MED, bgp_information),
                            'as_path': opt_search(AS_PATH, bgp_information),
                            'ip_neighbor': opt_search(FROM_NEIGHBOR, bgp_information)
                            if opt_search(FROM_NEIGHBOR, bgp_information) else 'Local_router',
                            'metric': opt_search(METRIC, bgp_information),
                            'next_hop': nh_list
                        }))
        return cls(routes=routes_list)
