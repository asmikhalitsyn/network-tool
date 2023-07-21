from parser.actions import TestBaseAction
from parser.Juniper import show_bgp_summury
import functools

STATE_NOT_CHANGE = 'BGP state of sessions are same'
STATE_CHANGE = ('BGP state of peers have changed:\n'
                'Precheck: {pre_dict}\n'
                'Postcheck: {post_dict}')
COMMAND = 'show bgp summary'


class BgpNeighborSessionCheck(TestBaseAction):

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def run_command(conn):
        return conn.send_command(COMMAND)

    def initial_bgp_neighbors(self, pre) -> show_bgp_summury.BgpPeers:
        return self.show_cached_command(COMMAND, pre)

    def bgp_neighbors(self, post) -> show_bgp_summury.BgpPeers:
        return self.show_cached_command(COMMAND, post)

    def run(self, pre, post):
        precheck_dict = {}
        postcheck_dict = {}
        initials_bgp_neighbors = self.initial_bgp_neighbors(pre)
        bgp_neighbors_after_work = self.bgp_neighbors(post)
        if initials_bgp_neighbors.peers == bgp_neighbors_after_work.peers:
            return STATE_NOT_CHANGE, 'OK'
        for peer in initials_bgp_neighbors.peers:
            if peer not in bgp_neighbors_after_work.peers:
                precheck_dict[peer.peer] = peer.state
        for peer in bgp_neighbors_after_work.peers:
            if peer not in initials_bgp_neighbors.peers:
                postcheck_dict[peer.peer] = peer.state

        return STATE_CHANGE.format(
            pre_dict=precheck_dict,
            post_dict=postcheck_dict
        ), 'FAIL'
