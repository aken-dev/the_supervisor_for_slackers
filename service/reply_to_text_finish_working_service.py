#!/usr/bin/env python3
import service.shared.line_tool_service as lt_sv
import service.shared.working_record_service as wr_sv
import service.shared.user_info_service as ui_sv
import common.constant as co

def main(operating_mode, userInfo, recieved_text):
    pre_chk = wr_sv.get_a_working_record_by_status(
        userInfo, co.PROCESS_CATEGORY_RECORD_WORKING_HOURS, co.PROCESS_STATUS_ON_RECORDING
    )
    if pre_chk['count'] < 1: return lt_sv.get_a_text_send_message('今、何も作業してない事になってるぞ。')
    finished = wr_sv.finish_the_work(userInfo)
    if finished['count'] > 0:
        workingRecord = finished['workingRecord']
        msg_instance = [
            lt_sv.get_a_text_send_message(
            '[# {} ]の作業が終わったんだな。\n'.format(workingRecord.stage)
            + '承ったぞ。'
            )
        ]
        msg_instance.extend(
            wr_sv.display_highlight_main(userInfo, ui_sv.is_remind_needed(userInfo))
        )
        return msg_instance        
    else:
        return lt_sv.get_a_text_send_message('すまん、暫く経ってから再度試してくれ。')
