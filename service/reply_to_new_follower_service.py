#!/usr/bin/env python3
import common.constant as co
import service.shared.line_tool_service as lt_sv

def get_a_reply_to_new_follower(userInfo, replyInstance):
    if replyInstance != None:
        return replyInstance
    elif userInfo.allowed == co.USER_ALLOWED:
        return lt_sv.get_a_text_send_message('おかえりなさい！')
    else:
        return lt_sv.get_a_text_send_message('その他のメッセージ')
