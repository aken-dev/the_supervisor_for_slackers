#!/usr/bin/env python3
import common.constant as co
import service.authenticate_service as au_sv
import service.line_tool_service as lt_sv

def get_a_reply_to_new_follower(operating_mode, event, line_name):
    userInfo, replyInstance = au_sv.get_authentication(operating_mode, event.source.user_id, line_name)
    if userInfo == None:
        print('No UserInfo : {} : {}'.format(event.source.user_id, line_name))
        return lt_sv.get_a_text_send_message('システムエラーが発生しました。システム管理者までお問い合わせください。')
    elif replyInstance != None:
        return replyInstance
    elif userInfo.allowed == co.USER_ALLOWED:
        return lt_sv.get_a_text_send_message('おかえりなさい！')
    else:
        return lt_sv.get_a_text_send_message('その他のメッセージ')

        
