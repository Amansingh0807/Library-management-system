import pyodbc
from datetime import datetime

# Database connection setup (here u have to write the server name of yours that u create in your system in my case i created library sytem 
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=YourServerName;'
    'DATABASE=LibraryDB;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Function to add a book
def add_book(title, author, genre, copies):
    cursor.execute("INSERT INTO Books (Title, Author, Genre, CopiesAvailable) VALUES (?, ?, ?, ?)",
                   title, author, genre, copies)
    conn.commit()
    print("Book added successfully.")

# Function to add a borrower
def add_borrower(name, email):
    cursor.execute("INSERT INTO Borrowers (Name, Email) VALUES (?, ?)", name, email)
    conn.commit()
    print("Borrower added successfully.")

# Function to borrow a book
def borrow_book(book_id, borrower_id):
    cursor.execute("SELECT CopiesAvailable FROM Books WHERE BookID = ?", book_id)
    book = cursor.fetchone()
    if book and book.CopiesAvailable > 0:
        cursor.execute("INSERT INTO BorrowedBooks (BookID, BorrowerID) VALUES (?, ?)", book_id, borrower_id)
        cursor.execute("UPDATE Books SET CopiesAvailable = CopiesAvailable - 1 WHERE BookID = ?", book_id)
        conn.commit()
        print("Book borrowed successfully.")
    else:
        print("Book not available.")

# Function to return a book
def return_book(borrowed_id):
    cursor.execute("SELECT BookID FROM BorrowedBooks WHERE BorrowedID = ? AND ReturnDate IS NULL", borrowed_id)
    record = cursor.fetchone()
    if record:
        book_id = record.BookID
        cursor.execute("UPDATE BorrowedBooks SET ReturnDate = ? WHERE BorrowedID = ?", datetime.now(), borrowed_id)
        cursor.execute("UPDATE Books SET CopiesAvailable = CopiesAvailable + 1 WHERE BookID = ?", book_id)
        conn.commit()
        print("Book returned successfully.")
    else:
        print("Invalid borrow record or book already returned.")

# Function to view all books
def view_books():
    cursor.execute("SELECT * FROM Books")
    for row in cursor.fetchall():
        print(row)

# Function to view all borrowers
def view_borrowers():
    cursor.execute("SELECT * FROM Borrowers")
    for row in cursor.fetchall():
        print(row)

# Function to view borrowed books
def view_borrowed_books():
    cursor.execute("""
        SELECT bb.BorrowedID, b.Title, br.Name, bb.BorrowDate, bb.ReturnDate
        FROM BorrowedBooks bb
        JOIN Books b ON bb.BookID = b.BookID
        JOIN Borrowers br ON bb.BorrowerID = br.BorrowerID
    """)
    for row in cursor.fetchall():
        print(row)

# Main menu
def main_menu():
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Add Borrower")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. View Books")
        print("6. View Borrowers")
        print("7. View Borrowed Books")
        print("8. Exit")
        
        choice = input("Enter your choice: ")
        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            genre = input("Enter book genre: ")
            copies = int(input("Enter number of copies: "))
            add_book(title, author, genre, copies)
        elif choice == '2':
            name = input("Enter borrower name: ")
            email = input("Enter borrower email: ")
            add_borrower(name, email)
        elif choice == '3':
            book_id = int(input("Enter book ID: "))
            borrower_id = int(input("Enter borrower ID: "))
            borrow_book(book_id, borrower_id)
        elif choice == '4':
            borrowed_id = int(input("Enter borrowed ID: "))
            return_book(borrowed_id)
        elif choice == '5':
            view_books()
        elif choice == '6':
            view_borrowers()
        elif choice == '7':
            view_borrowed_books()
        elif choice == '8':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main_menu()
