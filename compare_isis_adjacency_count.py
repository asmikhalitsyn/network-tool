from parser.Juniper import show_isis_count
from parser.actions import TestBaseAction

TOTAL_COUNT_NOT_CHANGE = 'Total number of ISIS peer are same'
TOTAL_COUNT_CHANGE = ('ISIS total peer changed:\n'
                      'Number_of_isis_peers of Precheck: {pre_total_number}\n'
                      'Number_of_isis_peers of Postcheck: {post_total_number}')
COMMAND = 'show isis adjacency | count'


class IsisAdjacencyCountCheck(TestBaseAction):

    @staticmethod
    def run_command(conn):
        return conn.send_command(COMMAND)

    def initial_isis_adjacency_count(self, pre) -> show_isis_count.IsisCount:
        return self.show_cached_command(COMMAND, pre)

    def isis_adjacency_count(self, post) -> show_isis_count.IsisCount:
        return self.show_cached_command(COMMAND, post)

    def run(self, pre, post):
        initials_isis_count = self.initial_isis_adjacency_count(pre)
        isis_count_after_work = self.isis_adjacency_count(post)
        if initials_isis_count.count != isis_count_after_work.count:
            return TOTAL_COUNT_CHANGE.format(
                pre_total_number=initials_isis_count.count,
                post_total_number=isis_count_after_work.count
            ), 'FAIL'
        return TOTAL_COUNT_NOT_CHANGE, 'OK'
