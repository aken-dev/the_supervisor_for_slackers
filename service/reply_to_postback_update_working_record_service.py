#!/usr/bin/env python3
import datetime
import common.constant as co
import service.shared.user_info_service as ui_sv
import service.shared.working_record_service as wr_sv
import service.shared.line_tool_service as lt_sv
import service.shared.datetime_calc_service as dc_sv

def main(operating_mode, userInfo, postbacked_data):
    # 更新対象のレコード取得
    target_record = wr_sv.get_a_working_record_by_record_id(postbacked_data['tar_id'])
    if target_record['count'] > 0:
        workingRecord = target_record['workingRecord']
    else:
        lt_sv.get_a_text_send_message('更新対象のレコード取得に失敗しました。')
    # DBレコード更新処理
    updated = wr_sv.update_working_record(
        workingRecord,
        postbacked_data['tar_el'], 
        postbacked_data['new_val'] if postbacked_data['postbackedDateType'] == 'not_date' 
        else postbacked_data['postbackedDateValue']
    )
    if updated['count'] <= 0:
        return lt_sv.get_a_text_send_message('更新対象レコードの更新に失敗しました。')
    else:
        workingRecord = updated['workingRecord']
        # 変更する要素がstart_timeかfinish_timeの場合、再計算バッチを予約する
        if postbacked_data['tar_el'] == 'start_time' or postbacked_data['tar_el'] == 'finish_time':
            # working_recordの予約
            reserve_recalc_wr_result = wr_sv.update_working_record(
            workingRecord,
            'standby_status', 
            co.STANDBY_STATUS_WAITING_BATCH_PROCESS_RECALCULATE,
            datetime.datetime.now(),
            'update_working_record_from_postback'
            )
            if reserve_recalc_wr_result['count'] <= 0:
                return lt_sv.get_a_text_send_message('workingRecordの再計算予約に失敗しました。')
            else:
                # user_infoの再計算予約
                reserve_recalc_ui_result = ui_sv.update_user_info(
                    userInfo,
                    'standby_status', 
                    co.STANDBY_STATUS_WAITING_BATCH_PROCESS_RECALCULATE,
                    datetime.datetime.now(),
                    'update_working_record_from_postback'
                )
                if reserve_recalc_ui_result['count'] <= 0:
                    return lt_sv.get_a_text_send_message('userInfoの再計算予約に失敗しました。')
                
    ## 以下、返信テキストを作成する
    return lt_sv.get_a_text_send_message(
        '[変更完了]\n'
        + ' {}\n'.format(postbacked_data['label'])
        + '    {} {} {}\n'.format(
            postbacked_data['uni_before_val'], 
            dc_sv.get_datetime_from_string(postbacked_data['cur_val']) if postbacked_data['new_val'] == 'datetime' else 
                postbacked_data['cur_val'], 
            postbacked_data['uni_after_val']
        )
        + '         → {} {} {}'.format(
            postbacked_data['uni_before_val'], 
            postbacked_data['new_val'] if postbacked_data['postbackedDateType'] == 'not_date' else 
                postbacked_data['postbackedDateValue'], 
            postbacked_data['uni_after_val']
        )
    )
        