from flask import Flask, render_template, request, redirect, url_for
from mongita import MongitaClientDisk
import os
import json 
app = Flask(__name__)

# ------------------------------------------
# Mongita Setup (local embedded NoSQL DB)
# ------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
client = MongitaClientDisk(os.path.join(BASE_DIR, "mongita_data"))

db = client.bookstore
categories_col = db.category
books_col = db.book


# ------------------------------------------
# Helper Functions
# ------------------------------------------
def get_categories():
    categories = list(categories_col.find())
    return sorted(categories, key=lambda c: c["categoryName"])


def get_next_book_id():
    books = list(books_col.find())

    if not books:
        return 1

    return max(book["bookId"] for book in books) + 1


# ------------------------------------------
# HOME PAGE
# ------------------------------------------
@app.route("/", methods=["GET"])
def home():
    categories = get_categories()
    return render_template("index.html", categories=categories)

# READ ALL BOOKS  /read
@app.route("/read", methods=["GET"])
def read():
    categories = get_categories()
    books = sorted(list(books_col.find()), key=lambda b: b["title"])
    return render_template("read.html", categories=categories, books=books)


# ------------------------------------------
# CATEGORY PAGE
# /category?categoryId=1
# ------------------------------------------
@app.route("/category", methods=["GET"])
def category():
    category_id = request.args.get("categoryId", type=int)

    categories = get_categories()
    selected_category = categories_col.find_one({"categoryId": category_id})

    books = list(books_col.find({"categoryId": category_id}))
    books = sorted(books, key=lambda b: b["title"])

    return render_template(
        "category.html",
        categories=categories,
        selectedCategory=selected_category,
        books=books,
        searchTerm=None,
        nothingFound=False
    )


# ------------------------------------------
# SEARCH
# ------------------------------------------
@app.route("/search", methods=["POST"])
def search():
    term = request.form.get("search", "").strip()

    categories = get_categories()
    all_books = list(books_col.find())

    books = [
        book for book in all_books
        if term.lower() in book["title"].lower()
    ]
    books = sorted(books, key=lambda b: b["title"])

    return render_template(
        "category.html",
        categories=categories,
        selectedCategory=None,
        books=books,
        searchTerm=term,
        nothingFound=(len(books) == 0)
    )


# ------------------------------------------
# BOOK DETAIL PAGE
# /book?bookId=3
# ------------------------------------------
@app.route("/book", methods=["GET"])
def book_detail():
    book_id = request.args.get("bookId", type=int)

    categories = get_categories()
    book = books_col.find_one({"bookId": book_id})

    if not book:
        return render_template("error.html", error="Book not found"), 404

    return render_template(
        "book_detail.html",
        book=book,
        categories=categories
    )


# CREATE BOOK  GET /create  POST /create_post

@app.route("/create", methods=["GET"])
def create():
    categories = get_categories()
    return render_template("create.html", categories=categories)
 
 
@app.route("/create_post", methods=["POST"])
def create_post():
    categories = get_categories()
    title       = request.form.get("title")
    author      = request.form.get("author")
    isbn        = request.form.get("isbn")
    price       = request.form.get("price", type=float)
    image       = request.form.get("image")
    category_id = request.form.get("categoryId", type=int)
    read_now    = int(request.form.get("readNow", 0))
 
    selected_category = next((c for c in categories if c["categoryId"] == category_id), None)
 
    new_book = {
        "bookId":       get_next_book_id(),
        "categoryId":   category_id,
        "categoryName": selected_category["categoryName"] if selected_category else "",
        "title":        title,
        "author":       author,
        "isbn":         isbn,
        "price":        price,
        "image":        image,
        "readNow":      read_now
    }
    books_col.insert_one(new_book)
    return redirect(url_for("read"))
 

# EDIT BOOK  GET /edit/<id>  POST /edit_post/<id>

@app.route("/edit/<int:book_id>", methods=["GET"])
def edit(book_id):
    categories = get_categories()
    book = books_col.find_one({"bookId": book_id})
    if not book:
        return render_template("error.html", categories=categories, error="Book not found"), 404
    return render_template("edit.html", book=book, categories=categories)
 
 
@app.route("/edit_post/<int:book_id>", methods=["POST"])
def edit_post(book_id):
    categories = get_categories()
    title       = request.form.get("title")
    author      = request.form.get("author")
    isbn        = request.form.get("isbn")
    price       = request.form.get("price", type=float)
    image       = request.form.get("image")
    category_id = request.form.get("categoryId", type=int)
    read_now    = int(request.form.get("readNow", 0))
 
    selected_category = next((c for c in categories if c["categoryId"] == category_id), None)
 
    books_col.replace_one({"bookId": book_id}, {
        "bookId":       book_id,
        "categoryId":   category_id,
        "categoryName": selected_category["categoryName"] if selected_category else "",
        "title":        title,
        "author":       author,
        "isbn":         isbn,
        "price":        price,
        "image":        image,
        "readNow":      read_now
    })
    return redirect(url_for("read"))
 
 
# DELETE BOOK  /delete/<id>
@app.route("/delete/<int:book_id>", methods=["GET"])
def delete(book_id):
    books_col.delete_one({"bookId": book_id})
    return redirect(url_for("read"))
 
 

# JSON EXPORT  /export
@app.route("/export", methods=["GET"])
def export():
    def strip_id(docs):
        return [{k: v for k, v in d.items() if k != "_id"} for d in docs]
 
    cats  = strip_id(list(categories_col.find()))
    books = strip_id(list(books_col.find()))
    json.dump(cats,  open(os.path.join(BASE_DIR, "categories.json"), "w"), indent=2)
    json.dump(books, open(os.path.join(BASE_DIR, "books.json"),      "w"), indent=2)
    return redirect(url_for("read"))
 
 
# ------------------------------------------
# ERRORS
# ------------------------------------------
@app.errorhandler(Exception)
def handle_error(e):
    return render_template("error.html", error=e), 500


# ------------------------------------------
# RUN APP
# ------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
