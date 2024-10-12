#!/usr/bin/env python3
import datetime
import sys
import json
import common.constant as co
import repository.working_record_repository as wr_rp
import service.shared.line_tool_service as lt_sv
from entity.working_record_entity import WorkingRecord

# WorkingRecord
def get_a_working_record(userInfo, process_category=None, process_status=None, limit_value=1):
    result_count, result = wr_rp.a_working_record_select_by_user_id(
        userInfo.id, process_category, process_status, limit_value)
    if result_count == 0:
        return None
    else:
        workingRecord = WorkingRecord()
        workingRecord.setEntityFromRecord(result)
        return workingRecord

def add_new_working_record(userInfo):
    workingRecord = WorkingRecord(
        user_id = userInfo.id,
        line_user_id = userInfo.line_user_id,
        process_category = co.PROCESS_CATEGORY_RECORD_WORKING_HOURS,
        process_status = co.PROCESS_STATUS_NOT_STARTED,
        stage = userInfo.current_stage,
        registered_datetime = datetime.datetime.now(),
        registered_by = sys._getframe().f_code.co_name,
        updated_datetime = datetime.datetime.now(),
        updated_by = sys._getframe().f_code.co_name
    )
    result_count = wr_rp.new_working_record_insert(workingRecord)
    return workingRecord if result_count != 0 else None

def start_the_work(workingRecord):
    if workingRecord.process_category != co.PROCESS_CATEGORY_RECORD_WORKING_HOURS \
        or workingRecord.process_status != co.PROCESS_STATUS_NOT_STARTED \
        or workingRecord.standby_status != co.STANDBY_STATUS_READY:
        return None
    workingRecord.process_status = co.PROCESS_STATUS_ON_RECORDING
    workingRecord.start_time = datetime.datetime.now() if workingRecord.start_time == None \
    else workingRecord.start_time
    workingRecord.updated_datetime = datetime.datetime.now()
    workingRecord.updated_by = sys._getframe().f_code.co_name
    result_count = wr_rp.working_record_status_update(workingRecord)
    return workingRecord if result_count != 0 else None

def finish_the_work(workingRecord):
    if workingRecord.process_category != co.PROCESS_CATEGORY_RECORD_WORKING_HOURS \
        or workingRecord.process_status != co.PROCESS_STATUS_ON_RECORDING \
        or workingRecord.standby_status != co.STANDBY_STATUS_READY:
        return None
    workingRecord.process_status = co.PROCESS_STATUS_RECORDED_SUCCESS
    workingRecord.finish_time = datetime.datetime.now() if workingRecord.finish_time == None \
    else workingRecord.finish_time
    workingRecord.updated_datetime = datetime.datetime.now()
    workingRecord.updated_by = sys._getframe().f_code.co_name
    result_count = wr_rp.working_record_update_category_status_start_time_finish_time(workingRecord)
    return workingRecord if result_count != 0 else None

def update_working_record(workingRecord, target_element_column, new_value):
    exec('workingRecord.{} = {}{}{}'.format(
        target_element_column,
        '' if type(new_value) == 'number' else '"',
        new_value,
        '' if type(new_value) == 'number' else '"'        
    ))
    workingRecord.updated_datetime = datetime.datetime.now(),
    workingRecord.updated_by = sys._getframe().f_code.co_name
    result_count = wr_rp.working_record_update(workingRecord, target_element_column)
    return workingRecord if result_count != 0 else None

