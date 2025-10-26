#!/usr/bin/env python3
"""
Library Database Examples
Demonstrates various operations with the library database
"""

from library_db import LibraryDatabase


def main():
    """Run example operations"""
    print("="*70)
    print("LIBRARY DATABASE EXAMPLES")
    print("="*70)
    
    # Connect to database
    db = LibraryDatabase("example_library.db")
    db.connect()
    
    # Initialize schema
    print("\n1. Initializing database schema...")
    db.initialize_schema()
    print("   ✓ Schema initialized")
    
    # Add categories
    print("\n2. Adding categories...")
    fiction_id = db.add_category("Fiction", "Fictional literature")
    scifi_id = db.add_category("Science Fiction", "Speculative science-based fiction")
    print(f"   ✓ Added Fiction (ID: {fiction_id})")
    print(f"   ✓ Added Science Fiction (ID: {scifi_id})")
    
    # Add publishers
    print("\n3. Adding publishers...")
    publisher_id = db.add_publisher(
        "Example Publishing House",
        "123 Book Street, New York, NY",
        "555-1234",
        "info@examplepub.com",
        "www.examplepub.com"
    )
    print(f"   ✓ Added publisher (ID: {publisher_id})")
    
    # Add authors
    print("\n4. Adding authors...")
    author1_id = db.add_author(
        "Isaac", "Asimov",
        "1920-01-02", "American",
        "Renowned science fiction author and biochemist"
    )
    author2_id = db.add_author(
        "Ursula", "Le Guin",
        "1929-10-21", "American",
        "Award-winning science fiction and fantasy author"
    )
    print(f"   ✓ Added Isaac Asimov (ID: {author1_id})")
    print(f"   ✓ Added Ursula Le Guin (ID: {author2_id})")
    
    # Add books
    print("\n5. Adding books...")
    book1_id = db.add_book(
        isbn="9780553293357",
        title="Foundation",
        publisher_id=publisher_id,
        publication_date="1951-06-01",
        language="English",
        pages=255,
        description="First book in the Foundation series",
        category_id=scifi_id,
        shelf_location="SF-101",
        total_copies=3
    )
    
    book2_id = db.add_book(
        isbn="9780441172719",
        title="The Left Hand of Darkness",
        publisher_id=publisher_id,
        publication_date="1969-03-01",
        language="English",
        pages=304,
        description="Groundbreaking science fiction novel",
        category_id=scifi_id,
        shelf_location="SF-102",
        total_copies=2
    )
    print(f"   ✓ Added Foundation (ID: {book1_id})")
    print(f"   ✓ Added The Left Hand of Darkness (ID: {book2_id})")
    
    # Link books to authors
    print("\n6. Linking books to authors...")
    db.link_book_author(book1_id, author1_id)
    db.link_book_author(book2_id, author2_id)
    print("   ✓ Books linked to their authors")
    
    # Add members
    print("\n7. Adding library members...")
    member1_id = db.add_member(
        "MEM001", "Alice", "Johnson",
        "alice@example.com", "555-0101",
        "123 Oak Street", "1990-05-15",
        "Premium"
    )
    member2_id = db.add_member(
        "MEM002", "Bob", "Smith",
        "bob@example.com", "555-0102",
        "456 Maple Avenue", "1985-08-22",
        "Standard"
    )
    print(f"   ✓ Added Alice Johnson (ID: {member1_id})")
    print(f"   ✓ Added Bob Smith (ID: {member2_id})")
    
    # Create loans
    print("\n8. Creating loans...")
    loan1_id = db.create_loan(book1_id, member1_id, loan_days=14)
    loan2_id = db.create_loan(book2_id, member2_id, loan_days=21)
    print(f"   ✓ Alice borrowed Foundation (Loan ID: {loan1_id})")
    print(f"   ✓ Bob borrowed The Left Hand of Darkness (Loan ID: {loan2_id})")
    
    # Add reviews
    print("\n9. Adding book reviews...")
    review1_id = db.add_review(
        book1_id, member1_id, 5,
        "An absolute masterpiece of science fiction! The psychohistory concept is brilliant."
    )
    review2_id = db.add_review(
        book2_id, member2_id, 4,
        "Thought-provoking and imaginative. Le Guin's world-building is exceptional."
    )
    print(f"   ✓ Added review for Foundation (ID: {review1_id})")
    print(f"   ✓ Added review for The Left Hand of Darkness (ID: {review2_id})")
    
    # Search for books
    print("\n10. Searching for books...")
    results = db.search_books("Foundation")
    print(f"   ✓ Found {len(results)} book(s) matching 'Foundation':")
    for book in results:
        print(f"     - {book['title']} by {book['authors']}")
    
    # View available books
    print("\n11. Viewing available books...")
    available = db.get_available_books()
    print(f"   ✓ {len(available)} book(s) available:")
    for book in available:
        print(f"     - {book['title']} ({book['available_copies']}/{book['total_copies']} available)")
    
    # View member loan history
    print("\n12. Viewing Alice's loan history...")
    loans = db.get_member_loans(member1_id)
    print(f"   ✓ Alice has {len(loans)} loan(s):")
    for loan in loans:
        print(f"     - {loan['title']} (Status: {loan['status']})")
    
    # Return a book
    print("\n13. Returning a book...")
    success = db.return_book(loan1_id)
    if success:
        print(f"   ✓ Foundation returned successfully")
    
    # Check updated availability
    print("\n14. Checking updated availability...")
    available = db.get_available_books()
    for book in available:
        if book['book_id'] == book1_id:
            print(f"   ✓ Foundation now has {book['available_copies']}/{book['total_copies']} copies available")
    
    # Get statistics
    print("\n15. Library Statistics:")
    stats = db.get_statistics()
    print(f"   Total Books:        {stats['total_books']}")
    print(f"   Total Authors:      {stats['total_authors']}")
    print(f"   Active Members:     {stats['active_members']}")
    print(f"   Active Loans:       {stats['active_loans']}")
    print(f"   Overdue Loans:      {stats['overdue_loans']}")
    
    # Close connection
    db.close()
    
    print("\n" + "="*70)
    print("EXAMPLES COMPLETED SUCCESSFULLY")
    print("="*70)
    print(f"\nThe example database has been created as 'example_library.db'")
    print("You can explore it using any SQLite browser or the library_cli.py tool.")
    print("\nTo use the CLI with this database:")
    print("  python library_cli.py  (then manually change the db file in the code)")
    print("\nOr open it directly with sqlite3:")
    print("  sqlite3 example_library.db")


if __name__ == "__main__":
    main()
