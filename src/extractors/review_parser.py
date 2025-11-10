import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .utils_cleaner import clean_text

class ReviewParser:
    def __init__(self, config):
        self.headers = config.get("headers", {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        self.locale = config.get("locale", "de-DE")

    def scrape_reviews(self, product_url: str):
        try:
            response = requests.get(product_url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching {product_url}: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        reviews = []

        review_elements = soup.select(".review-item, .product-review")
        for element in review_elements:
            try:
                rating_el = element.select_one(".star-rating, .rating")
                rating = int(rating_el.get("data-rating", 0)) if rating_el else 0

                title_el = element.select_one(".review-title")
                text_el = element.select_one(".review-text, .content")
                author_el = element.select_one(".author-name")
                date_el = element.select_one("time")

                review = {
                    "productUrl": product_url,
                    "reviewId": hash(product_url + (title_el.text if title_el else "")),
                    "rating": rating,
                    "datePublished": date_el.get("datetime") if date_el else None,
                    "score": rating / 5,
                    "author": clean_text(author_el.text if author_el else "Anonymous"),
                    "date": clean_text(date_el.text if date_el else ""),
                    "isProductTest": False,
                    "isVerifiedPurchase": "verified" in element.text.lower(),
                    "storefront": {
                        "ident": self.locale.split("-")[0],
                        "locale": self.locale,
                        "domain": "kaufland.de"
                    },
                    "text": clean_text(text_el.text if text_el else ""),
                    "title": clean_text(title_el.text if title_el else ""),
                    "translation": None,
                    "variantAttributes": []
                }
                reviews.append(review)
            except Exception as e:
                print(f"Error parsing review: {e}")
        return reviews