import sys
import os
import traceback
import datetime
import common.db as db
import repository.user_info_batch_repository as ui_bt_rp
import repository.working_record_batch_repository as wr_bt_rp

def run():
    working_records_reserve_days_limit = int(os.getenv(\
        'SV_SLACKERS_APP_BATCH_RESERVE_RECALCULATE_WORKING_RECOEDS_RECENT_DAYS_LIMIT', None\
    ))
    if working_records_reserve_days_limit is None:
        print(
            'Specify SV_SLACKERS_APP_BATCH_RESERVE_RECALCULATE_WORKING_RECOEDS_RECENT_DAYS_LIMIT '\
            + 'as environment variable.'
        )
        sys.exit(1)
    try:
        connection = db.connect()
        result_count = mark_reserve_recalculate_working_record(connection, working_records_reserve_days_limit)
        print(datetime.datetime.now())
        if result_count > 0: print('WorkingRecord再計算予約レコード数:{}'.format(result_count))
        result_count = mark_reserve_recalculate_user_info(connection)
        print(datetime.datetime.now())
        if result_count > 0: print('UserInfo再計算予約レコード数:{}'.format(result_count))
        connection.close()

    except Exception as e:
        connection.rollback()
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())
        
def mark_reserve_recalculate_user_info(connection):
    result_count = ui_bt_rp.userinfo_standby_status_reserve_update(
        connection, 
        datetime.datetime.now().hour, 
        datetime.datetime.now(), 
        sys._getframe().f_code.co_name
    )
    connection.commit()
    return result_count

def mark_reserve_recalculate_working_record(connection, working_records_reserve_days_limit):
    result_count = wr_bt_rp.working_record_standby_status_reserve_update(
        connection, 
        datetime.datetime.now().hour, 
        datetime.datetime.now() - datetime.timedelta(days=working_records_reserve_days_limit), 
        datetime.datetime.now(), 
        sys._getframe().f_code.co_name
    )
    connection.commit()
    return result_count   