#!/usr/bin/env python3
import service.shared.line_tool_service as lt_sv
import service.reply_to_postback_display_choices_current_stage_service as current_stage_sv
import service.reply_to_postback_display_choices_required_working_hours_service as required_working_hours_sv
import service.reply_to_postback_display_choices_starting_time_of_a_day_service as starting_time_of_a_day_sv
import service.reply_to_postback_display_choices_the_last_stage_service as the_last_stage_sv
import service.reply_to_postback_display_display_terms_of_use_service as terms_of_use_sv

def action(operating_mode, userInfo, data):
    if data['type'] == 'choices':
        if data['target'] == 'current_stage':
            return current_stage_sv.main(operating_mode, userInfo, data)
        elif data['target'] == 'required_working_hours':
            return required_working_hours_sv.main(operating_mode, userInfo, data)
        elif data['target'] == 'starting_time_of_a_day':
            return starting_time_of_a_day_sv.main(operating_mode, userInfo, data)
        elif data['target'] == 'the_last_stage':
            return the_last_stage_sv.main(operating_mode, userInfo, data)
        else:
            return lt_sv.get_a_text_send_message('よくわかんねぇデータを受け取ったぞ') 
    elif data['type'] == 'display':
        if data['target'] == 'terms_of_use':
            return terms_of_use_sv.main(operating_mode, userInfo, data)
        else:
            return lt_sv.get_a_text_send_message('よくわかんねぇデータを受け取ったぞ')
    else:
        return lt_sv.get_a_text_send_message('よくわかんねぇデータを受け取ったぞ')
    