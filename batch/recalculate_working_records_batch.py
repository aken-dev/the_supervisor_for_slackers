import sys
import os
import traceback
import datetime
import common.constant as co
import common.db as db
import service.shared.datetime_calc_service as dc_sv
import repository.user_info_batch_repository as ui_bt_rp
import repository.working_record_batch_repository as wr_bt_rp
from entity.working_record_entity import WorkingRecord

def run():
    user_info_records_limit = int(os.getenv('SV_SLACKERS_APP_BATCH_RECALCULATE_USER_INFO_RECOEDS_LIMIT_ONCE', None))
    if user_info_records_limit is None:
        print('Specify SV_SLACKERS_APP_BATCH_RECALCULATE_USER_INFO_RECOEDS_LIMIT_ONCE as environment variable.')
        sys.exit(1)
    working_records_limit = int(os.getenv('SV_SLACKERS_APP_BATCH_RECALCULATE_WORKING_RECOEDS_LIMIT_ONCE', None))
    if working_records_limit is None:
        print('Specify SV_SLACKERS_APP_BATCH_RECALCULATE_WORKING_RECOEDS_LIMIT_ONCE as environment variable.')
        sys.exit(1)
    try:
        connection = db.connect()
        recalculate_user_info(
            connection, user_info_records_limit, working_records_limit
        )
        connection.close()

    except Exception as e:
        connection.rollback()
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())
        
def recalculate_user_info(connection, user_info_records_limit, working_records_limit):
    target_users = ui_bt_rp.ids_select_by_standby_status(
        connection,
        co.STANDBY_STATUS_WAITING_BATCH_PROCESS_RECALCULATE,
        user_info_records_limit
    )
    print(datetime.datetime.now())
    for target_user in target_users['result']:
        ui_bt_rp.userinfo_standby_status_update(
            connection, 
            target_user['id'], 
            co.STANDBY_STATUS_ON_BATCH_PROCESS, 
            datetime.datetime.now(), 
            'recalculate_user_info_batch'
        )
    connection.commit()
    for target_user in target_users['result']:
        is_completed = recalculate_working_record(
            connection, target_user['id'], target_user['starting_time_of_a_day'], working_records_limit
        )
        ui_bt_rp.userinfo_standby_status_update(
            connection, 
            target_user['id'], 
            co.STANDBY_STATUS_READY if is_completed else co.STANDBY_STATUS_WAITING_BATCH_PROCESS_RECALCULATE, 
            datetime.datetime.now(), 
            'recalculate_user_info_batch'
        )
        connection.commit()

