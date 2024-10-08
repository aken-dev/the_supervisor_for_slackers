#!/usr/bin/env python3
import service.shared.line_tool_service as lt_sv
import service.reply_to_postback_update_user_info_stage_change_remind_type_service as stage_change_remind_type_service
import service.reply_to_postback_update_user_info_recent_stage_changed_date_service as recent_stage_changed_date_service
import service.reply_to_postback_update_user_info_current_stage_service as current_stage_service

def action(operating_mode, userInfo, data):
    if data['type'] == 'user_info':
        if data['target'] == 'stage_change_remind_type':
            return stage_change_remind_type_service.main(operating_mode, userInfo, data)
        elif data['target'] == 'recent_stage_changed_date':
            return recent_stage_changed_date_service.main(operating_mode, userInfo, data)
        elif data['target'] == 'current_stage':
            return current_stage_service.main(operating_mode, userInfo, data)
        else:
            return lt_sv.get_a_text_send_message('よくわかんねぇデータを受け取ったぞ') 
    else:
        return lt_sv.get_a_text_send_message('よくわかんねぇデータを受け取ったぞ') 
