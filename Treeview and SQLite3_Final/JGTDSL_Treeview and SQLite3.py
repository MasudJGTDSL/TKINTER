from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import colorchooser
import sqlite3

from configparser import ConfigParser
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
root.geometry("1000x550")

parser = ConfigParser()
parser.read("configurations.ini")
saved_primary_color = parser.get("colors", "primary_color")
saved_secondary_color = parser.get("colors", "secondary_color")
saved_highlight_color = parser.get("colors", "highlight_color")

my_menu = Menu(root)
root.config(menu=my_menu)


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
                    (
                        "---"
                        if (str(record[3]) == "nan" or record[3] == None)
                        else record[3]
                    ),
                    (
                        "---"
                        if record[4] == "0000-00-00 00:00:00"
                        else datetime.strptime(record[4], "%Y-%m-%d %H:%M:%S").strftime(
                            "%d %b %Y"
                        )
                    ),
                    f"{record[5]:,.0f}",
                    record[6],
                    record[7],
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
                    (
                        "---"
                        if (str(record[3]) == "nan" or record[3] is None)
                        else record[3]
                    ),
                    (
                        "---"
                        if record[4] == "0000-00-00 00:00:00"
                        else datetime.strptime(record[4], "%Y-%m-%d %H:%M:%S").strftime(
                            "%d %b %Y"
                        )
                    ),
                    f"{record[5]:,.0f}",
                    record[6],
                    record[7],
                ),
                tags=("oddrow",),
            )

        count += 1


def query_database():
    # Create a database or connect to one that exists
    conn = sqlite3.connect("jg_employee.db")
    # Create a cursor instance
    c = conn.cursor()
    c.execute(
        """SELECT rowid, substr('000'||jgid, -3,3), employee_name, fathers_name, birth_date, basic_pay, email, substr('00000000000'||mobile, -11,11)  
              FROM employee ORDER BY substr('000'||jgid, -3,3)"""
    )  # ORDER BY substr('000'||jgid, -3,3) DESC
    records = c.fetchall()
    remove_all()
    code_block_for_query(records)
    conn.commit()
    conn.close()


# Configure our menu
def primary_color():
    primary_color = colorchooser.askcolor()[1]
    if primary_color:
        my_tree.tag_configure("oddrow", background=primary_color)
        # Set the color change
        parser.read("configurations.ini")
        parser.set("colors", "primary_color", primary_color)
        # Save the config file
        with open("configurations.ini", "w") as configfile:
            parser.write(configfile)


def secondary_color():
    secondary_color = colorchooser.askcolor()[1]
    if secondary_color:
        my_tree.tag_configure("evenrow", background=secondary_color)

        # Set the color change
        parser.read("configurations.ini")
        parser.set("colors", "secondary_color", secondary_color)
        # Save the config file
        with open("configurations.ini", "w") as configfile:
            parser.write(configfile)


def highlight_color():
    highlight_color = colorchooser.askcolor()[1]
    if highlight_color:
        style.map("Treeview", background=[("selected", highlight_color)])

        # Set the color change
        parser.read("configurations.ini")
        parser.set("colors", "highlight_color", highlight_color)
        # Save the config file
        with open("configurations.ini", "w") as configfile:
            parser.write(configfile)
def reset_color():
    my_tree.tag_configure("oddrow", background='papayawhip')
    my_tree.tag_configure("evenrow", background='white')
    style.map("Treeview", background=[("selected", '#838B83')])

    # Set the color change
    parser.read("configurations.ini")
    parser.set("colors", "primary_color", 'papayawhip')
    parser.set("colors", "secondary_color", 'white')
    parser.set("colors", "highlight_color", '#838B83')
    # Save the config file
    with open("configurations.ini", "w") as configfile:
        parser.write(configfile)


def search_records():
    lookup_record = search_entry.get()
    # Create a database or connect to one that exists
    conn = sqlite3.connect("jg_employee.db")
    # Create a cursor instance
    c = conn.cursor()
    qry = f"""SELECT rowid, substr('000'||jgid, -3,3), employee_name, fathers_name, birth_date, basic_pay, email, substr('00000000000'||mobile, -11,11)  
            FROM employee WHERE (employee_name || jgid) like '%{lookup_record}%' ORDER BY substr('000'||jgid, -3,3)"""
    c.execute(qry)
    print(qry)
    query_records = c.fetchall()
    remove_all()
    code_block_for_query(query_records)
    search.destroy()
    conn.commit()
    conn.close()


def lookup_records():
    global search_entry, search
    search = Toplevel(root)
    search.title("Search Records")
    search.geometry("400x200")
    search.iconbitmap("images/search.ico")
    # Create label frame
    search_frame = LabelFrame(search, text="Employee Name")
    search_frame.pack(padx=10, pady=10)
    # Add entry box

    search_entry = Entry(search_frame, font=("Helvetica"))
    search_entry.pack(pady=20, padx=20)
    # Create label frame
    search_frame = LabelFrame(search, text="Employee Name")
    search_frame.pack(padx=10, pady=10)
    # Add Button
    search_button = Button(search, text="Search", command=search_records)
    search_button.pack(padx=10, pady=10)


