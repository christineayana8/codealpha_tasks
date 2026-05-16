import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

GENRES = [
    "Mystery", "Historical Fiction", "Science Fiction", "Romance", "Thriller",
    "Fantasy", "Biography", "Self Help", "Children's", "Travel", "Horror",
    "Poetry", "Comics", "Business", "Cookbooks", "Psychology", "Philosophy",
    "Sports", "Music", "Art"
]

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
BASE_URL = "http://books.toscrape.com/catalogue/"
START_URL = "http://books.toscrape.com/catalogue/page-1.html"

def scrape_books(max_pages=20):
    books = []
    url = START_URL
    page = 1
    headers = {"User-Agent": "Mozilla/5.0"}

    while url and page <= max_pages:
        print(f"Scraping page {page}...")
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        for article in soup.select("article.product_pod"):
            title = article.h3.a["title"]
            price = float(article.select_one("p.price_color").text.strip().encode("ascii", "ignore").decode().replace("£", "").strip())
            rating = RATING_MAP.get(article.p["class"][1], 0)
            availability = article.select_one("p.availability").text.strip()
            link = BASE_URL + article.h3.a["href"].replace("../", "")

            # Retry logic for detail page
            for attempt in range(3):
                try:
                    detail = requests.get(link, headers=headers, timeout=10)
                    break
                except Exception as e:
                    print(f"  Retrying ({attempt+1}/3)...")
                    time.sleep(3)
            else:
                print(f"  Skipping: {title}")
                continue

            dsoup = BeautifulSoup(detail.text, "html.parser")
            crumbs = dsoup.select("ul.breadcrumb li")
            genre = crumbs[2].text.strip() if len(crumbs) >= 3 else "Unknown"
            desc_tag = dsoup.select_one("#product_description ~ p")
            description = desc_tag.text.strip() if desc_tag else ""

            books.append({
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
                "genre": genre,
                "description": description
            })
            time.sleep(0.3)

        next_btn = soup.select_one("li.next a")
        url = BASE_URL + next_btn["href"] if next_btn else None
        page += 1

    return pd.DataFrame(books)

print("Starting web scrape of books.toscrape.com...")
df = scrape_books(max_pages=20)
df.to_csv("books_data.csv", index=False)
print(f"\n✅ Done! Scraped {len(df)} books.")
print(df.head())
