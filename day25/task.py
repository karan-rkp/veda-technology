
# ==========================================
# PYTHON UTILITY MODULE
# Task 25 - Python Programming Track
# ==========================================

from pathlib import Path
from datetime import datetime


# ------------------------------------------
# 1. VALIDATE INTEGER INPUT
# ------------------------------------------
def is_valid_integer(value):
    """Check whether a string represents an integer."""
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False


# ------------------------------------------
# 2. VALIDATE EMAIL
# ------------------------------------------
def is_valid_email(email):
    """Perform basic email format validation."""
    if not isinstance(email, str):
        return False

    email = email.strip()

    if email.count("@") != 1:
        return False

    username, domain = email.split("@")

    return (
        bool(username)
        and bool(domain)
        and "." in domain
        and not domain.startswith(".")
        and not domain.endswith(".")
        and " " not in email
    )


# ------------------------------------------
# 3. FORMAT CURRENCY
# ------------------------------------------
def format_currency(amount, symbol="₹"):
    """Format a number as a currency amount."""
    return f"{symbol}{amount:,.2f}"


# ------------------------------------------
# 4. CALCULATOR
# ------------------------------------------
def calculate(a, b, operation):
    """Perform a basic arithmetic operation."""

    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b
    else:
        raise ValueError("Unsupported operation.")


# ------------------------------------------
# 5. FORMAT TEXT
# ------------------------------------------
def format_text(text):
    """Remove extra spaces and capitalize the text."""
    return " ".join(text.split()).title()


# ------------------------------------------
# 6. GET CURRENT DATE
# ------------------------------------------
def get_current_date():
    """Return today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


# ------------------------------------------
# 7. READ A TEXT FILE
# ------------------------------------------
def read_text_file(file_path):
    """Read a UTF-8 text file safely."""
    path = Path(file_path)

    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "Error: File not found."
    except (OSError, UnicodeError) as error:
        return f"Error reading file: {error}"


# ------------------------------------------
# 8. WRITE A TEXT FILE
# ------------------------------------------
def write_text_file(file_path, content):
    """Write text to a UTF-8 file."""
    path = Path(file_path)

    try:
        path.write_text(content, encoding="utf-8")
        return True
    except (OSError, UnicodeError) as error:
        print(f"Error writing file: {error}")
        return False
