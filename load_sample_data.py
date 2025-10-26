"""
Sample Data Loader for Library Database
Populates the database with sample books, authors, members, and loans
"""

from library_db import LibraryDatabase
from datetime import datetime, timedelta
import random


def load_sample_data():
    """Load sample data into the library database"""
    db = LibraryDatabase()
    db.connect()
    
    print("Initializing database schema...")
    db.initialize_schema()
    
    print("\nAdding categories...")
    categories = [
        ("Fiction", "Fictional literature including novels and short stories"),
        ("Non-Fiction", "Factual books including biographies and textbooks"),
        ("Science Fiction", "Speculative fiction based on scientific concepts"),
        ("Mystery", "Mystery and detective fiction"),
        ("Romance", "Romantic fiction"),
        ("Biography", "Life stories of real people"),
        ("History", "Historical accounts and analysis"),
        ("Science", "Scientific literature and research"),
        ("Technology", "Books about technology and computing"),
        ("Self-Help", "Personal development and self-improvement"),
        ("Children", "Books for children"),
        ("Fantasy", "Fantasy literature with magical elements"),
    ]
    
    category_ids = {}
    for name, desc in categories:
        cat_id = db.add_category(name, desc)
        category_ids[name] = cat_id
        print(f"  Added category: {name}")
    
    print("\nAdding publishers...")
    publishers = [
        ("Penguin Random House", "1745 Broadway, New York, NY", "212-782-9000", "info@penguinrandomhouse.com", "www.penguinrandomhouse.com"),
        ("HarperCollins", "195 Broadway, New York, NY", "212-207-7000", "info@harpercollins.com", "www.harpercollins.com"),
        ("Simon & Schuster", "1230 Avenue of the Americas, New York, NY", "212-698-7000", "info@simonandschuster.com", "www.simonandschuster.com"),
        ("Macmillan Publishers", "120 Broadway, New York, NY", "646-307-5151", "info@macmillan.com", "www.macmillan.com"),
        ("Hachette Book Group", "1290 Avenue of the Americas, New York, NY", "212-364-1100", "info@hbgusa.com", "www.hachettebookgroup.com"),
    ]
    
    publisher_ids = {}
    for name, addr, phone, email, web in publishers:
        pub_id = db.add_publisher(name, addr, phone, email, web)
        publisher_ids[name] = pub_id
        print(f"  Added publisher: {name}")
    
    print("\nAdding authors...")
    authors = [
        ("George", "Orwell", "1903-06-25", "British", "Eric Arthur Blair, known by his pen name George Orwell, was an English novelist and essayist."),
        ("Jane", "Austen", "1775-12-16", "British", "Jane Austen was an English novelist known for her six major novels."),
        ("Mark", "Twain", "1835-11-30", "American", "Samuel Langhorne Clemens, known by his pen name Mark Twain, was an American writer and humorist."),
        ("J.K.", "Rowling", "1965-07-31", "British", "Joanne Rowling, known by her pen name J.K. Rowling, is a British author and screenwriter."),
        ("Stephen", "King", "1947-09-21", "American", "Stephen Edwin King is an American author of horror, supernatural fiction, and suspense."),
        ("Agatha", "Christie", "1890-09-15", "British", "Dame Agatha Mary Clarissa Christie was an English writer of detective novels."),
        ("Isaac", "Asimov", "1920-01-02", "American", "Isaac Asimov was an American writer and professor of biochemistry."),
        ("Virginia", "Woolf", "1882-01-25", "British", "Adeline Virginia Woolf was an English writer and modernist."),
        ("Ernest", "Hemingway", "1899-07-21", "American", "Ernest Miller Hemingway was an American novelist, short-story writer, and journalist."),
        ("Toni", "Morrison", "1931-02-18", "American", "Chloe Anthony Wofford Morrison was an American novelist."),
        ("Margaret", "Atwood", "1939-11-18", "Canadian", "Margaret Eleanor Atwood is a Canadian poet, novelist, and literary critic."),
        ("Haruki", "Murakami", "1949-01-12", "Japanese", "Haruki Murakami is a Japanese writer."),
    ]
    
    author_ids = {}
    for fname, lname, birth, nation, bio in authors:
        auth_id = db.add_author(fname, lname, birth, nation, bio)
        author_ids[f"{fname} {lname}"] = auth_id
        print(f"  Added author: {fname} {lname}")
    
    print("\nAdding books...")
    books = [
        # (isbn, title, author_name, publisher, pub_date, category, pages, description, shelf, copies)
        ("9780451524935", "1984", "George Orwell", "Penguin Random House", "1949-06-08", "Fiction", 328, 
         "A dystopian social science fiction novel and cautionary tale.", "A-101", 5),
        ("9780141439518", "Pride and Prejudice", "Jane Austen", "Penguin Random House", "1813-01-28", "Fiction", 432,
         "A romantic novel of manners.", "A-205", 3),
        ("9780486280615", "Adventures of Huckleberry Finn", "Mark Twain", "HarperCollins", "1884-12-10", "Fiction", 366,
         "A novel about a young boy's adventures along the Mississippi River.", "B-102", 4),
        ("9780439708180", "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Scholastic", "1997-06-26", "Fantasy", 309,
         "The first novel in the Harry Potter series.", "C-301", 8),
        ("9780307743657", "The Shining", "Stephen King", "Penguin Random House", "1977-01-28", "Fiction", 447,
         "A horror novel about a family in an isolated hotel.", "D-105", 4),
        ("9780062073488", "And Then There Were None", "Agatha Christie", "HarperCollins", "1939-11-06", "Mystery", 272,
         "A mystery novel about ten strangers invited to an island.", "E-202", 6),
        ("9780553293357", "Foundation", "Isaac Asimov", "Penguin Random House", "1951-06-01", "Science Fiction", 255,
         "First book in the Foundation series about the fall of a galactic empire.", "F-401", 3),
        ("9780156907392", "Mrs. Dalloway", "Virginia Woolf", "HarperCollins", "1925-05-14", "Fiction", 194,
         "A novel about a day in the life of Clarissa Dalloway.", "A-308", 2),
        ("9780684801223", "The Old Man and the Sea", "Ernest Hemingway", "Simon & Schuster", "1952-09-01", "Fiction", 127,
         "A short novel about an aging fisherman's struggle with a giant marlin.", "B-201", 5),
        ("9781400033416", "Beloved", "Toni Morrison", "Penguin Random House", "1987-09-16", "Fiction", 324,
         "A novel about the aftermath of slavery.", "A-405", 3),
        ("9780385490818", "The Handmaid's Tale", "Margaret Atwood", "Penguin Random House", "1985-08-01", "Science Fiction", 311,
         "A dystopian novel set in a totalitarian theocracy.", "F-302", 6),
        ("9780307593313", "Norwegian Wood", "Haruki Murakami", "Penguin Random House", "1987-09-04", "Fiction", 296,
         "A nostalgic story of loss and sexuality in 1960s Tokyo.", "A-501", 4),
        ("9780141036144", "Animal Farm", "George Orwell", "Penguin Random House", "1945-08-17", "Fiction", 112,
         "A satirical allegorical novella about Soviet Russia.", "A-103", 7),
        ("9780060935467", "To Kill a Mockingbird", "Harper Lee", "HarperCollins", "1960-07-11", "Fiction", 324,
         "A novel about racial injustice in the American South.", "B-304", 5),
    ]
    
    # Note: Harper Lee not in authors list, so we'll add her
    lee_id = db.add_author("Harper", "Lee", "1926-04-28", "American", 
                           "Nelle Harper Lee was an American novelist best known for To Kill a Mockingbird.")
    author_ids["Harper Lee"] = lee_id
    
    book_ids = {}
    for isbn, title, author_name, publisher, pub_date, category, pages, desc, shelf, copies in books:
        # Get category and publisher IDs
        cat_id = category_ids.get(category)
        # Use first publisher if specific one not found
        pub_id = publisher_ids.get(publisher, list(publisher_ids.values())[0])
        
        book_id = db.add_book(isbn, title, pub_id, pub_date, None, "English", 
                             pages, desc, cat_id, shelf, copies)
        
        if book_id > 0:
            # Link to author
            auth_id = author_ids.get(author_name)
            if auth_id:
                db.link_book_author(book_id, auth_id)
            book_ids[title] = book_id
            print(f"  Added book: {title}")
    
    print("\nAdding members...")
    members = [
        ("MEM001", "Alice", "Johnson", "alice.johnson@email.com", "555-0101", "123 Oak St", "1990-05-15", "Premium"),
        ("MEM002", "Bob", "Smith", "bob.smith@email.com", "555-0102", "456 Maple Ave", "1985-08-22", "Standard"),
        ("MEM003", "Carol", "Davis", "carol.davis@email.com", "555-0103", "789 Pine Rd", "1992-11-30", "Standard"),
        ("MEM004", "David", "Wilson", "david.wilson@email.com", "555-0104", "321 Elm St", "1988-03-10", "Premium"),
        ("MEM005", "Emma", "Brown", "emma.brown@email.com", "555-0105", "654 Cedar Ln", "1995-07-25", "Standard"),
        ("MEM006", "Frank", "Miller", "frank.miller@email.com", "555-0106", "987 Birch Dr", "1982-12-05", "Standard"),
        ("MEM007", "Grace", "Taylor", "grace.taylor@email.com", "555-0107", "147 Spruce Way", "1993-09-18", "Student"),
        ("MEM008", "Henry", "Anderson", "henry.anderson@email.com", "555-0108", "258 Willow Ct", "1987-04-12", "Premium"),
    ]
    
    member_ids = {}
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    
    for mem_num, fname, lname, email, phone, addr, dob, mem_type in members:
        mem_id = db.add_member(mem_num, fname, lname, email, phone, addr, dob, 
                              mem_type, start_date, end_date)
        member_ids[mem_num] = mem_id
        print(f"  Added member: {fname} {lname}")
    
    print("\nCreating sample loans...")
    # Create some active loans
    sample_loans = [
        (book_ids.get("1984"), member_ids.get("MEM001"), 14),
        (book_ids.get("Pride and Prejudice"), member_ids.get("MEM002"), 14),
        (book_ids.get("Harry Potter and the Sorcerer's Stone"), member_ids.get("MEM003"), 21),
        (book_ids.get("The Shining"), member_ids.get("MEM004"), 14),
        (book_ids.get("Norwegian Wood"), member_ids.get("MEM005"), 14),
    ]
    
    for book_id, member_id, days in sample_loans:
        if book_id and member_id:
            loan_id = db.create_loan(book_id, member_id, days)
            if loan_id > 0:
                print(f"  Created loan ID: {loan_id}")
    
    print("\nAdding sample reviews...")
    # Add some reviews
    reviews = [
        (book_ids.get("1984"), member_ids.get("MEM001"), 5, "A masterpiece of dystopian fiction. Highly recommended!"),
        (book_ids.get("Pride and Prejudice"), member_ids.get("MEM002"), 4, "Wonderful romance with great character development."),
        (book_ids.get("Harry Potter and the Sorcerer's Stone"), member_ids.get("MEM003"), 5, "Magical and engaging! Perfect for all ages."),
        (book_ids.get("The Shining"), member_ids.get("MEM004"), 5, "Terrifying and brilliantly written."),
        (book_ids.get("Foundation"), member_ids.get("MEM005"), 4, "Great sci-fi classic with interesting concepts."),
    ]
    
    for book_id, member_id, rating, review_text in reviews:
        if book_id and member_id:
            review_id = db.add_review(book_id, member_id, rating, review_text)
            if review_id > 0:
                print(f"  Added review ID: {review_id}")
    
    print("\n" + "="*50)
    print("Sample data loaded successfully!")
    print("="*50)
    
    # Display statistics
    stats = db.get_statistics()
    print("\nLibrary Statistics:")
    print(f"  Total Books: {stats['total_books']}")
    print(f"  Total Authors: {stats['total_authors']}")
    print(f"  Active Members: {stats['active_members']}")
    print(f"  Active Loans: {stats['active_loans']}")
    print(f"  Overdue Loans: {stats['overdue_loans']}")
    
    print("\nAvailable Books:")
    available = db.get_available_books()
    for book in available[:10]:  # Show first 10
        print(f"  - {book['title']} by {book['authors']} ({book['available_copies']}/{book['total_copies']} available)")
    
    db.close()
    print("\nDatabase connection closed.")


if __name__ == "__main__":
    load_sample_data()
