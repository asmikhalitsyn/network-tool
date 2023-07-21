from compare_bgp_neighbors_count import BgpNeighborCountCheck
from compare_bgp_session_of_neighbors import BgpNeighborSessionCheck
from compare_bgp_neighbors_count_down import BgpNeighborCountCheckDown
from compare_isis_adjacency import IsisAdjacencyCheck
from compare_isis_adjacency_count import IsisAdjacencyCountCheck
from compare_bfd_session_count import BfdSessionCountCheck
from compare_bfd_session import BfdPeerSessionCheck
from compare_chassis_alarms import ChassisAlarmsCheck
from compare_system_alarms import SystemAlarmsCheck
from compare_route_static import RouteStaticCheck
from compare_route_direct import RouteDirectCheck
from compare_route_isis import RouteIsisCheck
from compare_route_local import RouteLocalCheck
from compare_route_rsvp import RouteRsvpCheck
from compare_route_bgp import RouteBgpCheck

TEST_CASE = {
    'TestBgpNeighborSession': BgpNeighborSessionCheck,
    'TestBgpNeighborCount': BgpNeighborCountCheck,
    'TestBgpNeighborCountDown': BgpNeighborCountCheckDown,
    'TestIsisAdjacency': IsisAdjacencyCheck,
    'TestIsisAdjacencyCount': IsisAdjacencyCountCheck,
    'TestBfdSessionCount': BfdSessionCountCheck,
    'TestBfdPeerSession': BfdPeerSessionCheck,
    'TestChassisAlarm': ChassisAlarmsCheck,
    'TestSystemAlarm': SystemAlarmsCheck,
    'TestRouteStatic': RouteStaticCheck,
    'TestRouteDirect': RouteDirectCheck,
    'TestRouteIsis': RouteIsisCheck,
    'TestRouteLocal': RouteLocalCheck,
    'TestRouteBgp': RouteBgpCheck,
    'TestRouteRsvp': RouteRsvpCheck,
}
