import json
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

FILE_NAME = "tasks.json"


# =========================
# FILE HANDLING
# =========================

def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    return []


def save_tasks():
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(tasks, file, indent=4)
    except OSError:
        print(Fore.RED + "Error: Unable to save tasks.")


tasks = load_tasks()


# =========================
# UI FUNCTIONS
# =========================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    print(Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + "              📝 MY TO-DO LIST")
    print(Fore.CYAN + "=" * 60)


def pause():
    input(Fore.WHITE + "\nPress Enter to continue...")


def show_menu():
    print(Fore.GREEN + "\n[1] ➕ Add Task")
    print(Fore.BLUE + "[2] 📋 View Tasks")
    print(Fore.YELLOW + "[3] ✏️  Update Task")
    print(Fore.CYAN + "[4] ✅ Complete Task")
    print(Fore.RED + "[5] 🗑️  Delete Task")
    print(Fore.MAGENTA + "[6] 🔍 Search Task")
    print(Fore.WHITE + "[7] 📊 Task Statistics")
    print(Fore.RED + "[8] 🚪 Exit")


# =========================
# ADD TASK
# =========================

def add_task():
    clear_screen()
    header()

    print(Fore.GREEN + "\n➕ ADD NEW TASK\n")

    title = input("Enter task: ").strip()

    if not title:
        print(Fore.RED + "\n❌ Task cannot be empty.")
        pause()
        return

    task = {
        "title": title,
        "completed": False,
        "created_at": datetime.now().strftime("%d-%m-%Y %H:%M")
    }

    tasks.append(task)
    save_tasks()

    print(Fore.GREEN + "\n✅ Task added successfully!")
    pause()


# =========================
# VIEW TASKS
# =========================

def view_tasks():
    clear_screen()
    header()

    print(Fore.BLUE + "\n📋 YOUR TASKS\n")

    if not tasks:
        print(Fore.YELLOW + "No tasks available.")
        pause()
        return

    for i, task in enumerate(tasks, start=1):

        if task["completed"]:
            status = Fore.GREEN + "✔ Completed"
        else:
            status = Fore.YELLOW + "⏳ Pending"

        print(Fore.CYAN + f"\n{i}. {task['title']}")
        print(f"   Status : {status}")
        print(Fore.WHITE + f"   Created: {task['created_at']}")

    print(Fore.CYAN + "\n" + "-" * 60)

    total = len(tasks)
    completed = sum(task["completed"] for task in tasks)
    pending = total - completed

    print(
        f"Total: {total} | "
        f"{Fore.GREEN}Completed: {completed}{Style.RESET_ALL} | "
        f"{Fore.YELLOW}Pending: {pending}"
    )

    pause()


# =========================
# UPDATE TASK
# =========================

def update_task():
    clear_screen()
    header()

    if not tasks:
        print(Fore.YELLOW + "\nNo tasks available.")
        pause()
        return

    print(Fore.YELLOW + "\n✏️ UPDATE TASK\n")

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['title']}")

    try:
        number = int(input("\nEnter task number: "))

        if 1 <= number <= len(tasks):

            new_title = input("Enter new task: ").strip()

            if not new_title:
                print(Fore.RED + "Task cannot be empty.")
            else:
                tasks[number - 1]["title"] = new_title
                save_tasks()

                print(Fore.GREEN + "\n✅ Task updated successfully!")

        else:
            print(Fore.RED + "\n❌ Invalid task number.")

    except ValueError:
        print(Fore.RED + "\n❌ Please enter a valid number.")

    pause()


# =========================
# COMPLETE TASK
# =========================

