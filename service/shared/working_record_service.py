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
def get_a_working_record_by_status(
        userInfo, 
        process_category=co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, 
        process_status=co.PROCESS_STATUS_ON_RECORDING, 
        limit_value=1
    ):
    result_count, result = wr_rp.a_working_record_select_by_user_id(
        userInfo.id, process_category, process_status, limit_value)
    if result_count <= 0: return None
    workingRecord = WorkingRecord()
    workingRecord.setEntityFromRecord(result[0])
    return workingRecord

def get_a_working_record_by_record_id(id):
    result_count, result = wr_rp.a_working_record_select_by_id(id)
    if result_count <= 0: return None
    workingRecord = WorkingRecord()
    workingRecord.setEntityFromRecord(result)
    return workingRecord

# def add_new_working_record(userInfo):
#     workingRecord = WorkingRecord(
#         user_id = userInfo.id,
#         line_user_id = userInfo.line_user_id,
#         process_category = co.PROCESS_CATEGORY_RECORD_WORKING_HOURS,
#         process_status = co.PROCESS_STATUS_NOT_STARTED,
#         stage = userInfo.current_stage,
#         registered_datetime = datetime.datetime.now(),
#         registered_by = sys._getframe().f_code.co_name,
#         updated_datetime = datetime.datetime.now(),
#         updated_by = sys._getframe().f_code.co_name
#     )
#     if wr_rp.new_working_record_insert(workingRecord) <= 0: return None
#     result_count, result = wr_rp.a_working_record_select_by_user_id(
#         userInfo.id, co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, co.PROCESS_STATUS_NOT_STARTED
#     )
#     if result_count <= 0: return None
#     workingRecord.setEntityFromRecord(result[0]) 
#     return workingRecord

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
        workingRecord = get_a_working_record_by_status(
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
    else: return lt_sv.get_a_text_send_message('記録が１件も無いぞ。')
        
def get_a_history(userInfo, workingRecord, future_start_time, previous_start_time):
    quick_reply_btns = []
    if previous_start_time != None:
        quick_reply_btns.append(lt_sv.get_quick_reply_button_for_postback(
            '1つ前を表示', 
            '1つ前の履歴を表示', 
            json.dumps({
                "action": "display",
                "type": "working_history",
                "target": dc_sv.get_string_from_datetime(previous_start_time, 'dt_with_sec')
            })
        ))
    if future_start_time != None:
        quick_reply_btns.append(lt_sv.get_quick_reply_button_for_postback(
            '1つ後を表示', 
            '1つ後の履歴を表示', 
            json.dumps({
                "action": "display",
                "type": "working_history",
                "target": dc_sv.get_string_from_datetime(future_start_time, 'dt_with_sec')
            })
        ))
    quick_reply_btns.extend(
        [
            lt_sv.get_quick_reply_button_for_postback(
                '課題番号を変更', 
                '課題番号を変更', 
                json.dumps({
                    "action": "display",
                    "type": "choices",
                    "tar_tbl": "working_record",
                    "tar_id": workingRecord.id,
                    "tar_el": "stage",
                    "tmp_val": workingRecord.stage,
                    "min": 1,
                    "max": userInfo.the_last_stage,
                    "cur_val": workingRecord.stage,
                    "label": "課題番号",
                    "uni_before_val": "#",
                    "uni_after_val": ""
                })
            ),  
            lt_sv.get_quick_reply_button_for_postback_datetime( 
                '作業開始日時を修正', 
                json.dumps({
                    "action": "update",
                    "type": "",
                    "tar_tbl": "working_record",
                    "tar_id": workingRecord.id,
                    "tar_el": "start_time",
                    "new_val": "datetime",
                    "label": "作業開始日時",
                    "cur_val": dc_sv.get_string_from_datetime(workingRecord.start_time) if 
                    workingRecord.start_time != None else '',
                    "uni_before_val": "",
                    "uni_after_val": ""
                }),
                'datetime',
                dc_sv.get_string_from_datetime(workingRecord.start_time) if 
                workingRecord.start_time!= None else '',
                dc_sv.get_string_from_datetime() if workingRecord.finish_time == None else 
                dc_sv.get_string_from_datetime(workingRecord.finish_time)
            )
        ]       
    )
    if workingRecord.process_status == co.PROCESS_STATUS_RECORDED_SUCCESS:
        quick_reply_btns.append(
            lt_sv.get_quick_reply_button_for_postback_datetime( 
                '作業終了日時を修正', 
                json.dumps({
                    "action": "update",
                    "type": "",
                    "tar_tbl": "working_record",
                    "tar_id": workingRecord.id,
                    "tar_el": "finish_time",
                    "new_val": "datetime",
                    "label": "作業終了日時",
                    "cur_val": dc_sv.get_string_from_datetime(workingRecord.finish_time),
                    "uni_before_val": "",
                    "uni_after_val": ""
                }),
                'datetime',
                dc_sv.get_string_from_datetime(workingRecord.finish_time) if 
                workingRecord.finish_time!= None else '',
                dc_sv.get_string_from_datetime(),
                dc_sv.get_string_from_datetime(workingRecord.start_time) if 
                workingRecord.start_time!= None else ''
            )
        )
    return lt_sv.get_a_text_send_message_includes_quick_reply_buttons(
        '【作業履歴】\n\n' \
        + '[課題番号]\n   #{}\n\n'.format(workingRecord.stage)
        + '[作業開始]\n   {}\n\n'.format(workingRecord.start_time)
        + '[作業終了]\n   {}\n\n'.format(workingRecord.finish_time if 
                                        workingRecord.process_status == co.PROCESS_STATUS_RECORDED_SUCCESS else 
                                            '（作業中）'
                                       )
        + '{}'.format('' if workingRecord.memo_1 == None else '[メモ1]\n  {}\n'.format(workingRecord.memo_1))
        + '{}'.format('' if workingRecord.memo_2 == None else '[メモ2]\n  {}\n'.format(workingRecord.memo_2))
        + '{}'.format('' if workingRecord.memo_3 == None else '[メモ3]\n  {}\n'.format(workingRecord.memo_3)),
        quick_reply_btns
    )
    
def get_worked_minutes_total_int_and_slacked_minutes_int(userInfo):
    datetime_start_of_the_day, datetime_end_of_the_day = dc_sv.get_users_time_range_of_the_day(
        userInfo.starting_time_of_a_day)
    worked_minutes_on_process = get_worked_minutes_on_process_int(
        userInfo.id, datetime_start_of_the_day, datetime_end_of_the_day
    )
    worked_minutes_finished = get_worked_minutes_finished_int(
        userInfo.id, datetime_start_of_the_day, datetime_end_of_the_day
    )
    datetime_how_many_time_passed_today = datetime.datetime.now() - datetime_start_of_the_day
    slacked_minutes = int(datetime_how_many_time_passed_today.seconds / 60) \
        - worked_minutes_on_process - worked_minutes_finished
    return worked_minutes_on_process + worked_minutes_finished, slacked_minutes

def get_worked_minutes_on_process_int(user_id, datetime_start_of_the_day, datetime_end_of_the_day):
    worked_minutes_on_process_result_count, worked_minutes_on_process_result = \
        wr_rp.worked_minutes_on_process_select(
            user_id, datetime_start_of_the_day, datetime_end_of_the_day
        )
    return (int(worked_minutes_on_process_result['worked_minutes']) if worked_minutes_on_process_result_count > 0 else 0)

def get_worked_minutes_finished_int(user_id, datetime_start_of_the_day, datetime_end_of_the_day):
    worked_minutes_finished_result_count, worked_minutes_finished_result = \
        wr_rp.worked_minutes_finished_select(
            user_id, datetime_start_of_the_day, datetime_end_of_the_day
        )
    return (int(worked_minutes_finished_result['worked_minutes']) if worked_minutes_finished_result_count > 0 else 0)

def get_stage_on_process(userInfo):
    workingRecord = get_a_working_record_by_status(userInfo)
    return workingRecord.stage if workingRecord != None else None

def get_minutes_slack_allowd_a_day(userInfo):
    return (24 - userInfo.required_working_hours) * 60
