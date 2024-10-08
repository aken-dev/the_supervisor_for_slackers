#!/usr/bin/env python3
import os
import service.authenticate_service as au_sv
import service.shared.line_tool_service as lt_sv
import controller.simple_text_start_working_controller as simple_text_start_working_cr
import controller.simple_text_finish_working_controller as simple_text_finish_working_cr
import controller.simple_text_highlight_controller as simple_text_highlight_cr
import controller.simple_text_history_controller as simple_text_history_cr
import controller.simple_text_tally_controller as simple_text_tally_cr
import controller.simple_text_setting_controller as simple_text_setting_cr

def action(event, line_name):
    operating_mode = int(os.getenv('SV_SLACKERS_APP_OPERATING_MODE', None))
    userInfo, authenticate_msg_instance = au_sv.get_authentication(
        operating_mode, event.source.user_id, line_name
    )
    if authenticate_msg_instance != None:
        return authenticate_msg_instance
    elif userInfo == None:
        return lt_sv.get_a_text_send_message('ユーザ認証に失敗しました。')
    recieved_text = event.message.text
    if recieved_text == '開始したよ' or recieved_text == 'start' or recieved_text == '1':
        return simple_text_start_working_cr.action(operating_mode, userInfo, recieved_text)
    elif recieved_text == '終わったよ' or recieved_text == 'finish' or recieved_text == '2':
        return simple_text_finish_working_cr.action(operating_mode, userInfo, recieved_text)
    elif recieved_text == '今日の実績' or recieved_text == 'highlight' or recieved_text == 'now' or recieved_text == '3':
        return simple_text_highlight_cr.action(operating_mode, userInfo, recieved_text)
    elif recieved_text == '履歴を見せて' or recieved_text == 'history' or recieved_text == '4':
        return simple_text_history_cr.action(operating_mode, userInfo, recieved_text)
    elif recieved_text == '集計を見せて' or recieved_text == 'tally' or recieved_text == '5':
        return simple_text_tally_cr.action(operating_mode, userInfo, recieved_text)
    elif recieved_text == '設定を見せて' or recieved_text == 'setting' or recieved_text == '6':
        return simple_text_setting_cr.action(operating_mode, userInfo, recieved_text)
    else:
        return lt_sv.get_a_text_send_message('よくわからねぇ。')