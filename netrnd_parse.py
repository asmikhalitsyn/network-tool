#!/usr/bin/env python3
from parser.Juniper.show_bgp_summury import BgpPeers
from parser.Juniper.show_isis_adjacency import IsisInterfaces
from parser.Juniper.show_isis_count import IsisCount
from parser.Juniper.show_bfd_session import BfdPeers
from parser.Juniper.show_alarm import ChassisSystemAlarm
from parser.Juniper.show_route_protocol_static import RouteTablesStatic
from parser.Juniper.show_route_protocol_direct import RouteTablesDirect
from parser.Juniper.show_route_protocol_local import RouteTablesLocal
from parser.Juniper.show_route_protocol_rsvp import RouteTablesRsvp
from parser.Juniper.show_route_protocol_isis import RouteTablesIsis
from parser.Juniper.show_route_protocol_bgp import RouteTablesBgp

from parser.Huawei.display_bgp_all_summary import HuaweiBgpPeers


JUNIPER = 'juniper_junos'
HUAWEI = 'huawei_vrp'

PARSERS = {
    JUNIPER: {
        'show bgp summary': BgpPeers,
        'show isis adjacency': IsisInterfaces,
        'show isis adjacency | count': IsisCount,
        'show bfd session': BfdPeers,
        'show system alarms': ChassisSystemAlarm,
        'show chassis alarms': ChassisSystemAlarm,
        'show route protocol static': RouteTablesStatic,
        'show route protocol direct': RouteTablesDirect,
        'show route protocol local': RouteTablesLocal,
        'show route protocol rsvp': RouteTablesRsvp,
        'show route protocol isis': RouteTablesIsis,
        'show route protocol bgp': RouteTablesBgp,

    },
    HUAWEI: {
        'display bgp all summary': HuaweiBgpPeers

    }
}


def parse_raw(command: str, output: str, platform: str):
    return PARSERS[platform][command].parse(output)


def parse_response_api(router):
    ip, _ = router.primary_ip.address.split('/')
    return ip, router.platform.name

