import traceback
import common.db as db
import common.constant as co

def working_records_select_by_standby_status(connection, user_id, standby_status, limit):
    try:
        cursor = connection.cursor()
        sql = "SELECT * FROM `working_record` "\
              + "WHERE `user_id`=%s AND `process_category`=%s AND `process_status`=%s AND `standby_status`=%s "\
              + "OR `user_id`=%s AND `process_category`=%s AND `process_status`=%s AND `standby_status`=%s "\
              + "ORDER BY `start_time` DESC LIMIT %s"
        result_count = cursor.execute(sql, (
            user_id,
            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS,
            co.PROCESS_STATUS_ON_RECORDING,
            standby_status,
            user_id,
            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS,
            co.PROCESS_STATUS_RECORDED_SUCCESS,
            standby_status,
            limit))
        result = cursor.fetchall()
        return {
            "count": result_count,
            "result": result
        }
    except Exception as e:
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())
        

def count_select_by_standby_status(connection, user_id, standby_status):
    try:
        cursor = connection.cursor()
        sql = "SELECT COUNT(*) AS 'count' FROM `working_record` "\
              + "WHERE `user_id`=%s AND `process_category`=%s AND `process_status`=%s AND `standby_status`=%s "\
              + "OR `user_id`=%s AND `process_category`=%s AND `process_status`=%s AND `standby_status`=%s "
        result_count = cursor.execute(sql, (
            user_id,
            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS,
            co.PROCESS_STATUS_ON_RECORDING,
            standby_status,
            user_id,
            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS,
            co.PROCESS_STATUS_RECORDED_SUCCESS,
            standby_status
        ))
        result = cursor.fetchone()
        return {
            "count": result_count,
            "result": result
        }
    except Exception as e:
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())
        
def working_record_standby_status_update(connection, id, standby_status, updated_at, updated_by):
    try:
        cursor = connection.cursor()
        sql = "UPDATE `working_record` SET `standby_status`=%s,`updated_datetime`=%s, `updated_by`=%s WHERE `id`=%s"
        result_count = cursor.execute(sql, (standby_status, updated_at, updated_by, id))
        return result_count
    except Exception as e:
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())

def working_record_batch_update(connection, workingRecord):
    try:
        cursor = connection.cursor()
        sql = "UPDATE `working_record` "\
              + "SET `process_category`=%s, `process_status`=%s, `finish_time`=%s, " \
              + "`updated_datetime`=%s, `updated_by`=%s, `standby_status`=%s WHERE `id`=%s"
        result_count = cursor.execute(sql, (
            workingRecord.process_category, workingRecord.process_status, workingRecord.finish_time,
            workingRecord.updated_datetime, workingRecord.updated_by, workingRecord.standby_status, workingRecord.id
        ))
        return result_count
    except Exception as e:
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())

def over_time_working_record_insert(connection, workingRecord):
    try:
        cursor = connection.cursor()
        sql = "INSERT INTO `working_record` " \
              + "(`user_id`, `line_user_id`, `process_category`, " \
              + "`process_status`, `stage`, `start_time`, "  \
              + "`finish_time`, `registered_datetime`, `registered_by`, " \
              + "`updated_datetime`, `updated_by`, `memo_1`, " \
              + "`memo_2`, `memo_3`,`standby_status` )" \
              + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        result_count = cursor.execute(sql, (
            workingRecord.user_id, workingRecord.line_user_id, workingRecord.process_category,
            workingRecord.process_status, workingRecord.stage, workingRecord.start_time, 
            workingRecord.finish_time, workingRecord.registered_datetime, workingRecord.registered_by, 
            workingRecord.updated_datetime, workingRecord.updated_by, workingRecord.memo_1,
            workingRecord.memo_2, workingRecord.memo_3, workingRecord.standby_status
        ))
        return result_count
    except Exception as e:
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())

def working_record_standby_status_reserve_update(
    connection, starting_time_of_a_day, target_start_time, updated_at, updated_by
):
    try:
        cursor = connection.cursor()
        sql = "UPDATE working_record AS wr "\
              + "INNER JOIN user_info AS ui ON wr.user_id = ui.id "\
              + "SET wr.standby_status=%s, wr.updated_datetime=%s, wr.updated_by=%s "\
              + "WHERE wr.process_category=%s AND wr.process_status=%s "\
              + "AND wr.start_time>=%s AND wr.standby_status=%s "\
              + "AND ui.starting_time_of_a_day=%s "\
              + "OR wr.process_category=%s AND wr.process_status=%s "\
              + "AND wr.start_time>=%s AND wr.standby_status=%s "\
              + "AND ui.starting_time_of_a_day=%s "
        result_count = cursor.execute(sql, (
            co.STANDBY_STATUS_WAITING_BATCH_PROCESS_RECALCULATE, updated_at, updated_by,
            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, co.PROCESS_STATUS_ON_RECORDING,
            target_start_time, co.STANDBY_STATUS_READY,
            starting_time_of_a_day,
            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, co.PROCESS_STATUS_RECORDED_SUCCESS,
            target_start_time, co.STANDBY_STATUS_READY,
            starting_time_of_a_day
        ))
        return result_count
    except Exception as e:
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())
        
def working_record_find_and_mark_defected_records_update(
    connection, waiting_batch_recalc_timeout_datetime, 
    on_batch_process_timeout_datetime, updated_at, updated_by
):
    try:
        cursor = connection.cursor()
        sql = "UPDATE `working_record` SET `standby_status` =%s,`updated_datetime` =%s, `updated_by` =%s "\
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
        
def working_record_find_and_mark_recorded_failure_records_update(
    connection, updated_at, updated_by
):
    try:
        cursor = connection.cursor()
        sql = "UPDATE `working_record` SET `process_status` =%s,`updated_datetime` =%s, `updated_by` =%s "\
              + "WHERE `process_category` =%s AND `process_status` =%s AND `start_time` IS NULL "\
              + "OR `process_category` =%s AND `process_status` =%s AND `start_time` IS NULL "\
              + "OR `process_category` =%s AND `process_status` =%s AND `finish_time` IS NULL "\
              + "OR `process_category` =%s AND `process_status` =%s AND `start_time` > `finish_time` "
        result_count = cursor.execute(sql, (
            co.PROCESS_STATUS_RECORDED_FAILURE, updated_at, updated_by,
            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, co.PROCESS_STATUS_ON_RECORDING,
            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, co.PROCESS_STATUS_RECORDED_SUCCESS,
            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, co.PROCESS_STATUS_RECORDED_SUCCESS,
            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, co.PROCESS_STATUS_RECORDED_SUCCESS
        ))
        return result_count
    except Exception as e:
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())