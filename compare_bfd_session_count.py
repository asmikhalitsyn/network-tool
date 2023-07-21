from compare_bfd_session import BfdPeerSessionCheck

TOTAL_COUNT_NOT_CHANGE = 'Total number of BFD peers are same'
TOTAL_COUNT_CHANGE = ('BFD total peer changed:\n'
                      'Number_of_bfd_peers of Precheck: {pre_total_number}\n'
                      'Number_of_bfd_peers of Postcheck: {post_total_number}')


class BfdSessionCountCheck(BfdPeerSessionCheck):

    def run(self, pre, post):
        initials_bfd_sessions = self.initial_bfd_sessions(pre)
        bfd_sessions_after_work = self.bfd_sessions(post)
        if initials_bfd_sessions.total_number_of_peers != bfd_sessions_after_work.total_number_of_peers:
            return TOTAL_COUNT_CHANGE.format(
                pre_total_number=initials_bfd_sessions.total_number_of_peers,
                post_total_number=bfd_sessions_after_work.total_number_of_peers
            ), 'FAIL'
        return TOTAL_COUNT_NOT_CHANGE, 'OK'
