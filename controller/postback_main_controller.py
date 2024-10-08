#!/usr/bin/env python3
import os
import service.authenticate_service as authenticate_sv
import service.shared.line_tool_service as lt_sv
import controller.postback_display_controller as postback_display_cr
import controller.postback_update_controller as postback_update_cr

def action(event, line_name):
    operating_mode = int(os.getenv('SV_SLACKERS_APP_OPERATING_MODE', None))
    data = lt_sv.get_postbacked_data(event)
    userInfo, authenticate_msg_instance = authenticate_sv.main(
        operating_mode, event.source.user_id, line_name, data
    )
    if authenticate_msg_instance != None:
        return authenticate_msg_instance
    elif userInfo == None:
        return lt_sv.get_a_text_send_message('ユーザ認証に失敗しました。')
    if data['action'] == 'display':
        return postback_display_cr.action(operating_mode, userInfo, data)
    elif data['action'] == 'update':
        return postback_update_cr.action(operating_mode, userInfo, data)
    else:
        return lt_sv.get_a_text_send_message('よくわかんねぇデータを受け取ったぞ')