option_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Options", menu=option_menu)
# Drop down menu
option_menu.add_command(label="Primary Color", command=primary_color)
option_menu.add_command(label="Secondary Color", command=secondary_color)
option_menu.add_command(label="Highlight Color", command=highlight_color)
option_menu.add_separator()
option_menu.add_command(label="Reset Color", command=reset_color)
option_menu.add_separator()
option_menu.add_command(label="Exit", command=root.quit)

search_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Search", menu=search_menu)
# Drop down menu
search_menu.add_command(label="Search Employee", command=lookup_records)
search_menu.add_separator()
search_menu.add_command(label="Reset", command=query_database)

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

conn = sqlite3.connect("jg_employee.db")
c = conn.cursor()
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
conn.commit()
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
style.map("Treeview", background=[("selected", saved_highlight_color)])

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
my_tree.tag_configure("oddrow", background=saved_primary_color)
my_tree.tag_configure("evenrow", background=saved_secondary_color)
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
    grabed_jgid = str(int(jgid_entry.get()))
    grabed_employee_name = en_entry.get()

    delete_confirmation = messagebox.askyesno(
        "Delete",
        f"Are You Sure? You want to delete record for\nJGID: {grabed_jgid}, Name: {grabed_employee_name}",
    )

    if delete_confirmation == 1:
        # x = my_tree.selection()[0]
        # my_tree.delete(x)
        conn = sqlite3.connect("jg_employee.db")
        c = conn.cursor()
        c.execute("DELETE FROM employee WHERE jgid =" + grabed_jgid)
        conn.commit()
        conn.close()
        clear_entry()
        my_tree.delete(*my_tree.get_children())
        query_database()
        messagebox.showinfo(
            "Delete",
            f"Record deleted for\nJGID: {grabed_jgid}, Name: {grabed_employee_name}",
        )


# Remove Many records
def remove_many():
    x = my_tree.selection()
    employee_list = [
        f'{my_tree.item(record, "values")[0]}: {my_tree.item(record, "values")[1]}\n'
        for record in x
    ]

    jgid_list = [str(int(my_tree.item(record, "values")[0])) for record in x]
    delete_confirmation = messagebox.askyesno(
        "Deletion Confirmation!!!",
        f"""❗️❗️❗️Are You Sure? You want to delete records for
    \nEmployees:\n-----------------------------------------\n{''.join(employee_list)}""",
    )

    if delete_confirmation == 1:
        records = [int(my_tree.item(record, "values")[0]) for record in x]
        conn = sqlite3.connect("jg_employee.db")
        c = conn.cursor()
        # c.execute("DELETE FROM employee WHERE jgid IN(" + ','.join(jgid_list)+")")
        # Or below query
        c.executemany("DELETE FROM employee WHERE jgid = ?", [(a,) for a in jgid_list])
        conn.commit()
        conn.close()
        clear_entry()
        my_tree.delete(*my_tree.get_children())
        query_database()
        messagebox.showinfo(
            "Deletion Information",
            f"Record deleted for\n\nEmployees:\n-----------------------------------------\n{''.join(employee_list)}"
            "",
        )

    # for record in x:
    #     my_tree.delete(record)


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
    conn = sqlite3.connect("jg_employee.db")
    c = conn.cursor()
    c.execute(
        """UPDATE  employee SET
            employee_name =   :ename, 
            fathers_name =    :fname,
            birth_date =      :bdate,
            basic_pay =       :bpay, 
            email =           :email, 
            mobile =          :mobile
            WHERE jgid = :oid
            """,
        {
            "ename": en_entry.get(),
            "fname": fn_entry.get(),
            "bdate": datetime.strptime(dob_entry.get(), "%d %b %Y").strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "bpay": int(basic_entry.get().replace(",", "")),
            "email": email_entry.get(),
            "mobile": mobile_entry.get(),
            "oid": int(jgid_entry.get()),
        },
    )
    conn.commit()
    conn.close()
    clear_entry()
    my_tree.delete(*my_tree.get_children())
    query_database()


def add_record():
    conn = sqlite3.connect("jg_employee.db")
    c = conn.cursor()
    c.execute(
        """INSERT INTO employee values(
            :jgid,
            :ename, 
            :fname,
            :bdate,
            :bpay, 
            :email, 
            :mobile)
            """,
        {
            "jgid": int(jgid_entry.get()),
            "ename": en_entry.get(),
            "fname": fn_entry.get(),
            "bdate": datetime.strptime(dob_entry.get(), "%d %b %Y").strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "bpay": int(basic_entry.get().replace(",", "")),
            "email": email_entry.get(),
            "mobile": mobile_entry.get(),
        },
    )
    conn.commit()
    conn.close()
    clear_entry()
    my_tree.delete(*my_tree.get_children())
    query_database()


#! Add Button ==========
button_frame = LabelFrame(root, text="Command")
button_frame.pack(fill="x", expand="yes", padx=20)

update_button = Button(button_frame, text="Update", command=update_record)
update_button.grid(row=0, column=0, padx=10, pady=10)

add_button = Button(button_frame, text="Add", command=add_record)
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
