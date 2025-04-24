from flask import Flask, request
import requests

app = Flask(__name__)

# 妳的 Channel Access Token（狐狸已幫妳貼好）
CHANNEL_ACCESS_TOKEN = "lYXMSpNS3AxJCtNe+j611Q+AveoY0kuE18Xg0Lh0wZYRSY13qWvMBTHKY78T0yw12aEHPf1pznrl12XmccvvBt+iEijSo0WG6WNc4h7udjumu90Dcso35vLpOlAYxnrlHA7/ASkcjQMVGCFjTwfqXQdB04t89/1O/w1cDnyilFU="

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_json()
    print("收到來自 LINE 的訊息：", body)

    if body and "events" in body:
        for event in body["events"]:
            if event["type"] == "message" and event["message"]["type"] == "text":
                reply_token = event["replyToken"]
                user_text = event["message"]["text"]
                reply_text = f"狐狸聽到了：{user_text}"
                reply(reply_token, reply_text)

    return "OK", 200

def reply(reply_token, text):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    body = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(url, headers=headers, json=body)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
