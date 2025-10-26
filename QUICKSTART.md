# Library Database - Quick Start Guide

## Get Started in 3 Easy Steps

### Step 1: Initialize the Database

Run the following command to create an empty library database:

```bash
python library_db.py
```

This creates `library.db` with all tables, indexes, and views.

### Step 2: Load Sample Data (Optional)

To populate your database with sample books, authors, and members:

```bash
python load_sample_data.py
```

This will add:
- 12 famous authors
- 5 publishers
- 12 categories
- 14 classic books
- 8 members
- 5 active loans
- 5 book reviews

### Step 3: Start Using the Database

#### Example 1: Search for Books

```python
from library_db import LibraryDatabase

db = LibraryDatabase()
db.connect()

# Search for books
results = db.search_books("Orwell")
for book in results:
    print(f"{book['title']} - {book['authors']}")

db.close()
```

#### Example 2: Check Out a Book

```python
from library_db import LibraryDatabase

db = LibraryDatabase()
db.connect()

# Create a loan (book_id=1, member_id=1, 14-day loan)
loan_id = db.create_loan(1, 1, 14)
print(f"Loan created with ID: {loan_id}")

db.close()
```

#### Example 3: View Library Statistics

```python
from library_db import LibraryDatabase

db = LibraryDatabase()
db.connect()

stats = db.get_statistics()
print(f"Total Books: {stats['total_books']}")
print(f"Active Members: {stats['active_members']}")
print(f"Active Loans: {stats['active_loans']}")

db.close()
```

## Common Operations

### Add a New Book

```python
db = LibraryDatabase()
db.connect()

# Add author
author_id = db.add_author("Neil", "Gaiman", "1960-11-10", "British")

# Add publisher
publisher_id = db.add_publisher("HarperCollins")

# Add category
category_id = db.add_category("Fantasy")

# Add book
book_id = db.add_book(
    isbn="9780062255655",
    title="American Gods",
    publisher_id=publisher_id,
    publication_date="2001-06-19",
    language="English",
    pages=465,
    description="A fantasy novel about old gods in modern America",
    category_id=category_id,
    shelf_location="F-505",
    total_copies=3
)

# Link book to author
db.link_book_author(book_id, author_id)

db.close()
```

### Register a New Member

```python
db = LibraryDatabase()
db.connect()

member_id = db.add_member(
    membership_number="MEM009",
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    phone="555-1234",
    address="123 Main St",
    membership_type="Standard"
)

print(f"Member registered with ID: {member_id}")

db.close()
```

### Return a Book

```python
db = LibraryDatabase()
db.connect()

# Return loan with ID 1
success = db.return_book(loan_id=1)
if success:
    print("Book returned successfully")

db.close()
```

### Add a Book Review

```python
db = LibraryDatabase()
db.connect()

review_id = db.add_review(
    book_id=1,
    member_id=1,
    rating=5,
    review_text="Excellent book! Highly recommended."
)

print(f"Review added with ID: {review_id}")

db.close()
```

## Useful Queries

### View All Available Books

```python
db = LibraryDatabase()
db.connect()

books = db.get_available_books()
for book in books:
    print(f"{book['title']} - {book['available_copies']} available")

db.close()
```

### Check for Overdue Loans

```python
db = LibraryDatabase()
db.connect()

overdue = db.get_overdue_loans()
for loan in overdue:
    print(f"{loan['book_title']} - {loan['member_name']} - {loan['days_overdue']} days overdue")

db.close()
```

### View Member's Loan History

```python
db = LibraryDatabase()
db.connect()

loans = db.get_member_loans(member_id=1)
for loan in loans:
    print(f"{loan['title']} - Borrowed: {loan['loan_date']}, Status: {loan['status']}")

db.close()
```

## Database File

The database is stored in `library.db` in the same directory as the Python scripts. You can:
- Open it with any SQLite client
- Back it up by copying the file
- Reset it by deleting the file and running the initialization scripts again

## Need Help?

Refer to `LIBRARY_README.md` for complete documentation including:
- Full API reference
- Database schema details
- Advanced queries
- Extension guide
