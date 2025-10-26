# Library Database System

A comprehensive library management database system built with SQLite and Python.

## Overview

This library database system provides a complete solution for managing a library's books, authors, members, loans, reservations, fines, and reviews. It includes a well-structured relational database schema with proper constraints, indexes, and views for common queries.

## Features

### Core Features
- **Book Management**: Track books with ISBN, title, authors, publisher, categories, and availability
- **Author Management**: Store author information including biography and nationality
- **Member Management**: Manage library members with membership types and status
- **Loan System**: Handle book checkouts and returns with due dates
- **Reservation System**: Allow members to reserve books
- **Fine Management**: Track and manage overdue fines
- **Review System**: Enable members to rate and review books
- **Staff Management**: Manage library staff information

### Database Features
- Foreign key constraints for data integrity
- Indexes for optimized query performance
- Views for common queries (available books, overdue loans, etc.)
- Triggers and constraints for business logic
- Support for multiple authors per book
- Track book copies and availability

## Database Schema

### Main Tables

1. **authors** - Author information
2. **publishers** - Publisher details
3. **categories** - Book categories
4. **books** - Book catalog with availability tracking
5. **book_authors** - Many-to-many relationship between books and authors
6. **members** - Library members
7. **loans** - Book loan records
8. **reservations** - Book reservations
9. **staff** - Library staff
10. **fines** - Fine records
11. **reviews** - Book reviews and ratings

### Database Views

- **available_books** - All books currently available for loan
- **overdue_loans** - All loans that are past due
- **member_loan_history** - Summary of each member's loan history
- **popular_books** - Books sorted by loan count and ratings

## Installation

### Prerequisites

- Python 3.6 or higher
- SQLite3 (usually included with Python)

### Setup

1. Clone or download this repository
2. Navigate to the project directory
3. No additional dependencies required (uses Python standard library)

## Usage

### Initialize the Database

```bash
python library_db.py
```

This will create an empty library database with all tables, indexes, and views.

### Load Sample Data

```bash
python load_sample_data.py
```

This will:
- Initialize the database schema
- Populate the database with sample books, authors, members, and loans
- Display statistics about the loaded data

### Using the Library Database in Your Code

```python
from library_db import LibraryDatabase

# Create database instance
db = LibraryDatabase("my_library.db")
db.connect()

# Add a new book
author_id = db.add_author("John", "Doe", "1970-01-01", "American")
publisher_id = db.add_publisher("Example Publishing")
category_id = db.add_category("Fiction")

book_id = db.add_book(
    isbn="9781234567890",
    title="Example Book",
    publisher_id=publisher_id,
    category_id=category_id,
    total_copies=3
)

# Link book to author
db.link_book_author(book_id, author_id)

# Add a member
member_id = db.add_member(
    membership_number="MEM001",
    first_name="Jane",
    last_name="Smith",
    email="jane@example.com"
)

# Create a loan
loan_id = db.create_loan(book_id, member_id, loan_days=14)

# Return a book
db.return_book(loan_id)

# Search for books
results = db.search_books("Example")

# Get statistics
stats = db.get_statistics()
print(f"Total books: {stats['total_books']}")

# Close connection
db.close()
```

## API Reference

### LibraryDatabase Class

#### Connection Methods
- `connect()` - Connect to the database
- `close()` - Close the database connection
- `initialize_schema(schema_file)` - Initialize database schema from SQL file

#### Author Methods
- `add_author(first_name, last_name, birth_date, nationality, biography)` - Add a new author

#### Publisher Methods
- `add_publisher(name, address, phone, email, website)` - Add a new publisher

#### Category Methods
- `add_category(name, description)` - Add a new category

#### Book Methods
- `add_book(isbn, title, publisher_id, publication_date, edition, language, pages, description, category_id, shelf_location, total_copies)` - Add a new book
- `link_book_author(book_id, author_id, author_order)` - Link a book to an author
- `search_books(search_term)` - Search for books by title, author, or ISBN
- `get_available_books()` - Get all available books

#### Member Methods
- `add_member(membership_number, first_name, last_name, email, phone, address, date_of_birth, membership_type, membership_start_date, membership_end_date)` - Add a new member
- `get_member_loans(member_id)` - Get all loans for a specific member

#### Loan Methods
- `create_loan(book_id, member_id, loan_days)` - Create a new loan
- `return_book(loan_id)` - Process a book return
- `get_overdue_loans()` - Get all overdue loans

#### Review Methods
- `add_review(book_id, member_id, rating, review_text)` - Add a book review

#### Statistics Methods
- `get_statistics()` - Get library statistics

## Database Schema Diagram

```
authors ──┐
          ├── book_authors ── books ── categories
publishers─┘                   │
                               ├── loans ── members
                               ├── reservations ─┘
                               └── reviews ───────┘

loans ── fines ── members

staff (independent table)
```

## Sample Data

The sample data includes:
- 12 famous authors (George Orwell, Jane Austen, Mark Twain, etc.)
- 5 major publishers
- 12 book categories
- 14 classic books
- 8 library members
- Sample active loans and reviews

## Business Rules

1. **Book Availability**: A book can only be loaned if `available_copies > 0`
2. **Loan Period**: Default loan period is 14 days
3. **Member Status**: Only active members can borrow books
4. **Constraints**:
   - `available_copies` cannot be negative
   - `available_copies` cannot exceed `total_copies`
   - Loan status must be: Active, Returned, Overdue, or Lost
   - Member status must be: Active, Inactive, or Suspended

## File Structure

```
library-database/
├── library_schema.sql       # Database schema definition
├── library_db.py           # Python database management class
├── load_sample_data.py     # Script to load sample data
├── library_cli.py          # Interactive CLI tool
├── examples.py             # Example usage script
├── LIBRARY_README.md       # Complete documentation (this file)
├── QUICKSTART.md           # Quick start guide
├── README.md               # Main repository README
├── requirements.txt        # Python dependencies
└── library.db              # SQLite database file (created on first run)
```

## Extending the System

### Adding New Tables

Add table definitions to `library_schema.sql`:

```sql
CREATE TABLE IF NOT EXISTS new_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- Add your columns here
);
```

### Adding New Methods

Add methods to the `LibraryDatabase` class in `library_db.py`:

```python
def new_method(self, param1, param2):
    """Description of the method"""
    sql = "SELECT * FROM table WHERE column = ?"
    self.cursor.execute(sql, (param1,))
    return self.cursor.fetchall()
```

## Query Examples

### Find all books by a specific author

```sql
SELECT b.title, b.isbn, b.publication_date
FROM books b
JOIN book_authors ba ON b.book_id = ba.book_id
JOIN authors a ON ba.author_id = a.author_id
WHERE a.last_name = 'Orwell';
```

### Find overdue loans

```sql
SELECT * FROM overdue_loans;
```

### Get member borrowing history

```sql
SELECT * FROM member_loan_history 
WHERE member_id = 1;
```

### Find most popular books

```sql
SELECT * FROM popular_books
LIMIT 10;
```

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to extend this database system with additional features such as:
- E-book management
- Digital resource tracking
- Event management
- Room booking system
- Automated fine calculation
- Email notification system
- Advanced reporting

## Support

For questions or issues, please refer to the code documentation or create an issue in the repository.
