#!/usr/bin/env python3
import os
from typing import List
import yaml

import click
from dotenv import load_dotenv
from scrapli import Scrapli
from scrapli.exceptions import (
    ScrapliConnectionError,
    ScrapliAuthenticationFailed,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from session_cache import (
    check_checkpoint,
    check_host_and_checkpoint,
    save_host,
    save_command
)
from check_utils import check_response
from connections import get_api_response, create_data
from logger import get_logger
from netrnd_parse import parse_response_api

load_dotenv()

file_path = os.getcwd() + '/check.db'
db_name = 'sqlite:///' + file_path
NETBOX_URL = 'https://10.43.171.82/'
NETBOX_TOKEN = os.getenv('TOKEN_NETBOX')
USERNAME_ROUTER = os.getenv('USERNAME_OF_ROUTER')
PASSWORD_ROUTER = os.getenv('PASSWORD_OF_ROUTER')
SAVE_TO_DB = 'Идет сохранение данных в БД'
COMMON_ERROR = 'Произошла ошибка: {error}'
FAIL_CONNECTION = ('Ошибка при подключении к устройству {host} '
                   'error: {error} ')
FAIL_AUTH = ('Проблема c аутентификацией или достпуностью при подключении к устройству {host} '
             'auth_error: {auth_error} ')
FAIL_CONNECTION_NB = ('Ошибка при подключении к  NetBox '
                      'с параметрами: '
                      '{url}, {token}. '
                      'error: {error}. ')
CONN_DEVICE = 'Подключение к устройству {ip}'

engine = create_engine(db_name)
session = Session(bind=engine)

log = get_logger(__name__)


def save_to_bd(result: List, checkpoint: str) -> None:
    log.info(SAVE_TO_DB)
    check = check_checkpoint(checkpoint)
    for host, platform, cases in result:
        host = save_host(str(host), platform, check.id)
        for case in cases:
            output, input_cmd, test_name = case
            save_command(
                command=input_cmd,
                test=test_name,
                output=output,
                checkpoint_id=check.id,
                host_id=host.id
            )


@click.command()
@click.option('--config_hostnames', '-hostnames', type=click.Path())
@click.option('--checkpoint', '-cp', required=True, type=str)
def main(config_hostnames, checkpoint):
    cases_of_responses = []
    with open(config_hostnames) as f:
        hostnames = yaml.safe_load(f)
    try:
        routers = get_api_response(hostnames, NETBOX_URL, NETBOX_TOKEN)
        new_dict_with_hostnames = {router: hostnames[str(router)] for router in routers}
        check_host_and_checkpoint(routers, checkpoint)
        for router, tests in new_dict_with_hostnames.items():
            router_after_check = check_response(router)
            ip_address, platform = parse_response_api(router_after_check)
            connection = {
                'host': ip_address,
                'auth_username': USERNAME_ROUTER,
                'auth_password': PASSWORD_ROUTER,
                'timeout_socket': 10,
                'timeout_transport': 10,
                'auth_strict_key': False,
                'platform': platform
            }
            try:
                log.info(CONN_DEVICE.format(ip=router_after_check))
                conn = Scrapli(**connection)
                conn.open()
                structure = create_data(str(router_after_check), tests, conn)
                if structure:
                    cases_of_responses.extend([structure])
            except ScrapliConnectionError as conn_error:
                log.exception(FAIL_CONNECTION.format(
                    error=conn_error,
                    host=router_after_check
                ))
            except ScrapliAuthenticationFailed as auth_error:
                log.exception(FAIL_AUTH.format(
                    auth_error=auth_error,
                    host=router_after_check
                ))
        save_to_bd(cases_of_responses, checkpoint)
    except Exception as err:
        error_msg = COMMON_ERROR.format(error=err)
        log.exception(error_msg)


if __name__ == '__main__':
    main()
