#!/usr/bin/env python3
import common.constant as co
import json
import service.shared.line_tool_service as lt_sv
import service.shared.user_info_service as ui_sv
import service.shared.datetime_calc_service as datetime_calc_sv
import service.shared.choice_maker_service as cm_sv

def main(operating_mode, userInfo, postbacked_data):
    # DBレコード更新処理
    userInfo = ui_sv.update_user_info(
        userInfo, 
        postbacked_data['target_element'], 
        postbacked_data['new_value'] if postbacked_data['postbackedDateType'] == 'nothing' 
        else postbacked_data['postbackedDateValue']
    )
    if userInfo == None:
        return lt_sv.get_a_text_send_message('ユーザ情報の更新に失敗しました。')
    ## 以下、返信テキストを作成する
    # リマインド種別を変更した場合
    elif postbacked_data['target_element'] == 'stage_change_remind_type':
        msg_instance = [
            lt_sv.get_a_text_send_message(
                '[変更完了]\n'
                + ' {}\n'.format(postbacked_data['label'])
                + '    {}\n'.format(
                    'リマインドしない' if postbacked_data['current_value'] == co.STAGE_CHANGE_REMIND_TYPE_NOTHING else (
                        '曜日ごとにリマインド' if postbacked_data['current_value'] == co.STAGE_CHANGE_REMIND_TYPE_DAY_OF_WEEK else (
                            '番号変更からの日数経過でリマインド'if postbacked_data['current_value'] == co.STAGE_CHANGE_REMIND_TYPE_DAYS else '設定なし'
                        )
                    )
                )
                + '         → {}'.format(
                    'リマインドしない' if postbacked_data['new_value'] == co.STAGE_CHANGE_REMIND_TYPE_NOTHING else (
                        '曜日ごとにリマインド' if postbacked_data['new_value'] == co.STAGE_CHANGE_REMIND_TYPE_DAY_OF_WEEK else (
                            '番号変更からの日数経過でリマインド'if postbacked_data['new_value'] == co.STAGE_CHANGE_REMIND_TYPE_DAYS else '設定なし'
                        )
                    )
                )
            )
        ]
        if postbacked_data['new_value'] == co.STAGE_CHANGE_REMIND_TYPE_DAY_OF_WEEK:
            quick_reply_btns = []
            for i in range(0, 6 + 1):
                day_label = co.WEEKDAY[i]
                quick_reply_btns.append(
                    lt_sv.get_quick_reply_button_for_postback(
                        '{}'.format(day_label), 
                        '（毎週）{}にリマインド'.format(day_label), 
                        json.dumps({
                            "action": "update",
                            "type": "",
                            "target_table": "user_info",
                            "target_element": "stage_change_remind_value",
                            "new_value": i,
                            "current_value": '',
                            "label": '（毎週）{}にリマインド'.format(day_label),
                            "unit_before_value": "",
                            "unit_after_value": ""
                        })
                    )
                )
            msg_instance.append(
                lt_sv.get_a_text_send_message_includes_quick_reply_buttons(
                    '何曜日にリマインドする？', quick_reply_btns
                )
            )
        elif postbacked_data['new_value'] == co.STAGE_CHANGE_REMIND_TYPE_DAYS:
            new_data = {
                "action": "display",
                "type": "choices",
                "target_table": "user_info",
                "target_element": "stage_change_remind_value",
                "tmp_value": 5,
                "min": 1,
                "max": 100,
                "current_value": "(未設定)",
                "label": "間隔",
                "unit_before_value": "変更の",
                "unit_after_value": "日後"
            }
            msg_instance.append(cm_sv.get_standard_choices(new_data))
        return msg_instance
    # リマインドする曜日を変更した場合
    elif userInfo.stage_change_remind_type == co.STAGE_CHANGE_REMIND_TYPE_DAY_OF_WEEK \
    and postbacked_data['target_element'] == 'stage_change_remind_value':
        return lt_sv.get_a_text_send_message(
            '[変更完了]\n'
            + '    → {}'.format(postbacked_data['label'])
        )
    # datetime関連のパラメータ変更の場合
    elif postbacked_data['postbackedDateType'] != 'nothing':
        return lt_sv.get_a_text_send_message(
            '[変更完了]\n'
            + ' {}\n'.format(postbacked_data['label'])
            + '    {}\n'.format(
                datetime_calc_sv.get_datetime_from_string(
                    postbacked_data['current_value'], postbacked_data['postbackedDateType']
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
                postbacked_data['unit_before_value'], postbacked_data['current_value'], postbacked_data['unit_after_value']
            )
            + '         → {} {} {}'.format(
                postbacked_data['unit_before_value'], postbacked_data['new_value'], postbacked_data['unit_after_value']
            )
        )
        