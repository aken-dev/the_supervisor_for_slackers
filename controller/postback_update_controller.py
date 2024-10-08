#!/usr/bin/env python3
import os
import service.reply_to_postbacked_message_service as reply_to_postbacked_message_sv

def action(operating_mode, userInfo, data):
    return reply_to_postbacked_message_sv.main(operating_mode, userInfo, data)