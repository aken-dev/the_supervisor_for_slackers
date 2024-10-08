#!/usr/bin/env python3
import json
import datetime
from linebot.models import PostbackAction, QuickReplyButton, MessageAction, QuickReply, TextSendMessage

#シンプルなテキストメッセージを作成
def get_a_text_send_message(text):
    return TextSendMessage(text) #ユーザーに送られる1通のテキスト

#クイックリプライボタンを含むメッセージを作成
def get_a_text_send_message_includes_quick_reply_buttons(text, quick_reply_buttons):
    if isinstance(quick_reply_buttons, list): #クイックリプライボタンを引数からList（複数）で受け取った場合
        return TextSendMessage(text=text, #ユーザーに送られる1通のテキスト
                               quick_reply=QuickReply(items=quick_reply_buttons)) #テキストに付随するクイックリプライボタン
    else: #クイックリプライボタンを1つだけ引数で受け取った場合
        return TextSendMessage(text=text, #ユーザーに送られる1通のテキスト
                               quick_reply=QuickReply(items=[quick_reply_buttons])) #テキストに付随するクイックリプライボタン

#クイックリプライボタン作成（シンプルテキスト用）
def get_quick_reply_button(lavel_text, body_text):
    return QuickReplyButton(action=MessageAction(
        label=f"{lavel_text}", #ボタンの見出し
        text=f"{body_text}")) #ユーザーがボタンを押すと送られるテキスト

#クイックリプライボタン作成（ポストバック用）
def get_quick_reply_button_for_postback(lavel_text, display_text, data):
    return QuickReplyButton(action=PostbackAction(
        label=f"{lavel_text}", #ボタンの見出し
        display_text=f"{display_text}", #ユーザーがボタンを押すと送られるテキスト
        data=f"{data}")) #ユーザーがボタンを押すと裏で送られるテキスト

#クイックリプライボタン作成（ポストバック用日付選択アクション）
def get_quick_reply_button_for_postback_datetime(lavel_text, data, mode='datetime', initial='', max='', min=''):
    return QuickReplyButton(action={
  "type": "datetimepicker",
  "label": f"{lavel_text}", #ボタンの見出し
  "data": f"{data}", #ユーザーの選択した日時のほか、ボタンを押すと裏で送られるテキスト
  "mode": f"{mode}", #選択肢（date=日付のみ，datetime=日時）
  "initial": f"{initial}", #初期値
  "max": f"{max}", #最大値
  "min": f"{min}" #最小値
})#日時はdatetime.strftime("%Y-%m-%dt%H:%M")で指定

#Postbackで受け取ったjsonを辞書型で返却
def get_postbacked_data(event):
    data = json.loads(event.postback.data)
    if ('params' in str(event.postback)):
        if('date' in event.postback.params):
            data['postbackedDateType'] = 'date'
            data['postbackedDateValue'] = datetime.datetime.strptime(event.postback.params['date'], '%Y-%m-%d').date()
        elif('time' in event.postback.params):
            data['postbackedDateType'] = 'time'
            data['postbackedDateValue'] = datetime.datetime.strptime('20200101{}'.format(event.postback.params['time']), '%H:%M').time()
        elif('datetime' in event.postback.params):
            data['postbackedDateType'] = 'datetime'
            data['postbackedDateValue'] = datetime.datetime.strptime(event.postback.params['datetime'], '%Y-%m-%dT%H:%M')
    else:
        data['postbackedDateType'] = 'nothing'
    return data