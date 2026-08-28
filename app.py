import gspread
from google.oauth2.service_account import Credentials

# =========================================================
# CONFIGURATION
# =========================================================

GOOGLE_SHEET_NAME = "car_parts"
SHEET1_NAME = "Sheet1"
SHEET2_NAME = "Sheet2"
SERVICE_ACCOUNT_FILE = "service_account.json"

# =========================================================
# GOOGLE SHEETS CONNECTION
# =========================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

client = gspread.authorize(credentials)

spreadsheet = client.open(GOOGLE_SHEET_NAME)

sheet1 = spreadsheet.worksheet(SHEET1_NAME)
sheet2 = spreadsheet.worksheet(SHEET2_NAME)

# =========================================================
# LOAD DATA FROM BOTH SHEETS
# =========================================================

parts_data = sheet1.get_all_records()
tires_data = sheet2.get_all_records()

print(f"Sheet1 records: {len(parts_data)}")
print(f"Sheet2 records: {len(tires_data)}")


# =========================================================
# SEARCH INVENTORY
# =========================================================

def search_inventory(search_text):

    search_text = search_text.lower().strip()

    results = []

    # -----------------------------------------------------
    # SEARCH SHEET1
    # -----------------------------------------------------

    for item in parts_data:

        searchable_text = " ".join(
            str(value) for value in item.values()
        ).lower()

        if search_text in searchable_text:

            results.append({
                "source": "Sheet1",
                "data": item
            })

    # -----------------------------------------------------
    # SEARCH SHEET2
    # -----------------------------------------------------

    for item in tires_data:

        searchable_text = " ".join(
            str(value) for value in item.values()
        ).lower()

        if search_text in searchable_text:

            results.append({
                "source": "Sheet2",
                "data": item
            })

    return results


# =========================================================
# FORMAT RESULT
# =========================================================

def format_results(results):

    if not results:
        return "Sorry, I couldn't find that item in our inventory."

    message = "Here are the matching items:\n\n"

    for result in results:

        source = result["source"]
        item = result["data"]

        message += f"📦 Source: {source}\n"

        # SKU
        if "SKU" in item:
            message += f"SKU: {item['SKU']}\n"

        # Brand
        if "Brand" in item:
            message += f"Brand: {item['Brand']}\n"

        # Tire Size
        if "Tire Size" in item:
            message += f"Tire Size: {item['Tire Size']}\n"

        # Product / Part Name
        if "Product Name" in item:
            message += f"Product: {item['Product Name']}\n"

        if "Part Name" in item:
            message += f"Part: {item['Part Name']}\n"

        # Quantity
        if "Quantity" in item:
            message += f"Quantity: {item['Quantity']}\n"

        # Price
        if "Price" in item:
            message += f"Price: ₱{item['Price']}\n"

        # Condition
        if "Condition" in item:
            message += f"Condition: {item['Condition']}\n"

        # Vehicle Compatibility
        if "Vehicle Compatibility" in item:
            message += (
                f"Vehicle Compatibility: "
                f"{item['Vehicle Compatibility']}\n"
            )

        # Description
        if "Description" in item:
            message += f"Description: {item['Description']}\n"

        message += "\n"

    return message


# =========================================================
# TEST SEARCH
# =========================================================

if __name__ == "__main__":

    print("\n===================================")
    print("CAR PARTS INVENTORY SEARCH")
    print("===================================\n")

    while True:

        search_text = input(
            "Enter product, tire size, brand, SKU, or vehicle "
            "(type 'exit' to quit): "
        )

        if search_text.lower() == "exit":
            break

        results = search_inventory(search_text)

        print("\n-----------------------------------")
        print(format_results(results))
        print("-----------------------------------\n")
