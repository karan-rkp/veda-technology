
# ==========================================
# JSON DATA PROCESSOR
# Python Programming Track - Task 21
# ==========================================

import json


# ------------------------------------------
# LOAD JSON FILE
# ------------------------------------------
def load_json(filename):

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Error: JSON must contain a list of records.")
            return None

        # Keep only dictionary records
        records = [item for item in data if isinstance(item, dict)]

        if len(records) != len(data):
            print("Warning: Some invalid records were skipped.")

        return records

    except FileNotFoundError:
        print(f"Error: File '{filename}' was not found.")

    except json.JSONDecodeError as error:
        print(f"Error: Invalid JSON format. {error}")

    except PermissionError:
        print("Error: Permission denied while reading the file.")

    except OSError as error:
        print(f"File error: {error}")

    return None


# ------------------------------------------
# DISPLAY RECORDS
# ------------------------------------------
def display_records(records):

    if not records:
        print("\nNo records found.")
        return

    print(f"\nFound {len(records)} record(s):")
    print("-" * 45)

    for index, record in enumerate(records, start=1):
        print(f"\nRecord {index}")

        for key, value in record.items():
            print(f"  {key.title():15}: {value}")

    print("-" * 45)


# ------------------------------------------
# SEARCH RECORDS
# ------------------------------------------
def search_records(records):

    keyword = input("Enter search keyword: ").strip().lower()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    results = []

    for record in records:
        if any(
            keyword in str(value).lower()
            for value in record.values()
            if value is not None
        ):
            results.append(record)

    display_records(results)


# ------------------------------------------
# FILTER RECORDS BY NUMERIC VALUE
# ------------------------------------------
def filter_records(records):

    field = input(
        "Enter numeric field (example: age, marks, salary): "
    ).strip()

    if not field:
        print("Field name cannot be empty.")
        return

    try:
        minimum = float(input("Enter minimum value: "))
    except ValueError:
        print("Error: Please enter a valid numeric value.")
        return

    results = []

    for record in records:
        try:
            value = float(record[field])

            if value >= minimum:
                results.append(record)

        except (KeyError, TypeError, ValueError):
            continue

    print(f"\nRecords where {field} >= {minimum:g}:")
    display_records(results)


# ------------------------------------------
# GENERATE SUMMARY
# ------------------------------------------
def generate_summary(records):

    print("\n========== JSON DATA SUMMARY ==========")

    print(f"Total records: {len(records)}")

    if not records:
        print("No data available for summary.")
        return

    # Display available fields
    fields = sorted({
        key
        for record in records
        for key in record.keys()
    })

    print("Available fields:", ", ".join(fields))

    # Calculate statistics for numeric fields
    for field in fields:

        values = []

        for record in records:
            try:
                value = record[field]

                # Avoid counting booleans as numbers
                if isinstance(value, bool) or value is None:
                    continue

                if isinstance(value, str) and not value.strip():
                    continue

                values.append(float(value))

            except (KeyError, TypeError, ValueError):
                continue

        if values:
            print(f"\nField: {field}")
            print(f"  Count   : {len(values)}")
            print(f"  Total   : {sum(values):,.2f}")
            print(f"  Average : {sum(values) / len(values):,.2f}")
            print(f"  Highest : {max(values):,.2f}")
            print(f"  Lowest  : {min(values):,.2f}")


# ------------------------------------------
# SAVE FILTERED RESULTS
# ------------------------------------------
def save_results(records):

    filename = input(
        "Enter output filename (example: results.json): "
    ).strip()

    if not filename:
        print("Filename cannot be empty.")
        return

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4, ensure_ascii=False)

        print(f"Results saved successfully to '{filename}'.")

    except (OSError, TypeError, ValueError) as error:
        print(f"Error saving JSON: {error}")


# ------------------------------------------
# MAIN MENU
# ------------------------------------------
def main():

    filename = input(
        "Enter JSON filename (example: students.json): "
    ).strip()

    if not filename:
        print("Filename cannot be empty.")
        return

    records = load_json(filename)

    if records is None:
        return

    print(f"\nSuccessfully loaded {len(records)} record(s).")

    while True:

        print("\n" + "=" * 40)
        print("          JSON DATA PROCESSOR")
        print("=" * 40)
        print("1. Display All Records")
        print("2. Search Records")
        print("3. Filter Numeric Records")
        print("4. Generate Summary")
        print("5. Save All Records to JSON")
        print("6. Reload JSON File")
        print("7. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            display_records(records)

        elif choice == "2":
            search_records(records)

        elif choice == "3":
            filter_records(records)

        elif choice == "4":
            generate_summary(records)

        elif choice == "5":
            save_results(records)

        elif choice == "6":
            updated_records = load_json(filename)

            if updated_records is not None:
                records = updated_records
                print("JSON file reloaded successfully.")

        elif choice == "7":
            print("Thank you for using JSON Data Processor!")
            break

        else:
            print("Invalid choice. Please select 1-7.")


# ------------------------------------------
# START PROGRAM
# ------------------------------------------
if __name__ == "__main__":
    main()
