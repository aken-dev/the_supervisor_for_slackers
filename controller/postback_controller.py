#!/usr/bin/env python3
import os
import service.reply_to_postbacked_message_service as rp_sv
def action(event, line_name):
    operating_mode = int(os.getenv('SV_SLACKERS_APP_OPERATING_MODE', None))
    return rp_sv.reply_to_message_postbacked(operating_mode, event, line_name)