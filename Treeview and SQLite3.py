from tkinter import *
from tkinter import ttk
import sqlite3

import numpy as np
import pandas as pd
import calendar
from datetime import datetime

# from ttkbootstrap.constants import *
# import ttkbootstrap as tb
# root = tb.Window(themename="superhero")
root = Tk()
root.title("CRM App With Treeview and SQLite3")
root.iconbitmap("images/MS24.ico")
root.geometry("1000x500")
#! Pandas operations =========================
"""
data_read = pd.read_csv("JGTDSL_Employee.csv")
selected_column = [
    "JGID",
    "PersonName",
    "FathersName",
    "DateOfBirth",
    "CurrentBasicPay",
    "Email",
    "Mobile",
]

selected_column_df = data_read[selected_column]
data_dict_df = selected_column_df.T.to_dict()
data = [[x for x in val.values()] for val in data_dict_df.values()]
"""

# Do some database stuff
# Create a database or connect to one that exists
conn = sqlite3.connect("jg_employee.db")
# Create a cursor instance
c = conn.cursor()
# Create Table
c.execute(
    """CREATE TABLE if not exists employee(
    jgid text,
    employee_name text,
    fathers_name text,
    birth_date text,
    basic_pay integer,
    email text,
    mobile text
)
          """
)

#! Add dummy data to table Onetime execute this code ===============
"""
for record in data:
    c.execute("INSERT INTO employee VALUES (:jgid,:employee_name, :fathers_name, :birth_date, :basic_pay, :email, :mobile)",
    {
    'jgid': record[0],
    'employee_name': record[1], 
    'fathers_name': record[2], 
    'birth_date': record[3], 
    'basic_pay': record[4], 
    'email': record[5], 
    'mobile': record[6]
    }
    )
"""
#! =================================================================

# Commit Changes =====
conn.commit()
# Close Connection ======
conn.close()


def code_block_for_query(data):
    global count
    count = 0
    for record in data:
        if count % 2 == 0:
            my_tree.insert(
                parent="",
                index="end",
                iid=count,
                values=(
                    record[1],
                    record[2],
                    ("---" if str(record[3]) == "nan" else record[3]),
                    (
                        "---"
                        if record[4] == "0000-00-00 00:00:00"
                        else datetime.strptime(record[4], "%Y-%m-%d %H:%M:%S").strftime(
                            "%d %b %Y"
                        )
                    ),
                    f"{record[5]:,.0f}",
                    record[6],
                    f"+880{record[7]}",
                ),
                tags=("evenrow",),
            )
        else:
            my_tree.insert(
                parent="",
                index="end",
                iid=count,
                values=(
                    record[1],
                    record[2],
                    ("---" if str(record[3]) == "nan" else record[3]),
                    (
                        "---"
                        if record[4] == "0000-00-00 00:00:00"
                        else datetime.strptime(record[4], "%Y-%m-%d %H:%M:%S").strftime(
                            "%d %b %Y"
                        )
                    ),
                    f"{record[5]:,.0f}",
                    record[6],
                    f"+880{record[7]}",
                ),
                tags=("oddrow",),
            )

        count += 1


def query_database():
    # Create a database or connect to one that exists
    conn = sqlite3.connect("jg_employee.db")
    # Create a cursor instance
    c = conn.cursor()
    c.execute("""SELECT rowid, substr('000'||jgid, -3,3), employee_name, fathers_name, birth_date, basic_pay, email, mobile 
              FROM employee """) #ORDER BY substr('000'||jgid, -3,3) DESC
    records = c.fetchall()
    print(records)
    code_block_for_query(records)
    # Commit Changes =====
    conn.commit()
    # Close Connection ======
    conn.close()


# Add some style =======
style = ttk.Style()
# Pick a theme =========
style.theme_use("default")

# Configure the treeview colors ===========
style.configure(
    "Treeview",
    background="#D3D3D3",
    foreground="black",
    rowheoght=25,
    fieldbackground="#D3D3D3",
)

# Change selected color ===========
style.map("Treeview", background=[("selected", "#347083")])

# Create a treeview frame =========
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Create a treeview scrollbar =========
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create treeview =========
my_tree = ttk.Treeview(
    tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended"
)
my_tree.pack()

# Configure the scroll =========
tree_scroll.config(command=my_tree.yview)

# Define Column ============
my_tree["columns"] = (
    "JGID",
    "Employee Name",
    "Fathers Name",
    "Birth Date",
    "Basic Pay",
    "Email",
    "Mobile",
)
# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("JGID", anchor=CENTER, width=40)
my_tree.column("Employee Name", anchor=W, width=190)
my_tree.column("Fathers Name", anchor=W, width=190)
my_tree.column("Birth Date", anchor=CENTER, width=100)
my_tree.column("Basic Pay", anchor=CENTER, width=100)
my_tree.column("Email", anchor=W, width=180)
my_tree.column("Mobile", anchor=CENTER, width=140)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("JGID", text="JGID", anchor=CENTER)
my_tree.heading("Employee Name", text="Employee Name", anchor=W)
my_tree.heading("Fathers Name", text="Fathers Name", anchor=W)
my_tree.heading("Birth Date", text="Birth Date", anchor=CENTER)
my_tree.heading("Basic Pay", text="Basic Pay", anchor=CENTER)
my_tree.heading("Email", text="Email", anchor=CENTER)
my_tree.heading("Mobile", text="Mobile", anchor=CENTER)

