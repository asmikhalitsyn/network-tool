from pydantic import BaseModel

from parser.Juniper._regex import ALARM


class ChassisSystemAlarm(BaseModel):
    alarm: str

    @classmethod
    def parse(cls, output: str) -> 'ChassisSystemAlarm':
        chassis_system_alarm = ALARM.search(output).groupdict()
        return cls.parse_obj(chassis_system_alarm)

