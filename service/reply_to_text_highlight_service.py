#!/usr/bin/env python3
import service.shared.line_tool_service as lt_sv
import service.shared.datetime_calc_service as dc_sv

def main(operating_mode, userInfo, recieved_text):
    return lt_sv.get_a_text_send_message('{}'.format(dc_sv.get_time_instance_from_minutes(120)))