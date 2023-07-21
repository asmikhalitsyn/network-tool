import os

import click
from dotenv import load_dotenv

from connections import get_api_response
from ping_utils import ping_ip_addresses, ping_table

load_dotenv()

NETBOX_URL = 'https://10.56.178.246/'
NETBOX_TOKEN = os.getenv('TOKEN_NETBOX')


@click.command()
@click.argument('hostnames', nargs=-1, required=False)
def main(hostnames):
    routers = get_api_response(hostnames, NETBOX_URL, NETBOX_TOKEN)
    ok, fail = ping_ip_addresses(routers)
    return print(ping_table(ok, fail))


if __name__ == '__main__':
    main()
