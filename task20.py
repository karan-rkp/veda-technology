
# ==========================================
# CSV DATA PROCESSOR
# Python Programming Track - Task 20
# ==========================================

import csv


# ------------------------------------------
# READ AND PROCESS CSV FILE
# ------------------------------------------
def process_csv(filename, value_column):

    records = []
    valid_values = []
    skipped_rows = 0

    try:
        with open(filename, "r", newline="", encoding="utf-8-sig") as file:

            reader = csv.DictReader(file)

            # Validate CSV headers
            if not reader.fieldnames:
                print("Error: CSV file is empty or has no headers.")
                return

            if value_column not in reader.fieldnames:
                print(f"Error: Column '{value_column}' not found.")
                print("Available columns:", ", ".join(reader.fieldnames))
                return

            # Read records one by one
            for row in reader:

                if not row or not any(
                    value and value.strip()
                    for value in row.values()
                    if value is not None
                ):
                    continue

                records.append(row)

                try:
                    raw_value = row.get(value_column, "")
                    value = float(raw_value)

                    if not raw_value or not raw_value.strip():
                        raise ValueError

                    valid_values.append(value)

                except (ValueError, AttributeError):
                    skipped_rows += 1

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    except PermissionError:
        print("Error: Permission denied while reading the file.")
        return

    except OSError as error:
        print(f"File error: {error}")
        return

    # --------------------------------------
    # CALCULATE STATISTICS
    # --------------------------------------
    print("\n" + "=" * 45)
    print("           CSV DATA REPORT")
    print("=" * 45)

    print(f"File name          : {filename}")
    print(f"Total records      : {len(records)}")
    print(f"Valid numeric rows : {len(valid_values)}")
    print(f"Invalid/missing    : {skipped_rows}")

    if not valid_values:
        print("\nNo valid numeric values to analyze.")
        return

    total = sum(valid_values)
    average = total / len(valid_values)
    highest = max(valid_values)
    lowest = min(valid_values)

    print("-" * 45)
    print(f"Column analyzed    : {value_column}")
    print(f"Total              : {total:,.2f}")
    print(f"Average            : {average:,.2f}")
    print(f"Highest value      : {highest:,.2f}")
    print(f"Lowest value       : {lowest:,.2f}")
    print("=" * 45)


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------
def main():

    print("\n========================================")
    print("          CSV DATA PROCESSOR")
    print("========================================")

    filename = input("Enter CSV filename (example: sales.csv): ").strip()
    value_column = input(
        "Enter numeric column to analyze (example: Sales): "
    ).strip()

    if not filename or not value_column:
        print("Error: Filename and column name are required.")
        return

    process_csv(filename, value_column)


# ------------------------------------------
# START PROGRAM
# ------------------------------------------
if __name__ == "__main__":
    main()
