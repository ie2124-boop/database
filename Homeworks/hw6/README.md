# Bookstore Database + Python CLI

## Name
Itgel Enkh-Amgalan

## Description
This project is a SQLite-based bookstore database with a Python command-line interface (CLI).  
It allows users to browse categories, view books, search by title, and manage bookstore data by adding, updating, and deleting books.  
An additional feature allows users to view books within a specified price range.

## How to Create the Database

### Step 1: Open SQLite
```bash
sqlite3 bookstore.db
```

### Step 2: Run SQL scripts
```bash
.read createTables.sql
.read insertRows.sql
.exit
```

## How to Run the Python CLI

```bash
python bookstore_cli.py
```