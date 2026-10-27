
"""
PROJECT: Veda Technology Business & Service Management System
VERSION: 1.0
LANGUAGE: Python 3
STORAGE: JSON

Features:
- Dashboard and business summary
- Technology program management
- Digital service management
- Training program management
- Internship management
- Customer inquiry management
- Service request management
- Search, update, delete and reporting
- JSON file storage and input validation
"""

import json
import os
from datetime import datetime
from pathlib import Path

# =========================================================
# CONFIGURATION
# =========================================================

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

DATA_FILE = DATA_DIR / "main.json"

MODULES = {
    "programs": "Technology Programs",
    "services": "Digital Services",
    "training": "Training Programs",
    "internships": "Internship Programs",
    "inquiries": "Customer Inquiries",
    "requests": "Service Requests",
}

DEFAULT_DATA = {key: [] for key in MODULES}


# =========================================================
# DISPLAY UTILITIES
# =========================================================

def line(char="=", length=72):
    print(char * length)


def heading(title):
    print()
    line()
    print(f"{title:^72}")
    line()


def pause():
    input("\nPress Enter to continue...")


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean_text(prompt, required=True):
    while True:
        value = input(prompt).strip()

        if value or not required:
            return value

        print("This field cannot be empty. Please try again.")


def choose_option(prompt, options):
    allowed = {str(item).lower() for item in options}

    while True:
        value = input(prompt).strip().lower()

        if value in allowed:
            return value

        print("Invalid choice. Available options:", ", ".join(options))


def confirm(prompt):
    return choose_option(f"{prompt} (y/n): ", ["y", "n"]) == "y"


# =========================================================
# JSON DATA MANAGEMENT
# =========================================================

def load_data():
    """Load records from JSON; recover safely from missing files."""
    if not DATA_FILE.exists():
        save_data(DEFAULT_DATA)
        return {key: [] for key in MODULES}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("The JSON root must be an object.")

        for key in MODULES:
            if not isinstance(data.get(key), list):
                data[key] = []

        return data

    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"\nWarning: Could not read data file: {error}")
        print("Your original file has not been overwritten.")
        print("Restore a valid backup before continuing.")
        raise SystemExit(1)


def save_data(data):
    """Write JSON atomically to reduce the chance of partial files."""
    temporary_file = DATA_FILE.with_suffix(".tmp")

    try:
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        os.replace(temporary_file, DATA_FILE)

    except OSError as error:
        print(f"Error saving data: {error}")

        try:
            if temporary_file.exists():
                temporary_file.unlink()
        except OSError:
            pass

        raise


data = load_data()


# =========================================================
# ID GENERATION AND RECORD HELPERS
# =========================================================

def next_id(module):
    """Generate the next numeric ID for a module."""
    existing_ids = []

    for record in data[module]:
        try:
            existing_ids.append(int(record["id"]))
        except (KeyError, ValueError, TypeError):
            continue

    return max(existing_ids, default=0) + 1


def find_record(module, record_id):
    for record in data[module]:
        if str(record.get("id")) == str(record_id):
            return record

    return None


def display_records(module, records=None):
    records = data[module] if records is None else records
    title = MODULES[module]

    heading(title)

    if not records:
        print("No records found.")
        return

    for record in records:
        print(f"\nID: {record.get('id', '-')}")
        for key, value in record.items():
            if key not in ("id", "created_at", "updated_at"):
                print(f"  {key.replace('_', ' ').title()}: {value}")

        if record.get("created_at"):
            print(f"  Created: {record['created_at']}")

        line("-")


# =========================================================
# GENERIC CREATE OPERATION
# =========================================================

def add_record(module, fields):
    heading(f"ADD {MODULES[module].upper()}")

    record = {"id": next_id(module)}

    for field, label in fields:
        record[field] = clean_text(f"{label}: ")

    record["created_at"] = now()
    record["updated_at"] = now()

    data[module].append(record)

    try:
        save_data(data)
    except OSError:
        data[module].pop()
        print("Record was not saved. Please check file permissions.")
        return

    print("\nRecord added successfully!")
    print(f"Generated ID: {record['id']}")


