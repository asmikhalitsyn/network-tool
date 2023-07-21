from parser.actions import TestBaseAction
from parser.Juniper import show_route_protocol_local

STATE_NOT_CHANGE = 'Route table local are same'
STATE_CHANGE = ('Route table local have changed:\n\n'
                'Precheck: {pre_dict}\n\n'
                'Postcheck: {post_dict}')
COMMAND = 'show route protocol local'


class RouteLocalCheck(TestBaseAction):

    @staticmethod
    def run_command(conn):
        return conn.send_command(COMMAND)

    def initial_route_local(self, pre) -> show_route_protocol_local.RouteTablesLocal:
        return self.show_cached_command(COMMAND, pre)

    def route_local(self, post) -> show_route_protocol_local.RouteTablesLocal:
        return self.show_cached_command(COMMAND, post)

    def run(self, pre, post):
        precheck_list = []
        postcheck_list = []
        initials_routes_local = self.initial_route_local(pre)
        routes_local_after_work = self.route_local(post)
        if initials_routes_local.routes == routes_local_after_work.routes:
            return STATE_NOT_CHANGE, 'OK'
        for route in initials_routes_local.routes:
            if route not in routes_local_after_work.routes:
                precheck_list.append({route.prefix: {'table': route.table,
                                                     'next_hop': route.next_hop,
                                                     'ad': route.ad}}
                                     )
        for route in routes_local_after_work.routes:
            if route not in initials_routes_local.routes:
                postcheck_list.append({route.prefix: {'table': route.table,
                                                      'next_hop': route.next_hop,
                                                      'ad': route.ad}}
                                      )
        return STATE_CHANGE.format(
            pre_dict=precheck_list,
            post_dict=postcheck_list
        ), 'FAIL'
