#!/usr/bin/env python3
import os
import service.reply_to_new_follower_service as rtnf_sv

def action(event, line_name):
    operating_mode = int(os.getenv('SV_SLACKERS_APP_OPERATING_MODE', None))
    return rtnf_sv.get_a_reply_to_new_follower(operating_mode, event, line_name)
