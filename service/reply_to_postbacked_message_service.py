#!/usr/bin/env python3
import service.shared.authenticate_service as au_sv
import service.shared.line_tool_service as lt_sv
def reply_to_message_postbacked(operating_mode, event, line_name):
    postbacked_data = lt_sv.get_postbacked_data(event)
    userInfo, authenticate_msg_instance = au_sv.get_authentication(
        operating_mode, event.source.user_id, line_name, postbacked_data
    )
    if authenticate_msg_instance != None:
        return authenticate_msg_instance
    elif userInfo == None:
        return lt_sv.get_a_text_send_message('ユーザ認証に失敗しました。')
    return lt_sv.get_a_text_send_message('ポストバックメッセージを受け取りました。')
