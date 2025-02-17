import traceback
import common.db as db
import common.constant as co

#WokingRecord
def a_working_record_select_by_id(id):
    try:
        connection = db.connect()
        cursor = connection.cursor()
        sql = "SELECT * FROM `working_record` WHERE `id`=%s"
        result_count = cursor.execute(sql, (id))
        result = cursor.fetchone()
        connection.close()
        return {
            "count": result_count,
            "result": result
        }
    except Exception as e:
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())
        
def a_working_record_select_by_user_id(
    user_id, 
    process_category=co.PROCESS_CATEGORY_RECORD_WORKING_HOURS,
    process_status=co.PROCESS_STATUS_ON_RECORDING,
    limit_value=1):
    try:
        connection = db.connect()
        cursor = connection.cursor()
        sql = "SELECT * FROM `working_record` " \
        "WHERE `user_id`=%s AND `process_category` =%s AND `process_status` =%s " \
        "ORDER BY start_time DESC LIMIT %s"
        result_count = cursor.execute(sql, (user_id, process_category, process_status, limit_value))
        result = cursor.fetchall()
        connection.close()
        return {
            "count": result_count,
            "result": result
        }
    except Exception as e:
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())

def a_working_record_select_by_user_id_start_time_for_past(
    user_id, 
    start_time,
    limit_value=1,
    sort_order='DESC'):
    try:
        connection = db.connect()
        cursor = connection.cursor()
        sql = "SELECT * FROM `working_record` " \
        + "WHERE `user_id`=%s AND start_time <=%s" \
        + "AND `process_category` =%s AND `process_status` =%s " \
        + "OR `user_id`=%s AND start_time <=%s" \
        + "AND `process_category` =%s AND `process_status` =%s " \
        + "ORDER BY `start_time` {} LIMIT %s".format(sort_order)
        result_count = cursor.execute(sql, (
            user_id, 
            start_time, 
            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, 
            co.PROCESS_STATUS_ON_RECORDING, 
            user_id, 
            start_time, 
            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, 
            co.PROCESS_STATUS_RECORDED_SUCCESS, 
            limit_value))
        result = cursor.fetchall()
        connection.close()
        return {
            "count": result_count,
            "result": result
        }
    except Exception as e:
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())

def a_working_record_select_by_user_id_start_time_for_future(
    user_id, 
    start_time,
    limit_value=1,
    sort_order='ASC'):
    try:
        connection = db.connect()
        cursor = connection.cursor()
        sql = "SELECT * FROM `working_record` " \
        + "WHERE `user_id`=%s AND start_time >=%s" \
        + "AND `process_category` =%s AND `process_status` =%s " \
        + "OR `user_id`=%s AND start_time >=%s" \
        + "AND `process_category` =%s AND `process_status` =%s " \
        + "ORDER BY `start_time` {} LIMIT %s".format(sort_order)
        result_count = cursor.execute(sql, (
            user_id, 
            start_time, 
            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, 
            co.PROCESS_STATUS_ON_RECORDING, 
            user_id, 
            start_time, 
            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, 
            co.PROCESS_STATUS_RECORDED_SUCCESS, 
            limit_value))
        result = cursor.fetchall()
        connection.close()
        return {
            "count": result_count,
            "result": result
        }
    except Exception as e:
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())
        
def new_working_record_insert(workingRecord):
    try:
        connection = db.connect()
        cursor = connection.cursor()
        sql = "INSERT INTO `working_record` " \
              + "(`user_id`, `line_user_id`, `process_category`, " \
              + "`process_status`, `stage`, `start_time`, "  \
              + "`finish_time`, `registered_datetime`, `registered_by`, " \
              + "`updated_datetime`, `updated_by`)" \
              + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        result_count = cursor.execute(sql, (
            workingRecord.user_id, workingRecord.line_user_id, workingRecord.process_category,
            workingRecord.process_status, workingRecord.stage, workingRecord.start_time, 
            workingRecord.finish_time, workingRecord.registered_datetime, workingRecord.registered_by, 
            workingRecord.updated_datetime, workingRecord.updated_by
        ))
        connection.commit()
        connection.close()
        return result_count
    except Exception as e:
        connection.rollback()
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())

