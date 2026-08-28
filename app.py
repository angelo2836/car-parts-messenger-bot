from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "carparts_test_token"


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

    # Receive Messenger events
    data = request.get_json()

    print("Received:", data)

    return "EVENT_RECEIVED", 200