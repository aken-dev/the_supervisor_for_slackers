import traceback
import common.db as db

#UserInfo
def user_info_select(line_user_id):
    try:
        connection = db.connect()
        cursor = connection.cursor()
        sql = "SELECT * FROM `user_info` WHERE `line_user_id`=%s"
        result_count = cursor.execute(sql, (line_user_id))
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
        
def userinfo_new_user_insert(userInfo):
    try:
        connection = db.connect()
        cursor = connection.cursor()
        sql = "INSERT INTO `user_info` "  \
        + "(`line_user_id`, `line_name`,"  \
        + " `allowed`, `recent_stage_changed_date`," \
        + " `registered_datetime`, `registered_by`," \
        + " `updated_datetime`, `updated_by`)" \
        + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        result_count = cursor.execute(sql, (userInfo.line_user_id, userInfo.line_name,
                                            userInfo.allowed, userInfo.recent_stage_changed_date,
                                            userInfo.registered_datetime, userInfo.registered_by, 
                                            userInfo.updated_datetime, userInfo.updated_by))
        connection.commit()
        connection.close()
        return result_count
    except Exception as e:
        connection.rollback()
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())

def userinfo_update(userInfo, target_column):
    try:
        connection = db.connect()
        cursor = connection.cursor()
        sql = "UPDATE `user_info` SET `{}` =%s,`updated_datetime` =%s, `updated_by` =%s WHERE `id` =%s".format(target_column)
        result_count = cursor.execute(sql, (eval('userInfo.{}'.format(target_column)), 
                                            userInfo.updated_datetime, userInfo.updated_by, userInfo.id))
        connection.commit()
        connection.close()
        return result_count
    except Exception as e:
        connection.rollback()
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())
