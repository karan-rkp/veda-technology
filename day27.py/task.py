
# ==========================================
# DATE AND TIME UTILITY
# Python Programming Track - Task 26
# ==========================================

from datetime import date, datetime, time, timedelta


# ------------------------------------------
# 1. GET VALID DATE INPUT
# ------------------------------------------
def get_date_input(message):
    """Read and validate a date in YYYY-MM-DD format."""

    while True:
        user_input = input(message).strip()

        try:
            return datetime.strptime(
                user_input, "%Y-%m-%d"
            ).date()

        except ValueError:
            print("Invalid date! Use YYYY-MM-DD format.")


# ------------------------------------------
# 2. CALCULATE AGE
# ------------------------------------------
def calculate_age(birth_date):
    """Calculate age in completed years."""

    today = date.today()

    if birth_date > today:
        raise ValueError("Birth date cannot be in the future.")

    age = today.year - birth_date.year

    # Reduce age if birthday has not occurred this year
    if (today.month, today.day) < (
        birth_date.month, birth_date.day
    ):
        age -= 1

    return age


# ------------------------------------------
# 3. DAYS BETWEEN TWO DATES
# ------------------------------------------
def days_between(start_date, end_date):
    """Return the absolute number of days between dates."""

    return abs((end_date - start_date).days)


# ------------------------------------------
# 4. COUNT WORKING DAYS
# ------------------------------------------
def count_working_days(start_date, end_date):
    """Count Monday-Friday days, including both endpoints."""

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    working_days = 0
    current_date = start_date

    while current_date <= end_date:
        # Monday = 0, Sunday = 6
        if current_date.weekday() < 5:
            working_days += 1

        current_date += timedelta(days=1)

    return working_days


# ------------------------------------------
# 5. FORMAT DATE AND TIME
# ------------------------------------------
def format_datetime(value=None):
    """Return a readable date and time."""

    if value is None:
        value = datetime.now()

    return value.strftime("%d %B %Y, %I:%M:%S %p")


# ------------------------------------------
# 6. ADD DAYS TO A DATE
# ------------------------------------------
def add_days(start_date, number_of_days):
    """Calculate a future or past date."""

    return start_date + timedelta(days=number_of_days)


# ------------------------------------------
# 7. DISPLAY MENU
# ------------------------------------------
def show_menu():
    print("\n" + "=" * 45)
    print("        DATE AND TIME UTILITY")
    print("=" * 45)
    print("1. Calculate Age")
    print("2. Days Between Two Dates")
    print("3. Count Working Days")
    print("4. Display Current Date and Time")
    print("5. Add or Subtract Days")
    print("6. Exit")
    print("=" * 45)


# ------------------------------------------
# 8. MAIN PROGRAM
# ------------------------------------------
def main():

    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        try:
            if choice == "1":
                birth_date = get_date_input(
                    "Enter birth date (YYYY-MM-DD): "
                )

                print("Your age:", calculate_age(birth_date), "years")

            elif choice == "2":
                start_date = get_date_input(
                    "Enter first date (YYYY-MM-DD): "
                )
                end_date = get_date_input(
                    "Enter second date (YYYY-MM-DD): "
                )

                print(
                    "Days between dates:",
                    days_between(start_date, end_date)
                )

            elif choice == "3":
                start_date = get_date_input(
                    "Enter start date (YYYY-MM-DD): "
                )
                end_date = get_date_input(
                    "Enter end date (YYYY-MM-DD): "
                )

                print(
                    "Working days (Mon-Fri):",
                    count_working_days(start_date, end_date)
                )

            elif choice == "4":
                print("Current date and time:", format_datetime())

            elif choice == "5":
                start_date = get_date_input(
                    "Enter a date (YYYY-MM-DD): "
                )

                try:
                    number = int(
                        input("Enter days to add (negative to subtract): ")
                    )
                    result = add_days(start_date, number)
                    print("Resulting date:", result.strftime("%Y-%m-%d"))

                except ValueError:
                    print("Please enter a valid whole number of days.")

            elif choice == "6":
                print("Thank you for using Date and Time Utility!")
                break

            else:
                print("Invalid choice! Please select 1-6.")

        except ValueError as error:
            print("Error:", error)

        input("\nPress Enter to continue...")


# ------------------------------------------
# START APPLICATION
# ------------------------------------------
if __name__ == "__main__":
    main()