def working_record_status_update(workingRecord):
    try:
        connection = db.connect()
        cursor = connection.cursor()
        sql = "UPDATE `working_record` " \
        + "SET `process_category` =%s, `process_status` =%s, " \
        + "`start_time` =%s, `finish_time` =%s, " \
        + "`updated_datetime` =%s, `updated_by` =%s WHERE `id` =%s"
        result_count = cursor.execute(sql, (workingRecord.process_category, workingRecord.process_status, 
                                            workingRecord.start_time, workingRecord.finish_time,
                                            workingRecord.updated_datetime, workingRecord.updated_by, workingRecord.id))
        connection.commit()
        connection.close()
        return result_count
    except Exception as e:
        connection.rollback()
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())

def working_record_update(workingRecord, target_column):
    try:
        connection = db.connect()
        cursor = connection.cursor()
        sql = "UPDATE `working_record` SET `{}` =%s,`updated_datetime` =%s, `updated_by` =%s WHERE `id` =%s".format(target_column)
        result_count = cursor.execute(sql, (eval('workingRecord.{}'.format(target_column)), 
                                            workingRecord.updated_datetime, workingRecord.updated_by, workingRecord.id))
        connection.commit()
        connection.close()
        return result_count
    except Exception as e:
        connection.rollback()
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())

#作業中のレコードの作業時間（単位：分）を算出(集計用)
def worked_minutes_on_process_select(user_id, start_time, finish_time):
    try:
        connection = db.connect()
        cursor = connection.cursor()
        sql = "SELECT FLOOR(SUM(TIMESTAMPDIFF(SECOND, `start_time`, NOW())) / 60) AS `worked_minutes` " \
                + " FROM `working_record`" \
                + " WHERE `user_id` =%s" \
                + " AND `process_category` =%s" \
                + " AND `process_status` =%s" \
                + " AND `start_time` >=%s AND `start_time` <=%s"
        result_count = cursor.execute(sql, (
                user_id, 
                co.PROCESS_CATEGORY_RECORD_WORKING_HOURS,
                co.PROCESS_STATUS_ON_RECORDING,
                start_time, finish_time
            ))
        result = cursor.fetchone()
        connection.close()
        return {
            "count": result_count,
            "result": result
        }
    except Exception as e:
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())

#作業記録正常終了のレコードの作業時間（単位：分）を算出(集計用)
def worked_minutes_finished_select(user_id, start_time, finish_time):
    try:
        connection = db.connect()
        cursor = connection.cursor()
        sql =  "SELECT FLOOR(SUM(TIMESTAMPDIFF(SECOND, `start_time`, `finish_time`)) / 60) AS `worked_minutes` " \
                + " FROM `working_record`" \
                + " WHERE `user_id` =%s" \
                + " AND `process_category` =%s" \
                + " AND `process_status` =%s" \
                + " AND `start_time` >=%s AND `finish_time` <=%s"
        result_count = cursor.execute(sql, (user_id, 
                                            co.PROCESS_CATEGORY_RECORD_WORKING_HOURS,
                                            co.PROCESS_STATUS_RECORDED_SUCCESS,
                                            start_time, finish_time
                                            ))
        result = cursor.fetchone()
        connection.close()
        return {
            "count": result_count,
            "result": result
        }
    except Exception as e:
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())

def working_record_standby_status_update(
    user_id, new_standby_status, standby_status, updated_at, updated_by
):
    try:
        connection = db.connect()
        cursor = connection.cursor()
        sql = "UPDATE `working_record` SET `standby_status`=%s, `updated_datetime`=%s, `updated_by`=%s "\
              + "WHERE `user_id`=%s AND `process_category`=%s AND `process_status`=%s AND `standby_status`=%s "\
              + "OR `user_id`=%s AND `process_category`=%s AND `process_status`=%s AND `standby_status`=%s "
        result_count = cursor.execute(sql, (
            new_standby_status, updated_at, updated_by, 
            user_id, co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, co.PROCESS_STATUS_ON_RECORDING, standby_status,
            user_id, co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, co.PROCESS_STATUS_RECORDED_SUCCESS, standby_status          
        ))
        connection.commit()
        connection.close()
        return result_count
    except Exception as e:
        connection.rollback()
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())
