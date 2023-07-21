from typing import List, Union, Optional

from pydantic import BaseModel

from parser.Juniper._regex import (
    VPN_TABLE,
    PREFIX,
    NEXT_HOP,
    NEXT_HOP_NULL,
    PROTOCOL,
    METRIC,
    AD

)
from parser.base import AbstractCommandSequence
from parser.utils import opt_search


class NextHopNull(BaseModel):
    next_hop: str

    def __str__(self):
        return str(self.next_hop)

    def __repr__(self):
        return str(self.next_hop)


class NextHop(BaseModel):
    next_hop: str

    def __str__(self):
        return str(self.next_hop)

    def __repr__(self):
        return str(self.next_hop)


class RouteAttribute(BaseModel):
    ad: int
    protocol: str
    table: str
    prefix: str
    next_hop: List[Union[NextHop, NextHopNull]]
    metric: Optional[int]


class RouteTablesStatic(AbstractCommandSequence):
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
        for idx_, routing_header in enumerate(routing_headers, start=1):
            if idx_ % 2 != 0:
                table_name = routing_tables[idx_]
            else:
                routing_information = routing_tables[idx_]
                prefix_tables = PREFIX.split(routing_information)
                for idx, prefix_header in enumerate(PREFIX.finditer(routing_information), start=1):
                    delta = prefix_tables[idx * 2]
                    if NEXT_HOP.search(delta):
                        nh_list = [NextHop.parse_obj(obj_match.groupdict())
                                   for obj_match in NEXT_HOP.finditer(delta)]
                    elif NEXT_HOP_NULL.search(delta):
                        nh_list = [NextHopNull.parse_obj(obj_match.groupdict())
                                   for obj_match in NEXT_HOP_NULL.finditer(delta)]
                    common_dict = {
                        'table': table_name,
                        'protocol': opt_search(PROTOCOL, delta),
                        'ad': opt_search(AD, delta),
                        'metric': opt_search(METRIC, delta),
                        **prefix_header.groupdict(),
                        'next_hop': nh_list
                    }
                    routes_list.append(common_dict)
        return cls(routes=routes_list)
