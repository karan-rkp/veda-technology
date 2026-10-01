# ==========================================
# PALINDROME CHECKER
# Python Programming Track - Task 12
# ==========================================


# ------------------------------------------
# PALINDROME CHECK FUNCTION
# ------------------------------------------
def is_palindrome(text):

    # Convert to lowercase
    text = text.lower()

    # Remove spaces and unnecessary characters
    cleaned_text = ""

    for char in text:
        if char.isalnum():
            cleaned_text += char

    # Compare original with reversed text
    return cleaned_text == cleaned_text[::-1]


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------
def main():

    print("\n==========================================")
    print("          PALINDROME CHECKER")
    print("==========================================")

    text = input("\nEnter a word or sentence: ")

    if not text.strip():
        print("❌ Please enter some text.")
        return

    # Check palindrome
    result = is_palindrome(text)

    print("\n==========================================")

    if result:
        print("✅ It is a PALINDROME!")
    else:
        print("❌ It is NOT a palindrome.")

    print("==========================================")


# ------------------------------------------
# START PROGRAM
# ------------------------------------------
if __name__ == "__main__":
    main()
    
