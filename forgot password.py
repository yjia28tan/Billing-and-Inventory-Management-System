# Forgot Password

import sqlite3
import tkinter as tk
import re
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

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
def change_password():
    check_count = 0
    msg = ""
    if email_entry.get() == "" or id_entry.get() == "" or password_entry.get() == "" or con_password.get() == "":
        msg = "Input box cannot be empty"
        messagebox.showinfo('message', msg)
    else:
        conn = sqlite3.connect('Poh Cheong Tong DB')
        cur = conn.cursor()
        cur.execute("SELECT * FROM user where user_id=? AND user_email=?", (id_entry.get(), email_entry.get()))
        row = cur.fetchone()
        if row:
            if len(password_entry.get()) < 5:
                msg = "Password too short"
                messagebox.showinfo('message', msg)
            else:
                if password_entry.get() != con_password_entry.get():
                    msg = "Password and confirm password did not match"
                    messagebox.showinfo('message', msg)
                else:
                    try:
                        cur.execute("UPDATE user SET password=? WHERE user_id=? AND user_email=?",
                                    [password_entry.get(), id_entry.get(), email_entry.get()])
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('confirmation', 'Password changed successfully')
                    except Exception as ect:
                        messagebox.showerror('', str(ect))
        else:
            msg = "Invalid email or id"
            messagebox.showinfo('message', msg)

# Show password
def show_password():
    if btn_value.get() == 1:
        password_entry.config(show='')
        con_password_entry.config(show='')
    else:
        password_entry.config(show='*')
        con_password_entry.config(show='*')


# Forgot Password Title
Label(window, text='Forgot Password', font=('Sigmar One', 60), fg='#707070', bg='#DFEEFF').place(x=550, y=50)

# Import Logo
logo = ImageTk.PhotoImage(Image.open("Logo.jpeg").resize((240, 240), resample=Image.LANCZOS))
logo1 = Label(window, image=logo, bg='#DFEEFF')
logo1.place(x=200, y=200)

# User Email Label and Text Entry Box
Label(window, text='Email', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=170)
user_email = StringVar()
email_entry = Entry(window, textvariable=user_email, font=20)
email_entry.place(x=600, y=210)

# User ID Label and Text Entry Box
Label(window, text='ID', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=240)
user_id = StringVar()
id_entry = Entry(window, textvariable=user_id, font=20)
id_entry.place(x=600, y=280)

# Password Label and Text Entry Box
Label(window, text='Password', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=310)
password = StringVar()
password_entry = Entry(window, textvariable=password, font=20, show='*')
password_entry.place(x=600, y=350)

# Confirm Password Label and Text Entry Box
Label(window, text='Confirm Password', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=380)
con_password = StringVar()
con_password_entry = Entry(window, textvariable=con_password, font=20, show='*')
con_password_entry.place(x=600, y=420)

# Check Button to show and hide password
btn_value = IntVar(value=0)
Checkbutton(window, text="Show password", variable=btn_value, command=show_password, bg='#DFEEFF').place(x=600, y=450)

# Submit Button
Button(window, text='Submit', font=('Segoe UI', 15, 'bold'), fg='#FFFFFF', bg='#8AC1FF', relief='groove',
       command=change_password).place(x=915, y=550)

# Cancel Button
Button(window, text='Cancel', font=('Segoe UI', 15, 'bold'), fg='#FFFFFF', bg='#FF8A8A', relief='groove',
       command=NONE).place(x=1030, y=550)

window.mainloop()
