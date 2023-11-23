from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tb
import calendar


def welfare_fund_calculation():
    last_basic = int(my_entry.get())
    twenty_five_percent_of_basic = last_basic * (0.25)
    cur_two_point_seven_five_percent = 0
    total_amount_to_pay = 0
    x = 0

    while x < 180:
        cur_two_point_seven_five_percent = twenty_five_percent_of_basic * (0.0275)

        total_amount_to_pay += (
            twenty_five_percent_of_basic - cur_two_point_seven_five_percent
        )

        twenty_five_percent_of_basic -= cur_two_point_seven_five_percent

        x += 1

    return round(total_amount_to_pay, 2)


click_num = False


# Create a Function for the Button
def change_label_text():
    global click_num
    if click_num == False:
        click_num = True
    else:
        if my_entry.get() == "":
            txt = f"Label Text is: Nothing"
        else:
            calculated_amount = welfare_fund_calculation()
            txt = f"Amount to pay= {calculated_amount:,.2f}"

        My_Label.config(text=txt, bootstyle="danger")
        click_num = False


def check_toggle():
    if var1.get() == 1:
        My_Button2.config(text="Button is Checked", bootstyle="success")
    else:
        My_Button2.config(text="Button is UnChecked", bootstyle="danger")


def combo_action():
    action = my_combo.get()
    My_Label.config(text=f"Combobox Value is: {action}", bootstyle="warning")


def click_bind(e):
    action = my_combo.get()
    My_Button2.config(text=f"Combobox Value is: {action}", bootstyle="danger")
    My_Label.config(bootstyle="warning")


root = tb.Window(themename="superhero")
root.title("Welfare Fund Calculation")
root.iconbitmap("images/MS24.ico")
root.geometry("500x600")
bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM)  #

# Create a Label ===============
My_Label = tb.Label(
    root,
    text="আপনার অবসর জীবন সমৃদ্ধ হউক!",
    font=("Helvetica", 16),
    bootstyle="primary inverse",
)
My_Label.pack(padx=5, pady=(20, 5))
# Create a Button ================
My_Button = tb.Button(text="Click Me", bootstyle="danger", command=change_label_text)
My_Button.pack(pady=5)


# Checkbutton ==================
var1 = IntVar()
Mycheck = tb.Checkbutton(
    root,
    text="Check Box",
    bootstyle="Success",
    variable=var1,
    onvalue=1,
    offvalue=0,
    command=check_toggle,
)
Mycheck.pack(pady=5)

# Toolbutton ==================
var2 = IntVar()
Mycheck2 = tb.Checkbutton(
    root,
    text="Check Box",
    bootstyle="Success toolbutton",
    variable=var2,
    onvalue=1,
    offvalue=0,
    command=check_toggle,
)
Mycheck2.pack(pady=5)

# Round Toggle ==================
var3 = IntVar()
Mycheck3 = tb.Checkbutton(
    root,
    text="Round Toggle",
    bootstyle="Success round-toggle",
    variable=var3,
    onvalue=1,
    offvalue=0,
    command=check_toggle,
)
Mycheck3.pack(pady=5)

# Square Toggle ==================
var4 = IntVar()
Mycheck4 = tb.Checkbutton(
    root,
    text="Square Toggle",
    bootstyle="warning square-toggle",
    variable=var4,
    onvalue=1,
    offvalue=0,
    command=check_toggle,
)
Mycheck4.pack(pady=5)

# Custom Style ==================
my_style = tb.Style()
my_style.configure("danger.Outline.TButton", font=("Helvetica", 14))
var5 = IntVar()
Mybutton5 = tb.Button(
    root,
    text="Style From my_style",
    style="danger.Outline.TButton",
    # variable=var5,
    # onvalue=1,
    # offvalue=0,
    command=combo_action,
)
Mybutton5.pack(padx=(5, 5), pady=5)

# Combobox ====================

var_days = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
]
days_name = [calendar.day_name[i] for i in var_days]
# print(days_name)
my_combo = tb.Combobox(
    root,
    text="Round Toggle",
    bootstyle="warning",
    values=days_name,
    # command=combo_action,
)
my_combo.pack(padx=(5, 5), pady=5)
my_combo.current(6)
my_combo.bind("<<ComboboxSelected>>", click_bind)

label_entry_01 = tb.Label(root, text="Input Last Basic :")
label_entry_01.pack(side=LEFT, padx=(5, 5), pady=5)
my_entry = tb.Entry(
    root,
    text="",
)  # show="*" [for password]
my_entry.pack(side=LEFT, padx=(5, 5), pady=5)

My_Button2 = tb.Button(bottomframe, text="Click Me", bootstyle="info, outline")
My_Button2.pack(pady=5)

root.mainloop()
