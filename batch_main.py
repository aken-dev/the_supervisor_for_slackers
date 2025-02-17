import sys
import traceback
import common.constant as co
import batch.recalculate_working_records_batch as recalculate_working_records_batch
import batch.reserve_for_recalculation_batch as reserve_for_recalculation_batch
import batch.find_defected_user_info_records_batch as find_defected_user_info_records_batch
import batch.find_defected_working_records_batch as find_defected_working_records_batch
from dotenv import load_dotenv
load_dotenv()
try:
    if len(sys.argv) != 2:
        print('引数の数が不正です。')
        sys.exit(1)
    elif not sys.argv[1].isdigit() or int(sys.argv[1]) < 0 or int(sys.argv[1]) > 3:
        print('引数1(BATCH_TYPE)が不正です。')
        sys.exit(1)
    else:
        batch_type = int(sys.argv[1])
        if batch_type == co.BATCH_TYPE_MARK_FOR_RESERVE_RECALCULATION:
            reserve_for_recalculation_batch.run()
        elif batch_type == co.BATCH_TYPE_EXECUTE_RECALCULATION:
            recalculate_working_records_batch.run()
        elif batch_type == co.BATCH_TYPE_FIND_DEFECTED_USER_INFO_RECORDS_AND_MARK_STATUS_FAILURE:
            find_defected_user_info_records_batch.run()
        elif batch_type == co.BATCH_TYPE_FIND_DEFECTED_WORKING_RECORDS_AND_MARK_STATUS_FAILURE:
            find_defected_working_records_batch.run()
    
except KeyboardInterrupt:
    print('Ctrl+Cで終了')
except Exception as e:
    print("Exception")
    print(e, type(e))
    print(traceback.format_exc())