import gspread
from google.oauth2.service_account import Credentials

# =========================================================
# CONFIGURATION
# =========================================================

GOOGLE_SHEET_NAME = "Reference"

SHEET1_NAME = "Sheet1"
SHEET2_NAME = "Sheet2"

SERVICE_ACCOUNT_FILE = "service_account.json"


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

print("Connected to Google Spreadsheet:", spreadsheet.title)


# =========================================================
# OPEN SHEET1
# =========================================================

try:
    sheet1 = spreadsheet.worksheet(SHEET1_NAME)
    print("✓ Sheet1 connected")

except Exception as e:
    print("❌ Could not open Sheet1")
    print(e)
    sheet1 = None


# =========================================================
# OPEN SHEET2
# =========================================================

try:
    sheet2 = spreadsheet.worksheet(SHEET2_NAME)
    print("✓ Sheet2 connected")

except Exception as e:
    print("❌ Could not open Sheet2")
    print(e)
    sheet2 = None


# =========================================================
# LOAD SHEET1 DATA
# =========================================================

sheet1_data = []

if sheet1:

    try:
        sheet1_data = sheet1.get_all_records()

        print(
            "✓ Sheet1 loaded:",
            len(sheet1_data),
            "records"
        )

    except Exception as e:

        print("❌ Error reading Sheet1")
        print(e)


# =========================================================
# LOAD SHEET2 DATA
# =========================================================

sheet2_data = []

if sheet2:

    try:
        sheet2_data = sheet2.get_all_records()

        print(
            "✓ Sheet2 loaded:",
            len(sheet2_data),
            "records"
        )

    except Exception as e:

        print("❌ Error reading Sheet2")
        print(e)


# =========================================================
# SHOW SHEET2 DATA
# =========================================================

print()
print("================================================")
print("TIRE INVENTORY FROM SHEET2")
print("================================================")

if len(sheet2_data) == 0:

    print("❌ Sheet2 contains no records.")

else:

    for row in sheet2_data:

        print(
            row.get("SKU", ""),
            "|",
            row.get("Brand", ""),
            "|",
            row.get("Tire Size", ""),
            "| Qty:",
            row.get("Quantity", ""),
            "| Price:",
            row.get("Price", "")
        )


# =========================================================
# SEARCH BOTH SHEETS
# =========================================================

def search_inventory(search_text):

    search_text = str(search_text).strip().lower()

    results = []

    if not search_text:
        return results


    # =====================================================
    # SEARCH SHEET1
    # =====================================================

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


    # =====================================================
    # SEARCH SHEET2
    # =====================================================

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

        print()
        print("❌ No matching inventory found.")
        return


    print()
    print("================================================")
    print("SEARCH RESULTS")
    print("================================================")


    for number, result in enumerate(results, start=1):

        item = result["data"]

        print()
        print("RESULT", number)
        print("Source:", result["sheet"])

        # SKU
        if "SKU" in item:
            print("SKU:", item["SKU"])

        # Brand
        if "Brand" in item:
            print("Brand:", item["Brand"])

        # Tire Size
        if "Tire Size" in item:
            print("Tire Size:", item["Tire Size"])

        # Tire Type
        if "Tire Type" in item:
            print("Tire Type:", item["Tire Type"])

        # Quantity
        if "Quantity" in item:
            print("Quantity:", item["Quantity"])

        # Price
        if "Price" in item:
            print("Price: ₱", item["Price"])

        # Condition
        if "Condition" in item:
            print("Condition:", item["Condition"])

        # Vehicle
        if "Vehicle Compatibility" in item:
            print(
                "Vehicle:",
                item["Vehicle Compatibility"]
            )

        # Description
        if "Description" in item:
            print(
                "Description:",
                item["Description"]
            )

        print("--------------------------------------------")


# =========================================================
# SEARCH LOOP
# =========================================================

print()
print("================================================")
print("INVENTORY SEARCH READY")
print("================================================")

print()
print("You can search using:")
print("- Brand       Example: Max")
print("- Tire size   Example: 225/45R17")
print("- SKU         Example: T001")
print("- Vehicle     Example: Toyota Corolla")
print("- Product     Example: Michelin")
print()
print("Type 'exit' to close the program.")
print()


while True:

    search_text = input("Search: ")

    if search_text.strip().lower() == "exit":

        print("Program closed.")
        break

    results = search_inventory(search_text)

    display_results(results)
