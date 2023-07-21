import subprocess
from tabulate import tabulate

from check_utils import check_response
from netrnd_parse import parse_response_api


def ping_ip_addresses(routers):
    ping_ok_list = []
    ping_fail_list = []
    for router in routers:
        router_after_check = check_response(router)
        ip_address, _ = parse_response_api(router_after_check)
        reply = subprocess.run(['ping', '-c', '3', ip_address],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               encoding='utf-8')
        if reply.returncode == 0:
            ping_ok_list.append(ip_address)
        else:
            ping_fail_list.append(ip_address)
    return ping_ok_list, ping_fail_list


def ping_table(ping_ok, ping_fail):
    status_of_ping = {
        'Reachable': ping_ok,
        'Unreachable': ping_fail
    }
    return tabulate(
        status_of_ping,
        headers='keys',
        tablefmt="grid"
    )