# =========================================================
# GENERIC SEARCH OPERATION
# =========================================================

def search_records(module):
    heading(f"SEARCH {MODULES[module].upper()}")

    query = clean_text(
        "Enter ID, name, keyword, email, or status: "
    ).lower()

    matches = []

    for record in data[module]:
        searchable_text = " ".join(
            str(value) for value in record.values()
        ).lower()

        if query in searchable_text:
            matches.append(record)

    display_records(module, matches)
    print(f"\nMatching records: {len(matches)}")


# =========================================================
# GENERIC UPDATE OPERATION
# =========================================================

def update_record(module):
    heading(f"UPDATE {MODULES[module].upper()}")

    record_id = clean_text("Enter record ID: ")
    record = find_record(module, record_id)

    if record is None:
        print("Record not found.")
        return

    display_records(module, [record])

    editable_fields = [
        key for key in record
        if key not in ("id", "created_at", "updated_at")
    ]

    changes = {}

    print("\nLeave a field blank to keep its current value.")

    for field in editable_fields:
        current = record[field]

        value = input(
            f"{field.replace('_', ' ').title()} [{current}]: "
        ).strip()

        if value:
            changes[field] = value

    if not changes:
        print("No changes entered.")
        return

    if not confirm("Save these changes?"):
        print("Update cancelled.")
        return

    old_record = record.copy()
    record.update(changes)
    record["updated_at"] = now()

    try:
        save_data(data)
    except OSError:
        record.clear()
        record.update(old_record)
        print("Update could not be saved.")
        return

    print("Record updated successfully!")


# =========================================================
# GENERIC DELETE OPERATION
# =========================================================

def delete_record(module):
    heading(f"DELETE {MODULES[module].upper()}")

    record_id = clean_text("Enter record ID: ")
    record = find_record(module, record_id)

    if record is None:
        print("Record not found.")
        return

    display_records(module, [record])

    if not confirm("Are you sure you want to delete this record?"):
        print("Deletion cancelled.")
        return

    index = data[module].index(record)
    data[module].pop(index)

    try:
        save_data(data)
    except OSError:
        data[module].insert(index, record)
        print("Deletion could not be saved.")
        return

    print("Record deleted successfully!")


# =========================================================
# MODULE FIELD DEFINITIONS
# =========================================================

FIELDS = {
    "programs": [
        ("name", "Program name"),
        ("category", "Category"),
        ("description", "Description"),
        ("duration", "Duration"),
        ("status", "Status (Active/Inactive)"),
    ],
    "services": [
        ("name", "Service name"),
        ("category", "Category"),
        ("description", "Description"),
        ("price", "Price or quotation"),
        ("status", "Status (Available/Unavailable)"),
    ],
    "training": [
        ("name", "Training course name"),
        ("technology", "Technology"),
        ("duration", "Duration"),
        ("fee", "Fee or Free"),
        ("status", "Status (Open/Closed)"),
    ],
    "internships": [
        ("title", "Internship title"),
        ("technology", "Technology"),
        ("duration", "Duration"),
        ("eligibility", "Eligibility"),
        ("status", "Status (Open/Closed)"),
    ],
    "inquiries": [
        ("customer_name", "Customer name"),
        ("email", "Email address"),
        ("subject", "Inquiry subject"),
        ("message", "Inquiry message"),
        ("status", "Status (New/In Progress/Resolved)"),
    ],
    "requests": [
        ("customer_name", "Customer name"),
        ("service_name", "Requested service"),
        ("description", "Request description"),
        ("priority", "Priority (Low/Medium/High)"),
        ("status", "Status (Pending/In Progress/Completed)"),
    ],
}


