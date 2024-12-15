import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'books.json')

def get_all_books():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_books(books):
    with open(DATA_FILE, 'w') as f:
        json.dump(books, f, indent=2)
