from parser.actions import TestBaseAction
from parser.Juniper import show_route_protocol_direct

STATE_NOT_CHANGE = 'Route table direct are same'
STATE_CHANGE = ('Route table direct have changed:\n\n'
                'Precheck: {pre_dict}\n\n'
                'Postcheck: {post_dict}')
COMMAND = 'show route protocol direct'


class RouteDirectCheck(TestBaseAction):

    @staticmethod
    def run_command(conn):
        return conn.send_command(COMMAND)

    def initial_route_direct(self, pre) -> show_route_protocol_direct.RouteTablesDirect:
        return self.show_cached_command(COMMAND, pre)

    def route_direct(self, post) -> show_route_protocol_direct.RouteTablesDirect:
        return self.show_cached_command(COMMAND, post)

    def run(self, pre, post):
        precheck_list = []
        postcheck_list = []
        initials_routes_direct = self.initial_route_direct(pre)
        routes_direct_after_work = self.route_direct(post)
        if initials_routes_direct.routes == routes_direct_after_work.routes:
            return STATE_NOT_CHANGE, 'OK'
        for route in initials_routes_direct.routes:
            if route not in routes_direct_after_work.routes:
                precheck_list.append({route.prefix: {'table': route.table,
                                                     'next_hop': route.next_hop,
                                                     'ad': route.ad}}
                                     )
        for route in routes_direct_after_work.routes:
            if route not in initials_routes_direct.routes:
                postcheck_list.append({route.prefix: {'table': route.table,
                                                      'next_hop': route.next_hop,
                                                      'ad': route.ad}}
                                      )
        return STATE_CHANGE.format(
            pre_dict=precheck_list,
            post_dict=postcheck_list
        ), 'FAIL'
