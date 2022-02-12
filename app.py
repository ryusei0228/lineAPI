from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os
import requests
import pprint

app=Flask(__name__)
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api=LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers["X-Line-Signature"]

    body=request.get_data(as_text=True)
    app.logger.info("Request body"+body)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    rec_text = event.message.text

    rep_text = talkapi_response(rec_text)

    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=rep_text))

def talkapi_response(text):
    Talk_api = "https://api.a3rt.recruit.co.jp/talk/v1/smalltalk"
    apikey = os.environ["TALK_API_KEY"]
    data = {"apikey": apikey, "query": text}
    response = requests.post(Talk_api, data = data)
    return response.json()['results'][0]['reply']

if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)
