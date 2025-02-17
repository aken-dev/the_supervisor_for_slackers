import dataclasses
import datetime
import common.constant as co

@dataclasses.dataclass
class WorkingRecord:
    id: int = None #レコードID
    user_id: int = None #ユーザID
    line_user_id: str = None #LINE_USER_ID
    process_category: int = co.PROCESS_CATEGORY_RECORD_WORKING_HOURS #処理区分（0=メンテ，1=装着記録，2=メモのみ）DEFAULT=1
    process_status: int = co.PROCESS_STATUS_NOT_STARTED #処理状態（0=メンテナンス, 1=未開始，2=記録中，3=記録正常終了，4=記録異常終了，5=メモのみ）DEFAULT=0
    stage: int = None #作業番号
    start_time: datetime = None #作業開始日時
    finish_time: datetime = None #作業終了日時
    registered_datetime: datetime = None #登録日時
    registered_by: str = None #登録機能
    updated_datetime: datetime = None #更新日時
    updated_by: datetime = None #更新機能
    memo_1: str = None #メモ1
    memo_2: str = None #メモ2
    memo_3: str = None #メモ3
    standby_status: int = co.STANDBY_STATUS_READY #待機状態（0=準備完了，1=バッチ処理中，2=バッチ再計算処理待ち，3=バッチ異常終了）
    def setEntityFromRecord(self, record):
        self.id = record['id']
        self.user_id = record['user_id']
        self.line_user_id = record['line_user_id']
        self.process_category = record['process_category']
        self.process_status = record['process_status']
        self.stage = record['stage']
        self.start_time = record['start_time']
        self.finish_time = record['finish_time']
        self.registered_datetime = record['registered_datetime']
        self.registered_by = record['registered_by']
        self.updated_datetime = record['updated_datetime']
        self.updated_by = record['updated_by']
        self.memo_1 = record['memo_1']
        self.memo_2 = record['memo_2']
        self.memo_3 = record['memo_3']
        self.standby_status = record['standby_status']
