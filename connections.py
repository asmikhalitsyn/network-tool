#!/usr/bin/env python3
import requests
from typing import List
import urllib3

import pynetbox
from scrapli import Scrapli

from exceptions import LengthError
from logger import get_logger
from settings import TEST_CASE

CONN_DEVICE = 'Подключение к устройству {ip}'
CONN_NETBOX = 'Подключение к Netbox'
LEN_NOT_EQUAL = ('Размер списка устройств полученный от NetBox не совпадает.\n'
                 'Начальный размер списка: {len_pre}.\n'
                 'Полученный размер списка: {len_post}')

FAIL_CONNECTION = ('Ошибка при подключении к устройству {host} '
                   'error: {error} ')
FAIL_AUTH = ('Проблема c аутентификацией при подключении к устройству {host} '
             'auth_error: {auth_error} ')
FAIL_CONNECTION_NB = ('Ошибка при подключении к  NetBox '
                      'с параметрами: '
                      '{url}, {token}. '
                      'error: {error}. ')

log = get_logger(__name__)


def create_data(router_after_check: str, tests: List, conn: Scrapli):
    responses = [[TEST_CASE[test].run_command(conn).result, TEST_CASE[test].run_command(conn).channel_input, test]
                 for test in tests]
    return router_after_check, conn.textfsm_platform, responses


def get_api_response(devices, url, token):
    try:
        log.info(CONN_NETBOX)
        urllib3.disable_warnings()
        nb = pynetbox.api(url=url, token=token)
        nb.http_session.verify = False
        list_devices = list(nb.dcim.devices.filter(name=devices))
        if len(devices) != len(list_devices):
            raise LengthError(LEN_NOT_EQUAL.format(
                len_pre=len(devices),
                len_post=len(list_devices)
            ))
    except requests.exceptions.ConnectionError as err:
        raise ConnectionError(FAIL_CONNECTION_NB.format(
            url=url,
            token=token,
            error=err
        ))
    return list_devices
