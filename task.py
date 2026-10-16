
# ============================================================
# PROJECT: ADVANCED REST API CLIENT
# Python Programming Track - Task 27
# API: JSONPlaceholder
# ============================================================

import json
from pathlib import Path

import requests


BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 10
PAGE_SIZE = 10

# Reuse a session for HTTP requests
session = requests.Session()
session.headers.update({
    "Accept": "application/json",
    "User-Agent": "Karan-Advanced-API-Client/1.0"
})


# ------------------------------------------------------------
# 1. DISPLAY HEADER
# ------------------------------------------------------------
def show_header():
    print("\n" + "=" * 62)
    print("             ADVANCED REST API CLIENT")
    print("                 Python Project")
    print("=" * 62)


# ------------------------------------------------------------
# 2. FETCH DATA FROM API
# ------------------------------------------------------------
def fetch_data(endpoint, params=None):
    """Fetch JSON data and handle common API errors."""

    url = f"{BASE_URL}/{endpoint.lstrip('/')}"

    try:
        response = session.get(
            url,
            params=params,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        data = response.json()
        return data

    except requests.exceptions.Timeout:
        print("\n[ERROR] Request timed out.")
        print("Try again when your internet connection is stable.")

    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Unable to connect to the API.")
        print("Check your internet connection.")

    except requests.exceptions.HTTPError as error:
        status = error.response.status_code
        print(f"\n[HTTP ERROR] Status code: {status}")

    except requests.exceptions.RequestException as error:
        print(f"\n[REQUEST ERROR] {error}")

    except ValueError:
        print("\n[ERROR] The API returned invalid JSON.")

    return None


# ------------------------------------------------------------
# 3. GET ALL POSTS
# ------------------------------------------------------------
def get_all_posts():
    print("\nFetching posts...")

    posts = fetch_data("posts")

    if not isinstance(posts, list):
        print("Could not retrieve posts.")
        return

    print(f"\nSuccessfully retrieved {len(posts)} posts.")

    for post in posts:
        print(
            f"\nID: {post.get('id')} | "
            f"User: {post.get('userId')}"
        )
        print(f"Title: {post.get('title')}")
        print("-" * 62)

    print(f"\nTotal posts displayed: {len(posts)}")


# ------------------------------------------------------------
# 4. GET POST BY ID
# ------------------------------------------------------------
def get_post_by_id():
    try:
        post_id = int(input("\nEnter post ID (1-100): ").strip())

        if not 1 <= post_id <= 100:
            print("Post ID must be between 1 and 100.")
            return

    except ValueError:
        print("Invalid input. Please enter a whole number.")
        return

    post = fetch_data(f"posts/{post_id}")

    if not isinstance(post, dict) or "id" not in post:
        print("Post could not be found.")
        return

    print("\n" + "=" * 62)
    print("                     POST DETAILS")
    print("=" * 62)
    print(f"Post ID : {post.get('id')}")
    print(f"User ID : {post.get('userId')}")
    print(f"Title   : {post.get('title')}")
    print("\nContent:")
    print(post.get("body", "No content available."))
    print("=" * 62)


# ------------------------------------------------------------
# 5. FILTER POSTS BY USER
# ------------------------------------------------------------
def get_posts_by_user():
    try:
        user_id = int(input("\nEnter user ID (1-10): ").strip())

        if not 1 <= user_id <= 10:
            print("User ID must be between 1 and 10.")
            return

    except ValueError:
        print("Invalid input. Please enter a whole number.")
        return

    posts = fetch_data("posts", params={"userId": user_id})

    if not isinstance(posts, list):
        print("Unable to retrieve user posts.")
        return

    print(f"\nPosts belonging to User {user_id}")

    for post in posts:
        print(f"\n[{post.get('id')}] {post.get('title')}")
        print(f"     {post.get('body')}")

    print(f"\nTotal matching posts: {len(posts)}")


# ------------------------------------------------------------
# 6. SEARCH POSTS BY KEYWORD
# ------------------------------------------------------------
def search_posts():
    keyword = input("\nEnter a keyword to search: ").strip().casefold()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    posts = fetch_data("posts")

    if not isinstance(posts, list):
        print("Unable to retrieve posts for searching.")
        return

    matches = [
        post for post in posts
        if keyword in post.get("title", "").casefold()
        or keyword in post.get("body", "").casefold()
    ]

    print(f"\nSearch results for: {keyword!r}")
    print("-" * 62)

    if not matches:
        print("No matching posts found.")
        return

    for post in matches:
        print(f"\nID: {post.get('id')}")
        print(f"Title: {post.get('title')}")
        print(f"Body: {post.get('body')}")

    print(f"\nTotal matches: {len(matches)}")


# ------------------------------------------------------------
# 7. PAGINATION
# ------------------------------------------------------------
def browse_posts():
    posts = fetch_data("posts")

    if not isinstance(posts, list):
        print("Unable to retrieve posts.")
        return

    total = len(posts)
    page = 0

    while True:
        start = page * PAGE_SIZE
        current_posts = posts[start:start + PAGE_SIZE]

        if not current_posts:
            print("No posts on this page.")
        else:
            print(f"\nPAGE {page + 1}")
            print("-" * 62)

            for post in current_posts:
                print(f"\nID: {post.get('id')}")
                print(f"Title: {post.get('title')}")

        print(
            f"\nShowing {min(start + len(current_posts), total)}"
            f" of {total} posts."
        )
        print("N = Next page | P = Previous | Q = Quit")

        command = input("Your choice: ").strip().lower()

        if command == "n":
            if start + PAGE_SIZE < total:
                page += 1
            else:
                print("You are already on the last page.")

        elif command == "p":
            if page > 0:
                page -= 1
            else:
                print("You are already on the first page.")

        elif command == "q":
            break

        else:
            print("Invalid choice. Enter N, P, or Q.")


# ------------------------------------------------------------
# 8. EXPORT POSTS TO JSON
# ------------------------------------------------------------
def export_posts():
    posts = fetch_data("posts")

    if not isinstance(posts, list):
        print("Unable to export posts.")
        return

    output_file = Path("exported_posts.json")

    try:
        with output_file.open("w", encoding="utf-8") as file:
            json.dump(posts, file, indent=4, ensure_ascii=False)

        print(f"\nExport successful!")
        print(f"File saved to: {output_file.resolve()}")
        print(f"Records exported: {len(posts)}")

    except OSError as error:
        print(f"File error: {error}")


# ------------------------------------------------------------
# 9. MAIN MENU
# ------------------------------------------------------------
def main():
    try:
        while True:
            show_header()

            print("1. Fetch All Posts")
            print("2. View Post by ID")
            print("3. Filter Posts by User")
            print("4. Search Posts by Keyword")
            print("5. Browse Posts with Pagination")
            print("6. Export Posts to JSON")
            print("7. Exit")

            print("=" * 62)

            choice = input("Select an option (1-7): ").strip()

            if choice == "1":
                get_all_posts()

            elif choice == "2":
                get_post_by_id()

            elif choice == "3":
                get_posts_by_user()

            elif choice == "4":
                search_posts()

            elif choice == "5":
                browse_posts()

            elif choice == "6":
                export_posts()

            elif choice == "7":
                print("\nThank you for using Advanced API Client!")
                print("Goodbye!")
                break

            else:
                print("\nInvalid choice. Select a number from 1 to 7.")

            input("\nPress Enter to return to the menu...")

    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram closed safely.")

    finally:
        session.close()


# ------------------------------------------------------------
# PROGRAM ENTRY POINT
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
