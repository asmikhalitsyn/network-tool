from parser.Juniper import show_isis_adjacency
from parser.actions import TestBaseAction

STATE_NOT_CHANGE = 'ISIS adjacency is same'
STATE_CHANGE = ('ISIS adjacency has changed:\n'
                'Precheck: {pre_dict}\n'
                'Postcheck: {post_dict}')
COMMAND = 'show isis adjacency'


class IsisAdjacencyCheck(TestBaseAction):

    @staticmethod
    def run_command(conn):
        return conn.send_command(COMMAND)

    def initial_isis_adjacency(self, pre) -> show_isis_adjacency.IsisInterfaces:
        return self.show_cached_command(COMMAND, pre)

    def isis_adjacency(self, post) -> show_isis_adjacency.IsisInterfaces:
        return self.show_cached_command(COMMAND, post)

    def run(self, pre, post):
        precheck_dict = {}
        postcheck_dict = {}
        initials_isis_adjacency = self.initial_isis_adjacency(pre)
        isis_adjacency_after_work = self.isis_adjacency(post)
        if initials_isis_adjacency.isis_interface == isis_adjacency_after_work.isis_interface:
            return STATE_NOT_CHANGE, 'OK'
        for isis_interface in initials_isis_adjacency.isis_interface:
            if isis_interface not in isis_adjacency_after_work.isis_interface:
                precheck_dict[isis_interface.interface] = isis_interface.state
        for isis_interface in isis_adjacency_after_work.isis_interface:
            if isis_interface not in initials_isis_adjacency.isis_interface:
                postcheck_dict[isis_interface.interface] = isis_interface.state

        return STATE_CHANGE.format(
            pre_dict=precheck_dict,
            post_dict=postcheck_dict
        ), 'FAIL'
