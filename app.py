import os
import requests
import gspread

from flask import Flask, request
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# =========================================================
# CONFIGURATION
# =========================================================

VERIFY_TOKEN = "carparts_test_token"

PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")

GOOGLE_CREDENTIALS_FILE = "google_credentials.json"


# =========================================================
# GOOGLE SHEETS CONNECTION
# =========================================================

def get_google_sheet():

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly"
    ]

    credentials = Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_FILE,
        scopes=scopes
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)

    sheet = spreadsheet.sheet1

    return sheet


# =========================================================
# SEARCH GOOGLE SHEETS
# =========================================================

def search_parts(search_text):

    try:

        sheet = get_google_sheet()

        rows = sheet.get_all_records()

        search_text = search_text.lower().strip()

        search_words = search_text.split()

        results = []

        for row in rows:

            row_text = " ".join(
                str(value).lower()
                for value in row.values()
            )

            if all(
                word in row_text
                for word in search_words
            ):
                results.append(row)

        if not results:

            return (
                "❌ Sorry, I couldn't find a matching car part.\n\n"
                "Please try something like:\n"
                "• Toyota Vios brake pads\n"
                "• Honda Civic air filter\n"
                "• Toyota Vios oil filter"
            )

        response = "🔧 Car Parts Found:\n\n"

        for row in results[:5]:

            response += "--------------------\n"

            response += f"Part: {row.get('Part Name', '')}\n"
            response += f"Brand: {row.get('Brand', '')}\n"
            response += f"Vehicle: {row.get('Vehicle', '')}\n"
            response += f"Year: {row.get('Year', '')}\n"
            response += f"Price: ₱{row.get('Price', '')}\n"
            response += f"Stock: {row.get('Stock', '')}\n"

        response += (
            "\nWould you like to order this part?"
        )

        return response

    except Exception as e:

        print("Google Sheets error:", e)

        return (
            "⚠️ Sorry, I'm having trouble accessing "
            "our inventory right now."
        )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return "Car Parts Messenger Bot is running!"


# =========================================================
# META WEBHOOK
# =========================================================

@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # -----------------------------------------
    # META WEBHOOK VERIFICATION
    # -----------------------------------------

    if request.method == "GET":

        mode = request.args.get("hub.mode")

        token = request.args.get(
            "hub.verify_token"
        )

        challenge = request.args.get(
            "hub.challenge"
        )

        if (
            mode == "subscribe"
            and token == VERIFY_TOKEN
        ):

            print(
                "Webhook verified successfully!"
            )

            return challenge, 200

        return "Verification failed", 403


    # -----------------------------------------
    # RECEIVE MESSENGER EVENT
    # -----------------------------------------

    data = request.get_json()

    print("Received:", data)

    for entry in data.get("entry", []):

        for event in entry.get("messaging", []):

            # Ignore messages sent by the Page itself
            if event.get("message", {}).get("is_echo"):

                continue

            sender_id = event.get(
                "sender", {}
            ).get("id")

            message = event.get(
                "message", {}
            )

            text = message.get("text")


            if sender_id and text:

                print(
                    "Customer message:",
                    text
                )

                reply = search_parts(text)

                send_message(
                    sender_id,
                    reply
                )

    return "EVENT_RECEIVED", 200


# =========================================================
# SEND MESSAGE TO FACEBOOK
# =========================================================

def send_message(
    recipient_id,
    text
):

    url = (
        "https://graph.facebook.com/"
        "v23.0/me/messages"
    )

    payload = {

        "recipient": {
            "id": recipient_id
        },

        "message": {
            "text": text
        },

        "access_token": PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        url,
        json=payload
    )

    print(
        "Send response:",
        response.status_code,
        response.text
    )


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
