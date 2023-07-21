from parser.actions import TestBaseAction
from parser.Juniper import show_alarm

STATE_NOT_CHANGE = 'Chassis alarms are same'
STATE_CHANGE = ('Chassis alarms have changed:\n'
                'Precheck: {pre_alarm}\n'
                'Postcheck: {post_alarm}')
COMMAND = 'show chassis alarms'


class ChassisAlarmsCheck(TestBaseAction):

    @staticmethod
    def run_command(conn):
        return conn.send_command(COMMAND)

    def initial_chassis_alarm_sessions(self, pre) -> show_alarm.ChassisSystemAlarm:
        return self.show_cached_command(COMMAND, pre)

    def chassis_alarm_sessions(self, post) -> show_alarm.ChassisSystemAlarm:
        return self.show_cached_command(COMMAND, post)

    def run(self, pre, post):
        initials_chassis_alarm_sessions = self.initial_chassis_alarm_sessions(pre)
        chassis_alarm_after_work = self.chassis_alarm_sessions(post)
        if initials_chassis_alarm_sessions.alarm == chassis_alarm_after_work.alarm:
            return STATE_NOT_CHANGE, 'OK'
        return STATE_CHANGE.format(
            pre_alarm=initials_chassis_alarm_sessions.alarm,
            post_alarm=chassis_alarm_after_work.alarm
        ), 'FAIL'
