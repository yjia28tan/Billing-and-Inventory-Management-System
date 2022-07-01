import sqlite3
conn = sqlite3.connect('Poh Cheong Tong')

import tkinter  as tk 
from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window.geometry("1440x1024") 
window.title("Poh Cheong Tong Medical Hall System")
window.configure(bg = '#DFEEFF')

page1 = Frame(window) #Log-in
page2 = Frame(window) #Home
page3 = Frame(window) #Inventory
page4 = Frame(window) #
page5 = Frame(window) #Billing

for frame in (page1, page2, page3, page4, page5):
    frame.grid(row=0, column=0, sticky='nsew')

def show_frame(frame):
    frame.tkraise()

show_frame(page1)


# ==== Create the menubar =====
min_w = 70  # Minimum width of the frame
max_w = 145  # Maximum width of the frame
cur_width = min_w  # Increasing width of the frame
expanded = False  # Check if it is completely expanded

def expandForHome():
    global cur_width, expanded
    cur_width += 10  # Increase the width by 10
    rep = window.after(5, expandForHome)  # Repeat this func every 5 ms
    frame.config(width=cur_width)  # Change the width to new increase width
    if cur_width >= max_w:  # If width is greater than maximum width
        expanded = True  # Frame is expended
        window.after_cancel(rep)  # Stop repeating the function
        fillForHome()


def contractForHome():
    global cur_width, expanded
    cur_width -= 10  # Reduce the width by 10
    rep = window.after(5, contractForHome)  # Call this func every 5 ms
    frame.config(width=cur_width)  # Change the width to new reduced width
    if cur_width <= min_w:  # If it is back to normal width
        expanded = False  # Frame is not expanded
        window.after_cancel(rep)  # Stop repeating the function
        fillForHome()


def fillForHome(): 
    if expanded:  #If the frame is expanded
        # Show the label, and remove the image
        logout_b.config(text='Log-Out', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        home_b.config(text='Home', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        billing_b.config(text='Billing', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        inventory_b.config(text='Inventory', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        analysis_b.config(text='Analysis', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        register_b.config(text='Register\n New User', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
    else:
        # Bring the image back
        logout_b.config(image=logout, font=(0, 30))
        home_b.config(image=home, font=(0, 30))
        billing_b.config(image=billing, font=(0, 30))
        inventory_b.config(image=inventory, font=(0, 30))
        analysis_b.config(image=analysis, font=(0, 30))
        register_b.config(image=register, font=(0, 30))


# Define and resize the icons to be shown in Menu bar
logout = ImageTk.PhotoImage(Image.open('Logout.png').resize((40, 40), resample=Image.Resampling.LANCZOS))
home = ImageTk.PhotoImage(Image.open('Home.png').resize((40, 40), resample=Image.Resampling.LANCZOS))
billing = ImageTk.PhotoImage(Image.open('Bill.png').resize((40, 40), resample=Image.Resampling.LANCZOS))
inventory = ImageTk.PhotoImage(Image.open('Inventory.png').resize((40, 40), resample=Image.Resampling.LANCZOS))
analysis = ImageTk.PhotoImage(Image.open('Analysis.png').resize((40, 40), resample=Image.Resampling.LANCZOS))
register = ImageTk.PhotoImage(Image.open('Register.png').resize((40, 40), resample=Image.Resampling.LANCZOS))

window.update()  # For the width to get updated

menuFrame = Frame(page2, bg='#492F7C', width=150, height=window.winfo_height(),highlightbackground='white', highlightthickness=1)
menuFrame.place(x=0, y=100)


# Defining the buttons for menu bar in Home page
logout_b = Button(menuFrame, image=logout, bg='#252B61', relief='ridge')
home_b = Button(menuFrame, image=home, bg='#252B61', relief='ridge')
billing_b = Button(menuFrame, image=billing, bg='#252B61', relief='ridge')
inventory_b = Button(menuFrame, image=inventory, bg='#252B61', relief='ridge', command=lambda: show_frame(page3))
analysis_b = Button(menuFrame, image=analysis, bg='#252B61', relief='ridge')
register_b = Button(menuFrame, image=register, bg='#252B61', relief='ridge')


# Placing button in menu bar
logout_b.place(x=25, y=10, width = 100)
home_b.place(x=25, y=70, width = 100)
billing_b.place(x=25, y=130, width = 100)
inventory_b.place(x=25, y=190, width = 100)
analysis_b.place(x=25, y=250, width = 100)
register_b.place(x=25, y=310, width = 100)

# Bind to the frame, if centered or left
menuFrame.bind('<Enter>', lambda e: expandForHome())
menuFrame.bind('<Leave>', lambda e: contractForHome())

# So that it does not depend on the widgets inside the frame
menuFrame.grid_propagate(False)

window.mainloop
