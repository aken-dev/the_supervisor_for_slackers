#!/usr/bin/env python3
import service.shared.terms_of_use_service as tou_sv

def main(operating_mode, userInfo, postbacked_data):
    return tou_sv.get_terms_of_use()
