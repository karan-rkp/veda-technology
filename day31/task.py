
# ============================================================
# PROJECT: ADVANCED PASSWORD GENERATOR
# TASK 31 - PYTHON PROGRAMMING TRACK
# Modules: secrets, string
# ============================================================

import secrets
import string


def display_header():
    print("\n" + "=" * 55)
    print("           ADVANCED PASSWORD GENERATOR")
    print("=" * 55)


def get_password_length():
    """Get and validate the requested password length."""
    while True:
        try:
            length = int(input("Enter password length (8-128): "))

            if 8 <= length <= 128:
                return length

            print("Please choose a length between 8 and 128.")

        except ValueError:
            print("Invalid input. Enter a whole number.")


def choose_character_types():
    """Let the user choose which character groups to use."""
    print("\nChoose character types:")
    print("1. Lowercase letters (a-z)")
    print("2. Uppercase letters (A-Z)")
    print("3. Numbers (0-9)")
    print("4. Special characters (!@#$...)")

    while True:
        choices = input(
            "\nEnter choices separated by commas (e.g. 1,2,3,4): "
        ).strip()

        try:
            selected = {
                int(item.strip())
                for item in choices.split(",")
            }

            if selected and selected.issubset({1, 2, 3, 4}):
                return selected

            print("Choose one or more options from 1, 2, 3, 4.")

        except ValueError:
            print("Invalid input. Example: 1,2,3,4")


def generate_password(length, selected):
    """
    Generate a secure password.
    Include at least one character from each selected group.
    """
    groups = []

    if 1 in selected:
        groups.append(string.ascii_lowercase)

    if 2 in selected:
        groups.append(string.ascii_uppercase)

    if 3 in selected:
        groups.append(string.digits)

    if 4 in selected:
        groups.append("!@#$%^&*()-_=+[]{};:,.?/")

    if length < len(groups):
        raise ValueError("Password length is too short for these options.")

    # Guarantee one character from each selected group.
    password_chars = [
        secrets.choice(group)
        for group in groups
    ]

    # Fill the remaining positions from all selected groups.
    all_characters = "".join(groups)

    for _ in range(length - len(password_chars)):
        password_chars.append(secrets.choice(all_characters))

    # Securely shuffle the characters.
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)


def assess_password(length, selected):
    """Provide a simple estimate based on length and variety."""
    variety = len(selected)

    if length >= 20 and variety >= 3:
        return "Very strong configuration"
    elif length >= 14 and variety >= 3:
        return "Strong configuration"
    elif length >= 12 and variety >= 2:
        return "Good configuration"
    else:
        return "Consider a longer password and more character types"


def generate_multiple_samples():
    """Generate several example passwords."""
    print("\n--- Sample Password Generator ---")

    length = get_password_length()
    selected = choose_character_types()
    count = 5

    print(f"\nGenerating {count} sample passwords...")

    for number in range(1, count + 1):
        password = generate_password(length, selected)
        print(f"{number}. {password}")

    print("\nSamples are displayed only; they are not saved.")


def main():
    while True:
        display_header()

        print("1. Generate one password")
        print("2. Generate five sample passwords")
        print("3. Exit")

        choice = input("\nSelect an option (1-3): ").strip()

        if choice == "1":
            length = get_password_length()
            selected = choose_character_types()

            password = generate_password(length, selected)

            print("\n" + "-" * 55)
            print("Generated Password:", password)
            print("Length:", len(password))
            print("Assessment:", assess_password(length, selected))
            print("-" * 55)
            print("Keep your password private and secure.")

        elif choice == "2":
            generate_multiple_samples()

        elif choice == "3":
            print("\nThank you for using Password Generator!")
            break

        else:
            print("Invalid option. Please select 1, 2, or 3.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram closed safely.")
