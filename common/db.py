import pymysql.cursors
import os
import traceback

def connect():
    try:
        # Connect to the database
        connection = pymysql.connect(host=os.getenv('SV_SLACKERS_APP_DB_HOST', None),
                            user=os.getenv('SV_SLACKERS_APP_DB_NAME', None),
                            password=os.getenv('SV_SLACKERS_APP_DB_PASS', None),
                            db=os.getenv('SV_SLACKERS_APP_DB_SCHEMA', None),
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
        return connection
    except Exception as e:
        connection.close()
        print("Exception")
        print(e, type(e))
        print(traceback.format_exc())

