#!/usr/bin/env python3
import datetime
import sys
import json
import common.constant as co
import repository.user_info_repository as ui_rp
import service.shared.line_tool_service as lt_sv
import service.shared.datetime_calc_service as dc_sv
from entity.user_info_entity import UserInfo

# UserInfo
def get_user_info(line_user_id, line_name):
    selected_user = ui_rp.user_info_select(line_user_id)
    if selected_user['count'] == 0:
        added_new_user = add_new_user(line_user_id, line_name)
        if added_new_user['count'] == 0:
            print('新規ユーザレコード追加失敗 : {} : {}'.format(line_user_id, line_name))
            return {
                "userInfo": None,
                "count": added_new_user['count']
            }
        else:
            return {
                "userInfo": added_new_user['userInfo'],
                "count": added_new_user['count']
            }
    else:
        userInfo = UserInfo()
        userInfo.setEntityFromRecord(selected_user['result'])
        return {
            "userInfo": userInfo,
            "count": selected_user['count']
        }

def add_new_user(line_user_id, line_name):
    userInfo = UserInfo(
        line_user_id = line_user_id,
        line_name = line_name,
        allowed = co.USER_UNREGISTERED,
        recent_stage_changed_date = datetime.date.today(),
        registered_datetime = datetime.datetime.now(),
        registered_by = sys._getframe().f_code.co_name,
        updated_datetime = datetime.datetime.now(),
        updated_by = sys._getframe().f_code.co_name
    )
    result_count = ui_rp.userinfo_new_user_insert(userInfo)
    return {
        "userInfo": userInfo,
        "count": result_count
    }

def change_user_allowed(userInfo, new_allowed):
    userInfo.allowed = new_allowed
    userInfo.updated_datetime = datetime.datetime.now(),
    userInfo.updated_by = sys._getframe().f_code.co_name
    result_count = ui_rp.userinfo_update(userInfo, 'allowed')
    return {
        "userInfo": userInfo,
        "count": result_count
    }

def update_user_info(userInfo, target_element_column, new_value, updated_at= None, updated_by=None):
    if updated_at == None: updated_at = datetime.datetime.now()
    if updated_by == None: updated_by = sys._getframe().f_code.co_name
    exec('userInfo.{} = {}{}{}'.format(
        target_element_column,
        '' if type(new_value) == 'number' else '"',
        new_value,
        '' if type(new_value) == 'number' else '"'        
    ))
    userInfo.updated_datetime = updated_at
    userInfo.updated_by = updated_by
    result_count = ui_rp.userinfo_update(userInfo, target_element_column)
    return {
        "userInfo": userInfo,
        "count": result_count
    }

def display_user_info_main(userInfo, new_user_flag=False):
    msg_instances = []
    if new_user_flag:
        msg_instances.append(lt_sv.get_a_text_send_message(
            '君は怠惰で有名な{}だろ！？\n待ってたぞ。\nまずは質より量だ。はやく作業に取り掛るんだ！'
            .format(userInfo.line_name)
        ))
        msg_instances.append(lt_sv.get_a_text_send_message(
            '初期の設定内容だ。必要に応じて変更してくれ。' 
        ))
    msg_instances.append(get_user_info_details(userInfo))
    msg_instances.append(get_user_info_setting_func(userInfo))
    return msg_instances
    
def get_user_info_details(userInfo):
    return lt_sv.get_a_text_send_message(
        '【現在の設定内容】\n\n'
        + '[現在の課題番号]\n   #{}\n\n'.format(userInfo.current_stage)
        + '[直近の課題番号変更日]\n   {}（{}）\n\n'.format(
            (
                userInfo.recent_stage_changed_date if 
                userInfo.recent_stage_changed_date != None else '履歴なし'
            ), 
            (
                co.WEEKDAY[userInfo.recent_stage_changed_date.weekday()] if
                userInfo.recent_stage_changed_date != None else '履歴なし'
            )
        )
        + '[次の課題番号への変更]\n   {}\n\n'.format(
            'リマインドしない' if userInfo.stage_change_remind_type == co.STAGE_CHANGE_REMIND_TYPE_NOTHING else (
                '（毎週）{}にリマインド'.format(co.WEEKDAY[userInfo.stage_change_remind_value]) if 
                userInfo.stage_change_remind_type == co.STAGE_CHANGE_REMIND_TYPE_DAY_OF_WEEK 
                and userInfo.stage_change_remind_value <= 6 else (
                    '番号変更の{}日後にリマインド'.format(userInfo.stage_change_remind_value) if 
                    userInfo.stage_change_remind_type == co.STAGE_CHANGE_REMIND_TYPE_DAYS else 'リマインド間隔が未設定'
                )
            )
        )
        + '[作業目標時間（1日あたり）]\n   {}時間\n\n'.format(userInfo.required_working_hours)
        + '[1日のはじまりは何時？]\n   {}時\n\n'.format(userInfo.starting_time_of_a_day)
        + '[最後の課題番号]\n   #{}\n\n'.format(userInfo.the_last_stage)
    )
    
