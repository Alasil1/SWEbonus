from flask import Blueprint, request, jsonify
from data_access import get_all_books, save_books

books_bp = Blueprint('books', __name__)

@books_bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if not data or 'title' not in data or 'author' not in data or 'publishedYear' not in data or 'isbn' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    books = get_all_books()
    if any(b['isbn'] == data['isbn'] for b in books):
        return jsonify({"error": "Book with this ISBN already exists"}), 409

    new_book = {
        "title": data['title'],
        "author": data['author'],
        "publishedYear": data['publishedYear'],
        "isbn": data['isbn'],
        "genre": data.get('genre', None)
    }
    books.append(new_book)
    save_books(books)
    return jsonify(new_book), 201

@books_bp.route('/books', methods=['GET'])
def list_books():
    books = get_all_books()
    return jsonify(books), 200

@books_bp.route('/books/search', methods=['GET'])
def search_books():
    author = request.args.get('author')
    year = request.args.get('year')
    genre = request.args.get('genre')
    books = get_all_books()

    if author:
        books = [b for b in books if author.lower() in b['author'].lower()]
    if year:
        books = [b for b in books if str(b['publishedYear']) == year]
    if genre:
        books = [b for b in books if b['genre'] and genre.lower() in b['genre'].lower()]

    return jsonify(books), 200

@books_bp.route('/books/<string:isbn>', methods=['DELETE'])
def delete_book(isbn):
    books = get_all_books()
    book_to_delete = next((b for b in books if b['isbn'] == isbn), None)
    if not book_to_delete:
        return jsonify({"error": "Book not found"}), 404
    
    books = [b for b in books if b['isbn'] != isbn]
    save_books(books)
    return jsonify({"message": "Book deleted", "book": book_to_delete}), 200

@books_bp.route('/books/<string:isbn>', methods=['PUT'])
def update_book(isbn):
    data = request.get_json()
    books = get_all_books()
    book = next((b for b in books if b['isbn'] == isbn), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    if 'title' in data:
        book['title'] = data['title']
    if 'author' in data:
        book['author'] = data['author']
    if 'publishedYear' in data:
        book['publishedYear'] = data['publishedYear']
    if 'genre' in data:
        book['genre'] = data['genre']

    save_books(books)
    return jsonify(book), 200
