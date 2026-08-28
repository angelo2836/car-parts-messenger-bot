def search_parts(search_text):

    try:

        print("Connecting to Google Sheets...")
        print("Spreadsheet ID:", GOOGLE_SHEET_ID)

        sheet = get_google_sheet()

        print("Google Sheet connected successfully!")

        rows = sheet.get_all_records()

        print("Rows loaded:", len(rows))

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

        print("Matching results:", len(results))

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

        response += "\nWould you like to order this part?"

        return response

    except Exception as e:

        print("================================")
        print("GOOGLE SHEETS ERROR:")
        print(repr(e))
        print("================================")

        return (
            "⚠️ Sorry, I'm having trouble accessing "
            "our inventory right now."
        )
