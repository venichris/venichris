#!/usr/bin/env python3
"""
Library Database CLI Tool
Interactive command-line interface for managing the library database
"""

from library_db import LibraryDatabase
import sys


def print_menu():
    """Display the main menu"""
    print("\n" + "="*60)
    print("LIBRARY DATABASE MANAGEMENT SYSTEM")
    print("="*60)
    print("\n1.  Search for books")
    print("2.  View all available books")
    print("3.  View overdue loans")
    print("4.  Add a new book")
    print("5.  Add a new member")
    print("6.  Create a loan")
    print("7.  Return a book")
    print("8.  View member's loan history")
    print("9.  Add a book review")
    print("10. View library statistics")
    print("11. Add a new author")
    print("12. Add a new category")
    print("0.  Exit")
    print("="*60)


def search_books(db):
    """Search for books"""
    search_term = input("Enter search term (title, author, or ISBN): ")
    results = db.search_books(search_term)
    
    if not results:
        print("\nNo books found.")
        return
    
    print(f"\nFound {len(results)} book(s):")
    print("-" * 100)
    for book in results:
        print(f"ID: {book['book_id']}")
        print(f"Title: {book['title']}")
        print(f"Authors: {book['authors']}")
        print(f"ISBN: {book['isbn']}")
        print(f"Category: {book['category']}")
        print(f"Available: {book['available_copies']}/{book['total_copies']}")
        print("-" * 100)


def view_available_books(db):
    """View all available books"""
    books = db.get_available_books()
    
    if not books:
        print("\nNo books available.")
        return
    
    print(f"\nAvailable Books ({len(books)} total):")
    print("-" * 100)
    for book in books:
        print(f"ID: {book['book_id']} | {book['title']} by {book['authors']}")
        print(f"   ISBN: {book['isbn']} | Location: {book['shelf_location']} | Available: {book['available_copies']}/{book['total_copies']}")
        print("-" * 100)


def view_overdue_loans(db):
    """View overdue loans"""
    loans = db.get_overdue_loans()
    
    if not loans:
        print("\nNo overdue loans.")
        return
    
    print(f"\nOverdue Loans ({len(loans)} total):")
    print("-" * 100)
    for loan in loans:
        print(f"Loan ID: {loan['loan_id']}")
        print(f"Book: {loan['book_title']}")
        print(f"Member: {loan['member_name']} ({loan['email']})")
        print(f"Due Date: {loan['due_date']}")
        print(f"Days Overdue: {int(loan['days_overdue'])}")
        print("-" * 100)


def add_book(db):
    """Add a new book"""
    print("\nAdd New Book")
    print("-" * 60)
    
    isbn = input("ISBN: ")
    title = input("Title: ")
    pages = input("Number of pages (optional): ")
    description = input("Description (optional): ")
    shelf_location = input("Shelf location (e.g., A-101): ")
    total_copies = input("Total copies (default 1): ")
    
    pages = int(pages) if pages else None
    total_copies = int(total_copies) if total_copies else 1
    
    book_id = db.add_book(isbn, title, None, None, None, "English", 
                         pages, description, None, shelf_location, total_copies)
    
    if book_id > 0:
        print(f"\n✓ Book added successfully with ID: {book_id}")
    else:
        print("\n✗ Failed to add book.")


def add_member(db):
    """Add a new member"""
    print("\nAdd New Member")
    print("-" * 60)
    
    membership_number = input("Membership Number: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")
    phone = input("Phone (optional): ")
    address = input("Address (optional): ")
    membership_type = input("Membership Type (Standard/Premium/Student, default Standard): ")
    
    if not membership_type:
        membership_type = "Standard"
    
    member_id = db.add_member(membership_number, first_name, last_name, email,
                              phone if phone else None, 
                              address if address else None,
                              None, membership_type)
    
    if member_id > 0:
        print(f"\n✓ Member added successfully with ID: {member_id}")
    else:
        print("\n✗ Failed to add member.")


def create_loan(db):
    """Create a new loan"""
    print("\nCreate New Loan")
    print("-" * 60)
    
    book_id = input("Book ID: ")
    member_id = input("Member ID: ")
    loan_days = input("Loan period in days (default 14): ")
    
    loan_days = int(loan_days) if loan_days else 14
    
    loan_id = db.create_loan(int(book_id), int(member_id), loan_days)
    
    if loan_id > 0:
        print(f"\n✓ Loan created successfully with ID: {loan_id}")
    else:
        print("\n✗ Failed to create loan. Book may not be available.")


