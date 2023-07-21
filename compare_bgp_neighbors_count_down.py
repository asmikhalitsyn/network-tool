from compare_bgp_session_of_neighbors import BgpNeighborSessionCheck

COUNT_NOT_CHANGE = 'Number of BGP peers in down are same'
COUNT_CHANGE = ('BGP peer in down changed:\n'
                'Number_of_bgp_peers_in_down of Precheck: {pre_peers_in_down_state}\n'
                'Number_of_bgp_peers_in_down of Postcheck: {post_peers_in_down_state}\n')


class BgpNeighborCountCheckDown(BgpNeighborSessionCheck):

    def run(self, pre, post):
        initials_bgp_neighbors = self.initial_bgp_neighbors(pre)
        bgp_neighbors_after_work = self.bgp_neighbors(post)
        if initials_bgp_neighbors.peers_in_down_state != bgp_neighbors_after_work.peers_in_down_state:
            return COUNT_CHANGE.format(
                pre_peers_in_down_state=initials_bgp_neighbors.peers_in_down_state,
                post_peers_in_down_state=bgp_neighbors_after_work.peers_in_down_state
            ), 'FAIL'
        return COUNT_NOT_CHANGE, 'OK'
