import deepdiff as dd
import itertools

from parser.actions import TestBaseAction
from parser.Juniper import show_route_protocol_bgp

STATE_NOT_CHANGE = 'Route table BGP are same'
COMMAND = 'show route protocol bgp'


def humanize_diff_path(diff_path):
    item_human_names = {
        'lp': 'local_preference',
        'nh': 'next_hop',
    }
    return [str(item) if type(item) is int else item_human_names.get(item, item) for item in diff_path]


class RouteBgpCheck(TestBaseAction):

    @staticmethod
    def run_command(conn):
        return conn.send_command(COMMAND)

    def initial_route_bgp(self, pre) -> show_route_protocol_bgp.RouteTablesBgp:
        return self.show_cached_command(COMMAND, pre)

    def route_bgp(self, post) -> show_route_protocol_bgp.RouteTablesBgp:
        return self.show_cached_command(COMMAND, post)

    def run(self, pre, post):
        initials_routes_bgp = self.initial_route_bgp(pre)
        routes_bgp_after_work = self.route_bgp(post)
        diff = dd.DeepDiff(
            {r.diff_key: r for r in initials_routes_bgp.routes},
            {r.diff_key: r for r in routes_bgp_after_work.routes},
            ignore_order=True,
            view=dd.diff.TREE_VIEW
        )
        return self._diff(diff)

    def _diff(self, diff: dd.DeepDiff):
        msg_error_list = []
        if not diff:
            return STATE_NOT_CHANGE, 'OK'
        for i in itertools.chain(
                diff.get('values_changed', []),
                diff.get('dictionary_item_added', []),
                diff.get('dictionary_item_removed', []),
                diff.get('iterable_item_added', [])):
            diff_path, *rest = i.path(output_format='list')
            table, prefix, neighbor_ip = diff_path
            if rest and str(i.t1) == 'not present':
                attrib = rest[0]
                msg_error = f'Для префикса {prefix} полученного от соседа {neighbor_ip} в таблице {table} добавился {attrib} {i.t2}'
            elif rest:
                attrib = rest[0]
                msg_error = f'Для префикса {prefix} полученного от соседа {neighbor_ip} в таблице {table} изменился {attrib} c {i.t1} на {i.t2}'
            else:
                if str(i.t1) == 'not present':
                    msg_error = (
                        f'В ТМ {i.t2.table} появился префикс {i.t2.prefix} от соседа {i.t2.ip_neighbor} с параметрами: '
                        f'lp: {i.t2.localpref}, nh: {i.t2.next_hop}, as_path: {i.t2.as_path}')
                elif str(i.t2) == 'not present':
                    msg_error = (
                        f'Из ТМ {i.t1.table} пропал префикс {i.t1.prefix} от соседа {i.t1.ip_neighbor} с параметрами: '
                        f'lp: {i.t1.localpref}, nh: {i.t1.next_hop}, as_path: {i.t1.as_path}')
            msg_error_list.append(msg_error)

        return '\n'.join(sorted(msg_error_list)), 'FAIL'
