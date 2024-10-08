#!/usr/bin/env python3
import service.shared.line_tool_service as lt_sv

def reply_to_message_postbacked(operating_mode, userInfo, postbacked_data):
    return lt_sv.get_a_text_send_message('ポストバックメッセージを受け取りました。')
