from parser.actions import TestBaseAction
from parser.Juniper import show_route_protocol_rsvp

STATE_NOT_CHANGE = 'Route table rsvp are same'
STATE_CHANGE = ('Route table rsvp have changed:\n\n'
                'Precheck: {pre_dict}\n\n'
                'Postcheck: {post_dict}')
COMMAND = 'show route protocol rsvp'


class RouteRsvpCheck(TestBaseAction):

    @staticmethod
    def run_command(conn):
        return conn.send_command(COMMAND)

    def initial_route_rsvp(self, pre) -> show_route_protocol_rsvp.RouteTablesRsvp:
        return self.show_cached_command(COMMAND, pre)

    def route_rsvp(self, post) -> show_route_protocol_rsvp.RouteTablesRsvp:
        return self.show_cached_command(COMMAND, post)

    def run(self, pre, post):
        precheck_list = []
        postcheck_list = []
        initials_routes_rsvp = self.initial_route_rsvp(pre)
        routes_rsvp_after_work = self.route_rsvp(post)
        if initials_routes_rsvp.routes == routes_rsvp_after_work.routes:
            return STATE_NOT_CHANGE, 'OK'
        for route in initials_routes_rsvp.routes:
            if route not in routes_rsvp_after_work.routes:
                precheck_list.append({route.prefix: {'table': route.table,
                                                     'metric': route.metric,
                                                     'next_hop': route.next_hop,
                                                     'ad': route.ad}}
                                     )
        for route in routes_rsvp_after_work.routes:
            if route not in initials_routes_rsvp.routes:
                postcheck_list.append({route.prefix: {'table': route.table,
                                                      'metric': route.metric,
                                                      'next_hop': route.next_hop,
                                                      'ad': route.ad}}
                                      )
        return STATE_CHANGE.format(
            pre_dict=precheck_list,
            post_dict=postcheck_list
        ), 'FAIL'
