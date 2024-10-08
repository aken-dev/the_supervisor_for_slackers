#!/usr/bin/env python3
import service.reply_to_simple_text_message_service as reply_to_simple_text_message_sv

def action(operating_mode, userInfo, recieved_text):
    return reply_to_simple_text_message_sv.main(operating_mode, userInfo, recieved_text)