def get_user_info_setting_func(userInfo):
    return lt_sv.get_a_text_send_message_includes_quick_reply_buttons(
        '設定変更は下記のボタンから頼む。',
        [
            lt_sv.get_quick_reply_button_for_postback(
                '現在の課題番号を変更', 
                '現在の課題番号を変更', 
                json.dumps({
                    "action": "display",
                    "type": "choices",
                    "tar_tbl": "user_info",
                    "tar_id": "",
                    "tar_el": "current_stage",
                    "tmp_val": userInfo.current_stage,
                    "min": 1,
                    "max": userInfo.the_last_stage,
                    "cur_val": userInfo.current_stage,
                    "label": "現在の課題番号",
                    "uni_before_val": "[ #",
                    "uni_after_val": " ]"
                })
            ),
            lt_sv.get_quick_reply_button_for_postback_datetime( 
                '直近の番号変更日を修正', 
                json.dumps({
                    "action": "update",
                    "type": "",
                    "tar_tbl": "user_info",
                    "tar_id": "",
                    "tar_el": "recent_stage_changed_date",
                    "new_val": "date",
                    "label": "直近の番号変更日",
                    "cur_val": dc_sv.get_string_from_datetime(userInfo.recent_stage_changed_date, 'date') if 
                    userInfo.recent_stage_changed_date != None else '',
                    "uni_before_val": "",
                    "uni_after_val": ""
                }),
                'date',
                dc_sv.get_string_from_datetime(userInfo.recent_stage_changed_date, 'date') if 
                userInfo.recent_stage_changed_date != None else '',
                dc_sv.get_string_from_datetime(datetime.datetime.now(), 'date')
            ),
            lt_sv.get_quick_reply_button_for_postback(
                '曜日でリマインドを設定', 
                '曜日でリマインドを設定', 
                json.dumps({
                    "action": "update",
                    "type": "",
                    "tar_tbl": "user_info",
                    "tar_id": "",
                    "tar_el": "stage_change_remind_type",
                    "new_val": co.STAGE_CHANGE_REMIND_TYPE_DAY_OF_WEEK,
                    "cur_val": userInfo.stage_change_remind_type,
                    "label": "リマインド設定",
                    "uni_before_val": "",
                    "uni_after_val": ""
                })
            ),
            lt_sv.get_quick_reply_button_for_postback(
                '日数間隔でリマインドを設定', 
                '日数間隔でリマインドを設定', 
                json.dumps({
                    "action": "update",
                    "type": "",
                    "tar_tbl": "user_info",
                    "tar_id": "",
                    "tar_el": "stage_change_remind_type",
                    "new_val": co.STAGE_CHANGE_REMIND_TYPE_DAYS,
                    "cur_val": userInfo.stage_change_remind_type,
                    "label": "リマインド設定",
                    "uni_before_val": "",
                    "uni_after_val": ""
                })
            ),
            lt_sv.get_quick_reply_button_for_postback(
                'リマインド設定を解除', 
                'リマインド設定を解除', 
                json.dumps({
                    "action": "update",
                    "type": "",
                    "tar_tbl": "user_info",
                    "tar_id": "",
                    "tar_el": "stage_change_remind_type",
                    "new_val": co.STAGE_CHANGE_REMIND_TYPE_NOTHING,
                    "cur_val": userInfo.stage_change_remind_type,
                    "label": "リマインド設定",
                    "uni_before_val": "",
                    "uni_after_val": ""
                })
            ),
            lt_sv.get_quick_reply_button_for_postback(
                '目標作業時間（1日あたり）を変更', 
                '目標作業時間（1日あたり）を変更', 
                json.dumps({
                    "action": "display",
                    "type": "choices",
                    "tar_tbl": "user_info",
                    "tar_id": "",
                    "tar_el": "required_working_hours",
                    "tmp_val": userInfo.required_working_hours,
                    "min": 1,
                    "max": 24,
                    "cur_val": userInfo.required_working_hours,
                    "label": "目標作業時間",
                    "uni_before_val": "",
                    "uni_after_val": "時間"
                })
            ),
            lt_sv.get_quick_reply_button_for_postback(
                '1日のはじまりの時刻を変更', 
                '1日のはじまりの時刻を変更', 
                json.dumps({
                    "action": "display",
                    "type": "choices",
                    "tar_tbl": "user_info",
                    "tar_id": "",
                    "tar_el": "starting_time_of_a_day",
                    "tmp_val": userInfo.starting_time_of_a_day,
                    "min": 0,
                    "max": 23,
                    "cur_val": userInfo.starting_time_of_a_day,
                    "label": "1日のはじまりの時刻",
                    "uni_before_val": "",
                    "uni_after_val": "時"
                })
            ),
            lt_sv.get_quick_reply_button_for_postback(
                '最大の課題番号を変更', 
                '最大の課題番号を変更', 
                json.dumps({
                    "action": "display",
                    "type": "choices",
                    "tar_tbl": "user_info",
                    "tar_id": "",
                    "tar_el": "the_last_stage",
                    "tmp_val": userInfo.the_last_stage,
                    "min": 1,
                    "max": 100,
                    "cur_val": userInfo.the_last_stage,
                    "label": "最大の課題番号",
                    "uni_before_val": "[ #",
                    "uni_after_val": " ]"
                })
            ),
            lt_sv.get_quick_reply_button_for_postback(
                '利用規約を表示', 
                '利用規約を表示', 
                json.dumps({
                    "action": "display",
                    "type": "display",
                    "target": "terms_of_use"
                })
            )
        ]
    )
    
def is_remind_needed(userInfo):
    time_range = dc_sv.get_users_time_range_of_the_day(userInfo.starting_time_of_a_day)
    if userInfo.stage_change_remind_type == co.STAGE_CHANGE_REMIND_TYPE_DAY_OF_WEEK \
        and userInfo.stage_change_remind_value == time_range['start_of_the_day'].date().weekday() \
            and time_range['start_of_the_day'].date() != userInfo.recent_stage_changed_date:
                return True
    elif userInfo.stage_change_remind_type == co.STAGE_CHANGE_REMIND_TYPE_DAYS \
        and userInfo.recent_stage_changed_date != None \
            and userInfo.stage_change_remind_value >= 1 \
                and userInfo.recent_stage_changed_date + datetime.timedelta(
                    days=userInfo.stage_change_remind_value
                ) <= time_range['start_of_the_day'].date():
                    return True 
    return False