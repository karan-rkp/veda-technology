# ==========================================
# CONTACT BOOK USING DICTIONARIES
# Task 10 - Python Programming Track
# ==========================================

contacts = {}


# ------------------------------------------
# ADD CONTACT
# ------------------------------------------
def add_contact():
    print("\n========== ADD CONTACT ==========")

    phone = input("Enter phone number: ").strip()

    if phone in contacts:
        print("❌ Contact already exists!")
        return

    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip()

    contacts[phone] = {
        "name": name,
        "email": email
    }

    print("✅ Contact added successfully!")


# ------------------------------------------
# SEARCH CONTACT
# ------------------------------------------
def search_contact():
    print("\n========== SEARCH CONTACT ==========")

    phone = input("Enter phone number: ").strip()

    if phone in contacts:
        contact = contacts[phone]

        print("\n📱 Contact Found")
        print("----------------------")
        print(f"Name  : {contact['name']}")
        print(f"Phone : {phone}")
        print(f"Email : {contact['email']}")
    else:
        print("❌ Contact not found!")


# ------------------------------------------
# UPDATE CONTACT
# ------------------------------------------
def update_contact():
    print("\n========== UPDATE CONTACT ==========")

    phone = input("Enter phone number: ").strip()

    if phone not in contacts:
        print("❌ Contact not found!")
        return

    print("\nCurrent Information:")
    print(f"Name  : {contacts[phone]['name']}")
    print(f"Email : {contacts[phone]['email']}")

    name = input("\nEnter new name: ").strip()
    email = input("Enter new email: ").strip()

    if name:
        contacts[phone]["name"] = name

    if email:
        contacts[phone]["email"] = email

    print("✅ Contact updated successfully!")


# ------------------------------------------
# DELETE CONTACT
# ------------------------------------------
def delete_contact():
    print("\n========== DELETE CONTACT ==========")

    phone = input("Enter phone number: ").strip()

    if phone not in contacts:
        print("❌ Contact not found!")
        return

    contact = contacts[phone]

    print(f"\nName : {contact['name']}")
    print(f"Phone: {phone}")

    confirm = input("\nAre you sure you want to delete? (y/n): ").lower()

    if confirm == "y":
        del contacts[phone]
        print("✅ Contact deleted successfully!")
    else:
        print("❌ Delete cancelled.")


# ------------------------------------------
# VIEW ALL CONTACTS
# ------------------------------------------
def view_contacts():
    print("\n========== ALL CONTACTS ==========")

    if not contacts:
        print("📭 Contact book is empty.")
        return

    for number, contact in contacts.items():
        print("----------------------")
        print(f"Name  : {contact['name']}")
        print(f"Phone : {number}")
        print(f"Email : {contact['email']}")

    print("----------------------")
    print(f"Total Contacts: {len(contacts)}")


# ------------------------------------------
# MAIN MENU
# ------------------------------------------
def main():

    while True:

        print("\n")
        print("╔════════════════════════════════╗")
        print("║        📱 CONTACT BOOK         ║")
        print("╠════════════════════════════════╣")
        print("║ 1. Add Contact                 ║")
        print("║ 2. Search Contact              ║")
        print("║ 3. Update Contact              ║")
        print("║ 4. Delete Contact              ║")
        print("║ 5. View All Contacts            ║")
        print("║ 6. Exit                        ║")
        print("╚════════════════════════════════╝")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_contact()

        elif choice == "2":
            search_contact()

        elif choice == "3":
            update_contact()

        elif choice == "4":
            delete_contact()

        elif choice == "5":
            view_contacts()

        elif choice == "6":
            print("\n👋 Thank you for using Contact Book!")
            break

        else:
            print("❌ Invalid choice! Please select 1-6.")


# ------------------------------------------
# START PROGRAM
# ------------------------------------------
if __name__ == "__main__":
    main()