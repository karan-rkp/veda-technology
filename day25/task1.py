
# ==========================================
# MAIN PROGRAM
# Task 25 - Utility Module Demo
# ==========================================

import task as utils


def main():
    print("=" * 45)
    print("       PYTHON UTILITY TOOLKIT")
    print("=" * 45)

    # Input validation
    value = input("\nEnter an integer: ")

    if utils.is_valid_integer(value):
        print("Valid integer:", int(value))
    else:
        print("Invalid integer!")

    # Email validation
    email = input("\nEnter your email: ")
    print("Valid email:", utils.is_valid_email(email))

    # Text formatting
    text = input("\nEnter text: ")
    print("Formatted text:", utils.format_text(text))

    # Currency formatting
    try:
        amount = float(input("\nEnter an amount: "))
        print("Formatted amount:", utils.format_currency(amount))
    except ValueError:
        print("Please enter a valid amount.")

    # Calculator
    try:
        a = float(input("\nEnter first number: "))
        b = float(input("Enter second number: "))
        operation = input("Enter operation (+, -, *, /): ").strip()

        result = utils.calculate(a, b, operation)
        print("Result:", result)

    except ValueError as error:
        print("Calculation error:", error)

    # Current date
    print("\nCurrent date:", utils.get_current_date())

    # File utility demonstration
    filename = "sample.txt"
    content = "Hello Karan!\nThis file was created using a utility module."

    if utils.write_text_file(filename, content):
        print(f"\nFile '{filename}' created successfully.")
        print("File contents:")
        print(utils.read_text_file(filename))

    print("\nUtility module demonstration completed!")


if __name__ == "__main__":
    main()
