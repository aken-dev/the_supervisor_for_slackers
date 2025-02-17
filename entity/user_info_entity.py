import dataclasses
import datetime
import common.constant as co

@dataclasses.dataclass
class UserInfo:
    id: int = None #レコードID(ユーザID)
    line_user_id: str = None #LINE_USER_ID
    line_name: str = None #LINE_NAME（登録時）
    allowed: int = co.USER_UNREGISTERED
    supervisor_flag: bool = False #システム管理者フラグ
    the_last_stage: int = 10 #最後の課題番号
    current_stage: int = 1 #現在の課題番号 DEFAULT=1
    stage_change_remind_type: int = co.STAGE_CHANGE_REMIND_TYPE_NOTHING #課題番号変更リマインド間隔種別（0=しない，1=曜日，2=日数） DEFAULT=0
    stage_change_remind_value: int = 0 #課題番号変更リマインド間隔（0~6=月〜日曜日 or 日数） DEFAULT=0
    recent_stage_changed_date: datetime.date = None #直近の課題番号変更日
    required_working_hours: int = 8 #目標作業時間（1日あたり） DEFAULT=8
    starting_time_of_a_day: int = 0 #日付起算時刻（時） DEFAULT=0
    registered_datetime: datetime.datetime = None #登録日時
    registered_by: str = None #登録機能
    updated_datetime: datetime.datetime = None #更新日時
    updated_by: str = None #更新機能
    memo_1: str = None #メモ1
    memo_2: str = None #メモ2
    memo_3: str = None #メモ3
    standby_status: int = co.STANDBY_STATUS_READY #待機状態（0=準備完了，1=バッチ処理中，2=バッチ再計算処理待ち，3=バッチ異常終了）
    def setEntityFromRecord(self, record):
        self.id = record['id']
        self.line_user_id = record['line_user_id']
        self.line_name = record['line_name']
        self.allowed = record['allowed']
        self.supervisor_flag = record['supervisor_flag']
        self.the_last_stage = record['the_last_stage']
        self.current_stage = record['current_stage']
        self.stage_change_remind_type = record['stage_change_remind_type']
        self.stage_change_remind_value = record['stage_change_remind_value']
        self.recent_stage_changed_date = record['recent_stage_changed_date']
        self.required_working_hours = record['required_working_hours']
        self.starting_time_of_a_day = record['starting_time_of_a_day']
        self.registered_datetime = record['registered_datetime']
        self.registered_by = record['registered_by']
        self.updated_datetime = record['updated_datetime']
        self.updated_by = record['updated_by']
        self.memo_1 = record['memo_1']
        self.memo_2 = record['memo_2']
        self.memo_3 = record['memo_3']
        self.standby_status = record['standby_status']
