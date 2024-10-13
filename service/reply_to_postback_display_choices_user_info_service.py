#!/usr/bin/env python3
import service.shared.choice_maker_service as cm_sv

def main(operating_mode, userInfo, postbacked_data):
    return cm_sv.get_user_info_choices(postbacked_data)