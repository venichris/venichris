"""
Library Database Manager
A Python script to initialize and manage the library database
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Tuple, Optional

class LibraryDatabase:
    """Main class for managing the library database"""
    
    def __init__(self, db_path: str = "library.db"):
        """Initialize the database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Connect to the database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        print(f"Connected to database: {self.db_path}")
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")
    
    def initialize_schema(self, schema_file: str = "library_schema.sql"):
        """Initialize the database schema from SQL file"""
        if not os.path.exists(schema_file):
            print(f"Error: Schema file {schema_file} not found")
            return False
        
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        try:
            self.cursor.executescript(schema_sql)
            self.conn.commit()
            print("Database schema initialized successfully")
            return True
        except sqlite3.Error as e:
            print(f"Error initializing schema: {e}")
            return False
    
    def add_author(self, first_name: str, last_name: str, 
                   birth_date: str = None, nationality: str = None, 
                   biography: str = None) -> int:
        """Add a new author to the database"""
        sql = """INSERT INTO authors (first_name, last_name, birth_date, nationality, biography)
                 VALUES (?, ?, ?, ?, ?)"""
        try:
            self.cursor.execute(sql, (first_name, last_name, birth_date, nationality, biography))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding author: {e}")
            return -1
    
    def add_publisher(self, name: str, address: str = None, 
                      phone: str = None, email: str = None, 
                      website: str = None) -> int:
        """Add a new publisher to the database"""
        sql = """INSERT INTO publishers (name, address, phone, email, website)
                 VALUES (?, ?, ?, ?, ?)"""
        try:
            self.cursor.execute(sql, (name, address, phone, email, website))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding publisher: {e}")
            return -1
    
    def add_category(self, name: str, description: str = None) -> int:
        """Add a new category to the database"""
        sql = """INSERT INTO categories (name, description)
                 VALUES (?, ?)"""
        try:
            self.cursor.execute(sql, (name, description))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding category: {e}")
            return -1
    
    def add_book(self, isbn: str, title: str, publisher_id: int = None,
                 publication_date: str = None, edition: str = None,
                 language: str = "English", pages: int = None,
                 description: str = None, category_id: int = None,
                 shelf_location: str = None, total_copies: int = 1) -> int:
        """Add a new book to the database"""
        sql = """INSERT INTO books (isbn, title, publisher_id, publication_date, 
                 edition, language, pages, description, category_id, shelf_location, 
                 total_copies, available_copies)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        try:
            self.cursor.execute(sql, (isbn, title, publisher_id, publication_date,
                                     edition, language, pages, description, category_id,
                                     shelf_location, total_copies, total_copies))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding book: {e}")
            return -1
    
    def link_book_author(self, book_id: int, author_id: int, author_order: int = 1):
        """Link a book to an author"""
        sql = """INSERT INTO book_authors (book_id, author_id, author_order)
                 VALUES (?, ?, ?)"""
        try:
            self.cursor.execute(sql, (book_id, author_id, author_order))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error linking book to author: {e}")
            return False
    
    def add_member(self, membership_number: str, first_name: str, last_name: str,
                   email: str, phone: str = None, address: str = None,
                   date_of_birth: str = None, membership_type: str = "Standard",
                   membership_start_date: str = None, membership_end_date: str = None) -> int:
        """Add a new member to the database"""
        if not membership_start_date:
            membership_start_date = datetime.now().strftime("%Y-%m-%d")
        
        sql = """INSERT INTO members (membership_number, first_name, last_name, email,
                 phone, address, date_of_birth, membership_type, membership_start_date,
                 membership_end_date, status)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Active')"""
        try:
            self.cursor.execute(sql, (membership_number, first_name, last_name, email,
                                     phone, address, date_of_birth, membership_type,
                                     membership_start_date, membership_end_date))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding member: {e}")
            return -1
    
    def create_loan(self, book_id: int, member_id: int, 
                    loan_days: int = 14) -> int:
        """Create a new loan record"""
        loan_date = datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.now() + timedelta(days=loan_days)).strftime("%Y-%m-%d")
        
        # Check if book is available
        self.cursor.execute("SELECT available_copies FROM books WHERE book_id = ?", (book_id,))
        result = self.cursor.fetchone()
        
        if not result or result[0] <= 0:
            print("Book is not available for loan")
            return -1
        
        sql = """INSERT INTO loans (book_id, member_id, loan_date, due_date, status)
                 VALUES (?, ?, ?, ?, 'Active')"""
        try:
            self.cursor.execute(sql, (book_id, member_id, loan_date, due_date))
            # Update available copies
            self.cursor.execute("""UPDATE books SET available_copies = available_copies - 1
                                  WHERE book_id = ?""", (book_id,))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating loan: {e}")
            self.conn.rollback()
            return -1
    
    def return_book(self, loan_id: int) -> bool:
        """Process a book return"""
        return_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            # Get book_id from loan
            self.cursor.execute("SELECT book_id FROM loans WHERE loan_id = ?", (loan_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print("Loan not found")
                return False
            
            book_id = result[0]
            
            # Update loan status
            self.cursor.execute("""UPDATE loans SET return_date = ?, status = 'Returned'
                                  WHERE loan_id = ?""", (return_date, loan_id))
            # Update available copies
            self.cursor.execute("""UPDATE books SET available_copies = available_copies + 1
                                  WHERE book_id = ?""", (book_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error returning book: {e}")
            self.conn.rollback()
            return False
    
    def search_books(self, search_term: str) -> List[sqlite3.Row]:
        """Search for books by title, author, or ISBN"""
        sql = """SELECT DISTINCT b.book_id, b.isbn, b.title, 
                 GROUP_CONCAT(a.first_name || ' ' || a.last_name, ', ') AS authors,
                 c.name AS category, b.available_copies, b.total_copies
                 FROM books b
                 LEFT JOIN book_authors ba ON b.book_id = ba.book_id
                 LEFT JOIN authors a ON ba.author_id = a.author_id
                 LEFT JOIN categories c ON b.category_id = c.category_id
                 WHERE b.title LIKE ? OR b.isbn LIKE ? OR 
                       a.first_name LIKE ? OR a.last_name LIKE ?
                 GROUP BY b.book_id"""
        search_pattern = f"%{search_term}%"
        self.cursor.execute(sql, (search_pattern, search_pattern, search_pattern, search_pattern))
        return self.cursor.fetchall()
    
    def get_available_books(self) -> List[sqlite3.Row]:
        """Get all available books"""
        sql = "SELECT * FROM available_books"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def get_overdue_loans(self) -> List[sqlite3.Row]:
        """Get all overdue loans"""
        sql = "SELECT * FROM overdue_loans"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def get_member_loans(self, member_id: int) -> List[sqlite3.Row]:
        """Get all loans for a specific member"""
        sql = """SELECT l.loan_id, b.title, l.loan_date, l.due_date, 
                 l.return_date, l.status
                 FROM loans l
                 JOIN books b ON l.book_id = b.book_id
                 WHERE l.member_id = ?
                 ORDER BY l.loan_date DESC"""
        self.cursor.execute(sql, (member_id,))
        return self.cursor.fetchall()
    
    def add_review(self, book_id: int, member_id: int, rating: int, 
                   review_text: str = None) -> int:
        """Add a book review"""
        review_date = datetime.now().strftime("%Y-%m-%d")
        sql = """INSERT INTO reviews (book_id, member_id, rating, review_text, review_date)
                 VALUES (?, ?, ?, ?, ?)"""
        try:
            self.cursor.execute(sql, (book_id, member_id, rating, review_text, review_date))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding review: {e}")
            return -1
    
    def get_statistics(self) -> dict:
        """Get library statistics"""
        stats = {}
        
        # Total books
        self.cursor.execute("SELECT COUNT(*) FROM books")
        stats['total_books'] = self.cursor.fetchone()[0]
        
        # Total members
        self.cursor.execute("SELECT COUNT(*) FROM members WHERE status = 'Active'")
        stats['active_members'] = self.cursor.fetchone()[0]
        
        # Active loans
        self.cursor.execute("SELECT COUNT(*) FROM loans WHERE status = 'Active'")
        stats['active_loans'] = self.cursor.fetchone()[0]
        
        # Overdue loans
        self.cursor.execute("SELECT COUNT(*) FROM loans WHERE status = 'Active' AND due_date < DATE('now')")
        stats['overdue_loans'] = self.cursor.fetchone()[0]
        
        # Total authors
        self.cursor.execute("SELECT COUNT(*) FROM authors")
        stats['total_authors'] = self.cursor.fetchone()[0]
        
        return stats


def main():
    """Main function to demonstrate database usage"""
    db = LibraryDatabase()
    db.connect()
    
    # Initialize schema
    db.initialize_schema()
    
    # Get statistics
    stats = db.get_statistics()
    print("\nLibrary Statistics:")
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    db.close()


if __name__ == "__main__":
    main()
