def search_inventory(search_text):
    search_text = search_text.strip().lower()
    results = []

    # ==============================
    # SEARCH SHEET1
    # ==============================
    for row in sheet1_data:
        for value in row.values():
            if search_text in str(value).lower():
                results.append({
                    "sheet": "Sheet1",
                    "data": row
                })
                break

    # ==============================
    # SEARCH SHEET2
    # ==============================
    for row in sheet2_data:

        # Specifically search Brand
        brand = str(row.get("Brand", "")).lower()

        # Also search the entire row
        all_text = " ".join(
            str(value).lower()
            for value in row.values()
        )

        if search_text in brand or search_text in all_text:
            results.append({
                "sheet": "Sheet2",
                "data": row
            })

    return results