# =========================================================
# MODULE MENU
# =========================================================

def module_menu(module):
    while True:
        heading(MODULES[module].upper())

        print("1. Add record")
        print("2. View all records")
        print("3. Search records")
        print("4. Update record")
        print("5. Delete record")
        print("0. Back to main menu")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_record(module, FIELDS[module])
            pause()

        elif choice == "2":
            display_records(module)
            pause()

        elif choice == "3":
            search_records(module)
            pause()

        elif choice == "4":
            update_record(module)
            pause()

        elif choice == "5":
            delete_record(module)
            pause()

        elif choice == "0":
            break

        else:
            print("Invalid option. Choose from 0 to 5.")
            pause()


# =========================================================
# DASHBOARD AND PERFORMANCE REPORT
# =========================================================

def dashboard():
    heading("VEDA TECHNOLOGY - BUSINESS DASHBOARD")

    total = sum(len(data[module]) for module in MODULES)

    print(f"Total business records : {total}")

    for module, title in MODULES.items():
        print(f"{title:<30}: {len(data[module])}")

    print("\nRecent customer inquiries:")

    recent_inquiries = sorted(
        data["inquiries"],
        key=lambda item: item.get("created_at", ""),
        reverse=True
    )[:5]

    if not recent_inquiries:
        print("No inquiries available.")
    else:
        for inquiry in recent_inquiries:
            print(
                f"- #{inquiry['id']} "
                f"{inquiry.get('customer_name', 'Unknown')} | "
                f"{inquiry.get('status', 'New')}"
            )

    print("\nService request status summary:")

    requests = data["requests"]

    if not requests:
        print("No service requests available.")
    else:
        for status in ["Pending", "In Progress", "Completed"]:
            count = sum(
                item.get("status", "").lower() == status.lower()
                for item in requests
            )
            print(f"{status:<15}: {count}")


def export_report():
    heading("EXPORT BUSINESS REPORT")

    report_file = DATA_DIR / "business_report.txt"

    try:
        with report_file.open("w", encoding="utf-8") as file:
            file.write("VEDA TECHNOLOGY BUSINESS REPORT\n")
            file.write(f"Generated: {now()}\n")
            file.write("=" * 55 + "\n\n")

            for module, title in MODULES.items():
                file.write(f"{title}: {len(data[module])}\n")

                for record in data[module]:
                    file.write(
                        f"  ID: {record.get('id')} | "
                        f"{json.dumps(record, ensure_ascii=False)}\n"
                    )

                file.write("\n")

        print(f"Report saved to: {report_file}")

    except OSError as error:
        print(f"Could not export report: {error}")


# =========================================================
# MAIN APPLICATION
# =========================================================

def main():
    while True:
        heading("VEDA TECHNOLOGY")
        print("Business & Service Management System")
        line("-")

        print("1.  Dashboard")
        print("2.  Technology Programs")
        print("3.  Digital Services")
        print("4.  Training Programs")
        print("5.  Internship Programs")
        print("6.  Customer Inquiries")
        print("7.  Service Requests")
        print("8.  Export Business Report")
        print("9.  Save Data")
        print("0.  Exit")

        choice = input("\nEnter your choice: ").strip()

        menu_map = {
            "2": "programs",
            "3": "services",
            "4": "training",
            "5": "internships",
            "6": "inquiries",
            "7": "requests",
        }

        if choice == "1":
            dashboard()
            pause()

        elif choice in menu_map:
            module_menu(menu_map[choice])

        elif choice == "8":
            export_report()
            pause()

        elif choice == "9":
            try:
                save_data(data)
                print("Data saved successfully.")
            except OSError:
                print("Could not save data.")
            pause()

        elif choice == "0":
            if confirm("Exit the application?"):
                print("Thank you for using Veda Technology Management System.")
                break

        else:
            print("Invalid choice. Please select 0 to 9.")
            pause()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nApplication closed.")
