#!/usr/bin/env python3
import os
import service.authenticate_service as authenticate_sv
import service.shared.line_tool_service as lt_sv
import service.reply_to_text_start_working_service as reply_to_text_start_working_sv
import service.reply_to_text_finish_working_service as reply_to_text_finish_working_sv
import service.reply_to_text_highlight_service as reply_to_text_highlight_sv
import service.reply_to_text_history_service as reply_to_text_history_sv
import service.reply_to_text_tally_service as reply_to_text_tally_sv
import service.reply_to_text_setting_service as reply_to_text_setting_sv

def action(event, line_name):
    operating_mode = int(os.getenv('SV_SLACKERS_APP_OPERATING_MODE', None))
    auth = authenticate_sv.main(
        operating_mode, event.source.user_id, line_name
    )
    if auth['msg'] != None:
        return auth['msg']
    elif auth['userInfo'] == None:
        return lt_sv.get_a_text_send_message('ユーザ認証に失敗しました。')
    recieved_text = event.message.text
    if recieved_text == '開始したよ' or recieved_text == 'start' or recieved_text == '1':
        return reply_to_text_start_working_sv.main(operating_mode, auth['userInfo'], recieved_text)
    elif recieved_text == '終わったよ' or recieved_text == 'finish' or recieved_text == '2':
        return reply_to_text_finish_working_sv.main(operating_mode, auth['userInfo'], recieved_text)
    elif recieved_text == '今日の実績' or recieved_text == 'highlight' or recieved_text == 'now' or recieved_text == '3':
        return reply_to_text_highlight_sv.main(operating_mode, auth['userInfo'], recieved_text)
    elif recieved_text == '履歴を見せて' or recieved_text == 'history' or recieved_text == '4':
        return reply_to_text_history_sv.main(operating_mode, auth['userInfo'], recieved_text)
    elif recieved_text == '集計を見せて' or recieved_text == 'tally' or recieved_text == '5':
        return reply_to_text_tally_sv.main(operating_mode, auth['userInfo'], recieved_text)
    elif recieved_text == '設定を見せて' or recieved_text == 'setting' or recieved_text == '6':
        return reply_to_text_setting_sv.main(operating_mode, auth['userInfo'], recieved_text)
    else:
        return lt_sv.get_a_text_send_message('よくわからねぇ。')