def complete_task():
    clear_screen()
    header()

    if not tasks:
        print(Fore.YELLOW + "\nNo tasks available.")
        pause()
        return

    print(Fore.GREEN + "\n✅ COMPLETE TASK\n")

    for i, task in enumerate(tasks, start=1):
        status = "✔" if task["completed"] else "⏳"
        print(f"{i}. {status} {task['title']}")

    try:
        number = int(input("\nEnter task number: "))

        if 1 <= number <= len(tasks):

            if tasks[number - 1]["completed"]:
                print(Fore.YELLOW + "\nTask is already completed.")
            else:
                tasks[number - 1]["completed"] = True
                save_tasks()

                print(Fore.GREEN + "\n🎉 Task completed!")

        else:
            print(Fore.RED + "\n❌ Invalid task number.")

    except ValueError:
        print(Fore.RED + "\n❌ Please enter a valid number.")

    pause()


# =========================
# DELETE TASK
# =========================

def delete_task():
    clear_screen()
    header()

    if not tasks:
        print(Fore.YELLOW + "\nNo tasks available.")
        pause()
        return

    print(Fore.RED + "\n🗑️ DELETE TASK\n")

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['title']}")

    try:
        number = int(input("\nEnter task number: "))

        if 1 <= number <= len(tasks):

            confirm = input(
                Fore.YELLOW +
                "Are you sure? (y/n): "
            ).lower()

            if confirm == "y":
                deleted = tasks.pop(number - 1)
                save_tasks()

                print(
                    Fore.GREEN +
                    f"\n✅ '{deleted['title']}' deleted successfully!"
                )
            else:
                print(Fore.YELLOW + "\nDeletion cancelled.")

        else:
            print(Fore.RED + "\n❌ Invalid task number.")

    except ValueError:
        print(Fore.RED + "\n❌ Please enter a valid number.")

    pause()


# =========================
# SEARCH TASK
# =========================

def search_task():
    clear_screen()
    header()

    print(Fore.MAGENTA + "\n🔍 SEARCH TASK\n")

    keyword = input("Enter keyword: ").strip().lower()

    if not keyword:
        print(Fore.RED + "\n❌ Search keyword cannot be empty.")
        pause()
        return

    results = []

    for i, task in enumerate(tasks, start=1):
        if keyword in task["title"].lower():
            results.append((i, task))

    if not results:
        print(Fore.YELLOW + "\nNo matching tasks found.")
    else:
        print(Fore.GREEN + "\nMatching Tasks:\n")

        for number, task in results:
            status = "Completed" if task["completed"] else "Pending"

            print(
                f"{number}. {task['title']} "
                f"[{status}]"
            )

    pause()


# =========================
# STATISTICS
# =========================

def statistics():
    clear_screen()
    header()

    total = len(tasks)
    completed = sum(task["completed"] for task in tasks)
    pending = total - completed

    print(Fore.MAGENTA + "\n📊 TASK STATISTICS\n")

    print(Fore.CYAN + f"Total Tasks     : {total}")
    print(Fore.GREEN + f"Completed Tasks : {completed}")
    print(Fore.YELLOW + f"Pending Tasks   : {pending}")

    if total > 0:
        percentage = (completed / total) * 100
        print(
            Fore.BLUE +
            f"Completion Rate : {percentage:.1f}%"
        )

    pause()


# =========================
# MAIN PROGRAM
# =========================

while True:

    clear_screen()
    header()

    show_menu()

    print(Fore.CYAN + "\n" + "=" * 60)

    choice = input(Fore.WHITE + "Choose an option: ").strip()

    if choice == "1":
        add_task()

    elif choice == "2":
        view_tasks()

    elif choice == "3":
        update_task()

    elif choice == "4":
        complete_task()

    elif choice == "5":
        delete_task()

    elif choice == "6":
        search_task()

    elif choice == "7":
        statistics()

    elif choice == "8":
        clear_screen()
        print(Fore.GREEN + "\n👋 Thank you for using My To-Do List!")
        print(Fore.CYAN + "Have a productive day! 🚀\n")
        break

    else:
        print(Fore.RED + "\n❌ Invalid option. Please choose 1-8.")
        pause()