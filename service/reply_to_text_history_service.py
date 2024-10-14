#!/usr/bin/env python3
import service.shared.working_record_service as wr_sv

def main(operating_mode, userInfo, recieved_text):
    return wr_sv.display_working_history_main(userInfo)