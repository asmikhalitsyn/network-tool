import re

BGP_LOCAL_AS = re.compile(
    r'Local\sAS\snumber\s+:\s(\S+)', re.M)
BGP_LOCAL_ROUTER_ID = re.compile(
    r'BGP\slocal\srouter\sID\s+:\s(.+?)$', re.M)
BGP_NUMBER_ESTABLISHED_PEERS = re.compile(
    r'Peers\sin\sestablished\sstate\s:\s(\d+)', re.M)
BGP_TOTAL_NUMBER_OF_PEERS = re.compile(
    r'Total\snumber\sof\speers\s+:\s(\d+)', re.M)
BGP_NEIGHBOR = re.compile(
    r'^\s+(?P<neighbor>\S+)'
    r'\s+(?P<asn>\S+)'
    r'\s+(?P<message_received>\d+)'
    r'\s+(?P<message_sent>\d+)'
    r'\s+(?P<out_q>\d+)'
    r'\s+(?P<up_down>\S+)'
    r'\s+(?P<state>\S+)'
    r'\s+(?P<prefix_received>\d+)'
    r'\s+(?P<prefix_advertised>\d+)', re.M)
BGP_VPN_AWARE = re.compile(
    r'Peer\sof\sIPv4-family\sfor\svpn\sinstance\s+:', re.M)
VPN_PEER_TABLE = re.compile(
    r'^\s+VPN-Instance\s(?P<vpn_instance>\S+),\sRouter\sID\s(?P<local_router_id>.+?):\n', re.M)