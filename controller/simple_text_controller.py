#!/usr/bin/env python3
import os
import service.authenticate_service as au_sv
import service.reply_to_simple_text_message_service as rs_sv
import service.shared.line_tool_service as lt_sv

def action(event, line_name):
    operating_mode = int(os.getenv('SV_SLACKERS_APP_OPERATING_MODE', None))
    userInfo, authenticate_msg_instance = au_sv.get_authentication(
        operating_mode, event.source.user_id, line_name
    )
    if authenticate_msg_instance != None:
        return authenticate_msg_instance
    elif userInfo == None:
        return lt_sv.get_a_text_send_message('ユーザ認証に失敗しました。')
    return rs_sv.reply_to_message_postbacked(operating_mode, userInfo, event.message.text)