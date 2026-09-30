# ==========================================
# WORD AND CHARACTER COUNTER
# Python Programming Track
# ==========================================


# ------------------------------------------
# COUNT TEXT STATISTICS
# ------------------------------------------
def analyze_text(text):

    # Character count including spaces
    characters = len(text)

    # Word count
    words = len(text.split())

    # Space count
    spaces = text.count(" ")

    # Sentence count
    sentences = 0

    for char in text:
        if char in ".!?":
            sentences += 1

    return characters, words, sentences, spaces


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------
def main():

    print("\n==========================================")
    print("       WORD & CHARACTER COUNTER")
    print("==========================================")

    print("\nEnter your paragraph below.")
    print("Press Enter when you are finished.\n")

    text = input("Paragraph: ").strip()

    # Check empty input
    if not text:
        print("\n❌ No text entered!")
        return

    # Analyze text
    characters, words, sentences, spaces = analyze_text(text)

    # Display results
    print("\n==========================================")
    print("           TEXT STATISTICS")
    print("==========================================")

    print(f"Characters : {characters}")
    print(f"Words      : {words}")
    print(f"Sentences  : {sentences}")
    print(f"Spaces     : {spaces}")

    print("==========================================")


# ------------------------------------------
# START PROGRAM
# ------------------------------------------
if __name__ == "__main__":
    main()