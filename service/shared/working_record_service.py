#!/usr/bin/env python3
import datetime
import sys
import json
import common.constant as co
import repository.working_record_repository as wr_rp
import service.shared.line_tool_service as lt_sv
import service.shared.datetime_calc_service as dc_sv
from entity.working_record_entity import WorkingRecord

# WorkingRecord
def get_a_working_record(userInfo, process_category=None, process_status=None, limit_value=1):
    result_count, result = wr_rp.a_working_record_select_by_user_id(
        userInfo.id, process_category, process_status, limit_value)
    if result_count <= 0: return None
    workingRecord = WorkingRecord()
    workingRecord.setEntityFromRecord(result[0])
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
    if wr_rp.new_working_record_insert(workingRecord) <= 0: return None
    result_count, result = wr_rp.a_working_record_select_by_user_id(
        userInfo.id, co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, co.PROCESS_STATUS_NOT_STARTED
    )
    if result_count <= 0: return None
    workingRecord.setEntityFromRecord(result[0]) 
    return workingRecord

def start_the_work(userInfo, workingRecord=None):
    if workingRecord == None:
        workingRecord = WorkingRecord(
            user_id = userInfo.id,
            line_user_id = userInfo.line_user_id,
            process_category = co.PROCESS_CATEGORY_RECORD_WORKING_HOURS,
            process_status = co.PROCESS_STATUS_ON_RECORDING,
            stage = userInfo.current_stage,
            start_time = datetime.datetime.now(),
            registered_datetime = datetime.datetime.now(),
            registered_by = sys._getframe().f_code.co_name,
            updated_datetime = datetime.datetime.now(),
            updated_by = sys._getframe().f_code.co_name
        )
        return workingRecord if wr_rp.new_working_record_insert(workingRecord) > 0 else None
    else:
        if workingRecord.process_category != co.PROCESS_CATEGORY_RECORD_WORKING_HOURS \
            or workingRecord.process_status != co.PROCESS_STATUS_NOT_STARTED \
            or workingRecord.standby_status != co.STANDBY_STATUS_READY:
                return None
        workingRecord.process_status = co.PROCESS_STATUS_ON_RECORDING
        workingRecord.start_time = datetime.datetime.now() if workingRecord.start_time == None \
        else workingRecord.start_time
        workingRecord.updated_datetime = datetime.datetime.now()
        workingRecord.updated_by = sys._getframe().f_code.co_name
        return workingRecord if wr_rp.working_record_status_update(workingRecord) > 0 else None

def finish_the_work(userInfo, workingRecord=None):
    if workingRecord == None:
        workingRecord = get_a_working_record(
            userInfo, co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, co.PROCESS_STATUS_ON_RECORDING
        )
    if workingRecord == None \
        or workingRecord.process_category != co.PROCESS_CATEGORY_RECORD_WORKING_HOURS \
        or workingRecord.process_status != co.PROCESS_STATUS_ON_RECORDING \
        or workingRecord.standby_status != co.STANDBY_STATUS_READY:
        return None
    workingRecord.process_status = co.PROCESS_STATUS_RECORDED_SUCCESS
    workingRecord.finish_time = datetime.datetime.now() if workingRecord.finish_time == None \
    else workingRecord.finish_time
    workingRecord.updated_datetime = datetime.datetime.now()
    workingRecord.updated_by = sys._getframe().f_code.co_name
    return workingRecord if wr_rp.working_record_status_update(workingRecord) > 0 else None

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

def display_working_history_main(userInfo, target_start_time=None):
    result_count, result = wr_rp.a_working_record_select_by_user_id_start_time_for_past(
        userInfo.id, 
        target_start_time if target_start_time != None else datetime.datetime.now(),
        2,
    )
    if result_count >= 1:
        workingRecord = WorkingRecord()
        workingRecord.setEntityFromRecord(result[0])
        future_record_count_asc, future_records = wr_rp.a_working_record_select_by_user_id_start_time_for_future(
            userInfo.id, 
            workingRecord.start_time,
            2
        )
        if future_record_count_asc >= 2:
            futureWorkingRecord = WorkingRecord()
            futureWorkingRecord.setEntityFromRecord(future_records[1])
        return get_a_history(
            userInfo,
            workingRecord,
            None if future_record_count_asc < 2 else futureWorkingRecord.start_time,
            None if result_count < 2 else workingRecord.start_time + datetime.timedelta(seconds=-1)
        )
    return lt_sv.get_a_text_send_message('記録が１件も無いぞ。')
        
def get_a_history(userInfo, workingRecord, future_start_time, previous_start_time):
    quick_reply_btns = []
    if previous_start_time != None:
        quick_reply_btns.append(lt_sv.get_quick_reply_button_for_postback(
            '1つ前を表示', 
            '1つ前の履歴を表示', 
            json.dumps({
                "action": "display",
                "type": "working_history",
                "target_datetime": dc_sv.get_string_from_datetime(previous_start_time)
            })
        ))
    if future_start_time != None:
        quick_reply_btns.append(lt_sv.get_quick_reply_button_for_postback(
            '1つ後を表示', 
            '1つ後の履歴を表示', 
            json.dumps({
                "action": "display",
                "type": "working_history",
                "target_datetime": dc_sv.get_string_from_datetime(future_start_time)
            })
        ))
    quick_reply_btns.append(lt_sv.get_quick_reply_button_for_postback(
        '課題番号を変更', 
        '課題番号を変更', 
        json.dumps({
            "action": "display",
            "type": "choices",
            "target_table": "working_record",
            "target_record": workingRecord.id,
            "target_element": "stage",
            "tmp_value": workingRecord.stage,
            "min": 1,
            "max": userInfo.the_last_stage,
            "current_value": workingRecord.stage,
            "label": "課題番号",
            "unit_before_value": "#",
            "unit_after_value": ""
        })
    ))
    quick_reply_btns.append(
            lt_sv.get_quick_reply_button_for_postback_datetime( 
                '作業開始日時を修正', 
                json.dumps({
                    "action": "update",
                    "type": "",
                    "target_record": workingRecord.id,
                    "target_table": "working_record",
                    "target_element": "start_time",
                    "new_value": "datetime",
                    "label": "作業開始日時",
                    "current_value": dc_sv.get_string_from_datetime(workingRecord.start_time) if 
                    workingRecord.start_time != None else '',
                }),
                'datetime',
                dc_sv.get_string_from_datetime(workingRecord.start_time) if 
                workingRecord.start_time!= None else '',
                dc_sv.get_string_from_datetime()
            ),        
    )
    return lt_sv.get_a_text_send_message_includes_quick_reply_buttons(
        '【作業履歴】\n\n' \
        + '[課題番号]\n   #{}\n\n'.format(workingRecord.stage)
        + '[作業開始]\n   {}\n\n'.format(workingRecord.start_time)
        + '[作業終了]\n   {}\n\n'.format(
                                            workingRecord.finish_time if 
                                            workingRecord.process_status == co.PROCESS_STATUS_RECORDED_SUCCESS else 
                                            '（作業中）'
                                        )
        + '{}'.format('' if workingRecord.memo_1 == None else '[メモ1]\n  {}\n'.format(workingRecord.memo_1))
        + '{}'.format('' if workingRecord.memo_2 == None else '[メモ2]\n  {}\n'.format(workingRecord.memo_2))
        + '{}'.format('' if workingRecord.memo_3 == None else '[メモ3]\n  {}\n'.format(workingRecord.memo_3)),
        quick_reply_btns
    )
    