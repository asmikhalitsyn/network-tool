import functools

from parser.actions import TestBaseAction
from parser.Juniper import show_bfd_session

STATE_NOT_CHANGE = 'BFD state of sessions are same'
STATE_CHANGE = ('BFD state of peers have changed:\n'
                'Precheck: {pre_dict}\n'
                'Postcheck: {post_dict}')
COMMAND = 'show bfd session'


class BfdPeerSessionCheck(TestBaseAction):

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def run_command(conn):
        return conn.send_command(COMMAND)

    def initial_bfd_sessions(self, pre) -> show_bfd_session.BfdPeers:
        return self.show_cached_command(COMMAND, pre)

    def bfd_sessions(self, post) -> show_bfd_session.BfdPeers:
        return self.show_cached_command(COMMAND, post)

    def run(self, pre, post):
        precheck_dict = {}
        postcheck_dict = {}
        initials_bfd_sessions = self.initial_bfd_sessions(pre)
        bfd_sessions_after_work = self.bfd_sessions(post)
        if initials_bfd_sessions.bfd_peers == bfd_sessions_after_work.bfd_peers:
            return STATE_NOT_CHANGE, 'OK'
        for peer in initials_bfd_sessions.bfd_peers:
            if peer not in bfd_sessions_after_work.bfd_peers:
                precheck_dict[peer.bfd_peer] = peer.state
        for peer in bfd_sessions_after_work.bfd_peers:
            if peer not in initials_bfd_sessions.bfd_peers:
                postcheck_dict[peer.bfd_peer] = peer.state

        return STATE_CHANGE.format(
            pre_dict=precheck_dict,
            post_dict=postcheck_dict
        ), 'FAIL'
