#!/usr/bin/env python3
import service.shared.line_tool_service as lt_sv
import service.reply_to_postback_display_choices_user_info_service as reply_to_postback_display_choices_user_info_sv
import service.reply_to_postback_display_display_terms_of_use_service as terms_of_use_sv
import service.reply_to_postback_display_working_history_service as reply_to_postback_display_working_history_sv
import service.reply_to_postback_display_choices_working_record_service as reply_to_postback_display_choices_working_record_sv

def action(operating_mode, userInfo, data):
    if data['type'] == 'choices':
        if data['tar_tbl'] == 'user_info':
            return reply_to_postback_display_choices_user_info_sv.main(operating_mode, userInfo, data)
        elif data['tar_tbl'] == 'working_record':
            return reply_to_postback_display_choices_working_record_sv.main(operating_mode, userInfo, data)
        else:
            return lt_sv.get_a_text_send_message('よくわかんねぇデータを受け取ったぞ') 
    elif data['type'] == 'display':
        if data['target'] == 'terms_of_use':
            return terms_of_use_sv.main(operating_mode, userInfo, data)
        else:
            return lt_sv.get_a_text_send_message('よくわかんねぇデータを受け取ったぞ')
    elif data['type'] == 'working_history':
        return reply_to_postback_display_working_history_sv.main(operating_mode, userInfo, data)       
    else:
        return lt_sv.get_a_text_send_message('よくわかんねぇデータを受け取ったぞ')
    