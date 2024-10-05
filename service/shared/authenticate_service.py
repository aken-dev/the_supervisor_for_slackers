#!/usr/bin/env python3
import json
import common.constant as co
import line_tool_service as lt_sv
import terms_of_use_service as tou_sv
import user_info_service as ui_sv

# Authentication
def get_authentication(operating_mode, line_user_id, line_name, postback_data=None):
    userInfo = ui_sv.get_user_info(line_user_id, line_name)
    if userInfo == None:
        print('Cannot get UserInfo : {} : {}'.format(line_user_id, line_name))
        return None, None
    elif userInfo.standby_status == co.STATUS_ON_BATCH_PROCESS:
        print('UserInfoバッチ処理中のアクセス : {} : {}'.format(line_user_id, line_name))
        return userInfo, lt_sv.get_a_text_send_message('只今メンテナンス中です。しばらくしてから再度お試しください。')
    elif userInfo.allowed == co.USER_ALLOWED:
        return userInfo, None
    elif userInfo.allowed == co.USER_BANNED:
        print('禁止ユーザのアクセス : {} : {}'.format(line_user_id, line_name))
        return userInfo, lt_sv.get_a_text_send_message('利用を禁止されています。')
    elif postback_data != None:
        if postback_data['action'] == 'display' and postback_data['type'] == 'agreement':
            return userInfo, tou_sv.get_terms_of_use_with_agreement_buttons()
        elif postback_data['action'] == 'agreement' and postback_data['value'] == 'agree':
            if userInfo.allowed == co.USER_UNREGISTERED:
                new_user_flag = True 
            else:
                new_user_flag = False
            userInfo = ui_sv.change_user_allowed(userInfo, co.USER_ALLOWED)
            print('規約同意：{} : {}'.format(line_user_id, line_name))
            return userInfo, ui_sv.display_user_info(userInfo, new_user_flag)
        elif postback_data['action'] == 'agreement' and postback_data['value'] == 'disagree':
            print('規約不同意：{} : {}'.format(line_user_id, line_name))
            return userInfo, lt_sv.get_a_text_send_message('またのご利用をお待ちしております。')
    elif operating_mode == co.OPERATING_MODE_REFUSE_ALL_USERS_EXCEPT_ALLOWED_USERS:
        if userInfo.allowed == co.USER_UNALLOWED:
            print('未許可ユーザのアクセス : {} : {}'.format(line_user_id, line_name))
            return userInfo, lt_sv.get_a_text_send_message('利用を許可されていません。')
        elif userInfo.allowed == co.USER_UNREGISTERED:
            print('未登録ユーザのアクセス : {} : {}'.format(line_user_id, line_name))
            return userInfo, lt_sv.get_a_text_send_message('登録を許可されていません。')        
    elif operating_mode == co.OPERATING_MODE_APPROVE_ALL_USERS_EXCEPT_BANNED_USERS:
        if userInfo.allowed == co.USER_UNALLOWED:
            print('未許可ユーザのアクセス : {} : {}'.format(line_user_id, line_name))
            return userInfo, tou_sv.get_terms_of_use_with_agreement_buttons()
        elif userInfo.allowed == co.USER_UNREGISTERED:
            agreement_display_button = lt_sv.get_quick_reply_button_for_postback(
                '利用規約を表示する', '利用規約を表示', json.dumps({
                "action": "display",
                "type": "agreement"
                })
            )
            reply_text = '友達追加ありがとうございます。\n' \
                         'このアプリは勉強やトレーニングなどのシンドイ作業を日々継続できるようサポートします。\n' \
                         '使い方はめっちゃ簡単。\n' \
                         '作業開始時には「開始」ボタン、終了時には「終了」ボタンを押すだけです。\n\n' \
                         '利用規約に同意していただくことで、すぐに利用開始できます。'
            print('新規ユーザのアクセス : {} : {}'.format(line_user_id, line_name))
            return userInfo, lt_sv.get_a_text_send_message_includes_quick_reply_buttons(reply_text, agreement_display_button)
