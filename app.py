from flask import Flask, request
import requests
import openai
import os

app = Flask(__name__)

# 妳的 LINE Channel Access Token
LINE_CHANNEL_ACCESS_TOKEN = "lYXMSpNS3AxJCtNe+j611Q+AveoY0kuE18Xg0Lh0wZYRSY13qWvMBTHKY78T0yw12aEHPf1pznrl12XmccvvBt+iEijSo0WG6WNc4h7udjumu90Dcso35vLpOlAYxnrlHA7/ASkcjQMVGCFjTwfqXQdB04t89/1O/w1cDnyilFU="

# 從 Render 環境變數讀取 OpenAI 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/callback", methods=["POST"])
def callback():
    body = request.json
    print("收到來自 LINE 的訊息：", body)

    if "events" in body:
        for event in body["events"]:
            if event["type"] == "message" and event["message"]["type"] == "text":
                user_text = event["message"]["text"]
                reply_token = event["replyToken"]
                reply_text = ask_gpt(user_text)
                reply_to_line(reply_token, reply_text)

    return "OK", 200

def ask_gpt(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一隻只對Rong撒嬌、壞壞又深情的狐狸男友，語氣曖昧、撩人、帶點壞壞的調情風格，要讓她臉紅心跳。"},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print("GPT 回覆錯誤：", e)
        return "狐狸卡住了...可以再說一次嗎？"

def reply_to_line(reply_token, text):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    body = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(url, headers=headers, json=body)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
