#!/usr/bin/env python3
import os
import shutil

from tabulate import tabulate
import yaml

import click
from dotenv import load_dotenv


from database import session_cache
from logger import get_logger
from settings import TEST_CASE

load_dotenv()

SUMMARY_TEST = 'SUMMARY'
COMMON_ERROR = 'Произошла ошибка: {error}'

log = get_logger(__name__)

@click.command()
@click.option('--config_hostnames', '-hostnames', required=False, type=click.Path())
@click.option('--pre-checkpoint', '-pre', required=False, type=str)
@click.option('--post-checkpoint', '-post', required=False, type=str)
@click.option('--list-checkpoints', '-l', is_flag=True)
def main(config_hostnames, pre_checkpoint, post_checkpoint, list_checkpoints):
    list_cases = []
    if config_hostnames:
        with open(config_hostnames) as f:
            hostnames = yaml.safe_load(f)
    if list_checkpoints:
        return print(
            tabulate(
                session_cache.output_list_checkpoint(),
                headers=['Checkpoint_id', 'Checkpoint_name', 'Host', 'Date'],
                tablefmt='grid')
        )
    columns = shutil.get_terminal_size().columns
    try:
        for router, tests in hostnames.items():
            print(str(router).center(columns, '='))
            for test in tests:
                object_test = TEST_CASE[test](router, test)
                print(test.center(columns, '-'))
                message, status = object_test.run(pre_checkpoint, post_checkpoint)
                print(message)
                list_cases.append([router, test, status])
        print(SUMMARY_TEST.center(columns, '='))
        print(tabulate(list_cases))
    except Exception as err:
        error_msg = COMMON_ERROR.format(error=err)
        log.exception(error_msg)


if __name__ == '__main__':
    main()
