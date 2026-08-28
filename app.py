import os
import requests
import pandas as pd
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "carparts_test_token"
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")

EXCEL_FILE = "car_parts.xlsx"


# Load car parts from Excel
def load_parts():
    try:
        df = pd.read_excel(EXCEL_FILE)

        # Convert all columns to text
        df = df.fillna("")

        return df

    except Exception as e:
        print("Excel loading error:", e)
        return pd.DataFrame()


# Search the Excel file
def search_parts(search_text):

    df = load_parts()

    if df.empty:
        return "Sorry, our car-parts database is currently unavailable."

    search_text = search_text.lower()

    results = []

    for _, row in df.iterrows():

        row_text = " ".join(str(value).lower() for value in row.values)

        if search_text in row_text:
            results.append(row)

    if not results:
        return (
            "Sorry, I couldn't find a matching car part. "
            "Please send the vehicle brand, model, year, or part name."
        )

    response = "🔧 Car Parts Found:\n\n"

    for row in results[:5]:

        response += "--------------------\n"

        for column in df.columns:
            value = row[column]

            if str(value).strip():
                response += f"{column}: {value}\n"

    return response


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

                print("Customer:", text)

                # Search Excel database
                reply = search_parts(text)

                # Send result back to Messenger
                send_message(sender_id, reply)

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

    print(
        "Send response:",
        response.status_code,
        response.text
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
