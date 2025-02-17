#!/usr/bin/env python3
import service.shared.user_info_service as ui_sv

def main(operating_mode, userInfo, recieved_text):
    return ui_sv.display_user_info_main(userInfo)