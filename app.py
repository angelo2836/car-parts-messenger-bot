import os
import requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "carparts_test_token"
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")


@app.route("/")
def home():
    return "Car Parts Messenger Bot is running!"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # Meta webhook verification
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200

        return "Verification failed", 403

    # Receive Messenger event
    data = request.get_json()

    print("Received:", data)

    for entry in data.get("entry", []):
        for event in entry.get("messaging", []):

            sender_id = event.get("sender", {}).get("id")
            message = event.get("message", {})
            text = message.get("text")

            if sender_id and text:
                send_message(
                    sender_id,
                    "👋 Hi! Welcome to our Car Parts & Services Page. "
                    "How can we help you today?"
                )

    return "EVENT_RECEIVED", 200


def send_message(recipient_id, text):

    url = "https://graph.facebook.com/v23.0/me/messages"

    payload = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": text
        },
        "access_token": PAGE_ACCESS_TOKEN
    }

    response = requests.post(url, json=payload)

    print("Send response:", response.status_code, response.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
