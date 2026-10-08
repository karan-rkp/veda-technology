# ==========================================
# READ AND PROCESS A TEXT FILE
# Python Programming Track - Task 19
# ==========================================


# ------------------------------------------
# PROCESS TEXT FILE
# ------------------------------------------
def process_file(filename):

    try:
        # Open file in read mode
        with open(filename, "r", encoding="utf-8") as file:

            line_count = 0
            word_count = 0
            character_count = 0
            space_count = 0

            # Process file line by line
            for line in file:

                line_count += 1

                # Count words
                word_count += len(line.split())

                # Count characters
                character_count += len(line)

                # Count spaces
                space_count += line.count(" ")

        # Display statistics
        print("\n==========================================")
        print("          TEXT FILE STATISTICS")
        print("==========================================")

        print(f"File Name  : {filename}")
        print(f"Lines      : {line_count}")
        print(f"Words      : {word_count}")
        print(f"Characters : {character_count}")
        print(f"Spaces     : {space_count}")

        print("==========================================")

    except FileNotFoundError:
        print("\n❌ Error: File not found!")
        print("Please check the filename and try again.")

    except PermissionError:
        print("\n❌ Error: Permission denied.")
        print("You don't have permission to read this file.")

    except UnicodeDecodeError:
        print("\n❌ Error: Unable to decode the file.")
        print("Please use a valid text file.")

    except OSError as error:
        print(f"\n❌ File error: {error}")


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------
def main():

    print("\n==========================================")
    print("       📄 TEXT FILE PROCESSOR")
    print("==========================================")

    filename = input(
        "Enter the text filename "
        "(example: sample.txt): "
    ).strip()

    if not filename:
        print("❌ Filename cannot be empty.")
        return

    process_file(filename)


# ------------------------------------------
# START PROGRAM
# ------------------------------------------
if __name__ == "__main__":
    main()