#!/usr/bin/env python3
import datetime
import sys
import json
import traceback
import re
import common.constant as co
import repository.user_info_repository as ui_rp
import service.line_tool_service as lt_sv
from entity.user_info_entity import UserInfo

# UserInfo
def get_user_info(line_user_id, line_name):
    result_count, result = ui_rp.user_info_select(line_user_id)
    if result_count == 0:
        userInfo = add_new_user(line_user_id, line_name)
        if userInfo == None:
            print('新規ユーザレコード追加失敗 : {} : {}'.format(line_user_id, line_name))
            return None
        else:
            return userInfo
    else:
        userInfo = UserInfo()
        userInfo.setEntityFromRecord(result)
        return userInfo

def add_new_user(line_user_id, line_name):
    userInfo = UserInfo(
        line_user_id = line_user_id,
        line_name = line_name,
        allowed = co.USER_UNREGISTERED,
        registered_datetime = datetime.datetime.now(),
        registered_by = sys._getframe().f_code.co_name,
        updated_datetime = datetime.datetime.now(),
        updated_by = sys._getframe().f_code.co_name
    )
    result_count = ui_rp.userinfo_new_user_insert(userInfo)
    if result_count == 0:
        return None
    else:
        return userInfo

def change_user_allowed(userInfo, new_allowed):
    userInfo.allowed = new_allowed
    userInfo.updated_datetime = datetime.datetime.now(),
    userInfo.updated_by = sys._getframe().f_code.co_name
    result_count = ui_rp.userinfo_update(userInfo, 'allowed')
    if result_count == 0:
        return None
    else:
        return userInfo

def update_user_info(userInfo, target_column, new_value):
    eval('userInfo.{} = {}'.format(target_column, new_value))
    userInfo.updated_datetime = datetime.datetime.now(),
    userInfo.updated_by = sys._getframe().f_code.co_name
    result_count = ui_rp.userinfo_update(userInfo, target_column)
    if result_count == 0:
        return None
    else:
        return userInfo

def display_user_info(userInfo, new_user_flag=False):
    msg_instances = []
    if new_user_flag == True:
        msg_instances.append(lt_sv.get_a_text_send_message(
            '君は怠惰で有名な{}だろ！？\n待ってたぞ。\nまずは質より量だ。はやく作業に取り掛るんだ！'
            .format(userInfo.line_name)
        ))
        msg_instances.append(lt_sv.get_a_text_send_message(
            '初期の設定内容だ。必要に応じて変更してくれ。' 
        ))
    msg_instances.append(get_user_info_setting(userInfo))
    msg_instances.append(get_txt_with_quick_reply_btns_for_user_info(userInfo))
    return msg_instances
    
def get_user_info_setting(userInfo):
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
    
def get_txt_with_quick_reply_btns_for_user_info(userInfo):
    return lt_sv.get_a_text_send_message_includes_quick_reply_buttons(
        '設定変更は下記のボタンから頼む。',
        [
            lt_sv.get_quick_reply_button_for_postback(
                '現在の課題番号を変更', 
                '現在の課題番号を変更', 
                json.dumps({
                    "action": "display",
                    "type": "choices",
                    "target": "current_stage",
                    "min": 1,
                    "max": userInfo.the_last_stage,
                    "current": userInfo.current_stage
                })
            ),
            lt_sv.get_quick_reply_button_for_postback_datetime( 
                '直近の課題番号変更日を変更', 
                json.dumps({
                    "action": "update",
                    "type": "choices",
                    "target": "recent_stage_changed_date",
                    "min": 1,
                    "max": userInfo.the_last_stage,
                    "current": userInfo.current_stage
                }),
                'date',
                userInfo.recent_stage_changed_date.strftime("%Y-%m-%d") if 
                userInfo.recent_stage_changed_date != None else '',
                datetime.datetime.now().strftime("%Y-%m-%d")
            )
        ]
    )
        