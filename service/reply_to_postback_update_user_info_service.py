#!/usr/bin/env python3
import common.constant as co
import json
import datetime
import service.shared.line_tool_service as lt_sv
import service.shared.user_info_service as ui_sv
import service.shared.working_record_service as wr_sv
import service.shared.datetime_calc_service as dc_sv
import service.shared.choice_maker_service as cm_sv

def main(operating_mode, userInfo, postbacked_data):
    # 課題番号を変更する場合は、直近の課題番号変更日を同時に更新する
    if postbacked_data['tar_el'] == 'current_stage':
        me = ui_sv.update_user_info(
            userInfo, 
            'recent_stage_changed_date', 
            datetime.date.today(),
            userInfo.updated_datetime,
            'update_user_info_tmp'
        )
        if me['count'] > 0: 
            userInfo = me['userInfo']
        else:    
            return lt_sv.get_a_text_send_message('ユーザ情報の前更新に失敗しました。')
    # 日付起算時刻を変更する場合は、WorkingRecord適正化バッチの適用を予約する
    elif postbacked_data['tar_el'] == 'starting_time_of_a_day':
        me = ui_sv.update_user_info(
            userInfo, 
            'standby_status', 
            co.STANDBY_STATUS_WAITING_BATCH_PROCESS_RECALCULATE,
            userInfo.updated_datetime,
            'update_user_info_tmp'
        )
        if me['count'] > 0: 
            userInfo = me['userInfo']
        else:    
            return lt_sv.get_a_text_send_message('ユーザ情報の前更新に失敗しました。')
        wr_sv.reserve_batch_recalculate(userInfo)
    ## DBレコード更新処理
    me = ui_sv.update_user_info(
        userInfo, 
        postbacked_data['tar_el'], 
        postbacked_data['new_val'] if postbacked_data['postbackedDateType'] == 'not_date' 
        else postbacked_data['postbackedDateValue']
    )
    if me['count'] > 0:
        userInfo = me['userInfo']
    else: 
        return lt_sv.get_a_text_send_message('ユーザ情報の更新に失敗しました。')
    ## 以下、返信テキストを作成する
    # リマインド種別を変更した場合
    if postbacked_data['tar_el'] == 'stage_change_remind_type':
        msg_instance = [
            lt_sv.get_a_text_send_message(
                '[変更完了]\n'
                + ' {}\n'.format(postbacked_data['label'])
                + '    {}\n'.format(
                    'リマインドしない' if postbacked_data['cur_val'] == co.STAGE_CHANGE_REMIND_TYPE_NOTHING else (
                        '曜日ごとにリマインド' if postbacked_data['cur_val'] == co.STAGE_CHANGE_REMIND_TYPE_DAY_OF_WEEK else (
                            '番号変更からの日数経過でリマインド'if postbacked_data['cur_val'] == co.STAGE_CHANGE_REMIND_TYPE_DAYS else '設定なし'
                        )
                    )
                )
                + '         → {}'.format(
                    'リマインドしない' if postbacked_data['new_val'] == co.STAGE_CHANGE_REMIND_TYPE_NOTHING else (
                        '曜日ごとにリマインド' if postbacked_data['new_val'] == co.STAGE_CHANGE_REMIND_TYPE_DAY_OF_WEEK else (
                            '番号変更からの日数経過でリマインド'if postbacked_data['new_val'] == co.STAGE_CHANGE_REMIND_TYPE_DAYS else '設定なし'
                        )
                    )
                )
            )
        ]
        if postbacked_data['new_val'] == co.STAGE_CHANGE_REMIND_TYPE_DAY_OF_WEEK:
            quick_reply_btns = []
            for i in range(0, 6 + 1):
                quick_reply_btns.append(
                    lt_sv.get_quick_reply_button_for_postback(
                        '{}'.format(co.WEEKDAY[i]), 
                        '（毎週）{}にリマインド'.format(co.WEEKDAY[i]), 
                        json.dumps({
                            "action": "update",
                            "type": "",
                            "tar_tbl": "user_info",
                            "tar_id": "",
                            "tar_el": "stage_change_remind_value",
                            "new_val": i,
                            "cur_val": '',
                            "label": '（毎週）{}にリマインド'.format(co.WEEKDAY[i]),
                            "uni_before_val": "",
                            "uni_after_val": ""
                        })
                    )
                )
            msg_instance.append(
                lt_sv.get_a_text_send_message_includes_quick_reply_buttons(
                    '何曜日にリマインドする？', quick_reply_btns
                )
            )
        elif postbacked_data['new_val'] == co.STAGE_CHANGE_REMIND_TYPE_DAYS:
            new_data = {
                "action": "display",
                "type": "choices",
                "tar_tbl": "user_info",
                "tar_id": "",
                "tar_el": "stage_change_remind_value",
                "tmp_val": 5,
                "min": 1,
                "max": 100,
                "cur_val": "( )",
                "label": "日数間隔",
                "uni_before_val": "変更の",
                "uni_after_val": "日後"
            }
            msg_instance.append(cm_sv.get_standard_choices(new_data))
        return msg_instance
    # リマインドする曜日を変更した場合
    elif userInfo.stage_change_remind_type == co.STAGE_CHANGE_REMIND_TYPE_DAY_OF_WEEK \
        and postbacked_data['tar_el'] == 'stage_change_remind_value':
            return lt_sv.get_a_text_send_message(
                '[変更完了]\n'
                + '    → {}'.format(postbacked_data['label'])
            )
    # datetime関連のパラメータ変更の場合
    elif postbacked_data['postbackedDateType'] != 'not_date':
        return lt_sv.get_a_text_send_message(
            '[変更完了]\n'
            + ' {}\n'.format(postbacked_data['label'])
            + '    {}\n'.format(
                '' if postbacked_data['cur_val'] == '' else (
                    dc_sv.get_datetime_from_string(
                        postbacked_data['cur_val'], postbacked_data['postbackedDateType']
                    )
                )
            )
            + '         → {}'.format(postbacked_data['postbackedDateValue'])
        )
    # 一般のパラメータ変更の場合
    else:
        return lt_sv.get_a_text_send_message(
            '[変更完了]\n'
            + ' {}\n'.format(postbacked_data['label'])
            + '    {} {} {}\n'.format(
                postbacked_data['uni_before_val'], postbacked_data['cur_val'], postbacked_data['uni_after_val']
            )
            + '         → {} {} {}'.format(
                postbacked_data['uni_before_val'], postbacked_data['new_val'], postbacked_data['uni_after_val']
            )
        )
        