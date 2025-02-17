#!/usr/bin/env python3
import service.shared.working_record_service as wr_sv
import service.shared.user_info_service as ui_sv

def main(operating_mode, userInfo, recieved_text):
    return wr_sv.display_highlight_main(userInfo, ui_sv.is_remind_needed(userInfo))