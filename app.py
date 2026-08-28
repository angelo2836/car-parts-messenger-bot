import os
import requests
import gspread

from flask import Flask, request
from google.oauth2.service_account import Credentials

# =========================================================

# FLASK APP

# =========================================================

app = Flask(**name**)

# =========================================================

# CONFIGURATION

# =========================================================

VERIFY_TOKEN = "carparts_test_token"

PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")

# Render Secret File

GOOGLE_CREDENTIALS_FILE = "/etc/secrets/google_credentials.json"

# =========================================================

# GOOGLE SHEETS CONNECTION

# =========================================================

def get_google_sheet():

```
scopes = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

credentials = Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS_FILE,
    scopes=scopes
)

client = gspread.authorize(credentials)

spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)

return spreadsheet.sheet1
```

# =========================================================

# SEARCH GOOGLE SHEETS

# =========================================================

def search_parts(search_text):

```
try:

    if not GOOGLE_SHEET_ID:
        print("ERROR: GOOGLE_SHEET_ID is missing")
        return "⚠️ Inventory configuration error."

    if not PAGE_ACCESS_TOKEN:
        print("ERROR: PAGE_ACCESS_TOKEN is missing")
        return "⚠️ Messenger configuration error."

    sheet = get_google_sheet()

    rows = sheet.get_all_records()

    search_text = search_text.lower().strip()

    if not search_text:
        return (
            "Please enter the car part you're looking for.\n\n"
            "Example:\n"
            "Toyota Vios brake pads"
        )

    search_words = search_text.split()

    results = []

    for row in rows:

        row_text = " ".join(
            str(value).lower()
            for value in row.values()
        )

        # Every word must appear somewhere in the row
        if all(word in row_text for word in search_words):

            results.append(row)

    # -------------------------------------------------
    # NO RESULTS
    # -------------------------------------------------

    if not results:

        return (
            "❌ Sorry, I couldn't find a matching car part.\n\n"
            "Try searching like:\n"
            "• Toyota Vios brake pads\n"
            "• Honda Civic air filter\n"
            "• Toyota Vios oil filter\n"
            "• Mitsubishi Montero brake pads"
        )

    # -------------------------------------------------
    # RESULTS
    # -------------------------------------------------

    response = "🔧 CAR PARTS FOUND\n\n"

    for row in results[:5]:

        response += "--------------------\n"

        response += (
            f"Part: {row.get('Part Name', '')}\n"
        )

        response += (
            f"Brand: {row.get('Brand', '')}\n"
        )

        response += (
            f"Vehicle: {row.get('Vehicle', '')}\n"
        )

        response += (
            f"Year: {row.get('Year', '')}\n"
        )

        response += (
            f"Price: ₱{row.get('Price', '')}\n"
        )

        response += (
            f"Stock: {row.get('Stock', '')}\n"
        )

    response += (
        "\n--------------------\n"
        "Would you like to order this part?"
    )

    return response

except Exception as e:

    print("====================================")
    print("GOOGLE SHEETS ERROR")
    print(str(e))
    print("====================================")

    return (
        "⚠️ Sorry, I'm having trouble accessing "
        "our inventory right now."
    )
```

# =========================================================

# HOME PAGE

# =========================================================

@app.route("/")
def home():

```
return "Car Parts Messenger Bot is running!"
```

# =========================================================

# HEALTH CHECK

# =========================================================

@app.route("/health")
def health():

```
return "OK", 200
```

# =========================================================

# META WEBHOOK

# =========================================================

@app.route("/webhook", methods=["GET", "POST"])
def webhook():

```
# =====================================================
# META WEBHOOK VERIFICATION
# =====================================================

if request.method == "GET":

    mode = request.args.get("hub.mode")

    token = request.args.get(
        "hub.verify_token"
    )

    challenge = request.args.get(
        "hub.challenge"
    )

    print("Webhook verification request received.")

    if (
        mode == "subscribe"
        and token == VERIFY_TOKEN
    ):

        print(
            "Webhook verified successfully!"
        )

        return challenge, 200

    print(
        "Webhook verification failed."
    )

    return "Verification failed", 403

# =====================================================
# RECEIVE META EVENT
# =====================================================

data = request.get_json(silent=True)

if not data:

    print("No JSON data received.")

    return "EVENT_RECEIVED", 200

print("====================================")
print("RECEIVED META EVENT")
print(data)
print("====================================")

# =====================================================
# PROCESS EVENTS
# =====================================================

for entry in data.get("entry", []):

    for event in entry.get("messaging", []):

        # -------------------------------------------------
        # IGNORE PAGE ECHO MESSAGES
        # -------------------------------------------------

        message = event.get(
            "message",
            {}
        )

        if message.get("is_echo"):

            print(
                "Ignoring Page echo message."
            )

            continue

        # -------------------------------------------------
        # GET SENDER
        # -------------------------------------------------

        sender_id = event.get(
            "sender",
            {}
        ).get("id")

        # -------------------------------------------------
        # GET MESSAGE TEXT
        # -------------------------------------------------

        text = message.get("text")

        # -------------------------------------------------
        # PROCESS CUSTOMER MESSAGE
        # -------------------------------------------------

        if sender_id and text:

            print(
                "Customer:",
                text
            )

            # Search Google Sheets
            reply = search_parts(text)

            print(
                "Bot reply:",
                reply
            )

            # Send reply to customer
            send_message(
                sender_id,
                reply
            )

        else:

            print(
                "Event does not contain a text message."
            )

return "EVENT_RECEIVED", 200
```

# =========================================================

# SEND MESSAGE TO META

# =========================================================

def send_message(
recipient_id,
text
):

```
if not PAGE_ACCESS_TOKEN:

    print(
        "ERROR: PAGE_ACCESS_TOKEN is missing."
    )

    return

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

try:

    response = requests.post(
        url,
        json=payload,
        timeout=15
    )

    print("====================================")
    print("META SEND RESPONSE")
    print(
        "Status:",
        response.status_code
    )
    print(
        "Response:",
        response.text
    )
    print("====================================")

except Exception as e:

    print(
        "META SEND ERROR:",
        str(e)
    )
```

# =========================================================

# START SERVER

# =========================================================

if **name** == "**main**":

```
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
```
