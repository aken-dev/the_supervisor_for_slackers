import traceback
import common.db as db

#TermsOfUse
def terms_of_use_select():
    try:
        connection = db.connect()
        cursor = connection.cursor()
        sql = "SELECT * FROM `terms_of_use` WHERE `current`=1"
        result_count = cursor.execute(sql)
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
