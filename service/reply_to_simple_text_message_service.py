#!/usr/bin/env python3
import service.shared.line_tool_service as lt_sv

def reply_to_message_postbacked(operating_mode, userInfo, recieved_text):
    return lt_sv.get_a_text_send_message(recieved_text)#ひとまず受信したテキストをそのまま返しておく