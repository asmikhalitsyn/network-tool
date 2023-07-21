#!/usr/bin/env python3
from typing import Optional, List, Any

from sqlalchemy import distinct, select

from database.models_db import session
from database.models_db import Host, Checkpoint, Commands
from logger import get_logger

CHECK_HOST = 'Идет проверка на наличие дубликатов в БД'
HOST_ROW_EXIST = 'Данная запись для хоста {name} c чекпоинтом {cp} уже существует в БД'
FORMAT_OF_LOGS = ('%(asctime)s - %(name)s - %(lineno)s - '
                  '%(levelname)s - %(funcName)s()- %(message)s')


log = get_logger(__name__)


def read_command(command: str, host: str, checkpoint: str, test_name: str) -> Optional[Host]:
    return _read_command_output(
        command=command,
        host=host,
        checkpoint=checkpoint,
        test_name=test_name
    )


def _read_command_output(host: str, command: str, checkpoint: str, test_name: str) -> Optional[Host]:
    return session.execute(
        select(
            Commands.command,
            Commands.output,
            Host.platform,
        ).join(Host.hst).join(Checkpoint).where(
            Host.host == host).where(
            Commands.command == command).where(Commands.test_name == test_name).where(
            Checkpoint.checkpoint_name == checkpoint
        )).first()


def output_list_checkpoint() -> Optional[Host]:
    return session.execute(
        select(
            distinct(Host.checkpoint_id),
            Checkpoint.checkpoint_name,
            Host.host,
            Checkpoint.created_on
        ).where(Checkpoint.id == Host.checkpoint_id).join(Checkpoint)
    ).all()


def check_host_and_checkpoint(hosts: List, cp_name: str) -> None:
    log.info(CHECK_HOST)
    for host in hosts:
        filter_check = [
            Host.host == str(host),
            Checkpoint.checkpoint_name == cp_name
        ]
        checkpoint = session.query(Host).join(Checkpoint).filter(*filter_check).first()
        if checkpoint:
            log.warning(HOST_ROW_EXIST.format(name=str(host), cp=cp_name))


def check_checkpoint(checkpoint_name: str) -> Any:
    filter_check = [
        Checkpoint.checkpoint_name == checkpoint_name
    ]
    checkpoint = session.query(Checkpoint).filter(*filter_check).first()
    if checkpoint:
        return checkpoint
    check = Checkpoint(checkpoint_name=checkpoint_name)
    session.add(check)
    session.commit()
    return check


def save_host(hostname: str, platform: str, checkpoint_id: int):
    add_host = Host(
        host=hostname,
        platform=platform,
        checkpoint_id=checkpoint_id
    )
    session.add(add_host)
    session.commit()
    return add_host


def save_command(command: str, output: str, test: str, checkpoint_id: int, host_id: int):
    add_cmd = Commands(
        command=command,
        output=output,
        test_name=test,
        checkp_id=checkpoint_id,
        host_id=host_id
    )
    session.add(add_cmd)
    session.commit()
    return add_cmd
