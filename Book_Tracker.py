import tkinter as tk
import mysql.connector
from tkinter import ttk
import yaml

with open('mysql_database.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Connect to MySQL database
db = mysql.connector.connect(
    host=data['my_host'],
    user=data['my_user'],
    password=data['my_pass'],
    database=data['my_database']
)
cursor = db.cursor()

def add_book():
    title = entry_title.get()
    author = entry_author.get()
    month = entry_month.get()
    year = entry_year.get()

    # Insert book details into the database
    sql = "INSERT INTO books (book_title, author, month_read, year_read) VALUES (%s, %s, %s, %s)"
    values = (title, author, month, year)
    cursor.execute(sql, values)
    db.commit()

    # Clear input fields
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_month.delete(0, tk.END)
    entry_year.delete(0, tk.END)

    # Refresh book list
    refresh_book_list()

def refresh_book_list():
    # Clear existing book list
    for row in treeview.get_children():
        treeview.delete(row)

    # Grab all books from the database without the book_id values
    cursor.execute("SELECT book_title, author, CONCAT(month_read, '/', year_read) FROM books")
    books = cursor.fetchall()

    # Insert books into the book list table
    for book in books:
        treeview.insert("", tk.END, values=book)

# Create the Tkinter window
window = tk.Tk()
window.title("Book Tracker")
window.geometry("1000x400")

for i in range(6):  # Assuming you have 6 rows (0 to 5) in your grid
    window.grid_rowconfigure(i, weight=1)

for i in range(2):  # Assuming you have 2 columns (0 to 1) in your grid
    window.grid_columnconfigure(i, weight=1)

# Add My Book Tracker at the top of the window
title_label = tk.Label(window, text="My Book\nTracker", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

# Create input labels
label_title = tk.Label(window, text="Title:")
label_title.grid(row=1, column=0, padx=10, pady=5)
label_author = tk.Label(window, text="Author:")
label_author.grid(row=2, column=0, padx=10, pady=5)
label_month = tk.Label(window, text="Month Read:")
label_month.grid(row=3, column=0, padx=10, pady=5)
label_year = tk.Label(window, text="Year Read:")
label_year.grid(row=4, column=0, padx=10, pady=5)

# Create input fields
entry_title = tk.Entry(window)
entry_title.grid(row=1, column=1, padx=10, pady=5)
entry_author = tk.Entry(window)
entry_author.grid(row=2, column=1, padx=10, pady=5)
entry_month = tk.Entry(window)
entry_month.grid(row=3, column=1, padx=10, pady=5)
entry_year = tk.Entry(window)
entry_year.grid(row=4, column=1, padx=10, pady=5)

# Create "Add Book" button
btn_add = tk.Button(window, text="Add Book", command=add_book)
btn_add.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Create a frame for the book list table
list_frame = tk.Frame(window)
list_frame.grid(row=0, column=2, rowspan=5, padx=10, pady=5)

# Create a scrollbar
scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a Treeview widget to display the book list
treeview = ttk.Treeview(list_frame, yscrollcommand=scrollbar.set, show='headings')
treeview.pack(fill=tk.BOTH, expand=True)

# Configure the scrollbar
scrollbar.config(command=treeview.yview)

# Define columns for the Treeview
treeview['columns'] = ('Title', 'Author', 'Date Read')
treeview.heading("Title", text="Title")
treeview.column("Title", width=200, minwidth=150)
treeview.heading("Author", text="Author")
treeview.column("Author", width=200, minwidth=150)
treeview.heading("Date Read", text="Date Read")
treeview.column("Date Read", width=200, minwidth=150)

# Refresh the book list
refresh_book_list()

# Start the Tkinter event loop
window.mainloop()

# Close the database connection
db.close()