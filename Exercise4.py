from peewee import *
import datetime

db = SqliteDatabase('library.db')

class BaseModel(Model):
    class Meta:
        database = db

class Book(BaseModel):
    BookID = CharField(primary_key=True)
    Title = CharField()
    Author = CharField()
    ISBN = CharField()
    Status = CharField()

class User(BaseModel):
    UserID = CharField(primary_key=True)
    Name = CharField()
    Email = CharField()

class Reservation(BaseModel):
    ReservationID = CharField(primary_key=True)
    Book = ForeignKeyField(Book, backref='reservations')
    User = ForeignKeyField(User, backref='reservations')
    ReservationDate = DateField()

def prompt(message):
    return input(message + ": ")

def add_book():
    data = {
        'BookID': prompt("Please enter BookID"),
        'Title': prompt("Please enter the title"),
        'Author': prompt("Please enter author"),
        'ISBN': prompt("Please enter ISBN"),
        'Status': prompt("Please enter the status (available or reserved)")
    }
    Book.create(**data)
    print("Book added successfully!")

def display_book(book):
    print(book.__data__)

def find_book_by_id():
    book_id = prompt("Please enter BookID")
    book = Book.select().join(Reservation, JOIN.LEFT_OUTER).switch(Book).join(User, JOIN.LEFT_OUTER).where(Book.BookID == book_id).get()
    display_book(book)

def find_all_books():
    books = Book.select().join(Reservation, JOIN.LEFT_OUTER).switch(Book).join(User, JOIN.LEFT_OUTER)
    for book in books:
        display_book(book)

def update_book():
    book_id = prompt("Please enter BookID")
    book = Book.get(Book.BookID == book_id)

    data = {
        'Title': prompt("Please enter a new title or leave it blank"),
        'Author': prompt("Please enter a new author or leave blank"),
        'ISBN': prompt("Please enter a new ISBN or leave it blank"),
        'Status': prompt("Please enter a new status or leave it blank (available or reserved)")
    }

    for key, value in data.items():
        if value:
            setattr(book, key, value)
    book.save()
    print("Book updated successfully!")

def delete_book():
    book_id = prompt("Please enter BookID")
    Book.get(Book.BookID == book_id).delete_instance(recursive=True)
    print("Book deleted successfully!")

def main():
    ACTIONS = {
        '1': add_book,
        '2': find_book_by_id,
        '3': find_all_books,
        '4': update_book,
        '5': delete_book
    }

    db.connect()
    db.create_tables([Book, User, Reservation])

    while True:
        choice = input('''
        Please select an action:

        1. Add new book
        2. Find book details based on BookID
        3. Find all books
        4. Update the book details
        5. Delete book
        6. Quit
        ''')
        
        if choice == '6':
            break
        
        action = ACTIONS.get(choice)
        if action:
            action()

if __name__ == "__main__":
    main()
