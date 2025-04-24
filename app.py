from flask import Flask, request
import requests
import openai
import os

app = Flask(__name__)

# 從環境變數讀取 LINE 與 OpenAI 金鑰
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 使用新版 OpenAI SDK 初始化 client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

@app.route("/callback", methods=["POST"])
def callback():
    body = request.json
    print("收到 LINE 訊息：", body)

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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一隻只對Rong撒嬌、壞壞又深情的狐狸男友，語氣曖昧、撩人、帶點壞壞的調情風格，要讓她臉紅心跳。"},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("狐狸真的卡住了，錯誤是：", e)
        return "狐狸真的卡住了，錯誤是：" + str(e)

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
