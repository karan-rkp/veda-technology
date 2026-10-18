
# ============================================================
# PROJECT: ADVANCED WEB SCRAPING PROGRAM
# TASK 29 - PYTHON PROGRAMMING TRACK
# Website: Books to Scrape (practice website)
# Libraries: requests, BeautifulSoup, csv
# ============================================================

import csv
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


BASE_URL = "https://books.toscrape.com/"
OUTPUT_FILE = Path("books_data.csv")
TIMEOUT = 15
DELAY_SECONDS = 0.5
MAX_PAGES = 50

CSV_FIELDS = [
    "title",
    "price",
    "availability",
    "rating",
    "product_url",
]


def create_session():
    """Create an HTTP session with retry handling."""
    session = requests.Session()

    session.headers.update({
        "User-Agent": "EducationalBookScraper/1.0",
        "Accept": "text/html,application/xhtml+xml",
    })

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


def validate_url(url):
    """Accept only URLs from the practice website."""
    parsed = urlparse(url)

    allowed_hosts = {
        "books.toscrape.com",
        "www.books.toscrape.com",
    }

    return (
        parsed.scheme == "https"
        and parsed.hostname in allowed_hosts
    )


def fetch_html(session, url):
    """Download HTML and handle request errors."""
    if not validate_url(url):
        print("[ERROR] URL is outside the permitted practice website.")
        return None

    try:
        response = session.get(url, timeout=TIMEOUT)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "html" not in content_type.lower():
            print("[ERROR] The server did not return HTML.")
            return None

        return response.text

    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timed out: {url}")

    except requests.exceptions.HTTPError as error:
        print(f"[HTTP ERROR] {error}")

    except requests.exceptions.RequestException as error:
        print(f"[REQUEST ERROR] {error}")

    return None


def clean_text(value):
    """Normalize spaces in extracted text."""
    return " ".join(value.split())


def get_rating(article):
    """Convert the CSS rating class into a readable value."""
    rating_tag = article.select_one(".star-rating")

    if not rating_tag:
        return "Unknown"

    rating_classes = rating_tag.get("class", [])
    valid_ratings = {"One", "Two", "Three", "Four", "Five"}

    for value in rating_classes:
        if value in valid_ratings:
            return value

    return "Unknown"


def extract_books(html, page_url):
    """Extract book details from one catalogue page."""
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for article in soup.select("article.product_pod"):
        title_tag = article.select_one("h3 a")
        price_tag = article.select_one(".price_color")
        availability_tag = article.select_one(".availability")
        link_tag = article.select_one("h3 a")

        if not title_tag or not price_tag:
            continue

        title = clean_text(
            title_tag.get("title")
            or title_tag.get_text(" ", strip=True)
        )

        price = clean_text(price_tag.get_text(" ", strip=True))

        availability = (
            clean_text(availability_tag.get_text(" ", strip=True))
            if availability_tag
            else "Unknown"
        )

        product_url = urljoin(page_url, link_tag.get("href", ""))

        books.append({
            "title": title,
            "price": price,
            "availability": availability,
            "rating": get_rating(article),
            "product_url": product_url,
        })

    return books, soup


def save_to_csv(books):
    """Write all extracted book records to a CSV file."""
    try:
        with OUTPUT_FILE.open(
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=CSV_FIELDS
            )
            writer.writeheader()
            writer.writerows(books)

        print(f"\n[SUCCESS] CSV saved: {OUTPUT_FILE.resolve()}")
        return True

    except OSError as error:
        print(f"[FILE ERROR] Could not save CSV: {error}")
        return False


def scrape_books(start_url, max_pages):
    """Scrape catalogue pages and prevent duplicate records."""
    session = create_session()
    all_books = []
    seen_urls = set()
    current_url = start_url
    pages_scraped = 0

    try:
        while current_url and pages_scraped < max_pages:
            if not validate_url(current_url):
                print("[WARNING] Stopping: unexpected page URL.")
                break

            print(
                f"\n[PAGE {pages_scraped + 1}/{max_pages}] "
                f"Fetching {current_url}"
            )

            html = fetch_html(session, current_url)

            if html is None:
                print("[WARNING] Stopping after a page error.")
                break

            books, soup = extract_books(html, current_url)
            new_books = 0

            for book in books:
                if book["product_url"] not in seen_urls:
                    seen_urls.add(book["product_url"])
                    all_books.append(book)
                    new_books += 1

            pages_scraped += 1

            print(
                f"[OK] Found {new_books} new books "
                f"on page {pages_scraped}."
            )

            next_link = soup.select_one("li.next a")

            if next_link and next_link.get("href"):
                next_url = urljoin(
                    current_url,
                    next_link["href"]
                )

                if validate_url(next_url):
                    current_url = next_url
                else:
                    print("[WARNING] Invalid next-page URL.")
                    break
            else:
                print("[INFO] No more catalogue pages.")
                break

            # Be polite to the practice website.
            time.sleep(DELAY_SECONDS)

    finally:
        session.close()

    print("\n" + "=" * 55)
    print("                 SCRAPING SUMMARY")
    print("=" * 55)
    print(f"Pages processed : {pages_scraped}")
    print(f"Unique books    : {len(all_books)}")

    if all_books:
        save_to_csv(all_books)
        show_preview(all_books)

    else:
        print("No book records were collected.")

    return all_books


def show_preview(books):
    """Display a short preview in the terminal."""
    print("\nBOOK PREVIEW")
    print("-" * 55)

    for number, book in enumerate(books[:5], start=1):
        print(f"\n{number}. {book['title']}")
        print(f"   Price        : {book['price']}")
        print(f"   Availability : {book['availability']}")
        print(f"   Rating       : {book['rating']}")
        print(f"   URL          : {book['product_url']}")

    if len(books) > 5:
        print(f"\n...and {len(books) - 5} more books in the CSV.")


def main():
    print("=" * 55)
    print("          ADVANCED WEB SCRAPING PROGRAM")
    print("=" * 55)
    print("1. Scrape first 5 pages")
    print("2. Scrape all catalogue pages (up to 50)")
    print("3. Enter number of pages")
    print("4. Exit")

    choice = input("\nSelect an option (1-4): ").strip()

    if choice == "1":
        max_pages = 5

    elif choice == "2":
        max_pages = MAX_PAGES

    elif choice == "3":
        try:
            max_pages = int(
                input("Enter pages to scrape (1-50): ").strip()
            )

            if not 1 <= max_pages <= MAX_PAGES:
                print("Please enter a number between 1 and 50.")
                return

        except ValueError:
            print("Invalid input. Enter a whole number.")
            return

    elif choice == "4":
        print("Program closed.")
        return

    else:
        print("Invalid choice.")
        return

    print(f"\nStarting scraper for up to {max_pages} pages...")
    scrape_books(BASE_URL, max_pages)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
