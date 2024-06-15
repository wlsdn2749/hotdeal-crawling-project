from typing import Optional, List

def load_valid_categories(file_path: str) -> set:
    with open(file_path, 'r', encoding="utf-8") as f:
        categories = {line.strip() for line in f if line.strip()}
    return categories