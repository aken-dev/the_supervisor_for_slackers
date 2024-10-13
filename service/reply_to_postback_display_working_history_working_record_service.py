#!/usr/bin/env python3
import service.shared.working_record_service as wr_sv
import service.shared.datetime_calc_service as dc_sv

def main(operating_mode, userInfo, postbacked_data):
    return wr_sv.display_working_history_main(
        userInfo, 
        dc_sv.get_datetime_from_string(postbacked_data['target'], 'dt_with_sec')
    )