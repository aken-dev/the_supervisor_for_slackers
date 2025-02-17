#!/usr/bin/env python3
import service.shared.line_tool_service as lt_sv
import service.reply_to_postback_update_user_info_service as reply_to_postback_update_user_info_sv
import service.reply_to_postback_update_working_record_service as reply_to_postback_update_working_record_sv

def action(operating_mode, userInfo, data):
    if data['tar_tbl'] == 'user_info':
        return reply_to_postback_update_user_info_sv.main(operating_mode, userInfo, data)
    if data['tar_tbl'] == 'working_record':
        return reply_to_postback_update_working_record_sv.main(operating_mode, userInfo, data)
    else:
        return lt_sv.get_a_text_send_message('よくわかんねぇデータを受け取ったぞ') 
