import sys
import os
import traceback
import datetime
import common.db as db
import repository.user_info_batch_repository as ui_bt_rp

def run():
    waiting_recalc_timeout_minutes = int(os.getenv(\
        'SV_SLACKERS_APP_WAITING_RECALCULATION_USER_INFO_TIMEOUT_MINUTES', None\
    ))
    if waiting_recalc_timeout_minutes is None:
        print(
            'Specify SV_SLACKERS_APP_WAITING_RECALCULATION_USER_INFO_TIMEOUT_MINUTES '\
            + 'as environment variable.'
        )
        sys.exit(1)
    batch_process_timeout_minutes = int(os.getenv(\
        'SV_SLACKERS_APP_ON_BATCH_PROCESS_USER_INFO_TIMEOUT_MINUTES', None\
    ))
    if batch_process_timeout_minutes is None:
        print(
            'Specify SV_SLACKERS_APP_ON_BATCH_PROCESS_USER_INFO_TIMEOUT_MINUTES '\
            + 'as environment variable.'
        )
        sys.exit(1)
    try:
        connection = db.connect()
        result_count = mark_defected_user_info(
            connection, waiting_recalc_timeout_minutes, batch_process_timeout_minutes
        )
        print(datetime.datetime.now())
        if result_count > 0: print('UserInfoタイムアウトレコード数:{}'.format(result_count))
        connection.close()

    except Exception as e:
        connection.rollback()
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())
        
def mark_defected_user_info(
    connection, waiting_recalc_timeout_minutes, batch_process_timeout_minutes
):
    result_count = ui_bt_rp.userinfo_find_and_mark_defected_records_update(
        connection,
        datetime.datetime.now() - datetime.timedelta(minutes=waiting_recalc_timeout_minutes), 
        datetime.datetime.now() - datetime.timedelta(minutes=batch_process_timeout_minutes),
        datetime.datetime.now(), 
        sys._getframe().f_code.co_name
    )
    connection.commit()
    return result_count
