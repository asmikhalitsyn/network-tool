from compare_bgp_session_of_neighbors import BgpNeighborSessionCheck

TOTAL_COUNT_NOT_CHANGE = 'Total number of BGP peers are same'
TOTAL_COUNT_CHANGE = ('BGP total peer changed:\n'
                      'Number_of_bgp_peers of Precheck: {pre_total_number}\n'
                      'Number_of_bgp_peers of Postcheck: {post_total_number}')


class BgpNeighborCountCheck(BgpNeighborSessionCheck):

    def run(self, pre, post):
        initials_bgp_neighbors = self.initial_bgp_neighbors(pre)
        bgp_neighbors_after_work = self.bgp_neighbors(post)
        if initials_bgp_neighbors.total_number_of_peers != bgp_neighbors_after_work.total_number_of_peers:
            return TOTAL_COUNT_CHANGE.format(
                pre_total_number=initials_bgp_neighbors.total_number_of_peers,
                post_total_number=bgp_neighbors_after_work.total_number_of_peers
            ), 'FAIL'
        return TOTAL_COUNT_NOT_CHANGE, 'OK'
