import traceback
import common.constant as co

#UserInfo
def ids_select_by_standby_status(connection, standby_status, limit):
    try:
        cursor = connection.cursor()
        sql = "SELECT `id`, `starting_time_of_a_day` FROM `user_info` WHERE `standby_status`=%s "\
              + "ORDER BY `updated_datetime` DESC LIMIT %s"
        result_count = cursor.execute(sql, (standby_status, limit))
        result = cursor.fetchall()
        return {
            "count": result_count,
            "result": result
        }

    except Exception as e:
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())
        
def userinfo_standby_status_update(connection, user_id, standby_status, updated_at, updated_by):
    try:
        cursor = connection.cursor()
        sql = "UPDATE `user_info` SET `standby_status` =%s,`updated_datetime` =%s, `updated_by` =%s WHERE `id` =%s"
        result_count = cursor.execute(sql, (standby_status, updated_at, updated_by, user_id))
        return result_count
    except Exception as e:
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())
        
def userinfo_standby_status_reserve_update(connection, starting_time_of_a_day, updated_at, updated_by):
    try:
        cursor = connection.cursor()
        sql = "UPDATE `user_info` SET `standby_status` =%s,`updated_datetime` =%s, `updated_by` =%s "\
              + "WHERE `starting_time_of_a_day` =%s AND `standby_status` =%s"
        result_count = cursor.execute(sql, (
            co.STANDBY_STATUS_WAITING_BATCH_PROCESS_RECALCULATE, updated_at, updated_by,
            starting_time_of_a_day, co.STANDBY_STATUS_READY
        ))
        return result_count
    except Exception as e:
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())

def userinfo_find_and_mark_defected_records_update(
    connection, waiting_batch_recalc_timeout_datetime, 
    on_batch_process_timeout_datetime, updated_at, updated_by
):
    try:
        cursor = connection.cursor()
        sql = "UPDATE `user_info` SET `standby_status` =%s,`updated_datetime` =%s, `updated_by` =%s "\
              + "WHERE `standby_status` =%s AND `updated_datetime` <%s"\
              + "OR `standby_status` =%s AND `updated_datetime` <%s"
        result_count = cursor.execute(sql, (
            co.STANDBY_STATUS_BATCH_PROCESSED_FAILURE, updated_at, updated_by,
            co.STANDBY_STATUS_WAITING_BATCH_PROCESS_RECALCULATE, waiting_batch_recalc_timeout_datetime,
            co.STANDBY_STATUS_ON_BATCH_PROCESS, on_batch_process_timeout_datetime
        ))
        return result_count
    except Exception as e:
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())
