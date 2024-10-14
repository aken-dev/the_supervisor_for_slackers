#!/usr/bin/env python3
import json
import service.shared.line_tool_service as lt_sv

def get_standard_choices(postbacked_data, update_type=''):
    choice_range_min = (
        postbacked_data['tmp_val'] - 5 if 
        postbacked_data['tmp_val'] - 5 >= postbacked_data['min'] else postbacked_data['min']
    )
    choice_range_max = (
        choice_range_min + 10 if 
        choice_range_min + 10 <= postbacked_data['max'] else postbacked_data['max']
    )
    reply_buttons = [] if choice_range_min <= postbacked_data['min'] else [
        lt_sv.get_quick_reply_button_for_postback(
            '{} {} {}以下の選択肢を表示'.format(postbacked_data['uni_before_val'], choice_range_min -1, postbacked_data['uni_after_val']), 
            '{} {} {}以下の選択肢を表示'.format(postbacked_data['uni_before_val'], choice_range_min -1, postbacked_data['uni_after_val']), 
            json.dumps({
                "action": postbacked_data['action'],
                "type": postbacked_data['type'],
                "tar_tbl": postbacked_data['tar_tbl'],
                "tar_id": postbacked_data['tar_id'],
                "tar_el": postbacked_data['tar_el'],
                "tmp_val": (postbacked_data['min'] if choice_range_min - 5 <= postbacked_data['min'] else choice_range_min - 5),
                "min": postbacked_data['min'],
                "max": postbacked_data['max'],
                "cur_val": postbacked_data['cur_val'],
                "label": postbacked_data['label'],
                "uni_before_val": postbacked_data['uni_before_val'],
                "uni_after_val": postbacked_data['uni_after_val']
            })
        )
    ]
    for i in range(choice_range_min, choice_range_max + 1):
        reply_buttons.append(
            lt_sv.get_quick_reply_button_for_postback(
                '{} {} {}'.format(postbacked_data['uni_before_val'], i, postbacked_data['uni_after_val']), 
                '{}を {} {} {}  →  {} {} {} に変更'.format(
                    postbacked_data['label'], postbacked_data['uni_before_val'], postbacked_data['cur_val'], 
                    postbacked_data['uni_after_val'], postbacked_data['uni_before_val'], i, postbacked_data['uni_after_val']
                ), 
                json.dumps({
                    "action": "update",
                    "type": update_type,
                    "tar_tbl": postbacked_data['tar_tbl'],
                    "tar_id": postbacked_data['tar_id'],
                    "tar_el": postbacked_data['tar_el'],
                    "new_val": i,
                    "cur_val": postbacked_data['cur_val'],
                    "label": postbacked_data['label'],
                    "uni_before_val": postbacked_data['uni_before_val'],
                    "uni_after_val": postbacked_data['uni_after_val']
                })
            )
        )
    if choice_range_max < postbacked_data['max']:
        reply_buttons.append(
            lt_sv.get_quick_reply_button_for_postback(
                '{} {} {} 以上の選択肢を表示'.format(postbacked_data['uni_before_val'], choice_range_max +1, postbacked_data['uni_after_val']), 
                '{} {} {} 以上の選択肢を表示'.format(postbacked_data['uni_before_val'], choice_range_max +1, postbacked_data['uni_after_val']), 
                json.dumps({
                    "action": postbacked_data['action'],
                    "type": postbacked_data['type'],
                    "tar_tbl": postbacked_data['tar_tbl'],
                    "tar_id": postbacked_data['tar_id'],
                    "tar_el": postbacked_data['tar_el'],
                    "tmp_val": (postbacked_data['max'] if choice_range_max + 5 >= postbacked_data['max'] else choice_range_max + 5),
                    "min": postbacked_data['min'],
                    "max": postbacked_data['max'],
                    "cur_val": postbacked_data['cur_val'],
                    "label": postbacked_data['label'],
                    "uni_before_val": postbacked_data['uni_before_val'],
                    "uni_after_val": postbacked_data['uni_after_val']
                })
            )
        )
    return lt_sv.get_a_text_send_message_includes_quick_reply_buttons(
        '{}を変更\n   {} {} {} → 選択してくれ'.format(
            postbacked_data['label'], postbacked_data['uni_before_val'], postbacked_data['cur_val'], postbacked_data['uni_after_val']
        ),
        reply_buttons
    )
