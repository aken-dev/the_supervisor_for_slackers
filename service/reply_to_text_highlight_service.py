#!/usr/bin/env python3
import service.shared.line_tool_service as lt_sv
import service.shared.working_record_service as wr_sv

def main(operating_mode, userInfo, recieved_text):
    return wr_sv.display_highlight_main(userInfo)