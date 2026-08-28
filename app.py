import gspread
from google.oauth2.service_account import Credentials

# ==============================
# CONFIG
# ==============================

GOOGLE_SHEET_NAME = "car_parts"
SERVICE_ACCOUNT_FILE = "service_account.json"

# ==============================
# CONNECT TO GOOGLE SHEETS
# ==============================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

client = gspread.authorize(credentials)

spreadsheet = client.open(GOOGLE_SHEET_NAME)

# ==============================
# OPEN BOTH SHEETS
# ==============================

sheet1 = spreadsheet.worksheet("Sheet1")
sheet2 = spreadsheet.worksheet("Sheet2")

# ==============================
# READ BOTH SHEETS
# ==============================

sheet1_data = sheet1.get_all_records()
sheet2_data = sheet2.get_all_records()

print("Sheet1 rows:", len(sheet1_data))
print("Sheet2 rows:", len(sheet2_data))

# ==============================
# SEARCH BOTH SHEETS
# ==============================

def search_inventory(search_text):

    search_text = search_text.lower().strip()

    results = []

    # Search Sheet1
    for row in sheet1_data:

        text = " ".join(
            str(value).lower()
            for value in row.values()
        )

        if search_text in text:
            results.append({
                "sheet": "Sheet1",
                "data": row
            })

    # Search Sheet2
    for row in sheet2_data:

        text = " ".join(
            str(value).lower()
            for value in row.values()
        )

        if search_text in text:
            results.append({
                "sheet": "Sheet2",
                "data": row
            })

    return results


# ==============================
# DISPLAY RESULTS
# ==============================

def display_results(results):

    if not results:
        print("\n❌ No matching inventory found.")
        return

    print("\n✅ MATCHING INVENTORY:\n")

    for result in results:

        print("Source:", result["sheet"])

        for key, value in result["data"].items():
            print(f"{key}: {value}")

        print("-----------------------------")


# ==============================
# TEST
# ==============================

while True:

    search = input(
        "\nSearch inventory "
        "(type exit to quit): "
    )

    if search.lower() == "exit":
        break

    results = search_inventory(search)

    display_results(results)
