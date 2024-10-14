#!/usr/bin/env python3
import service.shared.working_record_service as wr_sv
import service.shared.line_tool_service as lt_sv
import service.shared.datetime_calc_service as dc_sv

def main(operating_mode, userInfo, postbacked_data):
    # 更新対象のレコード取得
    workingRecord = wr_sv.get_a_working_record_by_record_id(postbacked_data['tar_id'])
    # DBレコード更新処理
    workingRecord = wr_sv.update_working_record(
        workingRecord,
        postbacked_data['tar_el'], 
        postbacked_data['new_val'] if postbacked_data['postbackedDateType'] == 'not_date' 
        else postbacked_data['postbackedDateValue']
    )
    if workingRecord == None:
        return lt_sv.get_a_text_send_message('ユーザ情報の更新に失敗しました。')
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
        