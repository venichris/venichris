-- Library Database Schema
-- A comprehensive database for managing a library system

-- Create Authors table
CREATE TABLE IF NOT EXISTS authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE,
    nationality VARCHAR(100),
    biography TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Publishers table
CREATE TABLE IF NOT EXISTS publishers (
    publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Categories table
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Books table
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn VARCHAR(13) UNIQUE,
    title VARCHAR(300) NOT NULL,
    publisher_id INTEGER,
    publication_date DATE,
    edition VARCHAR(50),
    language VARCHAR(50) DEFAULT 'English',
    pages INTEGER,
    description TEXT,
    category_id INTEGER,
    shelf_location VARCHAR(50),
    total_copies INTEGER DEFAULT 1,
    available_copies INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    CHECK (available_copies >= 0),
    CHECK (available_copies <= total_copies)
);

-- Create Book_Authors junction table (many-to-many relationship)
CREATE TABLE IF NOT EXISTS book_authors (
    book_id INTEGER,
    author_id INTEGER,
    author_order INTEGER DEFAULT 1,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
);

-- Create Members table
CREATE TABLE IF NOT EXISTS members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    membership_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    date_of_birth DATE,
    membership_type VARCHAR(50) DEFAULT 'Standard',
    membership_start_date DATE NOT NULL,
    membership_end_date DATE,
    status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (status IN ('Active', 'Inactive', 'Suspended'))
);

-- Create Loans table
CREATE TABLE IF NOT EXISTS loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    status VARCHAR(20) DEFAULT 'Active',
    renewal_count INTEGER DEFAULT 0,
    fine_amount DECIMAL(10, 2) DEFAULT 0.00,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    CHECK (status IN ('Active', 'Returned', 'Overdue', 'Lost'))
);

-- Create Reservations table
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    reservation_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    notified BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    CHECK (status IN ('Pending', 'Ready', 'Fulfilled', 'Cancelled', 'Expired'))
);

-- Create Staff table
CREATE TABLE IF NOT EXISTS staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    position VARCHAR(100),
    hire_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (status IN ('Active', 'Inactive', 'On Leave'))
);

-- Create Fines table
CREATE TABLE IF NOT EXISTS fines (
    fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    reason VARCHAR(200),
    issue_date DATE NOT NULL,
    paid_date DATE,
    status VARCHAR(20) DEFAULT 'Unpaid',
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    CHECK (status IN ('Unpaid', 'Paid', 'Waived'))
);

-- Create Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    review_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- Create Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_books_isbn ON books(isbn);
CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
CREATE INDEX IF NOT EXISTS idx_books_category ON books(category_id);
CREATE INDEX IF NOT EXISTS idx_members_email ON members(email);
CREATE INDEX IF NOT EXISTS idx_members_membership ON members(membership_number);
CREATE INDEX IF NOT EXISTS idx_loans_status ON loans(status);
CREATE INDEX IF NOT EXISTS idx_loans_member ON loans(member_id);
CREATE INDEX IF NOT EXISTS idx_loans_book ON loans(book_id);
CREATE INDEX IF NOT EXISTS idx_reservations_status ON reservations(status);
CREATE INDEX IF NOT EXISTS idx_fines_status ON fines(status);

-- Create Views for common queries
CREATE VIEW IF NOT EXISTS available_books AS
SELECT 
    b.book_id,
    b.isbn,
    b.title,
    GROUP_CONCAT(a.first_name || ' ' || a.last_name, ', ') AS authors,
    c.name AS category,
    p.name AS publisher,
    b.available_copies,
    b.total_copies,
    b.shelf_location
FROM books b
LEFT JOIN book_authors ba ON b.book_id = ba.book_id
LEFT JOIN authors a ON ba.author_id = a.author_id
LEFT JOIN categories c ON b.category_id = c.category_id
LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
WHERE b.available_copies > 0
GROUP BY b.book_id;

CREATE VIEW IF NOT EXISTS overdue_loans AS
SELECT 
    l.loan_id,
    b.title AS book_title,
    m.first_name || ' ' || m.last_name AS member_name,
    m.email,
    m.phone,
    l.loan_date,
    l.due_date,
    julianday('now') - julianday(l.due_date) AS days_overdue
FROM loans l
JOIN books b ON l.book_id = b.book_id
JOIN members m ON l.member_id = m.member_id
WHERE l.status = 'Active' AND l.due_date < DATE('now');

CREATE VIEW IF NOT EXISTS member_loan_history AS
SELECT 
    m.member_id,
    m.first_name || ' ' || m.last_name AS member_name,
    m.membership_number,
    COUNT(l.loan_id) AS total_loans,
    SUM(CASE WHEN l.status = 'Active' THEN 1 ELSE 0 END) AS active_loans,
    SUM(CASE WHEN l.status = 'Returned' THEN 1 ELSE 0 END) AS returned_loans,
    SUM(CASE WHEN l.status = 'Overdue' THEN 1 ELSE 0 END) AS overdue_loans
FROM members m
LEFT JOIN loans l ON m.member_id = l.member_id
GROUP BY m.member_id;

CREATE VIEW IF NOT EXISTS popular_books AS
SELECT 
    b.book_id,
    b.title,
    GROUP_CONCAT(a.first_name || ' ' || a.last_name, ', ') AS authors,
    COUNT(l.loan_id) AS loan_count,
    ROUND(AVG(r.rating), 2) AS average_rating,
    COUNT(DISTINCT r.review_id) AS review_count
FROM books b
LEFT JOIN book_authors ba ON b.book_id = ba.book_id
LEFT JOIN authors a ON ba.author_id = a.author_id
LEFT JOIN loans l ON b.book_id = l.book_id
LEFT JOIN reviews r ON b.book_id = r.book_id
GROUP BY b.book_id
ORDER BY loan_count DESC;
