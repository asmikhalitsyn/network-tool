from parser.actions import TestBaseAction
from parser.Juniper import show_route_protocol_isis

STATE_NOT_CHANGE = 'Route table isis are same'
STATE_CHANGE = ('Route table isis have changed:\n\n'
                'Precheck: {pre_dict}\n\n'
                'Postcheck: {post_dict}')
COMMAND = 'show route protocol isis'


class RouteIsisCheck(TestBaseAction):

    @staticmethod
    def run_command(conn):
        return conn.send_command(COMMAND)

    def initial_route_isis(self, pre) -> show_route_protocol_isis.RouteTablesIsis:
        return self.show_cached_command(COMMAND, pre)

    def route_isis(self, post) -> show_route_protocol_isis.RouteTablesIsis:
        return self.show_cached_command(COMMAND, post)

    def run(self, pre, post):
        precheck_list = []
        postcheck_list = []
        initials_routes_isis = self.initial_route_isis(pre)
        routes_isis_after_work = self.route_isis(post)
        if initials_routes_isis.routes == routes_isis_after_work.routes:
            return STATE_NOT_CHANGE, 'OK'
        for route in initials_routes_isis.routes:
            if route not in routes_isis_after_work.routes:
                precheck_list.append({route.prefix: {'table': route.table,
                                                     'metric': route.metric,
                                                     'next_hop': route.next_hop,
                                                     'ad': route.ad}}
                                     )
        for route in routes_isis_after_work.routes:
            if route not in initials_routes_isis.routes:
                postcheck_list.append({route.prefix: {'table': route.table,
                                                      'metric': route.metric,
                                                      'next_hop': route.next_hop,
                                                      'ad': route.ad}}
                                      )
        return STATE_CHANGE.format(
            pre_dict=precheck_list,
            post_dict=postcheck_list
        ), 'FAIL'
