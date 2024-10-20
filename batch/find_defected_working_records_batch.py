import sys
import os
import traceback
import datetime
import common.db as db
import repository.working_record_batch_repository as wr_bt_rp

def run():
    waiting_recalc_timeout_minutes = int(os.getenv(\
        'SV_SLACKERS_APP_WAITING_RECALCULATION_WORKING_RECORD_TIMEOUT_MINUTES', None\
    ))
    if waiting_recalc_timeout_minutes is None:
        print(
            'Specify SV_SLACKERS_APP_WAITING_RECALCULATION_WORKING_RECORD_TIMEOUT_MINUTES '\
            + 'as environment variable.'
        )
        sys.exit(1)
    batch_process_timeout_minutes = int(os.getenv(\
        'SV_SLACKERS_APP_ON_BATCH_PROCESS_WORKING_RECORD_TIMEOUT_MINUTES', None\
    ))
    if batch_process_timeout_minutes is None:
        print(
            'Specify SV_SLACKERS_APP_ON_BATCH_PROCESS_WORKING_RECORD_TIMEOUT_MINUTES '\
            + 'as environment variable.'
        )
        sys.exit(1)
    try:
        connection = db.connect()
        result_count = mark_defected_timeout_working_record(
            connection, waiting_recalc_timeout_minutes, batch_process_timeout_minutes
        )
        print(datetime.datetime.now())
        if result_count > 0: print('WorkingRecordタイムアウトレコード数:{}'.format(result_count))
        result_count = mark_recorded_failure_working_record(connection)
        print(datetime.datetime.now())
        if result_count > 0: print('WorkingRecord記録異常終了レコード数:{}'.format(result_count))
        connection.close()

    except Exception as e:
        connection.rollback()
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())
        
def mark_defected_timeout_working_record(
    connection, waiting_recalc_timeout_minutes, batch_process_timeout_minutes
):
    result_count = wr_bt_rp.working_record_find_and_mark_defected_records_update(
        connection,
        datetime.datetime.now() - datetime.timedelta(minutes=waiting_recalc_timeout_minutes), 
        datetime.datetime.now() - datetime.timedelta(minutes=batch_process_timeout_minutes),
        datetime.datetime.now(), 
        sys._getframe().f_code.co_name
    )
    connection.commit()
    return result_count

def mark_recorded_failure_working_record(connection):
    result_count = wr_bt_rp.working_record_find_and_mark_recorded_failure_records_update(
        connection,         
        datetime.datetime.now(), 
        sys._getframe().f_code.co_name
    )
    connection.commit()
    return result_count
