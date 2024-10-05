#!/usr/bin/env python3
import os
import service.reply_to_simple_text_message_service as rs_sv
def action(event, line_name):
    operating_mode = int(os.getenv('SV_SLACKERS_APP_OPERATING_MODE', None))
    return rs_sv.reply_to_message_postbacked(operating_mode, event, line_name)