#!/usr/bin/env python3
import service.shared.line_tool_service as lt_sv
import service.shared.working_record_service as wr_sv
import common.constant as co

def main(operating_mode, userInfo, recieved_text):
    if wr_sv.get_a_working_record(
        userInfo, co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, co.PROCESS_STATUS_ON_RECORDING) != None:
        return lt_sv.get_a_text_send_message('今、作業中になってるぞ。')
    workingRecord = wr_sv.add_new_working_record(userInfo)
    if workingRecord == None:
        return lt_sv.get_a_text_send_message('作業レコード追加に失敗しました。')
    workingRecord = wr_sv.start_the_work(workingRecord)
    if workingRecord == None:
        return lt_sv.get_a_text_send_message('作業レコード開始更新に失敗しました。')
    return [
        lt_sv.get_a_text_send_message(
        '作業開始したんだな。\n'
        + '承ったぞ。'
        )
    ]