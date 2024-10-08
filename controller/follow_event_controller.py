#!/usr/bin/env python3
import os
import service.authenticate_service as au_sv
import service.reply_to_new_follower_service as rtnf_sv
import service.shared.line_tool_service as lt_sv

def action(event, line_name):
    operating_mode = int(os.getenv('SV_SLACKERS_APP_OPERATING_MODE', None))
    userInfo, replyInstance = au_sv.get_authentication(operating_mode, event.source.user_id, line_name)
    if userInfo == None:
        print('No UserInfo : {} : {}'.format(event.source.user_id, line_name))
        return lt_sv.get_a_text_send_message('システムエラーが発生しました。システム管理者までお問い合わせください。')
    return rtnf_sv.get_a_reply_to_new_follower(userInfo, replyInstance)
