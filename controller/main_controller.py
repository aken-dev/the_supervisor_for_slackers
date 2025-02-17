#!/usr/bin/env python3
import sys
import os
from flask import request, abort, Blueprint
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent, PostbackEvent, MessageEvent, TextMessage
import controller.simple_text_controller
import controller.postback_main_controller
import controller.follow_event_controller

# LINEチャンネルシークレットとチャンネルアクセストークンの登録と確認
channel_secret = os.getenv('SV_SLACKERS_LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('SV_SLACKERS_LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
# 運用モードの登録確認
operating_mode = int(os.getenv('SV_SLACKERS_APP_OPERATING_MODE', None))
if operating_mode is None:
    print('Specify operating_mode as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

cb = Blueprint('cb', __name__)
@cb.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 通常のテキストメッセージを受信した場合の処理
@handler.add(MessageEvent, message=TextMessage)
def handle_getting_text_message(event):
    line_name = line_bot_api.get_profile(event.source.user_id).display_name
    reply_instance = controller.simple_text_controller.action(event, line_name)
    line_bot_api.reply_message(event.reply_token, reply_instance)

# ボタンの入力を受け取るPostbackEvent処理
@handler.add(PostbackEvent)
def handle_getting_on_postback(event):
    line_name = line_bot_api.get_profile(event.source.user_id).display_name
    reply_instance = controller.postback_main_controller.action(event, line_name)
    line_bot_api.reply_message(event.reply_token, reply_instance)

# 新規ユーザーにフォローされた場合の処理
@handler.add(FollowEvent)
def handle_getting_followed(event):
    line_name = line_bot_api.get_profile(event.source.user_id).display_name
    reply_instance = controller.follow_event_controller.action(event, line_name)
    line_bot_api.reply_message(event.reply_token, reply_instance)