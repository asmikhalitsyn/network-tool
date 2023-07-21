from abc import ABC

from database import session_cache
from netrnd_parse import parse_raw


class TestBaseAction(ABC):

    def __init__(self, host: str, test: str):
        self.host = host
        self.test = test

    def __str__(self):
        return 'TestBaseAction object'

    def show_cached_command(self, command: str, checkpoint: str):
        result = session_cache.read_command(
            command=command,
            host=self.host,
            checkpoint=checkpoint,
            test_name=self.test
        )
        command, output, platform = result
        return parse_raw(command, output, platform)
