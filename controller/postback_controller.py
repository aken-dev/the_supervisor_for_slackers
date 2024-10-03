#!/usr/bin/env python3
import os
import json
import service.authenticate_service as au_sv
import service.reply_to_postbacked_message_service as rp_sv
import service.line_tool_service as lt_sv
def action(event, line_name):
    data = json.loads(event.postback.data)
    operating_mode = int(os.getenv('SV_SLACKERS_APP_OPERATING_MODE', None))
    userInfo, authenticate_msg_instance = au_sv.get_authentication(
        operating_mode, event.source.user_id, line_name, data
    )
    if authenticate_msg_instance != None:
        return authenticate_msg_instance
    elif userInfo == None:
        return lt_sv.get_a_text_send_message(
            '不明なエラーが発生しました。しばらく経っても改善しない場合は運営にご連絡ください。'
        )
    else:
        return rp_sv.reply_to_message_postbacked(userInfo, data)