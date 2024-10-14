#!/usr/bin/env python3
import json
import service.shared.line_tool_service as lt_sv
import repository.terms_of_use_repository as tu_rp

def get_terms_of_use():
    terms_of_use = tu_rp.terms_of_use_select()
    if terms_of_use['count'] == 0 or terms_of_use['result'] == None: return None
    msg_instances = [
        lt_sv.get_a_text_send_message(
            '【利用規約（{} 改訂）】'.format(terms_of_use['result']['enforced'])
        ),
        lt_sv.get_a_text_send_message(terms_of_use['result']['text1'])
    ]
    if terms_of_use['result']['text2'] != None:
        msg_instances.append(lt_sv.get_a_text_send_message(terms_of_use['result']['text2']))
    if terms_of_use['result']['text3'] != None:
        msg_instances.append(lt_sv.get_a_text_send_message(terms_of_use['result']['text3']))
    return msg_instances

def get_terms_of_use_with_agreement_buttons():
    msg_instances = get_terms_of_use()
    msg_instances.append(
        lt_sv.get_a_text_send_message_includes_quick_reply_buttons(
            '利用規約に同意しますか？',
            [
                lt_sv.get_quick_reply_button_for_postback(
                    '同意する', \
                    '利用規約に同意します。', \
                    json.dumps({
                        "action": "agreement",
                        "value": "agree"
                    })
                ),
                lt_sv.get_quick_reply_button_for_postback(
                    '同意しない', \
                    '利用規約に同意しません。', \
                    json.dumps({
                        "action": "agreement",
                        "value": "disagree"
                    })
                )
            ]
        )
    )
    return msg_instances