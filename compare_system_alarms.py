from parser.actions import TestBaseAction
from parser.Juniper import show_alarm

STATE_NOT_CHANGE = 'System alarms are same'
STATE_CHANGE = ('System alarms have changed:\n'
                'Precheck: {pre_alarm}\n'
                'Postcheck: {post_alarm}')
COMMAND = 'show system alarms'


class SystemAlarmsCheck(TestBaseAction):

    @staticmethod
    def run_command(conn):
        return conn.send_command(COMMAND)

    def initial_system_alarm_sessions(self, pre) -> show_alarm.ChassisSystemAlarm:
        return self.show_cached_command(COMMAND, pre)

    def system_alarm_sessions(self, post) -> show_alarm.ChassisSystemAlarm:
        return self.show_cached_command(COMMAND, post)

    def run(self, pre, post):
        initials_system_alarm_sessions = self.initial_system_alarm_sessions(pre)
        system_alarm_after_work = self.system_alarm_sessions(post)
        if initials_system_alarm_sessions.alarm == system_alarm_after_work.alarm:
            return STATE_NOT_CHANGE, 'OK'
        return STATE_CHANGE.format(
            pre_alarm=initials_system_alarm_sessions.alarm,
            post_alarm=system_alarm_after_work.alarm
        ), 'FAIL'
