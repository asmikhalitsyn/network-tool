from pydantic import BaseModel

from parser.Juniper._regex import ISIS_COUNT


class IsisCount(BaseModel):
    count: int

    @classmethod
    def parse(cls, output: str) -> 'IsisCount':
        isis_amount = ISIS_COUNT.search(output).groupdict()
        return cls.parse_obj(isis_amount)


