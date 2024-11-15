-- Create Database
CREATE DATABASE LibraryDB;

-- Use the database
USE LibraryDB;

-- Create Books Table
CREATE TABLE Books (
    BookID INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(255),
    Author NVARCHAR(255),
    Genre NVARCHAR(50),
    CopiesAvailable INT
);

-- Create Borrowers Table
CREATE TABLE Borrowers (
    BorrowerID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(255),
    Email NVARCHAR(255)
);

-- Create BorrowedBooks Table
CREATE TABLE BorrowedBooks (
    BorrowedID INT IDENTITY(1,1) PRIMARY KEY,
    BookID INT FOREIGN KEY REFERENCES Books(BookID),
    BorrowerID INT FOREIGN KEY REFERENCES Borrowers(BorrowerID),
    BorrowDate DATE DEFAULT GETDATE(),
    ReturnDate DATE
);