# Create stripe row Tags ========================
my_tree.tag_configure("oddrow", background="white")
my_tree.tag_configure("evenrow", background="azure1")
# my_tree.tag_configure("oddrow",  font=('Nikosh', 12))

# Add our data to the screen ====================


# print(data)


# Add Record Entry Boxes
data_frame = LabelFrame(root, text="Record")
data_frame.pack(fill="x", expand="yes", padx=20)

jgid_label = Label(data_frame, text="JGID")
jgid_label.grid(row=0, column=0, padx=10, pady=10)
jgid_entry = Entry(data_frame)
jgid_entry.grid(row=0, column=1, padx=10, pady=10)

en_label = Label(data_frame, text="Employee Name")
en_label.grid(row=0, column=2, padx=10, pady=10)
en_entry = Entry(data_frame)
en_entry.grid(row=0, column=3, padx=10, pady=10)

fn_label = Label(data_frame, text="Fathers Name")
fn_label.grid(row=0, column=4, padx=10, pady=10)
fn_entry = Entry(data_frame)
fn_entry.grid(row=0, column=5, padx=10, pady=10)

dob_label = Label(data_frame, text="Birth Date")
dob_label.grid(row=1, column=0, padx=10, pady=10)
dob_entry = Entry(data_frame)
dob_entry.grid(row=1, column=1, padx=10, pady=10)

basic_label = Label(data_frame, text="Basic Pay")
basic_label.grid(row=1, column=2, padx=10, pady=10)
basic_entry = Entry(data_frame)
basic_entry.grid(row=1, column=3, padx=10, pady=10)

email_label = Label(data_frame, text="Email")
email_label.grid(row=1, column=4, padx=10, pady=10)
email_entry = Entry(data_frame)
email_entry.grid(row=1, column=5, padx=10, pady=10)

mobile_label = Label(data_frame, text="Mobile")
mobile_label.grid(row=1, column=6, padx=10, pady=10)
mobile_entry = Entry(data_frame)
mobile_entry.grid(row=1, column=7, padx=10, pady=10)


def clear_entry():
    # Clear entry boxes
    jgid_entry.delete(0, END)
    en_entry.delete(0, END)
    fn_entry.delete(0, END)
    dob_entry.delete(0, END)
    basic_entry.delete(0, END)
    email_entry.delete(0, END)
    mobile_entry.delete(0, END)


# Select Record
def select_record(e):
    # Clear entry boxes
    clear_entry()
    # Grab record Number
    selected = my_tree.focus()
    # Grab record values
    values = my_tree.item(selected, "values")

    # outpus to entry boxes
    jgid_entry.insert(0, values[0])
    en_entry.insert(0, values[1])
    fn_entry.insert(0, values[2])
    dob_entry.insert(0, values[3])
    basic_entry.insert(0, values[4])
    email_entry.insert(0, values[5])
    mobile_entry.insert(0, values[6])


# Move Row Up
def up():
    rows = my_tree.selection()
    for row in rows:
        my_tree.move(row, my_tree.parent(row), my_tree.index(row) - 1)


# Move Rown Down
def down():
    rows = my_tree.selection()
    for row in reversed(rows):
        my_tree.move(row, my_tree.parent(row), my_tree.index(row) + 1)


# Delete One Record ============
def remove_one():
    x = my_tree.selection()[0]
    my_tree.delete(x)


# Remove Many records
def remove_many():
    x = my_tree.selection()
    for record in x:
        my_tree.delete(record)


# Remove all records
def remove_all():
    for record in my_tree.get_children():
        my_tree.delete(record)


# Update record
def update_record():
    # Grab the record number
    selected = my_tree.focus()
    # Update record
    my_tree.item(
        selected,
        text="",
        values=(
            jgid_entry.get(),
            en_entry.get(),
            fn_entry.get(),
            dob_entry.get(),
            basic_entry.get(),
            email_entry.get(),
            mobile_entry.get(),
        ),
    )
    clear_entry()


#! Add Button ==========
button_frame = LabelFrame(root, text="Command")
button_frame.pack(fill="x", expand="yes", padx=20)

update_button = Button(button_frame, text="Update", command=update_record)
update_button.grid(row=0, column=0, padx=10, pady=10)

add_button = Button(button_frame, text="Add")
add_button.grid(row=0, column=1, padx=10, pady=10)

remove_all_button = Button(button_frame, text="Remove all", command=remove_all)
remove_all_button.grid(row=0, column=2, padx=10, pady=10)

remove_one_button = Button(button_frame, text="Remove Selected One", command=remove_one)
remove_one_button.grid(row=0, column=3, padx=10, pady=10)

remove_many_button = Button(
    button_frame, text="Remove all Selected", command=remove_many
)
remove_many_button.grid(row=0, column=4, padx=10, pady=10)

move_up_button = Button(button_frame, text="Move up", command=up)
move_up_button.grid(row=0, column=5, padx=10, pady=10)

move_down_button = Button(button_frame, text="Move Down", command=down)
move_down_button.grid(row=0, column=6, padx=10, pady=10)

select_record_button = Button(button_frame, text="Clear Entry", command=clear_entry)
select_record_button.grid(row=0, column=8, padx=10, pady=10)

# Bind The Treeview ================
my_tree.bind("<ButtonRelease-1>", select_record)
query_database()
root.mainloop()
