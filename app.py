import gspread
from google.oauth2.service_account import Credentials

# =========================================================
# CONFIGURATION
# =========================================================

GOOGLE_SHEET_NAME = "car_parts"
SERVICE_ACCOUNT_FILE = "service_account.json"

SHEET1_NAME = "Sheet1"
SHEET2_NAME = "Sheet2"


# =========================================================
# CONNECT TO GOOGLE SHEETS
# =========================================================

print("Connecting to Google Sheets...")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

client = gspread.authorize(credentials)

spreadsheet = client.open(GOOGLE_SHEET_NAME)

print("Connected to:", GOOGLE_SHEET_NAME)


# =========================================================
# OPEN SHEET1 AND SHEET2
# =========================================================

try:
    sheet1 = spreadsheet.worksheet(SHEET1_NAME)
    print("✓ Sheet1 found:", sheet1.title)
except Exception as e:
    print("✗ Cannot open Sheet1")
    print(e)
    sheet1 = None


try:
    sheet2 = spreadsheet.worksheet(SHEET2_NAME)
    print("✓ Sheet2 found:", sheet2.title)
except Exception as e:
    print("✗ Cannot open Sheet2")
    print(e)
    sheet2 = None


# =========================================================
# LOAD DATA
# =========================================================

sheet1_data = []
sheet2_data = []

if sheet1:
    try:
        sheet1_data = sheet1.get_all_records()
        print("✓ Sheet1 rows:", len(sheet1_data))
    except Exception as e:
        print("✗ Error reading Sheet1:")
        print(e)


if sheet2:
    try:
        sheet2_data = sheet2.get_all_records()
        print("✓ Sheet2 rows:", len(sheet2_data))
    except Exception as e:
        print("✗ Error reading Sheet2:")
        print(e)


# =========================================================
# SHOW SHEET2 DATA
# =========================================================

print("\n========================================")
print("SHEET2 / TIRE INVENTORY")
print("========================================")

if sheet2_data:

    for row in sheet2_data:
        print(row)

else:

    print("No data found in Sheet2.")


# =========================================================
# SEARCH INVENTORY
# =========================================================

def search_inventory(search_text):

    search_text = str(search_text).strip().lower()

    results = []

    if not search_text:
        return results

    # -----------------------------------------------------
    # SEARCH SHEET1
    # -----------------------------------------------------

    for row in sheet1_data:

        row_text = " ".join(
            str(value).lower()
            for value in row.values()
        )

        if search_text in row_text:

            results.append({
                "sheet": "Sheet1",
                "data": row
            })


    # -----------------------------------------------------
    # SEARCH SHEET2
    # -----------------------------------------------------

    for row in sheet2_data:

        row_text = " ".join(
            str(value).lower()
            for value in row.values()
        )

        if search_text in row_text:

            results.append({
                "sheet": "Sheet2",
                "data": row
            })


    return results


# =========================================================
# DISPLAY RESULTS
# =========================================================

def display_results(results):

    if not results:

        print("\n❌ NO MATCH FOUND")
        return


    print("\n========================================")
    print("MATCHING INVENTORY")
    print("========================================")


    for number, result in enumerate(results, start=1):

        print(f"\nRESULT {number}")
        print("Source:", result["sheet"])

        item = result["data"]

        # Print every column
        for key, value in item.items():

            print(f"{key}: {value}")

        print("----------------------------------------")


# =========================================================
# TEST SEARCH
# =========================================================

print("\n========================================")
print("INVENTORY SEARCH READY")
print("========================================")

print("""
Examples:

Max
Maxxis
225/45R17
Michelin
Toyota Corolla
T001

Type 'exit' to close.
""")


while True:

    search_text = input("\nSearch: ")

    if search_text.lower().strip() == "exit":

        print("Program closed.")
        break


    results = search_inventory(search_text)

    display_results(results)
