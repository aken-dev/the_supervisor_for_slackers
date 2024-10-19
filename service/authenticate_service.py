#!/usr/bin/env python3
import json
import common.constant as co
import service.shared.line_tool_service as lt_sv
import service.shared.terms_of_use_service as tou_sv
import service.shared.user_info_service as ui_sv

# Authentication
def main(operating_mode, line_user_id, line_name, postback_data=None):
    me = ui_sv.get_user_info(line_user_id, line_name)
    userInfo = me['userInfo']
    if userInfo == None:
        print('Cannot get UserInfo : {} : {}'.format(line_user_id, line_name))
        return {
            "userInfo": None,
            "msg": None
        }
    elif userInfo.standby_status == co.STATUS_ON_BATCH_PROCESS:
        print('UserInfoバッチ処理中のアクセス : {} : {}'.format(line_user_id, line_name))
        return {
            "userInfo": userInfo,
            "msg": lt_sv.get_a_text_send_message('只今メンテナンス中です。しばらくしてから再度お試しください。')
        }
    elif userInfo.standby_status == co.STATUS_BATCH_PROCESSED_FAILURE:
        print('UserInfo(バッチ異常終了)のアクセス : {} : {}'.format(line_user_id, line_name))
        return {
            "userInfo": userInfo,
            "msg": lt_sv.get_a_text_send_message('ユーザ情報データに異常があります。管理者までお問い合わせください。')
        }
    elif userInfo.allowed == co.USER_ALLOWED:
        return {
            "userInfo": userInfo,
            "msg": None
        }
    elif userInfo.allowed == co.USER_BANNED:
        print('禁止ユーザのアクセス : {} : {}'.format(line_user_id, line_name))
        return {
            "userInfo": userInfo,
            "msg": lt_sv.get_a_text_send_message('利用を禁止されています。')
        }
    elif postback_data != None:
        if postback_data['action'] == 'display' and postback_data['type'] == 'agreement':
            return {
                "userInfo": userInfo,
                "msg": tou_sv.get_terms_of_use_with_agreement_buttons()
            }
        elif postback_data['action'] == 'agreement' and postback_data['value'] == 'agree':
            if userInfo.allowed == co.USER_UNREGISTERED:
                new_user_flag = True 
            else:
                new_user_flag = False
            print('規約同意：{} : {}'.format(line_user_id, line_name))
            me = ui_sv.change_user_allowed(userInfo, co.USER_ALLOWED)
            if me['count'] > 0:
                return {
                    "userInfo": me['userInfo'],
                    "msg": ui_sv.display_user_info_main(me['userInfo'], new_user_flag)
                }
            else:    
                return {
                    "userInfo": userInfo,
                    "msg": lt_sv.get_a_text_send_message('ユーザ情報の更新に失敗しました。暫く経ってから再度お試しください。')
                }                
        elif postback_data['action'] == 'agreement' and postback_data['value'] == 'disagree':
            print('規約不同意：{} : {}'.format(line_user_id, line_name))
            return {
                "userInfo": userInfo,
                "msg": lt_sv.get_a_text_send_message('またのご利用をお待ちしております。')
            }
    elif operating_mode == co.OPERATING_MODE_REFUSE_ALL_USERS_EXCEPT_ALLOWED_USERS:
        if userInfo.allowed == co.USER_UNALLOWED:
            print('未許可ユーザのアクセス : {} : {}'.format(line_user_id, line_name))
            return {
                "userInfo": userInfo,
                "msg": lt_sv.get_a_text_send_message('利用を許可されていません。')
            }
        elif userInfo.allowed == co.USER_UNREGISTERED:
            print('未登録ユーザのアクセス : {} : {}'.format(line_user_id, line_name))
            return {
                "userInfo": userInfo,
                "msg": lt_sv.get_a_text_send_message('登録を許可されていません。') 
            }       
    elif operating_mode == co.OPERATING_MODE_APPROVE_ALL_USERS_EXCEPT_BANNED_USERS:
        if userInfo.allowed == co.USER_UNALLOWED:
            print('未許可ユーザのアクセス : {} : {}'.format(line_user_id, line_name))
            return {
                "userInfo": userInfo,
                "msg": tou_sv.get_terms_of_use_with_agreement_buttons()
            }
        elif userInfo.allowed == co.USER_UNREGISTERED:
            agreement_display_button = lt_sv.get_quick_reply_button_for_postback(
                '利用規約を表示する',
                '利用規約を表示',
                json.dumps({
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
            return {
                "userInfo": userInfo,
                "msg": lt_sv.get_a_text_send_message_includes_quick_reply_buttons(
                    reply_text, agreement_display_button
                )
            }
