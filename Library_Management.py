from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
def connect_to_mongodb():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        print("Connected to MongoDB")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

# Create Database and Collections
def create_library_collections(client):
    db = client["LibraryDB"]
    books = db["Books"]
    users = db["Users"]
    print("Library database and collections initialized")
    return books, users

# Add new book
def add_book(collection):
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    year = int(input("Enter publication year: "))
    copies = int(input("Enter number of copies: "))
    collection.insert_one({"title": title, "author": author, "year": year, "copies": copies})
    print("Book added successfully.")

# View all books
def view_books(collection):
    print("\nAvailable Books:")
    for book in collection.find():
        print(f"Title: {book['title']}, Author: {book['author']}, Year: {book['year']}, Copies: {book['copies']}")

# Update book details
def update_book(collection):
    title = input("Enter the title of the book to update: ")
    field = input("Enter the field to update (title, author, year, copies): ").strip()
    new_value = input("Enter the new value: ")
    try:
        if field == "year" or field == "copies":
            new_value = int(new_value)
        collection.update_one({"title": title}, {"$set": {field: new_value}})
        print("Book details updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Delete a book
def delete_book(collection):
    title = input("Enter the title of the book to delete: ")
    result = collection.delete_one({"title": title})
    if result.deleted_count > 0:
        print("Book deleted successfully.")
    else:
        print("Book not found.")

# Borrow a book
def borrow_book(books, users):
    user_name = input("Enter your name: ")
    book_title = input("Enter the title of the book to borrow: ")
    book = books.find_one({"title": book_title, "copies": {"$gt": 0}})
    if book:
        books.update_one({"title": book_title}, {"$inc": {"copies": -1}})
        users.insert_one({"user_name": user_name, "book_title": book_title, "borrow_date": datetime.now()})
        print("Book borrowed successfully.")
    else:
        print("Book not available or out of stock.")

# Return a book
def return_book(books, users):
    user_name = input("Enter your name: ")
    book_title = input("Enter the title of the book to return: ")
    record = users.find_one({"user_name": user_name, "book_title": book_title})
    if record:
        books.update_one({"title": book_title}, {"$inc": {"copies": 1}})
        users.delete_one({"_id": record["_id"]})
        print("Book returned successfully.")
    else:
        print("No record of borrowing found.")

# Main Menu
def main():
    client = connect_to_mongodb()
    if not client:
        return

    books, users = create_library_collections(client)

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. View Books")
        print("3. Update Book")
        print("4. Delete Book")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book(books)
        elif choice == "2":
            view_books(books)
        elif choice == "3":
            update_book(books)
        elif choice == "4":
            delete_book(books)
        elif choice == "5":
            borrow_book(books, users)
        elif choice == "6":
            return_book(books, users)
        elif choice == "7":
            print("Exiting Library Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    client.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
