# ==========================================
# EXCEPTION HANDLING PRACTICE
# Python Programming Track - Task 18
# ==========================================


# ------------------------------------------
# 1. INVALID NUMBER INPUT
# ------------------------------------------
def number_input_demo():

    print("\n========== 1. NUMBER INPUT ==========")

    try:
        number = int(input("Enter an integer: "))

    except ValueError:
        print("❌ Error: Please enter a valid integer.")

    else:
        print(f"✅ You entered: {number}")

    finally:
        print("✔ Number input operation completed.")


# ------------------------------------------
# 2. DIVISION BY ZERO
# ------------------------------------------
def division_demo():

    print("\n========== 2. DIVISION ==========")

    try:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))

        result = a / b

    except ValueError:
        print("❌ Error: Please enter valid numbers.")

    except ZeroDivisionError:
        print("❌ Error: Cannot divide by zero.")

    else:
        print(f"✅ Result: {result:.2f}")

    finally:
        print("✔ Division operation completed.")


# ------------------------------------------
# 3. LIST INDEX ERROR
# ------------------------------------------
def list_demo():

    print("\n========== 3. LIST ACCESS ==========")

    numbers = [10, 20, 30, 40, 50]

    try:
        index = int(input("Enter index (0-4): "))
        print(f"Value: {numbers[index]}")

    except ValueError:
        print("❌ Error: Index must be an integer.")

    except IndexError:
        print("❌ Error: Index is outside the list range.")

    else:
        print("✅ List value accessed successfully.")

    finally:
        print("✔ List operation completed.")


# ------------------------------------------
# 4. DICTIONARY KEY ERROR
# ------------------------------------------
def dictionary_demo():

    print("\n========== 4. DICTIONARY ACCESS ==========")

    student = {
        "name": "Karan",
        "course": "MCA",
        "language": "Python"
    }

    try:
        key = input("Enter key (name/course/language): ").strip()

        value = student[key]

    except KeyError:
        print("❌ Error: This key does not exist.")

    else:
        print(f"✅ Value: {value}")

    finally:
        print("✔ Dictionary operation completed.")


# ------------------------------------------
# 5. FILE NOT FOUND ERROR
# ------------------------------------------
def file_demo():

    print("\n========== 5. FILE ACCESS ==========")

    filename = input("Enter filename to open: ").strip()

    try:
        file = open(filename, "r")
        content = file.read()

    except FileNotFoundError:
        print("❌ Error: File was not found.")

    except PermissionError:
        print("❌ Error: You do not have permission to access this file.")

    else:
        print("✅ File opened successfully.")
        print("\nFile Content:")
        print(content)

    finally:
        try:
            file.close()
            print("✔ File operation completed.")
        except UnboundLocalError:
            print("✔ No file was opened.")


# ------------------------------------------
# 6. TYPE ERROR
# ------------------------------------------
def type_error_demo():

    print("\n========== 6. TYPE ERROR ==========")

    try:
        number = 100
        text = "Python"

        result = number + text

    except TypeError:
        print("❌ Error: Cannot add an integer and a string.")

    else:
        print(result)

    finally:
        print("✔ Type operation completed.")


# ------------------------------------------
# MAIN MENU
# ------------------------------------------
def main():

    while True:

        print("\n")
        print("╔════════════════════════════════════╗")
        print("║     EXCEPTION HANDLING PRACTICE    ║")
        print("╠════════════════════════════════════╣")
        print("║ 1. Invalid Number Input            ║")
        print("║ 2. Division by Zero                ║")
        print("║ 3. List Index Error                ║")
        print("║ 4. Dictionary Key Error            ║")
        print("║ 5. File Not Found Error            ║")
        print("║ 6. Type Error                      ║")
        print("║ 7. Exit                            ║")
        print("╚════════════════════════════════════╝")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            number_input_demo()

        elif choice == "2":
            division_demo()

        elif choice == "3":
            list_demo()

        elif choice == "4":
            dictionary_demo()

        elif choice == "5":
            file_demo()

        elif choice == "6":
            type_error_demo()

        elif choice == "7":
            print("\n👋 Program closed successfully!")
            break

        else:
            print("❌ Invalid choice. Please select 1-7.")


# ------------------------------------------
# START PROGRAM
# ------------------------------------------
if __name__ == "__main__":
    main()