# Register
import sqlite3
import tkinter as tk
import re
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# Create Window
window = Tk()
window.title("Poh Cheong Tong Medical Hall System")
window.configure(bg='#DFEEFF')
window.state('zoomed')

# Create Database
conn = sqlite3.connect('Poh Cheong Tong DB')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS user (
    user_id    VARCHAR UNIQUE
                       NOT NULL
                       PRIMARY KEY,
    user_name  VARCHAR NOT NULL,
    user_email VARCHAR NOT NULL,
    role       VARCHAR NOT NULL,
    password   VARCHAR NOT NULL);''')
conn.commit()


# Data Validation
def insert_data():
    check_count = 0
    msg = ""
    valid_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if re.search(valid_email, user_email.get()):
        check_count += 1
    else:
        msg = "Invalid email"
    if len(password.get()) < 5:
        msg = "Password too short"
    else:
        check_count += 1
    if password.get() != con_password.get():
        msg = "Password did not match"
    else:
        check_count += 1
    if user_email.get() == "" or user_id.get() == "" or user_name.get() == "" or role.get() == "" or password.get() == "" or con_password.get() == "":
        msg = "Input box cannot be empty"
    else:
        check_count += 1
    if check_count == 4:
        try:
            conn = sqlite3.connect('Poh Cheong Tong DB')
            cur = conn.cursor()
            cur.execute("INSERT INTO user VALUES (:user_id, :user_name, :user_email, :role, :password)",  {'user_id': user_id.get(), 'user_name': user_name.get(), 'user_email': user_email.get(), 'role': role.get(), 'password': password.get()})
            conn.commit()
            messagebox.showinfo('confirmation', 'Record Saved')
        except Exception as ect:
            messagebox.showerror('', str(ect))
    else:
        messagebox.showinfo('message', msg)


# Show password
def show_password():
    if btn_value.get() == 1:
        password_entry.config(show='')
        con_password_entry.config(show='')
    else:
        password_entry.config(show='*')
        con_password_entry.config(show='*')

# Register Title
Label(window, text='Register', font=('Sigmar One', 75), fg='#707070', bg='#DFEEFF').place(x=600, y=50)

# Import Logo
logo = ImageTk.PhotoImage(Image.open("Logo.jpeg").resize((240, 240), resample=Image.LANCZOS))
logo1 = Label(window, image=logo, bg='#DFEEFF')
logo1.place(x=200, y=200)

# User Email Label and Text Entry Box
Label(window, text='Email', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=170)
user_email = StringVar()
Entry(window, textvariable=user_email, font=20).place(x=600, y=210)

# User ID Label and Text Entry Box
Label(window, text='ID', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=240)
user_id = StringVar()
Entry(window, textvariable=user_id, font=20).place(x=600, y=280)

# User Name Label and Text Entry Box
Label(window, text='Name', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=310)
user_name = StringVar()
Entry(window, textvariable=user_name, font=20).place(x=600, y=350)

# Adding combobox drop down list for role
Label(window, text='Role', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=380)
role = tk.StringVar()
list_picker = ttk.Combobox(window, width=34, textvariable=role)
list_picker['values'] = (' Admin', ' User')
list_picker.place(x=600, y=420)

# Password Label and Text Entry Box
Label(window, text='Password', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=450)
password = StringVar()
password_entry = Entry(window, textvariable=password, font=20, show='*')
password_entry.place(x=600, y=490)

# Confirm Password Label and Text Entry Box
Label(window, text='Confirm Password', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=520)
con_password = StringVar()
con_password_entry = Entry(window, textvariable=con_password, font=20, show='*')
con_password_entry.place(x=600, y=560)

# Check Button to show and hide password
btn_value = IntVar(value=0)
Checkbutton(window, text="Show password", variable=btn_value, command=show_password).place(x=600, y=590)

# Register Button
Button(window, text='Register', font=('Segoe UI', 15, 'bold'), fg='#FFFFFF', bg='#8AC1FF', relief='groove',
       command=insert_data).place(x=915, y=550)

# Cancel Button
Button(window, text='Cancel', font=('Segoe UI', 15, 'bold'), fg='#FFFFFF', bg='#FF8A8A', relief='groove',
       command=None).place(x=1030, y=550)

window.mainloop()