def recalculate_working_record(
    connection, user_id, registered_users_time_a_day_starts, working_records_limit
):
    target_records = wr_bt_rp.working_records_select_by_standby_status(
        connection,
        user_id,
        co.STANDBY_STATUS_WAITING_BATCH_PROCESS_RECALCULATE,
        working_records_limit
    )
    status_change_result_count = 0
    for target_record in target_records['result']:
        status_change_result_count += wr_bt_rp.working_record_standby_status_update(
            connection,
            target_record['id'],
            co.STANDBY_STATUS_ON_BATCH_PROCESS,
            datetime.datetime.now(), 
            'recalculate_working_record_batch'
        )
    if target_records['count'] != status_change_result_count: 
        print('【WorkingRecord:status_change_Err(waiting→on_batch)】')
        print('ステータス更新対象レコード数:{}').format(target_records['count'])
        print('更新したレコード数:{}').format(status_change_result_count)
        print('【WorkingRecords】\n{}').format(target_records)
        connection.rollback()
        raise Exception()
    connection.commit()
    for target_record in target_records['result']:
        targetWorkingRecord = WorkingRecord()
        targetWorkingRecord.setEntityFromRecord(target_record)
        #target_recordのstart_timeから算出した、そのレコードの属する日の1日の開始日時と終了日時を取得
        target_time_range = dc_sv.get_users_time_range_of_the_day(
            registered_users_time_a_day_starts,
            targetWorkingRecord.start_time
        )
        # target_recordのステータスが記録中かつそのstart_timeが、
        # 今現在の日時から算出したtaime_rangeの開始日時よりも過去の場合、
        # target_recordのfinish_timeに、そのstart_timeから算出した
        # time_rangeの終了日時を設定したうえで、ステータスを記録正常終了で更新する。
        # さらに、target_recordのstart_time+1日をstart_timeに設定した、新レコードを生成する。
        if targetWorkingRecord.process_status == co.PROCESS_STATUS_ON_RECORDING:
            # 現在基準で算出した、そのユーザの今日の開始日時と終了日時
            todays_time_range = dc_sv.get_users_time_range_of_the_day(
                registered_users_time_a_day_starts
            )
            # target_recordのstart_timeが今日のstart_timeよりも過去の場合:
            if target_time_range['start_of_the_day'] < todays_time_range['start_of_the_day']:
                # target_recordをfinish_timeを設定した上で記録正常終了で更新する。
                targetWorkingRecord.process_status = co.PROCESS_STATUS_RECORDED_SUCCESS
                targetWorkingRecord.finish_time = target_time_range['end_of_the_day'] 
                targetWorkingRecord.updated_datetime = datetime.datetime.now()
                targetWorkingRecord.updated_by = 'recalculate_working_record_batch'
                target_update_cnt = wr_bt_rp.working_record_batch_update(connection, targetWorkingRecord)
                if target_update_cnt < 1:
                    print('【working_record_batch_update_Err(ON_RECORDING→RECORDED_SUCCESS)】')
                    print('更新対象レコード数:{}'.format(1))
                    print('更新したレコード数:{}'.format(target_update_cnt))
                    print('更新対象レコードid:{}'.format(WorkingRecord.id))
                    connection.rollback()
                    raise Exception()
                # target_recordのstart_timeをそのtimerengeのstart_time+1日で設定した新レコードを生成する
                targetsNextDayWorkingRecord = WorkingRecord()
                targetsNextDayWorkingRecord.setEntityFromRecord(target_record)
                targetsNextDayWorkingRecord.start_time = target_time_range['start_of_the_day']\
                    + datetime.timedelta(days=1)
                targetsNextDayWorkingRecord.finish_time = None
                targetsNextDayWorkingRecord.standby_status = co.STANDBY_STATUS_WAITING_BATCH_PROCESS_RECALCULATE
                targetsNextDayWorkingRecord.registered_datetime = datetime.datetime.now()
                targetsNextDayWorkingRecord.registered_by = 'recalculate_working_record_batch'
                targetsNextDayWorkingRecord.updated_datetime = datetime.datetime.now()
                targetsNextDayWorkingRecord.updated_by = 'recalculate_working_record_batch'
                targets_next_day_insert_cnt = wr_bt_rp.over_time_working_record_insert(
                    connection, targetsNextDayWorkingRecord
                )
                if targets_next_day_insert_cnt < 1:
                    print('【over_time_working_record_insert_Err】')
                    print('挿入レコード数:{}'.format(1))
                    print('挿入したレコード数:{}'.format(targets_next_day_insert_cnt))
                    print('レコード元id:{}'.format(targetWorkingRecord.id))
                    connection.rollback()
                    raise Exception()
        # target_recordのステータスが記録正常終了
        # かつ、target_recordのstart_timeから算出したtime_rangeの開始日時よりも
        # target_recordのfinish_timeから算出したtime_rangeの開始日時が過去の場合、
        # target_recordに関して、finish_time=target_recordのstart_timeから算出した終了日時で更新する
        # さらに、start_time=target_recordのstart_timeから算出したtime_rangeの開始日時+1日に設定した新レコードを生成する。
        elif targetWorkingRecord.process_status == co.PROCESS_STATUS_RECORDED_SUCCESS:
            target_time_ramge_made_from_start_time = target_time_range
            target_time_ramge_made_from_finish_time = dc_sv.get_users_time_range_of_the_day(
                registered_users_time_a_day_starts,
                targetWorkingRecord.finish_time
            )
            if target_time_ramge_made_from_start_time['start_of_the_day'] < target_time_ramge_made_from_finish_time['start_of_the_day']:
                targetWorkingRecord.finish_time = target_time_ramge_made_from_start_time['end_of_the_day']
                targetWorkingRecord.updated_datetime = datetime.datetime.now()
                targetWorkingRecord.updated_by = 'recalculate_working_record_batch'
                target_update_cnt = wr_bt_rp.working_record_batch_update(connection, targetWorkingRecord)
                if target_update_cnt < 1:
                    print('【working_record_batch_update_Err(finish_time更新)】')
                    print('更新対象レコード数:{}'.format(1))
                    print('更新したレコード数:{}'.format(target_update_cnt))
                    print('更新対象レコードid:{}'.format(targetWorkingRecord.id))
                    connection.rollback()
                    raise Exception()
                targetsNextDayWorkingRecord = WorkingRecord()
                targetsNextDayWorkingRecord.setEntityFromRecord(target_record)
                targetsNextDayWorkingRecord.start_time = target_time_ramge_made_from_start_time['start_of_the_day'] \
                    + datetime.timedelta(days=1)
                targetsNextDayWorkingRecord.standby_status = co.STANDBY_STATUS_WAITING_BATCH_PROCESS_RECALCULATE
                targetsNextDayWorkingRecord.registered_datetime = datetime.datetime.now()
                targetsNextDayWorkingRecord.registered_by = 'recalculate_working_record_batch'
                targetsNextDayWorkingRecord.updated_datetime = datetime.datetime.now()
                targetsNextDayWorkingRecord.updated_by = 'recalculate_working_record_batch'
                targets_next_day_insert_cnt = wr_bt_rp.over_time_working_record_insert(
                    connection, targetsNextDayWorkingRecord
                )
                if targets_next_day_insert_cnt < 1:
                    print('ここまできたよー')
                    print('【over_time_working_record_insert_Err】')
                    print('挿入レコード数:{}'.format(1))
                    print('挿入したレコード数:{}'.format(targets_next_day_insert_cnt))
                    print('レコード元id:{}'.format(targetWorkingRecord.id))
                    connection.rollback()
                    raise Exception()
    status_change_result_count = 0
    for target_record in target_records['result']:
        status_change_result_count += wr_bt_rp.working_record_standby_status_update(
            connection,
            target_record['id'],
            co.STANDBY_STATUS_READY,
            datetime.datetime.now(), 
            'recalculate_working_record_batch'
        )
    if target_records['count'] != status_change_result_count: 
        print('【WorkingRecord:status_change_Err(on_batch→ready)】')
        print('ステータス更新対象レコード数:{}'.format(target_records['count']))
        print('更新したレコード数:{}'.format(status_change_result_count))
        print('【WorkingRecords】\n{}'.format(target_records))
        connection.rollback()
        raise Exception()
    records_cnt_of_standby_statuys_waiting = wr_bt_rp.count_select_by_standby_status(
        connection,
        user_id, 
        co.STANDBY_STATUS_WAITING_BATCH_PROCESS_RECALCULATE
    )
    return records_cnt_of_standby_statuys_waiting['result']['count'] == 0
