
# ==========================================
# FILE ORGANIZER
# Python Programming Track - Task 22
# ==========================================

from pathlib import Path
import shutil


# ------------------------------------------
# FILE CATEGORIES
# ------------------------------------------
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Python": [".py", ".pyc"],
    "Code": [".html", ".css", ".js", ".java", ".cpp", ".c", ".php", ".json"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Installers": [".exe", ".msi", ".apk"],
}


# ------------------------------------------
# FIND CATEGORY
# ------------------------------------------
def get_category(file_path):

    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


# ------------------------------------------
# CREATE UNIQUE DESTINATION
# ------------------------------------------
def get_unique_path(destination):

    if not destination.exists():
        return destination

    parent = destination.parent
    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        new_path = parent / f"{stem}_{counter}{suffix}"

        if not new_path.exists():
            return new_path

        counter += 1


# ------------------------------------------
# ORGANIZE FILES
# ------------------------------------------
def organize_folder(folder_path):

    folder = Path(folder_path).expanduser()

    if not folder.exists():
        print("Error: Folder does not exist.")
        return

    if not folder.is_dir():
        print("Error: The provided path is not a folder.")
        return

    organized_count = 0
    skipped_count = 0
    error_count = 0

    # Only process files directly inside this folder
    for file_path in folder.iterdir():

        if not file_path.is_file():
            continue

        try:
            category = get_category(file_path)
            destination_folder = folder / category

            # Avoid moving the script into its own category
            destination_folder.mkdir(exist_ok=True)

            destination_path = get_unique_path(
                destination_folder / file_path.name
            )

            # Avoid moving a file onto itself
            if file_path.resolve() == destination_path.resolve():
                skipped_count += 1
                continue

            shutil.move(str(file_path), str(destination_path))

            print(f"Moved: {file_path.name} -> {category}/")
            organized_count += 1

        except PermissionError:
            print(f"Permission denied: {file_path.name}")
            error_count += 1

        except OSError as error:
            print(f"Could not move {file_path.name}: {error}")
            error_count += 1

    # --------------------------------------
    # SUMMARY
    # --------------------------------------
    print("\n" + "=" * 45)
    print("         FILE ORGANIZATION REPORT")
    print("=" * 45)
    print(f"Folder           : {folder}")
    print(f"Files organized  : {organized_count}")
    print(f"Files skipped    : {skipped_count}")
    print(f"Errors           : {error_count}")
    print("=" * 45)


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------
def main():

    print("\n========================================")
    print("           FILE ORGANIZER")
    print("========================================")
    print("Organizes files according to extensions.")
    print("Tip: Test this program on a sample folder.")
    print()

    folder_path = input(
        "Enter the folder path to organize: "
    ).strip().strip('"')

    if not folder_path:
        print("Error: Folder path cannot be empty.")
        return

    confirm = input(
        "Move files into category folders? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        organize_folder(folder_path)
    else:
        print("Operation cancelled. No files were moved.")


# ------------------------------------------
# START PROGRAM
# ------------------------------------------
if __name__ == "__main__":
    main()
