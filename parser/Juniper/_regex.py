import re

BGP_NUMBER_DOWN_PEERS = re.compile(
    r'Down peers:\s(\d+)', re.M
)
BGP_TOTAL_NUMBER_OF_PEERS = re.compile(
    r'Peers:\s(\d+)', re.M
)

BGP_PEER = re.compile(
    r'(?P<peer>^\d+\S+)'
    r'\s+(?P<asn>\S+)'
    r'\s+(?P<inpkt>\S+)'
    r'\s+(?P<outpkt>\S+)'
    r'\s+(?P<outq>\S+)'
    r'\s+(?P<flaps>\S+)'
    r'\s+(?P<last>\w*)'
    r'\s+(?P<up_down>[\d:]+)'
    r'\s+(?P<state>\w+)', re.M
)

ISIS_ADJACENCY = re.compile(
    r'(?P<interface>\w{2}-\d+/\d\/\S+)'
    r'\s+(?P<system>\S+)'
    r'\s+(?P<level>\d+)'
    r'\s+(?P<state>\S+)'
    r'\s+(?P<hold>\d+)', re.M
)

ISIS_COUNT = re.compile(
    r'Count: (?P<count>\d+)', re.M
)

BFD_SESSION = re.compile(
    r'(?P<bfd_peer>\d+\.\d+\.\d+\.\d+)'
    r'\s+(?P<state>\w+)'
    r'\s+(?P<interface>\S+)'
    r'\s+(?P<detect_time>\S+)'
    r'\s+(?P<transmit_interval>\S+)'
    r'\s+(?P<multiplier>\S+)', re.M
)

BFD_NUMBER_SESSION = re.compile(
    r'(?P<bfd_count>\d+) sessions', re.M
)

ALARM = re.compile(r'(?P<alarm>\w+ alarms currently active)', re.M)
VPN_TABLE = re.compile(
    r'^(?P<table>\S+):\s+', re.M
)

PREFIX = re.compile(
    r'^(?P<prefix>\d+\.\d+\.\d+\.\d+\/\d+)', re.M
)

NEXT_HOP = re.compile(r'\s+(to|via)\s+(?P<next_hop>.*)', re.M)
NEXT_HOP_NULL = re.compile(r'(?P<next_hop>Discard|Reject)', re.M)
PROTOCOL = re.compile(r'\[(?P<protocol>\S+)\/', re.M)
METRIC = re.compile(r'metric\s+(?P<metric>\S+)', re.M)
AD = re.compile(r'\/(?P<ad>\S+)\]', re.M)

AS_PATH = re.compile(r'AS path:\s+(?P<as_path>(\d+\s+)*(I|\?)),', re.M)
LOCALPREF = re.compile(r'localpref\s+(?P<localpref>\S+),', re.M)
MED = re.compile(r'MED\s+(?P<med>\S+),', re.M)
FROM_NEIGHBOR = re.compile(r'from (?P<ip_neighbor>\S+)', re.M)
PROTOCOL_AND_AD = re.compile(r'\[\S+\]', re.M)
