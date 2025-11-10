import json
import os

class Exporter:
    def __init__(self, output_path: str):
        self.output_path = output_path
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    def export(self, reviews: list):
        try:
            with open(self.output_path, "w", encoding="utf-8") as f:
                json.dump(reviews, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error exporting data: {e}")