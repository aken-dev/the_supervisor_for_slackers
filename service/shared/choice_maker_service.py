#!/usr/bin/env python3
import json
import service.shared.line_tool_service as lt_sv

def get_standard_choices(postbacked_data, label, update_type, update_target):
    choice_range_min = (
        postbacked_data['tmp_value'] - 5 if 
        postbacked_data['tmp_value'] - 5 >= postbacked_data['min'] else postbacked_data['min']
    )
    choice_range_max = (
        choice_range_min + 10 if 
        choice_range_min + 10 <= postbacked_data['max'] else postbacked_data['max']
    )
    reply_buttons = [] if choice_range_min <= postbacked_data['min'] else [
        lt_sv.get_quick_reply_button_for_postback(
            '# {} 以下の選択肢を表示'.format(choice_range_min -1), 
            '# {} 以下の選択肢を表示'.format(choice_range_min -1), 
            json.dumps({
                "action": postbacked_data['action'],
                "type": postbacked_data['type'],
                "target": postbacked_data['target'],
                "tmp_value": (postbacked_data['min'] if choice_range_min - 5 <= postbacked_data['min'] else choice_range_min - 5),
                "min": postbacked_data['min'],
                "max": postbacked_data['max'],
                "current_value": postbacked_data['current_value']
            })
        )
    ]
    for i in range(choice_range_min, choice_range_max + 1):
        reply_buttons.append(
            lt_sv.get_quick_reply_button_for_postback(
                '# {}'.format(i), 
                '{}を[ {} ] → [ {} ]に変更'.format(label, postbacked_data['current_value'], i), 
                json.dumps({
                    "action": "update",
                    "type": update_type,
                    "target": update_target,
                    "new_value": i,
                    "current_value": postbacked_data['current_value']
                })
            )           
        )
    if choice_range_max < postbacked_data['max']:
        reply_buttons.append(
            lt_sv.get_quick_reply_button_for_postback(
                '# {} 以上の選択肢を表示'.format(choice_range_max +1), 
                '# {} 以上の選択肢を表示'.format(choice_range_max +1), 
                json.dumps({
                    "action": postbacked_data['action'],
                    "type": postbacked_data['type'],
                    "target": postbacked_data['target'],
                    "tmp_value": (postbacked_data['max'] if choice_range_max + 5 >= postbacked_data['max'] else choice_range_max + 5),
                    "min": postbacked_data['min'],
                    "max": postbacked_data['max'],
                    "current_value": postbacked_data['current_value']
                })
            )
        )
    return lt_sv.get_a_text_send_message_includes_quick_reply_buttons(
        '{}を変更\n   # {} → 選択してくれ'.format(label, postbacked_data['current_value']),
        reply_buttons
    )