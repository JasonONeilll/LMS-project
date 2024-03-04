import csv
from datetime import datetime, timedelta

# Define roles and permissions
roles_permissions = {
    'Librarian': ['add_book', 'remove_book', 'checkout_book', 'return_book', 'generate_reports', 'display_account_info', 'display_patron_transactions', ],
    'Administrator': ['add_book', 'remove_book', 'checkout_book', 'return_book', 'generate_reports', 'add_patron', 'remove_patron', 'save_books_to_csv', 'display_account_info', 'display_patron_transactions'],
    'Patron': []
}

# User credentials
user_credentials = {
    'librarian': ('libpass', 'Librarian'),
    'administrator': ('adminpass', 'Administrator')
}

class Book:
    def __init__(self, title, author, isbn, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity

    def book_display(self):
        print(f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Quantity: {self.quantity}")

class Patron:
    def __init__(self, name, patron_id, contact_info, role='Librarian'):
        self.name = name
        self.patron_id = patron_id
        self.contact_info = contact_info
        self.role = role

    def display_account_info(self):
        print(
            f"Account Information:\nName: {self.name}\nID: {self.patron_id}\nContact Info: {self.contact_info}\nRole: {self.role}")
    def patron_display(self):
        print(f"Name: {self.name}, ID: {self.patron_id}, Contact: {self.contact_info}, Role: {self.role}")

class Transaction:
    def __init__(self, transaction_id, book, patron, checkout_date=datetime.now()):
        self.transaction_id = transaction_id
        self.book = book
        self.patron = patron
        self.checkout_date = checkout_date
        self.due_date = self.checkout_date + timedelta(days=14)  # Assuming a 2-week loan period
        self.return_date = None
        self.fine = 0

    def check_in(self, return_date=datetime.now()):
        self.return_date = return_date
        self.fine_calculator()

    def fine_calculator(self):
        if self.return_date > self.due_date:
            late_days = (self.return_date - self.due_date).days
            self.fine = late_days * 0.50  # $0.50 fine for each day late

    def transaction_display(self):
        print(f"Transaction ID: {self.transaction_id}, Book: {self.book.title}, Patron: {self.patron.name}")
        if self.return_date:
            print(f"Returned on: {self.return_date.strftime('%Y-%m-%d')}, Fine: ${self.fine:.2f}")
        else:
            print(f"Due Date: {self.due_date.strftime('%Y-%m-%d')}, Not yet returned")

class Library:
    def __init__(self):
        self.books = []
        self.patrons = []
        self.transactions = []

    def patron_display(self):
        print(f"Name: {self.name}, ID: {self.patron_id}, Contact: {self.contact_info}, Role: {self.role}")

    def display_account_info(self):
        print("Account Information:")
        print(f"Name: {self.name}")
        print(f"ID: {self.patron_id}")
        print(f"Contact Info: {self.contact_info}")
        print(f"Role: {self.role}")

    def add_book(self, book, acting_user):
        if 'add_book' in roles_permissions[acting_user.role]:
            self.books.append(book)
            print("Book added successfully.")
        else:
            print("Permission denied.")

    def remove_book(self, isbn, acting_user):
        if 'remove_book' in roles_permissions[acting_user.role]:
            for book in self.books:
                if book.isbn == isbn:
                    self.books.remove(book)
                    print("Book removed successfully.")
                    return
            print("Book not found.")
        else:
            print("Permission denied.")

    def add_patron(self, patron, acting_user):
        if 'add_patron' in roles_permissions[acting_user.role]:
            self.patrons.append(patron)
            print("Patron added successfully.")
        else:
            print("Permission denied.")

    def remove_patron(self, patron_id, acting_user):
        if 'remove_patron' in roles_permissions[acting_user.role]:
            for patron in self.patrons:
                if patron.patron_id == patron_id:
                    self.patrons.remove(patron)
                    print("Patron removed successfully.")
                    return
            print("Patron not found.")
        else:
            print("Permission denied.")

    def checkout_book(self, isbn, patron_id, acting_user):
        if 'checkout_book' in roles_permissions[acting_user.role]:
            book = self.find_book(isbn)
            patron = self.find_patron(patron_id)
            if book and patron:
                if book.quantity > 0:
                    book.quantity -= 1
                    transaction = Transaction(len(self.transactions) + 1, book, patron)
                    self.transactions.append(transaction)
                    print("Book checked out successfully.")
                else:
                    print("Book is not available.")
            else:
                print("Book or patron not found.")
        else:
            print("Permission denied.")

    def return_book(self, transaction_id, acting_user):
        if 'return_book' in roles_permissions[acting_user.role]:
            for transaction in self.transactions:
                if transaction.transaction_id == transaction_id:
                    if transaction.return_date is None:
                        transaction.check_in()
                        transaction.book.quantity += 1
                        print("Book returned successfully.")
                        return
            print("Transaction not found.")
        else:
            print("Permission denied.")

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def find_patron(self, patron_id):
        for patron in self.patrons:
            if patron.patron_id == patron_id:
                return patron
        return None

    def generate_reports(self, acting_user):
        if 'generate_reports' in roles_permissions[acting_user.role]:
            print("Library Report:")

            # Report on Books
            print("\nBooks in Library:")
            if len(self.books) > 0:
                for book in self.books:
                    book.book_display()
            else:
                print("No books available.")

            # Report on Patrons
            print("\nLibrary Patrons:")
            if len(self.patrons) > 0:
                for patron in self.patrons:
                    patron.patron_display()
            else:
                print("No registered patrons.")

            # Report on Transactions
            print("\nTransactions Record:")
            if len(self.transactions) > 0:
                for transaction in self.transactions:
                    transaction.transaction_display()
            else:
                print("No transactions to display.")
        else:
            print("Permission denied.")

    def save_books_to_csv(self, filepath, acting_user):
        if 'save_books_to_csv' in roles_permissions[acting_user.role]:
            with open(filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Title', 'Author', 'ISBN', 'Quantity'])
                for book in self.books:
                    writer.writerow([book.title, book.author, book.isbn, book.quantity])
            print("Books saved to CSV successfully.")
        else:
            print("Permission denied.")


    def display_patron_transactions(self, patron_id):
        print(f"Transactions for Patron ID {patron_id}:")
        found_transactions = False
        for transaction in self.transactions:
            if transaction.patron.patron_id == patron_id:
                found_transactions = True
                book_info = f"Book: {transaction.book.title} by {transaction.book.author}"
                checkout_info = f"Checked out on: {transaction.checkout_date.strftime('%Y-%m-%d')}"
                return_info = f"Returned on: {transaction.return_date.strftime('%Y-%m-%d')}" if transaction.return_date else "Not yet returned"
                fine_info = f"Fine: ${transaction.fine:.2f}" if transaction.fine else "No fine"
                print(f"- {book_info}, {checkout_info}, {return_info}, {fine_info}")

        if not found_transactions:
            print("No transactions found for this patron.")

        def display_patron_transactions(self, patron_id):
            print(f"Transactions for Patron ID {patron_id}:")
            found_transactions = False
            for transaction in self.transactions:
                if transaction.patron.patron_id == patron_id:
                    found_transactions = True
                    book_info = f"Book: {transaction.book.title} by {transaction.book.author}"
                    checkout_info = f"Checked out on: {transaction.checkout_date.strftime('%Y-%m-%d')}"
                    return_info = f"Returned on: {transaction.return_date.strftime('%Y-%m-%d')}" if transaction.return_date else "Not yet returned"
                    fine_info = f"Fine: ${transaction.fine:.2f}" if transaction.fine else "No fine"
                    print(f"- {book_info}, {checkout_info}, {return_info}, {fine_info}")

            if not found_transactions:
                print("No transactions found for this patron.")

def display_menu():
    print("\nLibrary Management System")
    print("1. Add Book")
    print("2. Remove Book")
    print("3. Checkout Book")
    print("4. Return Book")
    print("5. Generate Reports")
    print("6. Save Books to CSV")
    print("7. Add Patron")
    print("8. Remove Patron")
    print("9. View Account Info")
    print("10. View Transactions")
    print("11. Exit")
    choice = input("Enter choice: ")
    return choice

def login(credentials):
    username = input("Username: ")
    password = input("Password: ")
    user_info = credentials.get(username.lower())
    if user_info and user_info[0] == password:
        print(f"Login successful as {username}. Role: {user_info[1]}")
        return username, user_info[1]  # Return both username and role
    else:
        print("Login failed. Please check your username and password.")
        return None, None

def main():
    print("Welcome to the Library Management System")
    username, role = login(user_credentials)
    if role:
        print(f"Login successful. Welcome, {username}!")
        library = Library()
        acting_user = Patron(username, "1", "email@example.com", role)  # Example Patron for actions


        while True:
            user_choice = display_menu()

            if user_choice == "1":
                if 'add_book' in roles_permissions[role]:
                    title = input("Enter the book title: ")
                    author = input("Enter the author's name: ")
                    isbn = input("Enter the book ISBN: ")
                    quantity = int(input("Enter the quantity: "))
                    book = Book(title, author, isbn, quantity)
                    library.add_book(book, acting_user)
                else:
                    print("Permission denied.")

            elif user_choice == "2":
                if 'remove_book' in roles_permissions[role]:
                    isbn = input("Enter the book ISBN to remove: ")
                    library.remove_book(isbn, acting_user)
                else:
                    print("Permission denied.")

            elif user_choice == "3":
                if 'checkout_book' in roles_permissions[role]:
                    isbn = input("Enter book ISBN to checkout: ")
                    patron_id = input("Enter patron ID: ")
                    library.checkout_book(isbn, patron_id, acting_user)
                else:
                    print("Permission denied.")

            elif user_choice == "4":
                if 'return_book' in roles_permissions[role]:
                    transaction_id = int(input("Enter transaction ID to return a book: "))
                    library.return_book(transaction_id, acting_user)
                else:
                    print("Permission denied.")

            elif user_choice == "5":
                if 'generate_reports' in roles_permissions[role]:
                    library.generate_reports(acting_user)
                else:
                    print("Permission denied.")

            elif user_choice == "6":
                if 'save_books_to_csv' in roles_permissions[role]:
                    filepath = input("Enter filepath for CSV: ")
                    library.save_books_to_csv(filepath, acting_user)
                else:
                    print("Permission denied.")

            elif user_choice == "7":
                if 'add_patron' in roles_permissions[role]:
                    name = input("Enter the patron's name: ")
                    patron_id = input("Enter the patron ID: ")
                    contact_info = input("Enter the patron's contact info: ")
                    new_patron = Patron(name, patron_id, contact_info, 'Patron')  # Default role as 'Patron'
                    library.add_patron(new_patron, acting_user)
                else:
                    print("Permission denied.")

            elif user_choice == "8":
                if 'remove_patron' in roles_permissions[role]:
                    patron_id = input("Enter the patron ID to remove: ")
                    library.remove_patron(patron_id, acting_user)
                else:
                    print("Permission denied.")

            elif user_choice == "9":

                acting_user.display_account_info()

            elif user_choice == "10":
                if role in ['Librarian', 'Administrator']:
                    patron_id_input = input("Enter the patron ID to view transactions: ")
                    library.display_patron_transactions(patron_id_input)
                else:
                    # If a regular patron is logged in, show their own transactions
                    library.display_patron_transactions(acting_user.patron_id)


            elif user_choice == "11":  # Adjust based on your menu
                print("Exiting Library Management System.")
                break
            else:
                print("Invalid choice or insufficient permissions.")

if __name__ == '__main__':
    main()


#filepath for CSV: library.save_books_to_csv

#Logins
# 'librarian': ('libpass', 'Librarian'),
#'administrator': ('adminpass', 'Administrator')