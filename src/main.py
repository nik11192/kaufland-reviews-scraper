import json
import os
from extractors.review_parser import ReviewParser
from outputs.exporters import Exporter
from config import settings_loader

def load_input_urls(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    return urls

def main():
    config = settings_loader.load_settings()
    input_file = os.path.join("data", "inputs.sample.txt")
    output_file = os.path.join("data", "sample_output.json")

    urls = load_input_urls(input_file)
    scraper = ReviewParser(config)
    exporter = Exporter(output_file)

    all_reviews = []
    for url in urls:
        print(f"Scraping: {url}")
        reviews = scraper.scrape_reviews(url)
        all_reviews.extend(reviews)

    exporter.export(all_reviews)
    print(f"Exported {len(all_reviews)} reviews to {output_file}")

if __name__ == "__main__":
    main()