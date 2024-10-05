#!/usr/bin/env python3
import json
import service.shared.line_tool_service as lt_sv
import repository.terms_of_use_repository as tu_rp

def get_terms_of_use():
    result_count, result = tu_rp.terms_of_use_select()
    if result_count == 0 or result == None:
        return None
    msg_instances = []
    msg_instances.append(lt_sv.get_a_text_send_message(
        '【利用規約（{} 改訂）】'.format(result['enforced'])
    ))
    msg_instances.append(lt_sv.get_a_text_send_message(result['text1']))
    if result['text2'] != None:
        msg_instances.append(lt_sv.get_a_text_send_message(result['text2']))
    if result['text3'] != None:
        msg_instances.append(lt_sv.get_a_text_send_message(result['text3']))
    return msg_instances

def get_terms_of_use_with_agreement_buttons():
    msg_instances = get_terms_of_use()
    agreement_buttons = []
    agreement_buttons.append(
        lt_sv.get_quick_reply_button_for_postback(
            '同意する', \
            '利用規約に同意します。', \
            json.dumps({
                "action": "agreement",
                "value": "agree"
                })
        )
    )
    agreement_buttons.append(
        lt_sv.get_quick_reply_button_for_postback(
            '同意しない', \
            '利用規約に同意しません。', \
            json.dumps({
                "action": "agreement",
                "value": "disagree"
                })
        )
    )
    msg_instances.append(
        lt_sv.get_a_text_send_message_includes_quick_reply_buttons(
            '利用規約に同意しますか？', agreement_buttons
        )
    )
    return msg_instances