def return_book(db):
    """Return a book"""
    print("\nReturn Book")
    print("-" * 60)
    
    loan_id = input("Loan ID: ")
    
    success = db.return_book(int(loan_id))
    
    if success:
        print(f"\n✓ Book returned successfully.")
    else:
        print("\n✗ Failed to return book.")


def view_member_loans(db):
    """View member's loan history"""
    print("\nView Member Loan History")
    print("-" * 60)
    
    member_id = input("Member ID: ")
    loans = db.get_member_loans(int(member_id))
    
    if not loans:
        print("\nNo loans found for this member.")
        return
    
    print(f"\nLoan History ({len(loans)} total):")
    print("-" * 100)
    for loan in loans:
        print(f"Loan ID: {loan['loan_id']}")
        print(f"Book: {loan['title']}")
        print(f"Loan Date: {loan['loan_date']}")
        print(f"Due Date: {loan['due_date']}")
        print(f"Return Date: {loan['return_date'] or 'Not returned'}")
        print(f"Status: {loan['status']}")
        print("-" * 100)


def add_review(db):
    """Add a book review"""
    print("\nAdd Book Review")
    print("-" * 60)
    
    book_id = input("Book ID: ")
    member_id = input("Member ID: ")
    rating = input("Rating (1-5): ")
    review_text = input("Review text (optional): ")
    
    review_id = db.add_review(int(book_id), int(member_id), int(rating), 
                              review_text if review_text else None)
    
    if review_id > 0:
        print(f"\n✓ Review added successfully with ID: {review_id}")
    else:
        print("\n✗ Failed to add review.")


def view_statistics(db):
    """View library statistics"""
    stats = db.get_statistics()
    
    print("\n" + "="*60)
    print("LIBRARY STATISTICS")
    print("="*60)
    print(f"Total Books:        {stats['total_books']}")
    print(f"Total Authors:      {stats['total_authors']}")
    print(f"Active Members:     {stats['active_members']}")
    print(f"Active Loans:       {stats['active_loans']}")
    print(f"Overdue Loans:      {stats['overdue_loans']}")
    print("="*60)


def add_author(db):
    """Add a new author"""
    print("\nAdd New Author")
    print("-" * 60)
    
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    birth_date = input("Birth Date (YYYY-MM-DD, optional): ")
    nationality = input("Nationality (optional): ")
    biography = input("Biography (optional): ")
    
    author_id = db.add_author(first_name, last_name,
                              birth_date if birth_date else None,
                              nationality if nationality else None,
                              biography if biography else None)
    
    if author_id > 0:
        print(f"\n✓ Author added successfully with ID: {author_id}")
    else:
        print("\n✗ Failed to add author.")


def add_category(db):
    """Add a new category"""
    print("\nAdd New Category")
    print("-" * 60)
    
    name = input("Category Name: ")
    description = input("Description (optional): ")
    
    category_id = db.add_category(name, description if description else None)
    
    if category_id > 0:
        print(f"\n✓ Category added successfully with ID: {category_id}")
    else:
        print("\n✗ Failed to add category.")


def main():
    """Main function"""
    print("Connecting to library database...")
    db = LibraryDatabase()
    db.connect()
    
    # Initialize schema if needed
    db.initialize_schema()
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (0-12): ")
        
        try:
            if choice == '0':
                print("\nThank you for using the Library Database Management System!")
                break
            elif choice == '1':
                search_books(db)
            elif choice == '2':
                view_available_books(db)
            elif choice == '3':
                view_overdue_loans(db)
            elif choice == '4':
                add_book(db)
            elif choice == '5':
                add_member(db)
            elif choice == '6':
                create_loan(db)
            elif choice == '7':
                return_book(db)
            elif choice == '8':
                view_member_loans(db)
            elif choice == '9':
                add_review(db)
            elif choice == '10':
                view_statistics(db)
            elif choice == '11':
                add_author(db)
            elif choice == '12':
                add_category(db)
            else:
                print("\n✗ Invalid choice. Please try again.")
        except ValueError as e:
            print(f"\n✗ Invalid input: {e}")
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    db.close()
    print("Database connection closed. Goodbye!")


if __name__ == "__main__":
    main()
