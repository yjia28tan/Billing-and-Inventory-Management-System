#import modules
import tkinter as tk 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
from datetime import datetime
from datetime import date
import sqlite3
from io import BytesIO
import re
from verify_email import verify_email
import ttkwidgets.autocomplete
from fpdf import FPDF
import pandas as pd
import numpy as np  # For numerical
import matplotlib.pyplot as plt  # Built-in Matplotlib
import seaborn as sns  # For graphical
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import timedelta
from tkcalendar import Calendar, DateEntry
import os
from tryanalysisfunction import *



# configure window for application
window = Tk()
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.state('zoomed')#window full screen
window.title('Poh Cheong Tong Billing and Inventory System')#set name for window title


#make frames for pages
page1 = Frame(window)#login page
page2 = Frame(window)#page for admin
page3 = Frame(window)#page for staff


#set frame in window
for frame in (page1, page2, page3):
    frame.grid(row=0, column=0, sticky='nsew')

#function to show frame in window
def show_frame(frame):
    frame.tkraise()

#show page for admin
show_frame(page1)


#function to connect to database
def connect_database():
    try:
        global conn
        global cursor
        #connect to database
        conn = sqlite3.connect('Poh Cheong Tong.db')
        #define cursor 
        cursor =conn.cursor()
    except:
        messagebox.showerror('Error', 'Cannot connect to database!')



# ============= Page 1 (Log in) =============
#configure log in page
page1.config(background='#DFEEFF')

#connect to database
connect_database()

#set text variables for log in entries as string                                  
user_id_strvar = tk.StringVar()
password_strvar= tk.StringVar()
role_strvar = tk.StringVar()
#set text variables to display in home page
userName = tk.StringVar()
userEmail = tk.StringVar()
userRole = tk.StringVar()
userId = tk.StringVar()

#function to show password in log in
def show_password():
    if btn_value.get() == 1:
        pg1_entryPassword.config(show='')
    else:
        pg1_entryPassword.config(show='*')
        

#function for login
def login():
    connect_database()#connect to database
    
    #get entries from user
    userID = user_id_strvar.get()
    pw = password_strvar.get()
    role = role_strvar.get()
    
    try:
        #select data from database
        cursor.execute('SELECT * FROM user WHERE role=? AND user_id =? AND password LIKE ?', [role, userID, pw])
        
        #retrieve data from database
        login = cursor.fetchall()
        
        #define column in database
        for row in login:
            user_id= row[0]
            user_name = row [1]
            user_email = row[2]
            user_role = row[3]
            password = row[4]
            
    except Exception as ep:
        #show error message if error
        messagebox.showerror("Error",ep)            
    
    #validation for log in entry
    #validate if entry not filled
    if userID == '' or pw == '' or role =='': 
        messagebox.showerror('Login Error','You are required to fill in all the fields.')
    else:
        if login: 
            global userName
            global userEmail
            global userRole
            global userId
            #show log in status
            messagebox.showinfo('Login Status' , 'You have successfully Logged In!')
            
            #display user information in Home Page
            userName.set(user_name)
            userEmail.set(user_email)
            userRole.set(user_role)
            userId.set(user_id)

            #reset log in entry to empty
            for i in [user_id_strvar, password_strvar, role_strvar]:
                i.set('')
            
            if role =='Admin':
                #show frame for admin
                show_frame(page2)
                #show home page
                show_frame(HomeFrame)
            else:
                #show frame for staff
                show_frame(page3)
                #show home page
                show_frame(staff_HomeFrame)
                
        else:
            messagebox.showerror('Login Status', 'Invalid username or password or role')













       
   
#placing logo in log in page
bigimg = ImageTk.PhotoImage(Image.open("Logo.jpeg"))
pg1_img = Label(page1, image = bigimg)
pg1_img.place(x=250, y=280)

#placing label and entry box in log in page
pg1_label = Label(page1, text='ID', font=('Arial', 30, 'bold'), bg='#DFEEFF')
pg1_label.place(x=650, y=250)

pg1_entryID = Entry(page1, font=(20), textvariable = user_id_strvar)
pg1_entryID.place(x=920, y=263)

pg1_label1 = Label(page1, text="Log In", font=('Arial', 70),bg='#DFEEFF')
pg1_label1.place(x=650, y=50)

pg1_label2 = Label(page1, text='Password', font=('Arial', 30, 'bold'),bg='#DFEEFF')
pg1_label2.place(x=650, y=350)

pg1_entryPassword = Entry(page1, font=(20), textvariable = password_strvar, show='*')
pg1_entryPassword.place(x=920, y=363)

pg1_label3 = Label(page1, text='Role', font=('Arial', 30, 'bold'),bg='#DFEEFF')
pg1_label3.place(x=650, y=450)

pg1_entryRole = Entry(page1, font=(20), textvariable = role_strvar)
pg1_entryRole.place(x=920, y=463)

# Check Button for show and hide password
btn_value = IntVar(value=0)
Checkbutton(page1, text="Show password", variable=btn_value, command=show_password, bg='#DFEEFF', font =8).place(x=920, y=390)

#placing submit button in log in page
pg1_button = Button(page1, text='Submit', font=('Arial', 20, 'bold'), bg='#8AC1FF',fg='white', command=login)
pg1_button.place(x=1026, y=520)

# ======== Page 2 (home) ===========
#configure frame for admin
page2.config(background='#DFEEFF')
#frame for Home page
HomeFrame = Frame(page2, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
HomeFrame.place(x=150,y=0, height=850, width = 1390)



#frame for "Poh Cheong Tong"                             
HomeTopFrame=Frame(HomeFrame, bg='#492F7C', highlightbackground='white', highlightthickness=1)
HomeTopFrame.place(x=0,y=0, height=100,width = 1550)

HomeBottomFrame=Frame(HomeFrame, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
HomeBottomFrame.place(x=0,y=100, height=750, width = 1390)



#Display "Poh Cheong Tong"
HomeTopLabel = Label(HomeTopFrame, text='Poh Cheong Tong Medical Hall System', font=('Arial', 30), fg='white', bg='#492F7C')
HomeTopLabel.place(x=10, y=30)


HomeWelcomeLabel = Label(HomeBottomFrame, text='Welcome,', font=('Arial', 40, 'bold'), fg='black', bg='#DFEEFF')
HomeWelcomeLabel.place(x=20, y=20)
                   
HomeNameLabel= Label(HomeBottomFrame, textvariable = userName, font=('Arial', 40, 'bold'), fg='black', bg='#DFEEFF')
HomeNameLabel.place(x=280, y=20)

HomeEmail = Label(HomeBottomFrame, text = "Email :", font=('Arial', 25), fg='black', bg='#DFEEFF')
HomeEmail.place(x=20, y=160)

HomeEmailLabel = Label(HomeBottomFrame, textvariable = userEmail, font=('Arial', 25), fg='black', bg='#DFEEFF')
HomeEmailLabel.place(x=220, y=160)

HomeRole = Label(HomeBottomFrame, text = "Role   :", font=('Arial', 25), fg='black', bg='#DFEEFF')
HomeRole.place(x=20, y=210)

HomeRoleLabel = Label(HomeBottomFrame, textvariable = userRole, font=('Arial', 25), fg='black', bg='#DFEEFF')
HomeRoleLabel.place(x=220, y=210)

HomeID= Label(HomeBottomFrame,text = "ID      :", font=('Arial', 25), fg='black', bg='#DFEEFF')
HomeID.place(x=20, y=110)

HomeIDLabel= Label(HomeBottomFrame,textvariable = userId, font=('Arial', 25), fg='black', bg='#DFEEFF')
HomeIDLabel.place(x=220, y=110)

#frame for logo    
pg2RectangleFrame1=Frame(page2, bg='#492F7C', highlightbackground='white', highlightthickness=1)
pg2RectangleFrame1.place(x=0,y=0, height=100,width = 150)

#placing logo
img = ImageTk.PhotoImage(Image.open("miniLogo.jpeg"))
pg2Logo = Label(pg2RectangleFrame1, image = img)
pg2Logo.place(x=45, y=18)

#function for logout
def logout_system():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to logout?')
    if answer:
        show_frame(page1)
        messagebox.showinfo('Logout' , 'You have successfully Logged Out!')

def open_register():
    # Create Window
    register_window = Tk()
    register_window.title("Poh Cheong Tong Register User")
    register_window.configure(bg='#DFEEFF')
    register_window.state('zoomed')


    # Data Validation
    def insert_data():
        check_count = 0
        msg = ""
        valid_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        # Verify valid email
        if re.search(valid_email, register_user_email.get()):
            check_count += 1
        else:
            msg = "Invalid email"
        # Check length of the password
        if len(register_password.get()) < 5:
            msg = "Password too short"
        else:
            check_count += 1
        # Check password and confirm password match or not
        if register_password.get() != con_password.get():
            msg = "Password and confirm password did not match"
        else:
            check_count += 1
        # Check all input box is not empty
        if register_user_email.get() == "" or register_user_id.get() == "" or register_user_name.get() == "" or register_role.get() == "" or \
                register_password.get() == "" or con_password.get() == "":
            msg = "Input box cannot be empty"
        else:
            check_count += 1
        # If all condition is valid
        if check_count == 4:
            try:
                # Insert data to database
                conn = sqlite3.connect("Poh Cheong Tong.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO user VALUES (:user_id, :user_name, :user_email, :role, :password)",
                            {'user_id': register_user_id.get(), 'user_name': register_user_name.get(), 'user_email': register_user_email.get(),
                             'role': register_role.get(), 'password': register_password.get()})
                conn.commit()
                messagebox.showinfo('confirmation', 'Record Saved')
            except Exception as ect:
                messagebox.showerror('', str(ect))
        else:
            messagebox.showinfo('message', msg)


    # Show password
    def register_show_password():
        if register_btn_value.get() == 1:
            register_password_entry.config(show='')
            con_password_entry.config(show='')
        else:
            register_password_entry.config(show='*')
            con_password_entry.config(show='*')


    # Register Title
    Label(register_window, text='Register', font=('Sigmar One', 75), fg='#707070', bg='#DFEEFF').place(x=600, y=50)

    # Import Logo
    register_logo = ImageTk.PhotoImage(Image.open("Logo.jpeg").resize((240, 240)), master = register_window)
    logo1 = Label(register_window, image=register_logo, bg='#DFEEFF')
    logo1.place(x=200, y=200)

    # User Email Label and Text Entry Box
    Label(register_window, text='Email', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=170)
    register_user_email = StringVar(register_window)
    Entry(register_window, textvariable=register_user_email, font=20).place(x=600, y=210)

    # User ID Label and Text Entry Box
    Label(register_window, text='ID', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=240)
    register_user_id = StringVar(register_window)
    Entry(register_window, textvariable=register_user_id, font=20).place(x=600, y=280)

    # User Name Label and Text Entry Box
    Label(register_window, text='Name', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=310)
    register_user_name = StringVar(register_window)
    Entry(register_window, textvariable=register_user_name, font=20).place(x=600, y=350)

    # Adding combobox drop down list for role
    Label(register_window, text='Role', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=380)
    register_role = tk.StringVar(register_window)
    list_picker = ttk.Combobox(register_window, width=34, state="readonly", textvariable=register_role)
    list_picker['values'] = ('Admin', 'Staff')
    list_picker.place(x=600, y=420)

    # Password Label and Text Entry Box
    Label(register_window, text='Password', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=450)
    register_password = StringVar(register_window)
    register_password_entry = Entry(register_window, textvariable=register_password, font=20, show='*')
    register_password_entry.place(x=600, y=490)

    # Confirm Password Label and Text Entry Box
    Label(register_window, text='Confirm Password', font=('Arial', 20, 'bold'), bg='#DFEEFF').place(x=600, y=520)
    con_password = StringVar(register_window)
    con_password_entry = Entry(register_window, textvariable=con_password, font=20, show='*')
    con_password_entry.place(x=600, y=560)

    # Check Button to show and hide password
    register_btn_value = IntVar(register_window)
    register_btn_value.set(value=0)
    Checkbutton(register_window, text="Show password", variable=register_btn_value, command=register_show_password, bg='#DFEEFF').place(x=600, y=590)

    # Register Button
    Button(register_window, text='Register', font=('Segoe UI', 15, 'bold'), fg='#FFFFFF', bg='#8AC1FF', relief='groove',
           command=insert_data).place(x=915, y=550)

    # Cancel Button
    Button(register_window, text='Cancel', font=('Segoe UI', 15, 'bold'), fg='#FFFFFF', bg='#FF8A8A', relief='groove',
           command=register_window.destroy).place(x=1030, y=550)

    register_window.mainloop()




















# ========== Create side menu bar ==========

# Define and resize the icons to be shown in Menu bar
logout = ImageTk.PhotoImage(Image.open('Logout.png').resize((40, 40), resample=Image.Resampling.LANCZOS))
home = ImageTk.PhotoImage(Image.open('Home.png').resize((40, 40), resample=Image.Resampling.LANCZOS))
billing = ImageTk.PhotoImage(Image.open('Bill.png').resize((40, 40), resample=Image.Resampling.LANCZOS))
inventory = ImageTk.PhotoImage(Image.open('Inventory.png').resize((40, 40), resample=Image.Resampling.LANCZOS))
analysis = ImageTk.PhotoImage(Image.open('Analysis.png').resize((40, 40), resample=Image.Resampling.LANCZOS))
userInfo = ImageTk.PhotoImage(Image.open('User.png').resize((40, 40), resample=Image.Resampling.LANCZOS))
register = ImageTk.PhotoImage(Image.open('Register.png').resize((40, 40), resample=Image.Resampling.LANCZOS))


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
        userInfo_b.config(text='User Info', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        register_b.config(text='Register\n New User', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        
        
    else:
        # Bring the image back
        logout_b.config(image=logout, font=(0, 30))
        home_b.config(image=home, font=(0, 30))
        billing_b.config(image=billing, font=(0, 30))
        inventory_b.config(image=inventory, font=(0, 30))
        analysis_b.config(image=analysis, font=(0, 30))
        userInfo_b.config(image=userInfo, font=(0, 30))
        register_b.config(image=register, font=(0, 30))



window.update()  # For the width to get updated

#placing frame for menu bar
menuFrame = Frame(page2, bg='#492F7C', width=150, height=window.winfo_height(),highlightbackground='white', highlightthickness=1)
menuFrame.place(x=0, y=100)


# Defining the buttons for menu bar in Home page
logout_b = Button(menuFrame, image=logout, bg='#252B61', relief='ridge', command = logout_system)
home_b = Button(menuFrame, image=home, bg='#252B61', relief='ridge', command = lambda: show_frame(HomeFrame))
billing_b = Button(menuFrame, image=billing, bg='#252B61', relief='ridge', command = lambda: show_frame(BillingFrame))
inventory_b = Button(menuFrame, image=inventory, bg='#252B61', relief='ridge', command = lambda: show_frame(InventoryFrame))
analysis_b = Button(menuFrame, image=analysis, bg='#252B61', relief='ridge', command = open_analysis)
userInfo_b = Button(menuFrame, image=userInfo, bg='#252B61', relief='ridge', command= lambda: show_frame(UserInfoFrame))
register_b = Button(menuFrame, image=register, bg='#252B61', relief='ridge', command = open_register)



# Placing buttons in menu bar Home Page
logout_b.place(x=25, y=10, width = 100)
home_b.place(x=25, y=70, width = 100)
billing_b.place(x=25, y=130, width = 100)
inventory_b.place(x=25, y=190, width = 100)
analysis_b.place(x=25, y=250, width = 100)
userInfo_b.place(x=25, y=310, width = 100)
register_b.place(x=25, y=370, width = 100)

# Bind to the frame, if centered or left
menuFrame.bind('<Enter>', lambda e: expandForHome())
menuFrame.bind('<Leave>', lambda e: contractForHome())

# So that Frame does not depend on the widgets inside the frame
menuFrame.grid_propagate(False)



#framing Inventory page
InventoryFrame = Frame(page2, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
InventoryFrame.place(x=150,y=0, height=850, width = 1390)

InventoryTopFrame = Frame(InventoryFrame, bg='#492F7C', highlightbackground='white', highlightthickness=1)
InventoryTopFrame.place(x=0,y=000, height=100,width = 1390)

InventoryBottomFrame = Frame(InventoryFrame, bg='#492F7C', highlightbackground='white', highlightthickness=1)
InventoryBottomFrame.place(x=0,y=100, height=750,width = 1390)

#framing user info page
UserInfoFrame = Frame(page2, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
UserInfoFrame.place(x=150,y=0, height=850, width = 1390)





# ======== Inventory Page ===========
#display 'Inventory' in inventory page
InventoryLabel = Label(InventoryTopFrame, text='Inventory', font=('Arial', 30), fg='white', bg='#492F7C')
InventoryLabel.place(x=20, y=30)




# ======= Create tab ==========
#widget that manages a collection of windows/displays
notebook = ttk.Notebook(InventoryBottomFrame) 

# Create frame for tabs
tab1 = Frame(notebook, bg = '#DFEEFF') #new frame for tab 1
tab2 = Frame(notebook, bg = '#DFEEFF') #new frame for tab 2
tab3 = Frame(notebook, bg = '#DFEEFF') #new frame for tab 3
tab4 = Frame(notebook, bg = '#DFEEFF')

#place tab frames
tab1.pack(fill='both', expand=True)
tab2.pack(fill='both', expand=True)
tab3.pack(fill='both', expand=True)
tab4.pack(fill='both', expand=True)

#add tabs for inventory
notebook.add(tab1,text="Manage Inventory")
notebook.add(tab2,text="Inventory Alert")
notebook.add(tab3,text="Supplier Information")
notebook.add(tab4,text="Category")
notebook.pack(fill='both', expand=True)


#function to set expiry status for inventories
def set_expiry_status():
    connect_database() #connect to database
    cursor.execute('SELECT expiry_date as "d [datetime]" FROM product') #select data in database
    data = cursor.fetchall()#retrieve data from database
    for date, in data:
        if type(date) == str:
            today = datetime.now() #get today's date
            expiry_date = datetime.strptime(date, '%Y-%m-%d') #set format for expiry date
            
            if  today > expiry_date: #compare expiry date with today's date
                
                cursor.execute('UPDATE product SET expiry_status = "Good" WHERE expiry_date >= DATE("now")')
            else:
                cursor.execute('UPDATE product SET expiry_status = "Expired" WHERE expiry_date < DATE("now")')
        else:
            cursor.execute('UPDATE product SET expiry_status = "None"')
            
    # Commit changes
    conn.commit()

    


#function to set stock level for inventory
def stock_level():
    connect_database()#connect to databse
    cursor.execute('SELECT quantity, min_quantity FROM product')#select data in database
    data=cursor.fetchall()#fetch data from database
    
    for quantity in data:
                    
        cursor.execute('UPDATE product SET stock_level = "High" WHERE min_quantity < quantity')
               
        cursor.execute('UPDATE product SET stock_level = "Low" WHERE min_quantity >= quantity')
       
        cursor.execute('UPDATE product SET stock_level = "Finish" WHERE quantity = "0"')
        
        
        
    # Commit changes
    conn.commit()

        



#function to display product data from database in manage inventory tab
def display_product_database():
    #delete inventory list
    ManageInventoryTree.delete(*ManageInventoryTree.get_children()) #delete treeview
    
    connect_database()#connect to database
    cursor.execute("""SELECT product.pro_id, product.product_name, product.buy_price, product.sell_price,
                        product.quantity, product.min_quantity, product.expiry_date, category.cat_name, supplier.sup_id,
                        product.expiry_status,product.stock_level FROM product JOIN category
                        ON product.cat_id = category.cat_id
                        JOIN supplier ON supplier.sup_id= product.sup_id
                    """)#select data in database
    data = cursor.fetchall()#fetch data from database

    # Add our data to the screen
    for records in data:
        ManageInventoryTree.insert('', END, values= records)
		
    # Commit changes
    conn.commit()

  
    

#function to display product data in inventory alert tab
def display_alert_database():
    AlertTree.delete(*AlertTree.get_children()) #delete treeview
    
    connect_database()#connect to database
    cursor.execute("""SELECT product.pro_id, product.product_name, product.quantity, 
                        product.stock_level, product.expiry_status, supplier.sup_name, supplier.sup_phone FROM product 
                        JOIN supplier ON supplier.sup_id= product.sup_id
                        WHERE (product.stock_level LIKE 'Low') OR (product.stock_level LIKE 'Finish') OR (product.expiry_status LIKE 'Expired')
                    """)#select data in database
    data = cursor.fetchall()#fetch data from database

    # Add our data to the screen
    for records in data:
        AlertTree.insert('', END, values= records)
		
    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()




#function to display supplier data in supplier information tab
def display_supplier_database():
    SupplierTree.delete(*SupplierTree.get_children()) #delete treeview
    
    connect_database()#connect to database
    
    cursor.execute("""SELECT supplier.sup_id, supplier.sup_name, supplier.sup_phone, supplier.sup_email,
                    supplier.sup_company, supplier.sup_address FROM supplier ORDER BY supplier.sup_id
                    """)#select data in datbase
    data = cursor.fetchall()#fetch data from database
	
    # Add our data to the screen
    for records in data:
        SupplierTree.insert('', END, values=records)
		
    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()
    

#function to display category data in category tab
def display_category_database():
    CategoryTree.delete(*CategoryTree.get_children()) #delete treeview
    
    connect_database()#connect to database
    cursor.execute('SELECT * FROM category')#select data in database
    data = cursor.fetchall()#fetch data from database

    # Add our data to the screen
    for records in data:
        CategoryTree.insert('', END, values= records)
		
    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()




#manage inventory treeview
#configure inventory treeview
ManageInventoryTree = ttk.Treeview(tab1, selectmode="extended", show='headings',
                    columns = ('Product ID', 'Name', 'Buy Price', 'Sell Price', 'Quantity','Min.Quantity',
                               'Exp.Date', 'Category', 'Supplier ID', 'Expiry Status', 'Stock Level'))
ManageInventoryTree.place(relwidth=1.0, relheight=0.85)

#configure horizontal and vertical scrollbar for treeview
x_scroller= Scrollbar(ManageInventoryTree, orient = HORIZONTAL, command =ManageInventoryTree.xview)
y_scroller= Scrollbar(ManageInventoryTree, orient = VERTICAL, command =ManageInventoryTree.yview)
x_scroller.pack(side= BOTTOM, fill=X)
y_scroller.pack(side= RIGHT, fill=Y)
ManageInventoryTree.config(yscrollcommand=y_scroller.set, xscrollcommand=x_scroller.set)

#set heading name for treeview column
ManageInventoryTree.heading('Product ID', text = 'Product ID', anchor=CENTER)
ManageInventoryTree.heading('Name', text = 'Name', anchor=CENTER)
ManageInventoryTree.heading('Buy Price', text = 'Buy Price (RM)', anchor=CENTER)
ManageInventoryTree.heading('Sell Price', text = 'Sell Price (RM)', anchor=CENTER)
ManageInventoryTree.heading('Quantity', text = 'Quantity', anchor=CENTER)
ManageInventoryTree.heading('Min.Quantity', text = 'Min. Quantity', anchor=CENTER)
ManageInventoryTree.heading('Exp.Date', text = 'Exp. Date', anchor=CENTER)
ManageInventoryTree.heading('Category', text = 'Category', anchor=CENTER)
ManageInventoryTree.heading('Supplier ID', text = 'Supplier ID', anchor=CENTER)
ManageInventoryTree.heading('Expiry Status', text = 'Expiry Status', anchor=CENTER)
ManageInventoryTree.heading('Stock Level', text = 'Stock Level', anchor=CENTER)

#set column data for treeview
ManageInventoryTree.column("Product ID", anchor=CENTER, width=100)
ManageInventoryTree.column("Name", anchor=CENTER, width=200)
ManageInventoryTree.column("Buy Price", anchor=CENTER, width=90)
ManageInventoryTree.column("Sell Price", anchor=CENTER, width=90)
ManageInventoryTree.column("Quantity", anchor=CENTER, width=100)
ManageInventoryTree.column("Min.Quantity", anchor=CENTER, width=120)
ManageInventoryTree.column("Exp.Date", anchor=CENTER, width=140)
ManageInventoryTree.column("Category", anchor=CENTER, width=140)
ManageInventoryTree.column("Supplier ID", anchor=CENTER, width=140)
ManageInventoryTree.column("Expiry Status", anchor=CENTER, width=140)
ManageInventoryTree.column("Stock Level", anchor=CENTER, width=140)

#Inventory Alerts treeview
#configure treeview
AlertTree = ttk.Treeview(tab2, selectmode="browse", show='headings',
                    columns = ('Product ID', 'Product Name', 'Quantity', 'Stock Level', 'Expiry Status', 'Supplier Name', 'Supplier Phone No.'))
AlertTree.place(relwidth=1.0, relheight=1.0)

#configure vertical and horizontal scrollbar for treeview
x2_scroller= Scrollbar(AlertTree, orient = HORIZONTAL, command =AlertTree.xview)
y2_scroller= Scrollbar(AlertTree, orient = VERTICAL, command =AlertTree.yview)
x2_scroller.pack(side= BOTTOM, fill=X)
y2_scroller.pack(side= RIGHT, fill=Y)
AlertTree.config(yscrollcommand=y2_scroller.set, xscrollcommand=x2_scroller.set)

#set heading name for treeview column
AlertTree.heading('Product ID', text = 'Product ID', anchor=CENTER)
AlertTree.heading('Product Name', text = 'Product Name', anchor=CENTER)
AlertTree.heading('Quantity', text = 'Quantity', anchor=CENTER)
AlertTree.heading('Stock Level', text = 'Stock Level', anchor=CENTER)
AlertTree.heading('Expiry Status', text = 'Expiry Status', anchor=CENTER)
AlertTree.heading('Supplier Name', text = 'Supplier Name', anchor=CENTER)
AlertTree.heading('Supplier Phone No.', text = 'Supplier Phone No.', anchor=CENTER)

#set column data in treeview
AlertTree.column("Product ID", anchor=CENTER, width=100)
AlertTree.column("Product Name", anchor=CENTER, width=200)
AlertTree.column("Quantity", anchor=CENTER, width=100)
AlertTree.column("Stock Level", anchor=CENTER, width=200)
AlertTree.column("Expiry Status", anchor=CENTER, width=100)
AlertTree.column("Supplier Name", anchor=CENTER, width=200)
AlertTree.column("Supplier Phone No.", anchor=CENTER, width=200)

#display inventory alert list
display_alert_database()


#Supplier Information Treeview
#configure treeview for supplier information tab 
SupplierTree = ttk.Treeview(tab3, selectmode="browse", show='headings',
            columns = ('Supplier ID', 'Supplier Name', 'Phone No.', 'Email', 'Company', 'Company Address'))
SupplierTree.place(relwidth=1.0, relheight=0.85)

#configure horizontal and vertical scrollbar for treeview 
x3_scroller= Scrollbar(SupplierTree, orient = HORIZONTAL, command =SupplierTree.xview)
y3_scroller= Scrollbar(SupplierTree, orient = VERTICAL, command =SupplierTree.yview)
x3_scroller.pack(side= BOTTOM, fill=X)
y3_scroller.pack(side= RIGHT, fill=Y)
SupplierTree.config(yscrollcommand=y3_scroller.set, xscrollcommand=x3_scroller.set)

#set column heading name for treeview
SupplierTree.heading('Supplier ID', text = 'Supplier ID', anchor=CENTER)
SupplierTree.heading('Supplier Name', text = 'Supplier Name', anchor=CENTER)
SupplierTree.heading('Phone No.', text = 'Phone No.', anchor=CENTER)
SupplierTree.heading('Email', text = 'Email', anchor=CENTER)
SupplierTree.heading('Company', text = 'Company', anchor=CENTER)
SupplierTree.heading('Company Address', text = 'Company Address', anchor=CENTER)

#set column value in treeview
SupplierTree.column("Supplier ID", anchor=CENTER, width=80)
SupplierTree.column("Supplier Name", anchor=CENTER, width=80)
SupplierTree.column("Phone No.", anchor=CENTER, width=100)
SupplierTree.column("Email", anchor=CENTER, width=120)
SupplierTree.column("Company", anchor=CENTER, width=100)
SupplierTree.column("Company Address", anchor=CENTER, width=280)

#display list of supplier in supplier informtation tab
display_supplier_database()



#category treeview
#configure treeview for category tab
CategoryTree = ttk.Treeview(tab4, selectmode="browse", show='headings',
                    columns = ('Category ID', 'Category Name'))
CategoryTree.place(relwidth=1.0, relheight=0.85)

#configure horizontal and vertical scrollbar in treeview
x4_scroller= Scrollbar(CategoryTree, orient = HORIZONTAL, command =CategoryTree.xview)
y4_scroller= Scrollbar(CategoryTree, orient = VERTICAL, command =CategoryTree.yview)
x4_scroller.pack(side= BOTTOM, fill=X)
y4_scroller.pack(side= RIGHT, fill=Y)
CategoryTree.config(yscrollcommand=y4_scroller.set, xscrollcommand=x4_scroller.set)

#set name for category treeview heading
CategoryTree.heading('Category ID', text = 'Category ID', anchor=CENTER)
CategoryTree.heading('Category Name', text = 'Category Name', anchor=CENTER)

#set column value for treeview 
CategoryTree.column("Category ID", anchor=CENTER, width=100)
CategoryTree.column("Category Name", anchor=CENTER, width=200)

#display category data in category tab                            
display_category_database()


#convert input to string for edit_inventory function
edit_pro_id_strvar = tk.StringVar()
edit_product_name_strvar= tk.StringVar()
edit_buy_price_strvar = tk.StringVar()
edit_sell_price_strvar = tk.StringVar()
edit_quantity_intvar = tk.StringVar()
edit_min_quantity_intvar = tk.StringVar()
edit_expiry_date_strvar = tk.StringVar()
edit_category_id_strvar = tk.StringVar()
edit_supplier_id_strvar = tk.StringVar()



#convert input to string for add_inventory function
add_pro_id_strvar = tk.StringVar()
add_product_name_strvar= tk.StringVar()
add_buy_price_strvar = tk.StringVar()
add_sell_price_strvar = tk.StringVar()
add_quantity_intvar = tk.StringVar()
add_min_quantity_intvar = tk.StringVar()
add_expiry_date_strvar = tk.StringVar()
add_category_id_strvar = tk.StringVar()
add_supplier_id_strvar = tk.StringVar()





#convert input to string for search_inventory
search_inventory_by_strvar = tk.StringVar()
search_inventory_strvar = tk.StringVar()





#function for upload product image 
def upload_image():
    global get_imagefile
    global product_image
    global display_image
    file_type= [("png", "*.png"), ("jpg" , "*.jpg")]#type of files that can be uploaded
    get_imagefile = tk.filedialog.askopenfilename(title="SELECT IMAGE", filetypes=(file_type))#File dialog to select files
    product_image= Image.open(get_imagefile)#open file
    product_image_resized= product_image.resize((200,200))#resize product image
    product_image = ImageTk.PhotoImage(product_image_resized)#to display image for label
    display_image = Label(add_productImage_frame, image = product_image)#place image in frame
    display_image.place(x=0, y=0)#place image frame
    


#Image need to be convert into binary before insert into database
def convert_image_into_binary(get_imagefile):
    #read image file to binary
    with open(get_imagefile, 'rb') as file:
        photo_image = file.read()
    return photo_image



#function to empty the fields in Add Inventory page
def reset_add_inventory_fields():
    for i in ['add_pro_id_strvar', 'add_product_name_strvar', 'add_category_id_strvar', 'add_expiry_date_strvar', 'add_buy_price_strvar', 'add_sell_price_strvar', 'add_supplier_id_strvar']:
        exec(f"{i}.set('')")#set fields in Add Inventory page to empty
    try:
        convert_image_into_binary(get_imagefile)#convert image to binary
       
    except NameError:
        pass
    else:
        add_quantity_intvar.set('0')#set quantity field in Add Inventory page to empty
        add_min_quantity_intvar.set('0')#set minimum quantity field in Add Inventory page to empty
        display_image.config(image='')#set image frame to empty
 

#function to fill in entry in Edit Inventory page based on selection
def view_inventory():
    selected = ManageInventoryTree.focus()#select inventory
    values = ManageInventoryTree.item(selected)#get value in selection
    selection = values["values"]#set values in selection
    #set field in edit inventory page according to selected value
    edit_pro_id_strvar.set(selection[0])
    edit_product_name_strvar.set(selection[1])
    edit_buy_price_strvar.set (selection [2])
    edit_sell_price_strvar.set (selection [3])
    edit_quantity_intvar.set (selection [4])
    edit_min_quantity_intvar.set (selection [5])
    edit_expiry_date_strvar.set (selection [6])
    connect_database()#connect to database
    cursor.execute('SELECT cat_id FROM category WHERE cat_name LIKE ?', (str(selection [7]),))#get category ID
    cat_id_strvar = cursor.fetchall()#fetch data from database
    edit_category_id_strvar.set (cat_id_strvar)
    edit_supplier_id_strvar.set (selection [8])       




#function to update inventory data in database
def edit_inventory():
    
    #get input from entry in Edit Inventory page
    ID = edit_pro_id_strvar.get()
    name = edit_product_name_strvar.get()
    category_id= edit_category_id_strvar.get()
    expiry_date= edit_expiry_date_strvar.get()
    quantity = edit_quantity_intvar.get()
    min_quan =  edit_min_quantity_intvar.get()
    supply_price = edit_buy_price_strvar.get()
    selling_price = edit_sell_price_strvar.get()
    supplier_id = edit_supplier_id_strvar.get()
    
    #def format for expiry date
    format = '%Y-%m-%d'
    
    #define true boolean
    res = True
    #validate field is not empty 
    if not ID or not name or not category_id or not expiry_date or not quantity or not min_quan or not supply_price or not selling_price or not supplier_id:
            messagebox.showerror('Error', "Please fill in all the fields!")    

    else:
        try:
            #validate quantity is integer
            int(quantity)
        except ValueError:
            messagebox.showerror('Error', "Please insert the Quantity in number form")
        else:
            try:
                #validate minimum quantity is integer
                int(min_quan)
            except ValueError:
                messagebox.showerror('Error', "Please insert the Minimum Quantity in number form")
            else:
            
                try:
                    #validate format of expiry date input
                    res = bool(datetime.strptime(expiry_date, format))
                except ValueError:
                    messagebox.showerror('Error', "Please insert expiry date in YYYY-MM-DD format")
                        
                else:
                    
                    connect_database()#connect to database
                    cursor.execute("""SELECT product_name FROM product WHERE pro_id = ?""",(ID,))#select data from product table from database
                    find = cursor.fetchall()#fetch data
                    if len(find) == 0: #validate product ID 
                        messagebox.showerror('Error', "Product ID does not exist!")       
            
                    else:
                                
                        connect_database()#connect to database
                        cursor.execute("""UPDATE product SET product_name =?, 
                                            buy_price=?, sell_price =?, quantity =?, min_quantity=?, expiry_date=?, cat_id=?,
                                            sup_id=? WHERE pro_id = ?""",(name,supply_price, selling_price, quantity, min_quan, expiry_date, category_id,
                                            supplier_id, ID))#update product table in database

                        conn.commit() #commit changes made to database
                        conn.close()#close database connection
                        messagebox.showinfo('Record added', f"Record of {name} was successfully updated")
                        set_expiry_status()#set expiry status for product edited
                        stock_level()#set stock elvel status for product edited
                        display_product_database()#display the new list of inventories
                        display_alert_database()# update list of inventories in inventory alert tab
                        editInventoryWindow.destroy()
                        


#function to add inventory to database
def add_inventory():
    #get input from entry in Add Inventory page
    ID = add_pro_id_strvar.get()
    name = add_product_name_strvar.get()
    category_id= add_category_id_strvar.get()
    expiry_date= add_expiry_date_strvar.get()
    quantity = add_quantity_intvar.get()
    min_quan =  add_min_quantity_intvar.get()
    supply_price = add_buy_price_strvar.get()
    selling_price = add_sell_price_strvar.get()
    supplier_id = add_supplier_id_strvar.get()
    #def format for expiry date
    format = '%Y-%m-%d'
    #define true boolean
    res = True
    #validate all entries are filled in Add Inventory pagee
    if not ID or not name or not category_id or not expiry_date or not quantity or not min_quan or not supply_price or not selling_price or not supplier_id:
            messagebox.showerror('Error', "Please fill in all the fields!")    
    else:
        try:
            #convert image to binary
            pro_image = convert_image_into_binary(get_imagefile)
            
        except NameError or FileNotFoundError:
            messagebox.showerror('Error', "Please insert product image")
        else:
            try:
                #validate quantity is integer
                int(quantity)
            except ValueError:
                messagebox.showerror('Error', "Please insert the Quantity in number form")
            else:
                try:
                    #validate minimum quantity is integer
                    int(min_quan)
                except ValueError:
                    messagebox.showerror('Error', "Please insert the Minimum Quantity in number form")
                else:
            
                    try:
                        #validate expiry date is in correct format
                        res = bool(datetime.strptime(expiry_date, format))
                    except ValueError:
                        messagebox.showerror('Error', "Please insert expiry date in YYYY-MM-DD format")
                        
                    else:
                        #validate product ID format
                        if ID[0] !="P":
                            messagebox.showerror('Error', "Please insert the ID in format example P001!")    
                        elif len(ID) !=4:
                            messagebox.showerror('Error', "Please insert the ID in format example P001!")
                        else:
                            try:
                                connect_database()#connect to database
                                conn.execute("""INSERT INTO product (pro_id, product_name, image,
                                            buy_price, sell_price, quantity, min_quantity, expiry_date, cat_id, sup_id)
                                            VALUES(?,?,?,?,?,?,?,?,?,?)""",
                                            (ID, name, pro_image, supply_price, selling_price, quantity, min_quan, expiry_date, category_id,
                                            supplier_id))#insert data into product table in database
                                           
                            #validate UNIQUE constraint    
                            except sqlite3.IntegrityError :
                                 messagebox.showerror('Error', 'Product ID already exists')
                                
                            else:
                                conn.commit()#commit changed to database
                                conn.close()#close database connection
                                messagebox.showinfo('Record added', f"Record of {name} was successfully added")
                                set_expiry_status()#set expiry status for product added
                                stock_level()#set stock level of product added
                                display_product_database()#display the new list of inventories
                                display_alert_database()# update list of inventories in inventory alert tab
                                reset_add_inventory_fields()#set fields in add inventory to empty




def close_edit_inventory():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to quit Edit Inventory?')
    if answer:
        editInventoryWindow.destroy()#close Edit Inventory page
        display_product_database()#display list of inventory


           

#open window to edit inventory records
def open_edit_inventory():
    global editInventoryWindow
    global edit_productImage_frame
    
    connect_database()#connect to database

    #make sure inventory is selected
    if not ManageInventoryTree.selection():
        messagebox.showerror("Error", "Please select an item to edit")
    else:
        #configuring window for Edit Inventory
        editInventoryWindow = Toplevel(window)
        editInventoryWindow.rowconfigure(0, weight=1)
        editInventoryWindow.columnconfigure(0, weight=1)
        editInventoryWindow.state('zoomed')
        editInventoryWindow.configure(bg = '#DFEEFF')
        
        #placing labels, entry boxes, and buttons in Edit Inventory window
        editInventory_label = Label(editInventoryWindow, text="EDIT INVENTORY", font=('Arial', 35, 'bold'),bg='#DFEEFF')
        editInventory_label.place(x=600, y=30)
          
        
        productID_label = Label(editInventoryWindow, text="Product ID", font=('Arial', 18),bg='#DFEEFF')
        productID_label.place(x=200, y=115)
        productID_entry = Entry(editInventoryWindow, font=(20), textvariable = edit_pro_id_strvar, width = 30)
        productID_entry.place(x=200, y=150)
            
        productName_label = Label(editInventoryWindow, text="Product Name", font=('Arial', 18),bg='#DFEEFF')
        productName_label.place(x=200, y=200)
        productName_entry = Entry(editInventoryWindow, font=(20), textvariable = edit_product_name_strvar, width = 30)
        productName_entry.place(x=200, y=240)

            
        category_id_label = Label(editInventoryWindow, text="Category ID", font=('Arial', 18),bg='#DFEEFF')
        category_id_label.place(x=200, y=290)
        category_id_data = cursor.execute('SELECT cat_id FROM category')#select category ID from category table
        category_id_list = [x for x, in category_id_data]#list category IDs
        category_id_combobox =ttk.Combobox(editInventoryWindow, textvariable = edit_category_id_strvar, values = category_id_list, state = "readonly", width = 19, font = 15)
        category_id_combobox.place(x=200, y=330)

            
        expiryDate_label = Label(editInventoryWindow, text="Expiry Date", font=('Arial', 18),bg='#DFEEFF')
        expiryDate_label.place(x=700, y=115)
        expiryDate_entry = Entry(editInventoryWindow, font=(20), textvariable = edit_expiry_date_strvar)
        expiryDate_entry.place(x=700, y=155)

        quantity_label = Label(editInventoryWindow, text="Quantity", font=('Arial', 18),bg='#DFEEFF')
        quantity_label.place(x=700, y=205)
        quantity_entry = Entry(editInventoryWindow, font=(20), textvariable = edit_quantity_intvar)
        quantity_entry.place(x=700, y=245)

        minimumQuantity_label=Label(editInventoryWindow, text="Min. Quantity", font=('Arial', 18),bg='#DFEEFF')
        minimumQuantity_label.place(x=700, y=295)
        minimumQuantity_entry = Entry(editInventoryWindow, font=(20), textvariable = edit_min_quantity_intvar)
        minimumQuantity_entry.place(x=700, y=335)

        supplyPrice_label = Label(editInventoryWindow, text="Supply Price", font=('Arial', 18),bg='#DFEEFF')
        supplyPrice_label.place(x=700, y=385)
        supplyPrice_entry = Entry(editInventoryWindow, font=(20), textvariable = edit_buy_price_strvar)
        supplyPrice_entry.place(x=700, y=425)

        sellingPrice_label = Label(editInventoryWindow, text="Selling Price", font=('Arial', 18),bg='#DFEEFF')
        sellingPrice_label.place(x=700, y=455)
        sellingPrice_entry = Entry(editInventoryWindow, font=(20), textvariable = edit_sell_price_strvar)
        sellingPrice_entry.place(x=700, y=495)

        supplierID_label = Label(editInventoryWindow, text="Supplier ID", font=('Arial', 18),bg='#DFEEFF')
        supplierID_label.place(x=700, y=545)
        supplier_id_data = cursor.execute('SELECT sup_id FROM supplier') #select supplier ID from supplier table
        supplier_id_list = [x for x, in supplier_id_data]#list supplier IDs
        supplier_id_combobox =ttk.Combobox(editInventoryWindow, textvariable = edit_supplier_id_strvar, values = supplier_id_list, state = "readonly", font = 15, width =19)
        supplier_id_combobox.place(x=700, y=585)

        update_button= Button(editInventoryWindow, text= "UPDATE", font=('Arial', 15, 'bold'), command = edit_inventory)
        update_button.place(x=1100, y=115, height = 40, width = 220)

        cancel_edit_button= Button(editInventoryWindow, text= "QUIT", font=('Arial', 15, 'bold'), command = close_edit_inventory)
        cancel_edit_button.place(x=1100, y=165, height = 40, width = 220)

        view_inventory()#set the entries according to selected values

        editInventoryWindow.grab_set()#set window the highest level
        editInventoryWindow.mainloop()#run window
    


#funtion to close Add Inventory window    
def close_add_inventory():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to quit Add Inventory?')
    if answer:
        reset_add_inventory_fields()#set fields in add inventory to empty
        addInventoryWindow.destroy()#close add inventory window
        display_product_database()#display new list of inventory in manage inventory tab
    
    
    
#function to open Add Inventory window
def open_add_inventory():

    connect_database()#connect to database
    global addInventoryWindow
    global add_productImage_frame
    #configure Add Inventory window
    addInventoryWindow = Toplevel(window)
    addInventoryWindow.rowconfigure(0, weight=1)
    addInventoryWindow.columnconfigure(0, weight=1)
    addInventoryWindow.state('zoomed')
    addInventoryWindow.configure(bg = '#DFEEFF')
    
    #place label, buttons and entry boxes in Add Inventory window
    addInventory_label = Label(addInventoryWindow, text="ADD INVENTORY", font=('Arial', 35, 'bold'),bg='#DFEEFF')
    addInventory_label.place(x=620, y=30)
        
    productID_label = Label(addInventoryWindow, text="Product ID", font=('Arial', 18),bg='#DFEEFF')
    productID_label.place(x=200, y=115)
    productID_entry = Entry(addInventoryWindow, font=(20), textvariable = add_pro_id_strvar)
    productID_entry.place(x=200, y=150)
        
    productName_label = Label(addInventoryWindow, text="Product Name", font=('Arial', 18),bg='#DFEEFF')
    productName_label.place(x=200, y=200)
    productName_entry = Entry(addInventoryWindow, font=(20), textvariable = add_product_name_strvar)
    productName_entry.place(x=200, y=240)

    add_productImage_label = Label(addInventoryWindow, text="Product Image", font=('Arial', 18),bg='#DFEEFF')
    add_productImage_label.place(x=200, y=290)
    add_productImage_frame= Frame(addInventoryWindow, bg='white', highlightbackground='black', highlightthickness=1)
    add_productImage_frame.place(x=200, y=330, height=200,width = 200)
    add_chooseImage_button = Button(addInventoryWindow, text="Select Image", command= upload_image)
    add_chooseImage_button.place(x=200, y=550)
        
    category_id_label = Label(addInventoryWindow, text="Category ID", font=('Arial', 18),bg='#DFEEFF')
    category_id_label.place(x=200, y=600)
    category_id_data = cursor.execute('SELECT cat_id FROM category')#select category ID from category table
    category_id_list = [x for x, in category_id_data]#list category IDs
    category_id_combobox =ttk.Combobox(addInventoryWindow, textvariable = add_category_id_strvar, values = category_id_list, state = "readonly",  width = 19, font = 15)
    category_id_combobox.place(x=200, y=640)
        
    expiryDate_label = Label(addInventoryWindow, text="Expiry Date", font=('Arial', 18),bg='#DFEEFF')
    expiryDate_label.place(x=700, y=115)
    expiryDate_entry = Entry(addInventoryWindow, font=(20), textvariable = add_expiry_date_strvar)
    expiryDate_entry.place(x=700, y=155)

    quantity_label = Label(addInventoryWindow, text="Quantity", font=('Arial', 18),bg='#DFEEFF')
    quantity_label.place(x=700, y=205)
    quantity_entry = Entry(addInventoryWindow, font=(20), textvariable = add_quantity_intvar)
    quantity_entry.place(x=700, y=245)

    minimumQuantity_label=Label(addInventoryWindow, text="Min. Quantity", font=('Arial', 18),bg='#DFEEFF')
    minimumQuantity_label.place(x=700, y=295)
    minimumQuantity_entry = Entry(addInventoryWindow, font=(20), textvariable = add_min_quantity_intvar)
    minimumQuantity_entry.place(x=700, y=335)

    supplyPrice_label = Label(addInventoryWindow, text="Supply Price", font=('Arial', 18),bg='#DFEEFF')
    supplyPrice_label.place(x=700, y=385)
    supplyPrice_entry = Entry(addInventoryWindow, font=(20), textvariable = add_buy_price_strvar)
    supplyPrice_entry.place(x=700, y=425)

    sellingPrice_label = Label(addInventoryWindow, text="Selling Price", font=('Arial', 18),bg='#DFEEFF')
    sellingPrice_label.place(x=700, y=455)
    sellingPrice_entry = Entry(addInventoryWindow, font=(20), textvariable = add_sell_price_strvar)
    sellingPrice_entry.place(x=700, y=495)

    supplierID_label = Label(addInventoryWindow, text="Supplier ID", font=('Arial', 18),bg='#DFEEFF')
    supplierID_label.place(x=700, y=545)
    supplier_id_data = cursor.execute('SELECT sup_id FROM supplier')#select supplier ID from category table
    supplier_id_list = [x for x, in supplier_id_data]#list supplier IDs
    supplier_id_combobox =ttk.Combobox(addInventoryWindow, textvariable = add_supplier_id_strvar, values = supplier_id_list, state = "readonly",  width = 19, font = 15)
    supplier_id_combobox.place(x=700, y=585)

    add_button= Button(addInventoryWindow, text= "ADD", font=('Arial', 15, 'bold'), command = add_inventory)
    add_button.place(x=1100, y=115, height = 40, width = 220)

    cancel_add_button= Button(addInventoryWindow, text= "QUIT", font=('Arial', 15, 'bold'), command = close_add_inventory)
    cancel_add_button.place(x=1100, y=165, height = 40, width = 220)

    addInventoryWindow.grab_set()#set window to highest level
    addInventoryWindow.mainloop()#run window

        
#function to remove inventory records
def remove_inventory():
    #validate inventory is selected
    if not ManageInventoryTree.selection():
        messagebox.showerror("Error", "Please select an item to delete")
        
    else:
    	# Add a little message box for fun
        response = messagebox.askyesno("Delete", "This Will Delete EVERYTHING SELECTED From The Table\nAre You Sure?!")

	#Add logic for message box
        if response == 1:
		# Designate selections
                x = ManageInventoryTree.selection()

		# Create List of ID's
                ids_to_delete = []
		
		# Add selections to ids_to_delete list
                for record in x:
                    ids_to_delete.append(ManageInventoryTree.item(record, 'values')[0])

                #connect to database
                connect_database()
		

		# Delete Everything From The Table
                cursor.executemany("DELETE FROM product WHERE pro_id = ?", [(a,) for a in ids_to_delete])


		# Reset List
                ids_to_delete = []


		# Commit changes
                conn.commit()


                #display new database values
                display_product_database()
                display_alert_database()
                
		#display delete status
                messagebox.showinfo('Status' , 'You have successfully deleted the items!')
                

#function to search inventory
def search_inventory():
    #set combobox value to input
    cb_value1 = search_inventory_by_strvar.get()
    #set search entry value to input
    cb_value2 = search_inventory_strvar.get()

    if cb_value1 == "ID":
        connect_database()#connect to database
        cursor.execute("""SELECT product.pro_id, product.product_name, product.buy_price, product.sell_price,
                        product.quantity, product.min_quantity, product.expiry_date, category.cat_name, supplier.sup_id,
                        product.expiry_status,product.stock_level FROM product JOIN category
                        ON product.cat_id = category.cat_id
                        JOIN supplier ON supplier.sup_id= product.sup_id
                        WHERE product.pro_id LIKE ?""", ('%'+cb_value2+'%',))#select data from database
        data = cursor.fetchall()#fetch data selected
        
        if not cb_value2:#validate search field is filled            
            messagebox.showerror('Error', 'Please fill in the search field')

        elif len(data) !=0:#validate record existence
            ManageInventoryTree.delete(*ManageInventoryTree.get_children())
            
            for records in data:#display data fetched from database
                ManageInventoryTree.insert('', END, values= records)
                
            conn.commit()#commit changes
        else:
            messagebox.showerror('Error', 'Record is not found')
    

    elif cb_value1 == "NAME":
        connect_database()#conenct to database
        cursor.execute("""SELECT product.pro_id, product.product_name, product.buy_price, product.sell_price,
                        product.quantity, product.min_quantity, product.expiry_date, category.cat_name, supplier.sup_id,
                        product.expiry_status,product.stock_level FROM product JOIN category
                        ON product.cat_id = category.cat_id
                        JOIN supplier ON supplier.sup_id= product.sup_id
                        WHERE product.product_name LIKE ?""", ("%" + cb_value2 + "%",))#select data from database
        data = cursor.fetchall()#fetch data selected
        
        if not cb_value2:#validate search field is filled      
            messagebox.showerror('Error', 'Please fill in the search field')

        elif len(data) !=0:#validate record existence
            ManageInventoryTree.delete(*ManageInventoryTree.get_children())
            
            for records in data:#display data fetched from database
                ManageInventoryTree.insert('', END, values= records)
                
            conn.commit()#commit changes
            
        else:
            messagebox.showerror('Error', 'Record is not found')
    else:
        messagebox.showerror('Error', "Please select ID or NAME in the drop down box!")

        
#function to clear search fields and list all inventories
def clear_search_inventory():
    display_product_database()#list all inventories
    tab1_search_combobox.current(0)#clear search combobox
    for i in ['search_inventory_strvar']:
        exec(f"{i}.set('')")#clear search field
        

#set expiry status for inventory
set_expiry_status()
#set stock level for inventory
stock_level()
#display list of inventories
display_product_database()


#convert input to string for add_supplier
add_sup_id_strvar = tk.StringVar()
add_sup_name_strvar= tk.StringVar()
add_sup_phone_strvar = tk.StringVar()
add_sup_email_strvar = tk.StringVar()
add_sup_company_strvar = tk.StringVar()
add_sup_address_strvar = tk.StringVar()


#convert input to string for edit_supplier
edit_sup_id_strvar = tk.StringVar()
edit_sup_name_strvar= tk.StringVar()
edit_sup_phone_strvar = tk.StringVar()
edit_sup_email_strvar = tk.StringVar()
edit_sup_company_strvar = tk.StringVar()
edit_sup_address_strvar = tk.StringVar()


#convert input to string for search_supplier
search_supplier_by_strvar = tk.StringVar()
search_supplier_strvar = tk.StringVar()

#function to clear fields for Add Supplier window
def reset_add_supplier_fields():
    for i in ['add_sup_id_strvar', 'add_sup_name_strvar', 'add_sup_phone_strvar','add_sup_email_strvar', 'add_sup_company_strvar','add_sup_address_strvar']:
        exec(f"{i}.set('')")


#function to set supplier details in Edit Supplier window         
def view_supplier():
    selected = SupplierTree.focus()
    values = SupplierTree.item(selected)
    selection = values["values"]
    edit_sup_id_strvar.set(selection [0])
    edit_sup_name_strvar.set(selection [1])
    edit_sup_phone_strvar.set (selection [2])
    edit_sup_email_strvar.set (selection [3])
    edit_sup_company_strvar.set (selection [4])
    edit_sup_address_strvar.set (selection [5])

#function to add supplier information into database
def add_supplier():
    #get input from entry in Add Supplier page
    ID = add_sup_id_strvar.get()
    name = add_sup_name_strvar.get()
    phone_no= add_sup_phone_strvar.get()
    email = add_sup_email_strvar.get()
    company = add_sup_company_strvar.get()
    address =  add_sup_address_strvar.get()
    #def format for email
    valid_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    
    #validate all entries are filled in Add Supplier page
    if not ID or not name or not phone_no or not email or not company or not address:
        messagebox.showerror('Error', "Please fill in all the fields!")    
    else:
        #validate supplier ID format
        if ID[0] !="S":
            messagebox.showerror('Error', "Please insert the ID in format example S001!")    
        elif len(ID) !=4:
            messagebox.showerror('Error', "Please insert the ID in format example S001!")
        #validate phone number length
        elif len(phone_no) < 10 or len(phone_no) > 11:
            messagebox.showerror('Error', "Phone number has to be 10 or 11 numbers")
        #validate email address format
        elif re.search(valid_email, email) is None:
            messagebox.showerror('Error', "Invalid email")
        else:
            try:
                connect_database()#connect to database
                conn.execute("""INSERT INTO supplier (sup_id, sup_name, sup_phone, sup_email, sup_company, sup_address)
                                VALUES(?,?,?,?,?,?)""",
                                (ID, name,phone_no,email, company, address))#insert data into supplier table in database
                
            #validate ID UNIQUE constraint                       
            except sqlite3.IntegrityError:
                messagebox.showerror('Error', "Supplier ID already exists")
                        
            else:
                conn.commit()#commit changes
                conn.close()#close conenction to database
                messagebox.showinfo('Record added', f"Record of {name} was successfully added")
                display_supplier_database()#display list of suppliers in supplier information tab
                reset_add_supplier_fields()#clear entries in Add Supplier window
 


def edit_supplier():
    connect_database()#connect to database
    
    #get intput from entry in Edit Supplier Page
    ID = edit_sup_id_strvar.get()
    name = edit_sup_name_strvar.get()
    phone_no= edit_sup_phone_strvar.get()
    email = edit_sup_email_strvar.get()
    company = edit_sup_company_strvar.get()
    address =  edit_sup_address_strvar.get()
    #set email format
    valid_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    #select data in database
    cursor.execute("SELECT * FROM supplier WHERE sup_id = ?", (ID,))
    #fetch data from database
    validate = cursor.fetchall()

    #validate fields are not empty
    if not ID or not name or not phone_no or not email or not company or not address:
            messagebox.showerror('Error', "Please fill in all the fields!")    
    else:
        #validate ID format
        if ID[0] !="S":
            messagebox.showerror('Error', "Please insert the ID in format example S001!")
        #validate length of ID
        elif len(ID) !=4:
            messagebox.showerror('Error', "Please insert the ID in format example S001!")
        #validate length of phone number
        elif len(phone_no) < 10 or len(phone_no) > 11:
            messagebox.showerror('Error', "Phone number has to be 10 or 11 numbers")
        #validate email format
        elif re.search(valid_email, email)is None:
            messagebox.showerror('Error', "Invalid email")
        #validate existence of supplier ID
        elif len(validate) == 0:
            messagebox.showerror('Error', "Supplier ID does not exist")
            
        else:

            connect_database()#connect to database
            cursor.execute("""UPDATE supplier SET sup_name = ?, sup_phone = ?, sup_email = ?, sup_company = ?, sup_address = ? WHERE sup_id = ?"""
                             ,(name,phone_no,email, company,address,ID))#edit values in database
            conn.commit()#commit changes
                
            messagebox.showinfo('Record added', f"Record of {name} was successfully edited")
            display_supplier_database()##display new list of supplier information
            editSupplierWindow.destroy()#close Edit Supplier window
            

#function to close Add Supplier window
def close_add_supplier():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to quit Add Supplier?')
    if answer:
        reset_add_supplier_fields()#reset fields in Add Supplier page
        addSupplierWindow.destroy()#close Add Supplier page
        display_supplier_database()#display list of supplier information

#function to open add supplier window
def open_add_supplier():

    connect_database()#connect to database
    global add_companyAddress_entry
    global addSupplierWindow

    #configure Add Supplier window
    addSupplierWindow = Toplevel(window)
    addSupplierWindow.rowconfigure(0, weight=1)
    addSupplierWindow.columnconfigure(0, weight=1)
    addSupplierWindow.state('zoomed')
    addSupplierWindow.configure(bg = '#DFEEFF')

    #configure label, entry boxes, and buttons in Add Supplier window
    addSupplier_label = Label(addSupplierWindow, text="ADD SUPPLIER", font=('Arial', 35, 'bold'),bg='#DFEEFF')
    addSupplier_label.place(x=620, y=30)
        
    supplierID_label = Label(addSupplierWindow, text="Supplier ID", font=('Arial', 18),bg='#DFEEFF')
    supplierID_label.place(x=200, y=115)
    supplierID_entry = Entry(addSupplierWindow, font=(20), textvariable = add_sup_id_strvar)
    supplierID_entry.place(x=200, y=150)
        
    supplierName_label = Label(addSupplierWindow, text="Supplier Name", font=('Arial', 18),bg='#DFEEFF')
    supplierName_label.place(x=200, y=200)
    supplierName_entry = Entry(addSupplierWindow, font=(20), textvariable = add_sup_name_strvar)
    supplierName_entry.place(x=200, y=240)
        
    supplierPhone_label = Label(addSupplierWindow, text="Phone No.", font=('Arial', 18),bg='#DFEEFF')
    supplierPhone_label.place(x=200, y=290)
    supplierPhone_entry = Entry(addSupplierWindow, font=(20), textvariable = add_sup_phone_strvar)
    supplierPhone_entry.place(x=200, y=330)

    supplierEmail_label = Label(addSupplierWindow, text="Supplier Email", font=('Arial', 18),bg='#DFEEFF')
    supplierEmail_label.place(x=700, y=115)
    supplierEmail_entry = Entry(addSupplierWindow, font=(20), textvariable = add_sup_email_strvar)
    supplierEmail_entry.place(x=700, y=150)

    supplierCompany_label=Label(addSupplierWindow, text="Supplier Company", font=('Arial', 18),bg='#DFEEFF')
    supplierCompany_label.place(x=700, y=200)
    supplierCompany_entry = Entry(addSupplierWindow, font=(20), textvariable = add_sup_company_strvar)
    supplierCompany_entry.place(x=700, y=240)

    companyAddress_label = Label(addSupplierWindow, text="Company Address", font=('Arial', 18),bg='#DFEEFF')
    companyAddress_label.place(x=700, y=290)
    add_companyAddress_entry = Entry(addSupplierWindow, font=(20), textvariable = add_sup_address_strvar)
    add_companyAddress_entry.place(x=700, y=330,  height = 30, width =700)


    add_button= Button(addSupplierWindow, text= "ADD", font=('Arial', 15, 'bold'), command = add_supplier)
    add_button.place(x=1100, y=115, height = 40, width = 220)

    cancel_add_button= Button(addSupplierWindow, text= "QUIT", font=('Arial', 15, 'bold'), command = close_add_supplier)
    cancel_add_button.place(x=1100, y=165, height = 40, width = 220)

    addSupplierWindow.grab_set()#set add supplier window highest level
    addSupplierWindow.mainloop()#run add supplier window


#function to close edit supplier window                                
def close_edit_supplier():
    #request confirmation
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to quit EDIT Supplier?')
    if answer:
        editSupplierWindow.destroy()#close edit supplier window
        display_supplier_database()#display list of supplier information

#function to open edit supplier window
def open_edit_supplier():

    connect_database()#connect to database
    global editSupplierWindow
    global edit_companyAddress_entry

    #validate select supplier in treeview
    if not SupplierTree.selection():
        messagebox.showerror("Error", "Please select an item to edit")
    else:
        #configure supplier window
        editSupplierWindow = Toplevel(window)
        editSupplierWindow.rowconfigure(0, weight=1)
        editSupplierWindow.columnconfigure(0, weight=1)
        editSupplierWindow.state('zoomed')
        editSupplierWindow.configure(bg = '#DFEEFF')

        #configure labels, entry boxes, and buttons in edit supplier window
        editSupplier_label = Label(editSupplierWindow, text="EDIT SUPPLIER", font=('Arial', 35, 'bold'),bg='#DFEEFF')
        editSupplier_label.place(x=620, y=30)
            
        supplierID_label = Label(editSupplierWindow, text="Supplier ID", font=('Arial', 18),bg='#DFEEFF')
        supplierID_label.place(x=200, y=115)
        supplierID_entry = Entry(editSupplierWindow, font=(20), textvariable = edit_sup_id_strvar)
        supplierID_entry.place(x=200, y=150)
            
        supplierName_label = Label(editSupplierWindow, text="Supplier Name", font=('Arial', 18),bg='#DFEEFF')
        supplierName_label.place(x=200, y=200)
        supplierName_entry = Entry(editSupplierWindow, font=(20), textvariable = edit_sup_name_strvar)
        supplierName_entry.place(x=200, y=240)
            
        supplierPhone_label = Label(editSupplierWindow, text="Phone No.", font=('Arial', 18),bg='#DFEEFF')
        supplierPhone_label.place(x=200, y=290)
        supplierPhone_entry = Entry(editSupplierWindow, font=(20), textvariable = edit_sup_phone_strvar)
        supplierPhone_entry.place(x=200, y=330)

        supplierEmail_label = Label(editSupplierWindow, text="Supplier Email", font=('Arial', 18),bg='#DFEEFF')
        supplierEmail_label.place(x=700, y=115)
        supplierEmail_entry = Entry(editSupplierWindow, font=(20), textvariable = edit_sup_email_strvar)
        supplierEmail_entry.place(x=700, y=150)

        supplierCompany_label=Label(editSupplierWindow, text="Supplier Company", font=('Arial', 18),bg='#DFEEFF')
        supplierCompany_label.place(x=700, y=200)
        supplierCompany_entry = Entry(editSupplierWindow, font=(20), textvariable = edit_sup_company_strvar)
        supplierCompany_entry.place(x=700, y=240)

        companyAddress_label = Label(editSupplierWindow, text="Company Address", font=('Arial', 18),bg='#DFEEFF')
        companyAddress_label.place(x=700, y=295)
        edit_companyAddress_entry = Entry(editSupplierWindow, font=(20), textvariable = edit_sup_address_strvar)
        edit_companyAddress_entry.place(x=700, y=335, height = 30, width =700)


        edit_button= Button(editSupplierWindow, text= "EDIT", font=('Arial', 15, 'bold'), command = edit_supplier)
        edit_button.place(x=1100, y=115, height = 40, width = 220)

        cancel_edit_button= Button(editSupplierWindow, text= "QUIT", font=('Arial', 15, 'bold'), command = close_edit_supplier)
        cancel_edit_button.place(x=1100, y=165, height = 40, width = 220)

        view_supplier()# fill entry according to selected values
        

        editSupplierWindow.grab_set()# set edit supplier window as highest level
        editSupplierWindow.mainloop()# run edit supplier window 


                    

#function to remove supplier records
def remove_supplier():
    #validate select treeview
    if not SupplierTree.selection():
        messagebox.showerror("Error", "Please select an item to delete")
            
    else:
        connect_database()#connect to database
            
            # Add a little message box for fun
        response = messagebox.askyesno("Delete", "This Will Delete EVERYTHING SELECTED From The Table\nAre You Sure?!")

            #Add logic for message box
        if response == 1:
                # set selection
                x = SupplierTree.focus()
                # define values from selection
                values = SupplierTree.item(x)
                # set values
                selection = values ["values"]
                # select data in database and set as value
                cursor.execute("SELECT product.sup_id, supplier.sup_id FROM product NATURAL JOIN supplier WHERE supplier.sup_id = ?", (str(selection[0]),))
                # fetch data from database
                data = cursor.fetchall()
                # validate that product does not use supplier ID
                if len(data)== 0:
                    cursor.execute("DELETE FROM supplier WHERE sup_id = ?", (str(selection[0]),))# delete data in database
                    conn.commit()# commit changes
                    display_supplier_database()# display list of supplier information
                else:
                    messagebox.showerror("Error", "Supplier ID needed for product \nCannot Delete!")

#function to search list of supplier information
def search_supplier():
    #set combobox value to input
    cb_value1 = search_supplier_by_strvar.get()
    # set search entry value to input
    cb_value2 = search_supplier_strvar.get()

    if cb_value1 == "ID":
        connect_database()#connect to database
        cursor.execute("""SELECT sup_id, sup_name, sup_phone, sup_email, sup_company, sup_address FROM supplier
                        WHERE sup_id LIKE ?""", ('%'+cb_value2+'%',))# select data in database
        data = cursor.fetchall()#fetch data from database
        
        if not cb_value2:# validate search field is filled            
            messagebox.showerror('Error', 'Please fill in the search field')

        elif len(data) !=0:# validate record existence
            SupplierTree.delete(*SupplierTree.get_children())#delete supplier treeview
            
            for records in data:
                SupplierTree.insert('', END, values= records)#display list of supplier searched
                
            conn.commit()#commit changes
        else:
            messagebox.showerror('Error', 'Record is not found')
    

    elif cb_value1 == "NAME":
        connect_database()#connect to database
        cursor.execute("""SELECT sup_id, sup_name, sup_phone, sup_email, sup_company, sup_address FROM supplier
                        WHERE sup_name LIKE ?""", ("%" + cb_value2 + "%",))# select data in database
        data = cursor.fetchall()#fetch data from database
        
        if not cb_value2:# validate search field is filled          
            messagebox.showerror('Error', 'Please fill in the search field')

        elif len(data) !=0:# validate record existence
            SupplierTree.delete(*SupplierTree.get_children())#delete supplier treeview
            
            for records in data:
                SupplierTree.insert('', END, values= records)#display list of supplier searched
                
            conn.commit()
            
        else:
            messagebox.showerror('Error', 'Record is not found')
    else:
        messagebox.showerror('Error', "Please select ID or NAME in the drop down box!")

#function to clear search field in supplier tab
def clear_search_supplier():
    display_supplier_database()# show full list of supplier tab
    tab3_search_combobox.current(0)# set search combobox to 'search by'
    for i in ['search_supplier_strvar']:
        exec(f"{i}.set('')")#set search entry field to empty


#convert input to string for add_category
add_cat_id_strvar = tk.StringVar()
add_cat_name_strvar= tk.StringVar()


#convert input to string for edit_category
edit_cat_id_strvar = tk.StringVar()
edit_cat_name_strvar= tk.StringVar()


#convert input to string for search_category
search_category_by_strvar = tk.StringVar()
search_category_strvar = tk.StringVar()

#empty fields in add category window
def reset_add_category_fields():
    for i in ['add_cat_id_strvar', 'add_cat_name_strvar']:
        exec(f"{i}.set('')")

#insert values of category selection in edit category page
def view_category():
    selected = CategoryTree.focus()
    values = CategoryTree.item(selected)
    selection = values["values"]
    edit_cat_id_strvar.set(selection [0])
    edit_cat_name_strvar.set(selection [1])

#function to add category in the system
def add_category():
    ID = add_cat_id_strvar.get()
    name = add_cat_name_strvar.get()
     #validation    
    if not ID or not name :
        messagebox.showerror('Error', "Please fill in all the fields!")    
    else:
        if ID[0] !="C":
            messagebox.showerror('Error', "Please insert the ID in format example C001!")    
        elif len(ID) !=4:
            messagebox.showerror('Error', "Please insert the ID in format example C001!")

        else:
            try:
                connect_database()
                conn.execute("""INSERT INTO category (cat_id, cat_name)
                                VALUES(?,?)""",
                                (ID, name))
                                   
            except sqlite3.IntegrityError:
                messagebox.showerror('Error', "Category ID already exists")
                        
            else:
                conn.commit()
                conn.close()
                messagebox.showinfo('Record added', f"Record of {name} was successfully added")
                display_category_database()
                reset_add_category_fields()
                
#edit category details                
def edit_category():
    connect_database()
    ID = edit_cat_id_strvar.get()
    name = edit_cat_name_strvar.get()
    cursor.execute("SELECT * FROM category WHERE cat_id = ?", (ID,))
    validate = cursor.fetchall()
    #validation 
    if not ID or not name:
            messagebox.showerror('Error', "Please fill in all the fields!")    
    else:
        if ID[0] !="C":
            messagebox.showerror('Error', "Please insert the ID in format example S001!")    
        elif len(ID) !=4:
            messagebox.showerror('Error', "Please insert the ID in format example S001!")

        elif len(validate) == 0:
            messagebox.showerror('Error', "Category ID does not exist")
            
        else:
            connect_database()
            cursor.execute("""UPDATE category SET cat_name = ? WHERE cat_id = ?"""
                             ,(name,ID))
            conn.commit()
                
            messagebox.showinfo('Record added', f"Record of {name} was successfully edited")
            display_category_database()
            editCategoryWindow.destroy()

#close add category page
def close_add_category():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to quit Add Category?')
    if answer:
        reset_add_category_fields()
        addCategoryWindow.destroy()
        display_category_database()

#open add category page
def open_add_category():

    connect_database()
    global addCategoryWindow
    
    addCategoryWindow = Toplevel(window)
    addCategoryWindow.rowconfigure(0, weight=1)
    addCategoryWindow.columnconfigure(0, weight=1)
    addCategoryWindow.state('zoomed')
    addCategoryWindow.configure(bg = '#DFEEFF')
    
    addCategory_label = Label(addCategoryWindow, text="ADD CATEGORY", font=('Arial', 35, 'bold'),bg='#DFEEFF')
    addCategory_label.place(x=620, y=30)
        
    categoryID_label = Label(addCategoryWindow, text="Category ID", font=('Arial', 18),bg='#DFEEFF')
    categoryID_label.place(x=700, y=115)
    categoryID_entry = Entry(addCategoryWindow, font=(20), textvariable = add_cat_id_strvar)
    categoryID_entry.place(x=700, y=150)
        
    categoryName_label = Label(addCategoryWindow, text="Category Name", font=('Arial', 18),bg='#DFEEFF')
    categoryName_label.place(x=700, y=200)
    categoryName_entry = Entry(addCategoryWindow, font=(20), textvariable = add_cat_name_strvar)
    categoryName_entry.place(x=700, y=240)

    add_button= Button(addCategoryWindow, text= "ADD", font=('Arial', 15, 'bold'), command = add_category)
    add_button.place(x=700, y=290, height = 40, width = 220)

    cancel_add_button= Button(addCategoryWindow, text= "QUIT", font=('Arial', 15, 'bold'), command = close_add_category)
    cancel_add_button.place(x=700, y=340, height = 40, width = 220)

    addCategoryWindow.grab_set()
    addCategoryWindow.mainloop()

#close edit category page
def close_edit_category():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to QUIT Edit Category?')
    if answer:
        editCategoryWindow.destroy()
        display_category_database()

#open edit category page
def open_edit_category():

    connect_database()
    global editCategoryWindow


    if not CategoryTree.selection():
        messagebox.showerror("Error", "Please select an item to edit")
    else:

        editCategoryWindow = Toplevel(window)
        editCategoryWindow.rowconfigure(0, weight=1)
        editCategoryWindow.columnconfigure(0, weight=1)
        editCategoryWindow.state('zoomed')
        editCategoryWindow.configure(bg = '#DFEEFF')
        
        editCategory_label = Label(editCategoryWindow, text="EDIT CATEGORY", font=('Arial', 35, 'bold'),bg='#DFEEFF')
        editCategory_label.place(x=620, y=30)
            
        categoryID_label = Label(editCategoryWindow, text="Category ID", font=('Arial', 18),bg='#DFEEFF')
        categoryID_label.place(x=700, y=115)
        categoryID_entry = Entry(editCategoryWindow, font=(20), textvariable = edit_cat_id_strvar)
        categoryID_entry.place(x=700, y=150)
            
        categoryName_label = Label(editCategoryWindow, text="Category Name", font=('Arial', 18),bg='#DFEEFF')
        categoryName_label.place(x=700, y=200)
        categoryName_entry = Entry(editCategoryWindow, font=(20), textvariable = edit_cat_name_strvar)
        categoryName_entry.place(x=700, y=240)
            


        edit_button= Button(editCategoryWindow, text= "EDIT", font=('Arial', 15, 'bold'), command = edit_category)
        edit_button.place(x=700, y=290, height = 40, width = 220)

        cancel_edit_button= Button(editCategoryWindow, text= "QUIT", font=('Arial', 15, 'bold'), command = close_edit_category)
        cancel_edit_button.place(x=700, y=340, height = 40, width = 220)

        view_category()

        editCategoryWindow.grab_set()
        editCategoryWindow.mainloop()


# Remove category records
def remove_category():
    if not CategoryTree.selection():
        messagebox.showerror("Error", "Please select an item to delete")
        
    else:
        connect_database()
        
    	# Add a little message box for fun
        response = messagebox.askyesno("Delete", "This Will Delete EVERYTHING SELECTED From The Table\nAre You Sure?!")

	#Add logic for message box
        if response == 1:
		# Designate selections
                x = CategoryTree.focus()
                values = CategoryTree.item(x)
                selection = values ["values"]
                cursor.execute("SELECT product.cat_id, category.cat_id FROM product NATURAL JOIN category WHERE category.cat_id LIKE ?", (str(selection[0]),))
                data = cursor.fetchall()
                if len(data)== 0:
                    cursor.execute("DELETE FROM category WHERE cat_id = ?", (str(selection[0]),))
                    conn.commit()
                    display_category_database()
                else:
                    messagebox.showerror("Error", "Category ID needed for product \nCannot Delete!")



#function to search category
def search_category():
    cb_value1 = search_category_by_strvar.get()
    cb_value2 = search_category_strvar.get()

    if cb_value1 == "ID":
        connect_database()
        cursor.execute("""SELECT cat_id, cat_name FROM category
                        WHERE cat_id LIKE ?""", ('%' + cb_value2 + '%',))
        data = cursor.fetchall()
        
        if not cb_value2:            
            messagebox.showerror('Error', 'Please fill in the search field')

        elif len(data) !=0:
            CategoryTree.delete(*CategoryTree.get_children())
            
            for records in data:
                CategoryTree.insert('', END, values= records)
                
            conn.commit()
        else:
            messagebox.showerror('Error', 'Record is not found')
    

    elif cb_value1 == "NAME":
        connect_database()
        cursor.execute("""SELECT cat_id, cat_name FROM category
                        WHERE cat_name LIKE ?""", ("%" + cb_value2 + "%",))
        data = cursor.fetchall()
        
        if not cb_value2:            
            messagebox.showerror('Error', 'Please fill in the search field')

        elif len(data) !=0:
            CategoryTree.delete(*CategoryTree.get_children())
            
            for records in data:
                CategoryTree.insert('', END, values= records)
                
            conn.commit()
            
        else:
            messagebox.showerror('Error', 'Record is not found')
    else:
        messagebox.showerror('Error', "Please select ID or NAME in the drop down box!")


def clear_search_category():
    display_category_database()
    tab4_search_combobox.current(0)
    for i in ['search_category_strvar']:
        exec(f"{i}.set('')")



#place buttons in manage inventory tab
tab1_add_button= Button(tab1, text= "ADD", font=('Arial', 15, 'bold'),command = open_add_inventory)
tab1_add_button.place(x=910, y=620)

tab1_edit_button= Button(tab1, text= "EDIT", font=('Arial', 15, 'bold'),fg = 'blue', command = open_edit_inventory)
tab1_edit_button.place(x=1000, y=620)

tab1_delete_button= Button(tab1, text= "DELETE", font=('Arial', 15, 'bold'), fg = 'red',command = remove_inventory)
tab1_delete_button.place(x=1100, y=620)

tab1_search_button= Button(tab1, text= "SEARCH", font=('Arial', 15, 'bold'), command = search_inventory)
tab1_search_button.place(x=680, y=620)


tab1_search_combobox =ttk.Combobox(tab1, textvariable = search_inventory_by_strvar, values = ["SEARCH BY","ID","NAME"], state = "readonly", font=5)
tab1_search_combobox.place(x=100, y=630)
tab1_search_combobox.current(0)

tab1_search_entry =Entry(tab1, textvariable = search_inventory_strvar, font = 5)
tab1_search_entry.place(x=370, y=630)

tab1_clear_button= Button(tab1, text= "CLEAR", font=('Arial', 15, 'bold'), command = clear_search_inventory)
tab1_clear_button.place(x=800, y=620)



#place button in supplier information tab
tab3_add_button= Button(tab3, text= "ADD", font=('Arial', 15, 'bold'), command= open_add_supplier )
tab3_add_button.place(x=910, y=620)

tab3_edit_button= Button(tab3, text= "EDIT", font=('Arial', 15, 'bold'),fg = 'blue', command = open_edit_supplier)
tab3_edit_button.place(x=1000, y=620)

tab3_delete_button= Button(tab3, text= "DELETE", font=('Arial', 15, 'bold'), fg = 'red',command = remove_supplier)
tab3_delete_button.place(x=1100, y=620)

tab3_search_button= Button(tab3, text="SEARCH", font=('Arial', 15, 'bold'), command = search_supplier)
tab3_search_button.place(x=680, y=620)

tab3_search_combobox =ttk.Combobox(tab3, textvariable = search_supplier_by_strvar, values = ["SEARCH BY","ID","NAME"], state = "readonly", font=5)
tab3_search_combobox.place(x=100, y=630)
tab3_search_combobox.current(0)

tab3_search_entry =Entry(tab3, textvariable = search_supplier_strvar, font=5)
tab3_search_entry.place(x=370, y=630)

tab3_clear_button= Button(tab3, text= "CLEAR", font=('Arial', 15, 'bold'), command = clear_search_supplier)
tab3_clear_button.place(x=800, y=620)




#place button in category tab
tab4_add_button= Button(tab4, text= "ADD", font=('Arial', 15, 'bold'), command = open_add_category)
tab4_add_button.place(x=910, y=620)

tab4_edit_button= Button(tab4, text= "EDIT", font=('Arial', 15, 'bold'), fg = 'blue',command = open_edit_category)
tab4_edit_button.place(x=1000, y=620)

tab4_delete_button= Button(tab4, text= "DELETE", font=('Arial', 15, 'bold'),fg = 'red', command = remove_category)
tab4_delete_button.place(x=1100, y=620)

tab4_search_button= Button(tab4, text= "SEARCH", font=('Arial', 15, 'bold'), command = search_category)
tab4_search_button.place(x=680, y=620)

tab4_search_combobox =ttk.Combobox(tab4, textvariable = search_category_by_strvar, values = ["SEARCH BY","ID","NAME"], state = "readonly", font=5)
tab4_search_combobox.place(x=100, y=630)
tab4_search_combobox.current(0)

tab4_search_entry =Entry(tab4, textvariable = search_category_strvar, font=5)
tab4_search_entry.place(x=370, y=630)

tab4_clear_button= Button(tab4, text= "CLEAR", font=('Arial', 15, 'bold'), command = clear_search_category)
tab4_clear_button.place(x=800, y=620)



#==============User Information Page=======================


#configure page for user information
UserInfoTopFrame = Frame(UserInfoFrame, bg='#492F7C', highlightbackground='white', highlightthickness=1)
UserInfoTopFrame.place(x=0,y=000, height=100,width = 1390)

UserInfoBottomLeftFrame = Frame(UserInfoFrame, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
UserInfoBottomLeftFrame.place(x=0,y=100, height=750, width = 300)

UserInfoBottomRightFrame = Frame(UserInfoFrame, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
UserInfoBottomRightFrame.place(x=300,y=100, height=750,width = 1090)

UserInfoLabel = Label(UserInfoTopFrame, text='User Information', font=('Arial', 30), fg='white', bg='#492F7C')
UserInfoLabel.place(x=20, y=30)


#display list of user information
def display_userInfo_database():
    UserInfoTree.delete(*UserInfoTree.get_children()) #delete treeview
    
    connect_database()
    cursor.execute('SELECT * FROM user')
    data = cursor.fetchall()

    # Add our data to the screen
    for records in data:
        UserInfoTree.insert('', END, values= records)
		
    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()


#place list in user information page
UserInfoTree = ttk.Treeview(UserInfoBottomRightFrame, selectmode="browse", show='headings',
            columns = ('User ID', 'Name', 'Email', 'Role', 'Password'))
UserInfoTree.place(relwidth=1.0, relheight=1.0)

#place horizontal and vertical scrollbar in user information
x2_scroller= Scrollbar(UserInfoTree, orient = HORIZONTAL, command =UserInfoTree.xview)
y2_scroller= Scrollbar(UserInfoTree, orient = VERTICAL, command =UserInfoTree.yview)
x2_scroller.pack(side= BOTTOM, fill=X)
y2_scroller.pack(side= RIGHT, fill=Y)
UserInfoTree.config(yscrollcommand=y2_scroller.set, xscrollcommand=x2_scroller.set)

#set the heading for the table in user information
UserInfoTree.heading('User ID', text = 'User ID', anchor=CENTER)
UserInfoTree.heading('Name', text = 'Name', anchor=CENTER)
UserInfoTree.heading('Email', text = 'Email', anchor=CENTER)
UserInfoTree.heading('Role', text = 'Role', anchor=CENTER)
UserInfoTree.heading('Password', text = 'Password', anchor=CENTER)

#set values for column in the table in user information
UserInfoTree.column("User ID", anchor=CENTER, width=80)
UserInfoTree.column("Name", anchor=CENTER, width=80)
UserInfoTree.column("Email", anchor=CENTER, width=120)
UserInfoTree.column("Role", anchor=CENTER, width=100)
UserInfoTree.column("Password", anchor=CENTER, width=280)

#display list of user information
display_userInfo_database()


#convert input to string for edit_userInfo
user_ID_strvar = tk.StringVar()
user_name_strvar= tk.StringVar()
user_email_strvar = tk.StringVar()
user_role_strvar = tk.StringVar()
user_password_strvar = tk.StringVar()

#convert input to string for search_userInfo
search_userInfo_by_strvar = tk.StringVar()
search_userInfo_strvar = tk.StringVar()


#set entry box in user information page to empty
def reset_userInfo_fields():
    for i in ['user_ID_strvar', 'user_name_strvar','user_email_strvar', 'user_role_strvar','user_password_strvar']:
        exec(f"{i}.set('')")


#set the user info entry to selected values
def view_userInfo():
    if not UserInfoTree.selection():
        messagebox.showerror("Error", "Please select an item to fill in the entry")
    else:
        selected = UserInfoTree.focus()
        values = UserInfoTree.item(selected)
        selection = values["values"]
        user_ID_strvar.set(selection[0])
        user_name_strvar.set(selection[1])
        user_email_strvar.set(selection[2])
        user_role_strvar.set(selection[3])
        user_password_strvar.set(selection[4])


#update details of user information
def edit_userInfo():
    connect_database()
    ID = user_ID_strvar.get()
    name = user_name_strvar.get()
    email= user_email_strvar.get()
    role = user_role_strvar.get()
    password = user_password_strvar.get()
    valid_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    cursor.execute("SELECT * FROM user WHERE user_id = ?", (ID,))
    validate = cursor.fetchall()
     
    if not ID or not name or not email or not role or not password:
            messagebox.showerror('Error', "Please fill in all the fields!")    
    else:
        if ID[0] !="U":
            messagebox.showerror('Error', "Please insert the ID in format example U001!")    
        elif len(ID) !=4:
            messagebox.showerror('Error', "Please insert the ID in format example U001!")
        elif re.search(valid_email, email)is None:
            messagebox.showerror('Error', "Invalid email")
        elif len(password) < 5:
            messagebox.showerror('Error', "Password too short")
        elif len(validate) == 0:
            messagebox.showerror('Error', "User ID does not exist")
            
        else:

            connect_database()
            cursor.execute("""UPDATE user SET user_name = ?, user_email = ?, role = ?, password = ? WHERE user_id = ?"""
                             ,(name,email, role, password,ID))
            conn.commit()
                
            messagebox.showinfo('Record added', f"Record of {name} was successfully edited")
            display_userInfo_database()
            
           
# Remove user information records
def remove_userInfo():
    
    if not UserInfoTree.selection():
        messagebox.showerror("Error", "Please select an item to delete")
        
    else:
    	# Add a little message box for fun
        response = messagebox.askyesno("Delete", "This Will Delete EVERYTHING SELECTED From The Table\nAre You Sure?!")

	#Add logic for message box
        if response == 1:
		# Designate selections
                x = UserInfoTree.selection()

		# Create List of ID's
                ids_to_delete = []
		
		# Add selections to ids_to_delete list
                for record in x:
                    ids_to_delete.append(UserInfoTree.item(record, 'values')[0])

                #connect to database
                connect_database()
		

		# Delete Everything From The Table
                cursor.executemany("DELETE FROM user WHERE user_id = ?", [(a,) for a in ids_to_delete])


		# Reset List
                ids_to_delete = []


		# Commit changes
                conn.commit()


                #display new database values
                display_userInfo_database()
                
		#for fun
                messagebox.showinfo('Status' , 'You have successfully deleted the items!')


#search user information 
def search_userInfo():
    cb_value1 = search_userInfo_by_strvar.get()
    cb_value2 =search_userInfo_strvar.get()

    if cb_value1 == "ID":
        connect_database()
        cursor.execute("""SELECT * FROM user
                        WHERE user_id LIKE ?""", ('%'+ cb_value2 + '%',))
        data = cursor.fetchall()
        
        if not cb_value2:            
            messagebox.showerror('Error', 'Please fill in the search field')

        elif len(data) !=0:
            UserInfoTree.delete(*UserInfoTree.get_children())
            
            for records in data:
                UserInfoTree.insert('', END, values= records)
                
            conn.commit()
        else:
            messagebox.showerror('Error', 'Record is not found')
    

    elif cb_value1 == "NAME":
        connect_database()
        cursor.execute("""SELECT * FROM user
                        WHERE user_name LIKE ?""", ("%" + cb_value2 + "%",))
        data = cursor.fetchall()
        
        if not cb_value2:            
            messagebox.showerror('Error', 'Please fill in the search field')

        elif len(data) !=0:
            UserInfoTree.delete(*UserInfoTree.get_children())
            
            for records in data:
                UserInfoTree.insert('', END, values= records)
                
            conn.commit()
            
        else:
            messagebox.showerror('Error', 'Record is not found')

    elif cb_value1 == "ROLE":
        connect_database()
        cursor.execute("""SELECT * FROM user
                        WHERE role LIKE ?""", ("%" + cb_value2 + "%",))
        data = cursor.fetchall()
        
        if not cb_value2:            
            messagebox.showerror('Error', 'Please fill in the search field')

        elif len(data) !=0:
            UserInfoTree.delete(*UserInfoTree.get_children())
            
            for records in data:
                UserInfoTree.insert('', END, values= records)
                
            conn.commit()
            
        else:
            messagebox.showerror('Error', 'Record is not found')
        
    else:
        messagebox.showerror('Error', "Please select ID, NAME, or ROLE in the drop down box!")

def clear_userInfo_entry():
    display_userInfo_database()
    userInfo_search_combobox.current(0)
    userInfo_role_combobox.set('')
    for i in [user_ID_strvar, user_name_strvar, user_email_strvar, user_password_strvar, search_userInfo_strvar]:
        i.set('')



#UI for user info page

userInfo_id_label = Label(UserInfoBottomLeftFrame, text="User ID", font=('Arial', 18), bg='#DFEEFF')
userInfo_id_label.place(x=10, y=30)

userInfo_id_entry = Entry(UserInfoBottomLeftFrame, font=('Arial', 15), textvariable = user_ID_strvar)
userInfo_id_entry.place(x=10,y=70)

userInfo_name_label = Label(UserInfoBottomLeftFrame, text="Name", font=('Arial', 18), bg='#DFEEFF')
userInfo_name_label.place(x=10, y=110)

userInfo_name_entry = Entry(UserInfoBottomLeftFrame, font=('Arial', 15), textvariable = user_name_strvar)
userInfo_name_entry.place(x=10,y=150)

userInfo_email_label = Label(UserInfoBottomLeftFrame, text="Email", font=('Arial', 18), bg='#DFEEFF')
userInfo_email_label.place(x=10, y=190)

userInfo_email_entry = Entry(UserInfoBottomLeftFrame, font=('Arial', 15), textvariable = user_email_strvar)
userInfo_email_entry.place(x=10,y=230)

userInfo_role_label = Label(UserInfoBottomLeftFrame, text="Role", font=('Arial', 18), bg='#DFEEFF')
userInfo_role_label.place(x=10, y=270)

userInfo_role_combobox =ttk.Combobox(UserInfoBottomLeftFrame, textvariable = user_role_strvar, values = ["Admin","Staff"], state = "readonly", font =13 )
userInfo_role_combobox.place(x=10, y=310)
userInfo_role_combobox.set('')


user_password_label = Label(UserInfoBottomLeftFrame, text="Password", font=('Arial', 18), bg='#DFEEFF')
user_password_label.place(x=10, y=350)

user_password_entry = Entry(UserInfoBottomLeftFrame, font=('Arial', 15), textvariable = user_password_strvar)
user_password_entry.place(x=10,y=390)


userInfo_delete_button= Button(UserInfoBottomLeftFrame, text= "DELETE", font=('Arial', 13, 'bold'), fg='red', command = remove_userInfo)
userInfo_delete_button.place(x=70, y=430)


userInfo_edit_button= Button(UserInfoBottomLeftFrame, text= "EDIT", font=('Arial', 13, 'bold'),fg='blue', command = edit_userInfo)
userInfo_edit_button.place(x=10, y=430)

userInfo_select_button = Button(UserInfoBottomLeftFrame, text= "SELECT", font=('Arial', 13, 'bold'), command = view_userInfo)
userInfo_select_button.place(x=160, y=430)


userInfo_search_label = Label(UserInfoBottomLeftFrame, text="Search", font=('Arial', 18), bg='#DFEEFF')
userInfo_search_label.place(x=10, y=480)

userInfo_search_button= Button(UserInfoBottomLeftFrame, text= "SEARCH", font=('Arial', 13, 'bold'), command = search_userInfo)
userInfo_search_button.place(x=10, y=600)

userInfo_search_combobox =ttk.Combobox(UserInfoBottomLeftFrame, textvariable = search_userInfo_by_strvar, values = ["SEARCH BY","ID","NAME","ROLE"], state = "readonly", font =13)
userInfo_search_combobox.place(x=10, y=520)
userInfo_search_combobox.current(0)

userInfo_search_entry =Entry(UserInfoBottomLeftFrame, font=('Arial', 15), textvariable = search_userInfo_strvar)
userInfo_search_entry.place(x=10, y=560)

userInfo_clear_button =Button(UserInfoBottomLeftFrame, text= "CLEAR", font=('Arial', 13, 'bold'), command = clear_userInfo_entry)
userInfo_clear_button.place(x=100, y=600)




#framing Billing page
BillingFrame = Frame(page2, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
BillingFrame.place(x=150,y=0, height=850, width = 1390)

BillingTopFrame = Frame(BillingFrame, bg='#492F7C', highlightbackground='white', highlightthickness=1)
BillingTopFrame.place(x=0,y=000, height=100,width = 1390)

BillingBottomFrame = Frame(BillingFrame, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
BillingBottomFrame.place(x=0,y=100, height=750,width = 1390)



# ======== Billing Page ===========
#display 'Billing' in billing page
BillingLabel = Label(BillingTopFrame, text='Billing', font=('Arial', 30), fg='white', bg='#492F7C')
BillingLabel.place(x=20, y=30)


# Display table from database
def displayInvoice():
    conn = sqlite3.connect("Poh Cheong Tong.db")
    cur = conn.cursor()
    cur.execute("SELECT invoice_id, date, total FROM invoice GROUP BY invoice_id")
    rows = cur.fetchall()
    for row in rows:  # loop to display all the invoice
        ManageInvoice.insert("", END, values=row)


# Create tree view for Manage Invoice
ManageInvoice = ttk.Treeview(BillingBottomFrame, selectmode="extended", show='headings',
                             columns=('Invoice ID', 'Date Time', 'Total Price'))
ManageInvoice.place(relwidth=1, relheight=0.7)

ttk.Scrollbar(ManageInvoice, orient="vertical", command=ManageInvoice.yview).pack(side=RIGHT, fill=Y)

ManageInvoice.heading('Invoice ID', text='Invoice ID', anchor=CENTER)
ManageInvoice.heading('Date Time', text='Date & Time', anchor=CENTER)
ManageInvoice.heading('Total Price', text='Total Price', anchor=CENTER)

ManageInvoice.column("Invoice ID", anchor=CENTER, width=100)
ManageInvoice.column("Date Time", anchor=CENTER, width=200)
ManageInvoice.column("Total Price", anchor=CENTER, width=140)

displayInvoice()

# ======= Create New Bill ======
def createInvoice():
    addInvoice = Toplevel(window)
    addInvoice.geometry('1400x850')
    addInvoice.configure(bg='#DFEEFF')
    addInvoice.title('Create New Bill')

    conn = sqlite3.connect('Poh Cheong Tong.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM invoice')

    # Heading
    heading_frame = Frame(addInvoice, bd=8, bg="#DFEEFF")
    heading_frame.pack(side=TOP, fill="x")

    heading_label = Label(heading_frame, text="Add New Invoice", font=("times new roman", 18, "bold"), bg="#DFEEFF",
                          fg="black", pady=5)
    heading_label.pack()

    # add items function in create new invoice page
    def add_item_bt():
        if len(add_products.get()) == 0 or inventory.count(add_products.get()) == 0:
            tk.messagebox.showerror("Error", "Product Not Found!")
            return
        else:
            if not pro_stock.get().isdigit():
                tk.messagebox.showerror('Error', 'Invalid quantity!')
                return
            if int(pro_stock.get()) <= 0:
                tk.messagebox.showerror('Error', 'Invalid quantity!')
                return
            cur.execute("SELECT pro_id ,product_name FROM product WHERE product_name = ? ", (add_products.get(),))
            row = cur.fetchall()
            row = [list(row[0])]  # fetch the data from database and put into list
            # get the max ID from invoice table
            cur.execute('select max(ID) from invoice')
            PKid = cur.fetchall()

            if PKid[0][0] is not None:  # if ID is nothing
                for i in range(len(row)):  # each row ID + 1
                    ID_pk = PKid[i][0] + 1
            else:
                ID_pk = 1
            row[0].insert(0, ID_pk)  # row 0 = ID
            ID_pk += 1
            # get the input of product quantity and insert it into list
            row[0].append(int(pro_stock.get()))
            # calculate the product price by multiply unit price and quantity selected
            row[0].append((int(pro_stock.get()) * name_price[add_products.get()]))
            row = [tuple(row[0])]  # convert the row into tuple
            itemID.set(row[0][1])  # value from row 0, column 1 insert into itemID entry
            itemPrice.set(name_price[add_products.get()])  # get the price of selected product
            itemName.set(row[0][2])  # value from row 0, column 2 insert into itemName entry
            cur.execute("SELECT quantity FROM product WHERE pro_id=?", (row[0][1],))  # get the quantity from product id
            qli = cur.fetchall()
            # calculate the actual quantity of product - the quantity of product in the dictionary - quantity input
            if ((qli[0][0] - int(qty_id[row[0][1]])) - int(pro_stock.get())) < 0:
                if li[0][0] != 0:
                    tk.messagebox.showerror('Error', 'Product with this quantity not available!')
                    return
                else:
                    tk.messagebox.showerror('Error', 'Product out of stock!')
                    return

            qty_id[row[0][1]] += int(pro_stock.get())  # quantity of the product in dict(0) + quantity input
            itemQuantity.set(qli[0][0] - qty_id[row[0][1]])  # Left stock = actual quantity - quantity input
            for data in row:
                order_tabel.insert('', 'end', values=data)  # insert the selected product into table

            # convert price into 2dp
            price_product = (float(subtotalPrice.get()) + (float(int(pro_stock.get())) * float(name_price[add_products.get()])))
            price = "{:.2f}".format(price_product)
            subtotalPrice.set(price)
            # clear the entry after the item is successfully add
            pro_stock.set('1')
            add_products.set('')

    def remove_item_bt(event=None):
        re = order_tabel.selection()  # select product to remove from the cart
        if len(re) == 0:  # if not selecting any item
            tk.messagebox.showerror('Error', 'No item are selected')
            return
        if tk.messagebox.askyesno('Alert!', 'Remove Item?'):
            x = order_tabel.get_children()  # get the item id
            re = re[0]
            ol = []  # create empty list
            fi = []  # create empty list
            for n in x:
                if n != re:
                    ol.append(tuple((order_tabel.item(n))['values']))
                else:
                    fi = ((order_tabel.item(n))['values'])  # get the item values
            order_tabel.delete(*order_tabel.get_children())  # delete the products
            for n in ol:
                order_tabel.insert('', 'end', values=n)
            itemQuantity.set('')  # clear the field
            itemName.set('')
            itemID.set('')
            itemPrice.set('')
            add_products.set('')
            pro_stock.set('1')
            qty_id[str(fi[1])] -= fi[3]  # the actual quantity of product - quantity of selected product
            delproprice = float(subtotalPrice.get()) - float(fi[4])  # subtotal price - the item price
            delprice = "{:.2f}".format(delproprice)  # convert the subtotal price into float which is 2dp
            subtotalPrice.set(delprice)
            return

    # clear the entry box
    def clear_bt():
        itemID.set("")
        itemName.set("")
        itemPrice.set("")
        itemQuantity.set("")
        add_products.set("")
        pro_stock.set("1")

    # update the data to database
    def generateInvoice():
        if username_entry == "" or pay_amount_entry == ""  or paymeth_entry == "":
            tk.messagebox.showerror('Error', 'Please fill in the empty fields')
            return
        x = order_tabel.get_children()  # get customer's orders
        if len(x) == 0:
            tk.messagebox.showerror('Error', 'Empty cart!')
            return
        if tk.messagebox.askyesno('Alert!', 'Do you want to proceed?') == False:
            return
        a = []  # create an empty list
        cur.execute("select max(invoice_id) from invoice")
        invoice1 = cur.fetchall()
        invoice1 = invoice1[0][0] + 1  # invoice ID + 1 based on previous id
        for i in x:
            l = order_tabel.item(i)
            a.append(l['values'])  # append the values of order list treeview into the empty list 'a'

        for i in a:  # insert the invoice data into database
            sqlquery = "INSERT INTO invoice " \
                       "(invoice_id, date, user_id, pro_id, quantity, total, paid, change, payment_method) " \
                       "VALUES (?,?,?,?,?,?,?,?,?)"
            values = (
            int(invoice1), str(datetime_entry.get()), str(username_entry.get()), i[1], i[3], str(subtotalPrice.get()),
            str(pay_amount_entry.get()), str(change_entry.get()), str(paymeth_entry.get()))
            cur.execute(sqlquery, values, )
            # update the product quantity after the product is sold
            cur.execute("select quantity from product where pro_id=?", (i[1],))
            pq = cur.fetchall()
            cur.execute("update product set quantity=? where pro_id=?", (pq[0][0] - qty_id[str(i[1])], i[1]))
            conn.commit()
        tk.messagebox.showinfo('Success', 'Transaction Successful!')
        # Update the Billing Page tree view
        ManageInvoice.delete(*ManageInvoice.get_children())
        displayInvoice()

        # Clear create new invoice field
        order_tabel.delete(*order_tabel.get_children())
        itemQuantity.set('')
        itemName.set('')
        itemID.set('')
        itemPrice.set('')
        subtotalPrice.set(0)
        change.set(0)
        payamount.set('')
        PaymentMethod.set('')
        add_products.set('')
        pro_stock.set('1')
        # Re-fetch the products' data from databade
        cur.execute("select pro_id from product")
        l = cur.fetchall()
        for i in range(0, len(l)):
            qty_id[l[i][0]] = 0

    # === Invoice details ===
    invoice_frame1 = Frame(addInvoice, bg="#DFEEFF", relief=FLAT, height=100)
    invoice_frame1.pack(side=TOP, fill="x")

    # Invoice ID
    cur.execute("select max(invoice_id) from invoice")  # get the maximum no of invoice ID
    invoice = cur.fetchall()
    invoice = int(invoice[0][0]) + 1  # new invoice id = maximum invoice ID +1
    Label(invoice_frame1, text="Invoice ID: " + str(invoice), font=("arial", 13), bg="#DFEEFF").grid(row=0, column=0,
                                                                                                     padx=10)

    # Date & Time
    date_label = Label(invoice_frame1, text="Date & Time", font=("arial", 13), bg='#DFEEFF')
    date_label.grid(row=0, column=3, padx=20, pady=10)
    datetime_entry = Entry(invoice_frame1, width=20, font=("arial", 13), bd=1)
    datetime_entry.insert(END, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # get current time
    datetime_entry.grid(row=0, column=4, padx=5, pady=10)

    # declaring cashier name variable
    username = StringVar()
    query = "SELECT user_id FROM user"
    user_data = conn.execute(query)
    user_list = [r for r, in user_data]  # create a user list

    # Cashier Name
    username_label = Label(invoice_frame1, text="Cashier Name", font=("arial", 13), bd=1, bg='#DFEEFF')
    username_label.grid(row=0, column=5, padx=20, pady=10)
    username_entry = ttk.Combobox(invoice_frame1, font=("arial", 12), textvariable=username, values=user_list)
    username_entry.grid(row=0, column=6, padx=5, pady=10)

    # ========= Order Lists (Tree View for Selected Products) ==========
    

    # Create tree view to insert the products added into order lists
    orderList_frame = Frame(addInvoice, width=700, bg='#DFEEFF', relief=RIDGE)
    orderList_frame.place(x=5, y=300, height=400, width=1360)

    order_tabel_frame = Frame(orderList_frame)
    order_tabel_frame.place(x=10, y=25, height=300, width=1345)

    scrollbar_order_x = Scrollbar(order_tabel_frame, orient=HORIZONTAL)
    scrollbar_order_y = Scrollbar(order_tabel_frame, orient=VERTICAL)

    order_tabel = ttk.Treeview(order_tabel_frame, style="Treeview",
                               columns=("id", "product id", "name", 'quantity', 'total price'),
                               selectmode="browse", height=6, yscrollcommand=scrollbar_order_y.set,
                               xscrollcommand=scrollbar_order_x.set)
    order_tabel.heading("id", text="Transaction ID")
    order_tabel.heading("product id", text="Product ID")
    order_tabel.heading("name", text="Product Name")
    order_tabel.heading("quantity", text="Quantity")
    order_tabel.heading("total price", text="Total Price")
    order_tabel["displaycolumns"] = ("id", "product id", "name", "quantity", "total price")
    order_tabel["show"] = "headings"
    order_tabel.column("id", width=200, anchor='center', stretch=NO)
    order_tabel.column("product id", width=200, anchor='center', stretch=NO)
    order_tabel.column("name", width=200, anchor='center', stretch=NO)
    order_tabel.column("quantity", width=200, anchor='center', stretch=NO)
    order_tabel.column("total price", width=200, anchor='center', stretch=NO)

    scrollbar_order_x.pack(side=BOTTOM, fill=X)
    scrollbar_order_x.configure(command=order_tabel.xview)
    scrollbar_order_y.pack(side=RIGHT, fill=Y)
    scrollbar_order_y.configure(command=order_tabel.yview)

    order_tabel.pack(fill=BOTH, expand=1)

    productFrame = Frame(addInvoice, width=700, bg="#DFEEFF", relief=FLAT)
    productFrame.place(x=0, y=105)

    # Quantity input by user
    pro_stock = StringVar(value=1)

    # Variables for product need to add in cart
    add_products = StringVar()
    product_data = conn.execute("SELECT product_name FROM product")
    pro_list = [p for p, in product_data]  # create products list

    # For search frame: Search product entry and buttons
    additem_bt = ttk.Button(productFrame, text="Add Item", command=add_item_bt)
    additem_bt.grid(row=3, column=4, padx=5, pady=10)

    remove_bt = ttk.Button(productFrame, text="Remove Item", command=remove_item_bt)
    remove_bt.grid(row=3, column=5, padx=5, pady=10)

    clear_bt = ttk.Button(productFrame, text="Clear", command=clear_bt)
    clear_bt.grid(row=3, column=6, padx=5, pady=10)

    search_label = Label(productFrame, text="Search Products", font=("arial", 13), bg='#DFEEFF', pady=0)
    search_label.grid(row=1, column=3, padx=10, pady=5)
    product_combobox = ttkwidgets.autocomplete.AutocompleteCombobox(productFrame, width=25, font=("arial", 12),
                                                                    textvariable=add_products, completevalues=pro_list)
    product_combobox.grid(row=1, column=4, columnspan=2, padx=10, pady=5)

    qty_label = Label(productFrame, text="Quantity", font=("arial", 13), bg='#DFEEFF', pady=0)
    qty_label.grid(row=2, column=3, padx=10, pady=5)
    qty_entry = Entry(productFrame, font=("arial", 12), textvariable=pro_stock, width=26)
    qty_entry.grid(row=2, column=4, columnspan=2, padx=10, pady=5)

    # fetch product name and sell price of the product from database
    cur.execute("SELECT product_name, sell_price FROM product")
    li = cur.fetchall()
    inventory = [] # create an empty list
    name_price = dict()  # create dictionary on the product's name and price {product name : product sell price}
    for i in range(0, len(li)):  # looping on the products in range of 0 to the number of products
        if inventory.count(li[i][0]) == 0:
            inventory.append(li[i][0])  # append the sell price of the products into inventory
        name_price[li[i][0]] = li[i][1]  # the product's sell price = the row i column 0(product name) in dictionary
    product_combobox.set_completion_list(inventory)  # set the inventory list into the product combo box
    li = ['Product Id', 'Product Name', 'Price', 'Left Stock']
    for i in range(0, 4):  # looping on the list in range of 0 to 4
        Label(productFrame, text=li[i], font="roboto 14 bold", bg="#FFFFFF")

    # Products id, name, price, stock (Do not editable)
    # selected items variables（Cart）
    itemID = StringVar()
    itemName = StringVar()
    itemPrice = StringVar()
    itemQuantity = StringVar()

    product_label = Label(productFrame, text="Products ID", font=("arial", 13), bg='#DFEEFF', pady=0)
    product_label.grid(row=1, column=0, pady=5)
    product_entry = Entry(productFrame, font=("arial", 12), textvariable=itemID, width=25, state='readonly')
    product_entry.grid(row=1, column=1, pady=5)

    proname_label = Label(productFrame, text="Products Name", font=("arial", 13), bg='#DFEEFF', pady=0)
    proname_label.grid(row=2, column=0, pady=5)
    proname_entry = Entry(productFrame, font=("arial", 12), textvariable=itemName, width=25, state='readonly')
    proname_entry.grid(row=2, column=1, pady=5)

    proprice_label = Label(productFrame, text="Price", font=("arial", 13), bg='#DFEEFF', pady=0)
    proprice_label.grid(row=3, column=0, padx=20, pady=5)
    proprice_entry = Entry(productFrame, font=("arial", 12), textvariable=itemPrice, width=25, state='readonly')
    proprice_entry.grid(row=3, column=1, pady=5)

    stock_label = Label(productFrame, text="Left Stock", font=("arial", 13), bg='#DFEEFF', pady=0)
    stock_label.grid(row=4, column=0, pady=5)
    stock_entry = Entry(productFrame, font=("arial", 12), textvariable=itemQuantity, width=25, state='readonly')
    stock_entry.grid(row=4, column=1, pady=5)

    # Create dictionary to fetch product id from database
    qty_id = dict()
    cur.execute("select pro_id from product")
    pl = cur.fetchall()  #fetch the pro_id from database
    for i in range(0, len(pl)):  # looping on create dictionary for all the products
        qty_id[pl[i][0]] = 0  # set dictionary {product id 1 : price = 0}, {product id 2: price = 0}, ....

    # variable for subtotal price
    subtotalPrice = IntVar(value=0)
    # Sub total
    total_price_label = Label(orderList_frame, text="Sub Total", font=("arial", 13, "bold"), bg="#DFEEFF")
    total_price_label.pack(side=LEFT, anchor=SW, padx=5, pady=15)
    total_price_entry = Entry(orderList_frame, font="arial 12", textvariable=subtotalPrice, state='readonly', width=10)
    total_price_entry.pack(side=LEFT, anchor=SW, padx=5, pady=15)

    # Payment
    paymentframe = Frame(orderList_frame, bg="#DFEEFF", relief=FLAT)
    paymentframe.pack(side=LEFT, anchor=SW, padx=10, pady=5)
    paymentM_label = Label(paymentframe, text="Payment Method", font=("arial", 13, "bold"), bg="#DFEEFF")
    paymentM_label.grid(row=0, column=0, padx=10, pady=10)

    # payment method
    PaymentMethod = StringVar()
    PaymentM = ["Cash", "Debit/Credit Card"]  # Create list for payment method
    paymeth_entry = ttk.Combobox(paymentframe, font="arial 12", textvariable=PaymentMethod, values=PaymentM, width=10)
    paymeth_entry.grid(row=0, column=1, padx=5, pady=5)

    # pay amount by customer
    payamount = IntVar()
    pay_amount_label = Label(paymentframe, text="Amount Paid", font="arial 12", bg="#DFEEFF")
    pay_amount_label.grid(row=0, column=2, padx=10, pady=10)
    pay_amount_entry = Entry(paymentframe, font="arial 12", textvariable=payamount, width=10)
    pay_amount_entry.grid(row=0, column=3, padx=5, pady=5)

    # change amount to customers
    change = IntVar()
    # Calculate the change to customer
    def calculate():
        if float(payamount.get()) < float(subtotalPrice.get()):
            tk.messagebox.showerror("Error", "The pay amount is less than the sub-total price.")
            return
        else:
            Pricechange = float(payamount.get()) - float(subtotalPrice.get())
            changesP = "{:.2f}".format(Pricechange)
            change.set(changesP)

    change_label = Label(paymentframe, text="Change", font="arial 12", bg="#DFEEFF")
    change_label.grid(row=0, column=4, padx=10, pady=5)
    change_entry = Entry(paymentframe, font="arial 12", textvariable=change, state='readonly', width=10)
    change_entry.grid(row=0, column=5, padx=5, pady=5)

    calculate_bt = Button(paymentframe, text='Calculate', font=('Helvetica Neue', 12), relief='raised',
                          command=calculate)
    calculate_bt.grid(row=0, column=7, padx=10, pady=5)

    # Generate invoice
    generate_invoice_bt = Button(paymentframe, text='Generate Invoice', font=('Helvetica Neue', 12), relief='raised',
                                 command=generateInvoice)
    generate_invoice_bt.grid(row=0, column=8, padx=10, pady=5)

    # quit Create Invoice Window
    def quitCreateInvoice():
        if tk.messagebox.askyesno('Close?', 'Are you sure want to quit this window?') == True:
            addInvoice.destroy()

    cancel_close = tk.Button(addInvoice, text='Cancel', width=10, command=lambda: quitCreateInvoice())
    cancel_close.place(x=1100, y=750)


# ========= Delete Invoice ======
def deleteInvoice():
    if not ManageInvoice.selection():  # if not select any row
        tk.messagebox.showerror("Error", "Please select invoice to delete")
    else:  # To confirm the user really want to delete the invoice?
        result = tk.messagebox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                           icon="warning")
        if result == 'yes':
            curItem = ManageInvoice.focus()
            contents = (ManageInvoice.item(curItem))
            selecteditem = contents['values']
            ManageInvoice.delete(curItem)
            cursor = conn.execute("DELETE FROM invoice WHERE invoice_id=?", (str(selecteditem[0]),))
            conn.commit()  # delete data from database
            cursor.close()
            ManageInvoice.delete(*ManageInvoice.get_children())  # clear all rows in tree table
            displayInvoice()  # redisplay the data

def click():  # download bill button function
    if not ManageInvoice.selection():  # if not select a row
        tk.messagebox.showerror(title="Error", message="Please select invoice to download.")
        return
    else:  # Ask user to confirm he/she want to download the receipt
        if tk.messagebox.askyesno('Download invoices', 'Are you sure want to download the invoice?') == True:
            dlpdf()
            tk.messagebox.showinfo("Downloaded", "Invoice is successfully downloaded.")


def dlpdf():
    current_item = ManageInvoice.focus()  # read the selected row
    vl = ManageInvoice.item(current_item, "values")  # get the values on selected row from tree view

    curr = conn.execute(
        "SELECT "
        "i.invoice_id, "
        "i.date, "
        "u.user_name ,"
        "i.payment_method, "
        "i.pro_id, "
        "p.product_name, "
        "p.sell_price, "
        "i.quantity, "
        "i.total, "
        "i.paid, "
        "i.change "
        "FROM invoice i "
        "INNER JOIN product p ON p.pro_id=i.pro_id "
        "LEFT JOIN user u ON u.user_id=i.user_id WHERE invoice_id=?",
        (vl[0],))
    data = curr.fetchall()

    # convert data into dataframe
    df = pd.DataFrame(data, columns=("invoice id", "date", "username", "payment method", "product id", "name",
                                     "sell_price", "quantity", "total price", "paid amount", "change"))

    # Create PDF Template
    pdf = FPDF(orientation='P', unit='mm', format='A5')  # variable pdf to fixed paper orientation, unit and size

    pdf.add_page()  # Add a page
    pdf.set_margins(2, 2, 2)  # set margins(LEFT, TOP, RIGHT)

    pdf.set_font("Times", size=20)  # set style & size of font
    # pdf.cell(width, height, txt, border, Indicates, align)
    pdf.cell(w=125, h=10, txt="Receipt", ln=0, align='C')
    pdf.cell(w=148, h=10, txt='', border=0, ln=1, align='C')  # empty one line

    pdf.set_font("Arial", size=15)
    pdf.cell(w=148, h=10, txt="Poh Cheong Tong Medical Hall", ln=1, align='C')
    pdf.set_font('Helvetica', size=10)
    pdf.cell(w=148, h=5, txt="610-P, Jalan Paya Terubung,", ln=1, align='C')
    pdf.cell(w=148, h=5, txt="Kampung Pisang,", ln=1, align='C')
    pdf.cell(w=148, h=5, txt="11500 Ayer Itam, Pulau Pinang.", ln=1, align='C')

    pdf.set_font('Helvetica', size=13)
    pdf.cell(120, 10, 'Invoice ID: ' + str(df.iloc[0][0]), ln=1, align='L')
    pdf.cell(120, 10, 'Date & Time: ' + str(df.iloc[0][1]), ln=1, align='L')
    pdf.cell(120, 10, 'Cashier Name: ' + str(df.iloc[0][2]), ln=1, align='L')
    pdf.cell(120, 10, 'Payment Method: ' + str(df.iloc[0][3]), ln=1, align='L')
    pdf.cell(120, 6, '', 0, 1, 'C')  # empty one line

    line_height = pdf.font_size * 17.5  # set the line height and column width

    pdf.set_font('Helvetica', 'B', size=10)
    pdf.cell(20, 6, 'Product ID', 0, 0, 'L')  # column 1 heading
    pdf.cell(75, 6, 'Product Name', 0, 0, 'L')  # column 2 heading
    pdf.cell(15, 6, 'Price', 0, 0, 'L')  # column 3 heading
    pdf.cell(15, 6, 'Quantity', 0, 1, 'L')  # column 4 heading

    for i in range(len(df)):  # Create loop to display the products in tables

        pdf.set_font('Helvetica', size=10)
        pdf.cell(20, 6, str(df.loc[0 + i]['product id']), 1, 0, 'L')  # column 1
        pdf.cell(75, 6, str(df.loc[0 + i]['name']), 1, 0, 'L')  # column 2
        pdf.cell(15, 6, str(df.loc[0 + i]['sell_price']), 1, 0, 'L')  # column 3
        pdf.cell(15, 6, str(df.loc[0 + i]['quantity']), 1, 1, 'L')  # column 4

    pdf.cell(80, 6, '', 0, 1, 'C')  # empty line
    pdf.cell(80, 6, '', 0, 1, 'C')  # empty line
    pdf.set_font('Helvetica', size=13)

    pdf.cell(200, 10, 'Sub Total: RM ' + str(df.loc[0]["total price"]), ln=1, align='L')
    pdf.cell(200, 10, 'Paid Amount: RM ' + str(df.loc[0]["paid amount"]), ln=1, align='L')
    pdf.cell(200, 10, 'Change: RM ' + str(df.loc[0]["change"]), ln=1, align='L')

    pdf.output(str(df.loc[0]['invoice id']) + '.pdf', 'F')  # Download file


# Create New Invoice Button
admin_add_button = tk.Button(BillingBottomFrame, text="+ Add", font=('Helvetica Neue', 12), width=10, height=1, relief='raised',
                       command=createInvoice)
admin_add_button.place(x=525, y=600)

# Delete Invoice Button
admin_delete_button = tk.Button(BillingBottomFrame, text="Delete", font=('Helvetica Neue', 12), width=10, height=1,
                          command=deleteInvoice)
admin_delete_button.place(x=775, y=600)

# View Invoice button
admin_download_button = tk.Button(BillingBottomFrame, text="Download\nInvoice", font=('Helvetica Neue', 12), width=10, height=2, relief='raised', command=click)
admin_download_button.place(x=650, y=600)













































#======================== Page 3(Staff Home Page)========================
page3.config(bg = '#DFEEFF')
def expandForHome_staff():
    global cur_width, expanded
    cur_width += 10  # Increase the width by 10
    rep = window.after(5, expandForHome_staff)  # Repeat this func every 5 ms
    frame.config(width=cur_width)  # Change the width to new increase width
    if cur_width >= max_w:  # If width is greater than maximum width
        expanded = True  # Frame is expended
        window.after_cancel(rep)  # Stop repeating the function
        fillForHome_staff()


def contractForHome_staff():
    global cur_width, expanded
    cur_width -= 10  # Reduce the width by 10
    rep = window.after(5, contractForHome_staff)  # Call this func every 5 ms
    frame.config(width=cur_width)  # Change the width to new reduced width
    if cur_width <= min_w:  # If it is back to normal width
        expanded = False  # Frame is not expanded
        window.after_cancel(rep)  # Stop repeating the function
        fillForHome_staff()



def fillForHome_staff(): 
    if expanded:  #If the frame is expanded
        # Show the label, and remove the image
        staff_logout_b.config(text='Log-Out', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        staff_home_b.config(text='Home', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        staff_billing_b.config(text='Billing', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        staff_inventory_b.config(text='Inventory', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        
        
    else:
        # Bring the image back
        staff_logout_b.config(image=logout, font=(0, 30))
        staff_home_b.config(image=home, font=(0, 30))
        staff_billing_b.config(image=billing, font=(0, 30))
        staff_inventory_b.config(image=inventory, font=(0, 30))
        



staffMenuFrame = Frame(page3, bg='#492F7C', width=150, height=window.winfo_height(),highlightbackground='white', highlightthickness=1)
staffMenuFrame.place(x=0, y=100)


# Defining the buttons for menu bar in Staff Home page
staff_logout_b = Button(staffMenuFrame, image=logout, bg='#252B61', relief='ridge', command = logout_system)
staff_home_b = Button(staffMenuFrame, image=home, bg='#252B61', relief='ridge', command = lambda: show_frame(staff_HomeFrame))
staff_billing_b = Button(staffMenuFrame, image=billing, bg='#252B61', relief='ridge', command = lambda:show_frame(staff_BillingFrame))
staff_inventory_b = Button(staffMenuFrame, image=inventory, bg='#252B61', relief='ridge', command = lambda: show_frame(staff_InventoryFrame))


# Placing buttons in menu bar Staff Home Page
staff_logout_b.place(x=25, y=10, width = 100)
staff_home_b.place(x=25, y=70, width = 100)
staff_billing_b.place(x=25, y=130, width = 100)
staff_inventory_b.place(x=25, y=190, width = 100)


# Bind to the frame, if centered or left
staffMenuFrame.bind('<Enter>', lambda e: expandForHome_staff())
staffMenuFrame.bind('<Leave>', lambda e: contractForHome_staff())

# So that Frame does not depend on the widgets inside the frame
staffMenuFrame.grid_propagate(False)





#Inventory page
staff_InventoryFrame = Frame(page3, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
staff_InventoryFrame.place(x=150,y=0, height=850, width = 1390)

staff_InventoryTopFrame = Frame(staff_InventoryFrame, bg='#492F7C', highlightbackground='white', highlightthickness=1)
staff_InventoryTopFrame.place(x=0,y=000, height=100,width = 1390)

staff_InventoryBottomFrame = Frame(staff_InventoryFrame, bg='#492F7C', highlightbackground='white', highlightthickness=1)
staff_InventoryBottomFrame.place(x=0,y=100, height=750,width = 1390)

#user info page
staff_UserInfoFrame = Frame(page3, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
staff_UserInfoFrame.place(x=150,y=0, height=850, width = 1390)

staff_InventoryLabel = Label(staff_InventoryTopFrame, text='Inventory', font=('Arial', 30), fg='white', bg='#492F7C')
staff_InventoryLabel.place(x=20, y=30)


# ======= Create tab ==========
#widget that manages a collection of windows/displays
staff_notebook = ttk.Notebook(staff_InventoryBottomFrame) 

# Create frame for tabs
staff_tab1 = Frame(staff_notebook, bg = '#DFEEFF') #new frame for tab 1
staff_tab2 = Frame(staff_notebook, bg = '#DFEEFF') #new frame for tab 2
staff_tab3 = Frame(staff_notebook, bg = '#DFEEFF') #new frame for tab 3
staff_tab4 = Frame(staff_notebook, bg = '#DFEEFF')

#place tabs 
staff_tab1.pack(fill='both', expand=True)
staff_tab2.pack(fill='both', expand=True)
staff_tab3.pack(fill='both', expand=True)
staff_tab4.pack(fill='both', expand=True)

#add tab to notebook for inventory for staff
staff_notebook.add(staff_tab1,text="Manage Inventory")
staff_notebook.add(staff_tab2,text="Inventory Alert")
staff_notebook.add(staff_tab3,text="Supplier Information")
staff_notebook.add(staff_tab4,text="Category")

staff_notebook.pack(fill='both', expand=True)


#display list of products for staff
def display_product_database_staff():
    
    StaffManageInventoryTree.delete(*StaffManageInventoryTree.get_children()) #delete treeview
    
    connect_database()
    cursor.execute("""SELECT product.pro_id, product.product_name, product.buy_price, product.sell_price,
                        product.quantity, product.min_quantity, product.expiry_date, category.cat_name, supplier.sup_id,
                        product.expiry_status,product.stock_level FROM product JOIN category
                        ON product.cat_id = category.cat_id
                        JOIN supplier ON supplier.sup_id= product.sup_id
                    """)
    data = cursor.fetchall()

    # Add our data to the screen
    for records in data:
        StaffManageInventoryTree.insert('', END, values= records)
		
    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()

#display list of product that is either expired of low
def display_alert_database_staff():
    StaffAlertTree.delete(*StaffAlertTree.get_children()) #delete treeview
    
    connect_database()
    cursor.execute("""SELECT product.pro_id, product.product_name, product.quantity, 
                        product.stock_level, product.expiry_status, supplier.sup_name, supplier.sup_phone FROM product 
                        JOIN supplier ON supplier.sup_id= product.sup_id
                        WHERE (product.stock_level LIKE 'Low') OR (product.stock_level LIKE 'Finish') OR (product.expiry_status LIKE 'Expired')
                    """)
    data = cursor.fetchall()

    # Add our data to the screen
    for records in data:
        StaffAlertTree.insert('', END, values= records)
		
    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()

#display list of supplier for staff user
def display_supplier_database_staff():
    StaffSupplierTree.delete(*StaffSupplierTree.get_children()) #delete treeview
    
    connect_database()
    
    cursor.execute("""SELECT supplier.sup_id, supplier.sup_name, supplier.sup_phone, supplier.sup_email,
                    supplier.sup_company, supplier.sup_address FROM supplier ORDER BY supplier.sup_id
                    """)
    data = cursor.fetchall()
	
    # Add our data to the screen
    for records in data:
        StaffSupplierTree.insert('', END, values=records)
		
    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()


#display list of categories for staff
def display_category_database_staff():
    StaffCategoryTree.delete(*StaffCategoryTree.get_children()) #delete treeview
    
    connect_database()
    cursor.execute('SELECT * FROM category')
    data = cursor.fetchall()

    # Add our data to the screen
    for records in data:
        StaffCategoryTree.insert('', END, values= records)
		
    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()

#manage inventory treeview for staff
StaffManageInventoryTree = ttk.Treeview(staff_tab1, selectmode="extended", show='headings',
                    columns = ('Product ID', 'Name', 'Buy Price', 'Sell Price', 'Quantity','Min.Quantity',
                               'Exp.Date', 'Category', 'Supplier ID', 'Expiry Status', 'Stock Level'))

StaffManageInventoryTree.place(relwidth=1.0, relheight=0.85)

Staffx_scroller= Scrollbar(StaffManageInventoryTree, orient = HORIZONTAL, command =StaffManageInventoryTree.xview)
Staffy_scroller= Scrollbar(StaffManageInventoryTree, orient = VERTICAL, command =StaffManageInventoryTree.yview)
Staffx_scroller.pack(side= BOTTOM, fill=X)
Staffy_scroller.pack(side= RIGHT, fill=Y)

StaffManageInventoryTree.config(yscrollcommand=Staffy_scroller.set, xscrollcommand=Staffx_scroller.set)

StaffManageInventoryTree.heading('Product ID', text = 'Product ID', anchor=CENTER)
StaffManageInventoryTree.heading('Name', text = 'Name', anchor=CENTER)
StaffManageInventoryTree.heading('Buy Price', text = 'Buy Price (RM)', anchor=CENTER)
StaffManageInventoryTree.heading('Sell Price', text = 'Sell Price (RM)', anchor=CENTER)
StaffManageInventoryTree.heading('Quantity', text = 'Quantity', anchor=CENTER)
StaffManageInventoryTree.heading('Min.Quantity', text = 'Min. Quantity', anchor=CENTER)
StaffManageInventoryTree.heading('Exp.Date', text = 'Exp. Date', anchor=CENTER)
StaffManageInventoryTree.heading('Category', text = 'Category', anchor=CENTER)
StaffManageInventoryTree.heading('Supplier ID', text = 'Supplier ID', anchor=CENTER)
StaffManageInventoryTree.heading('Expiry Status', text = 'Expiry Status', anchor=CENTER)
StaffManageInventoryTree.heading('Stock Level', text = 'Stock Level', anchor=CENTER)

StaffManageInventoryTree.column("Product ID", anchor=CENTER, width=100)
StaffManageInventoryTree.column("Name", anchor=CENTER, width=200)
StaffManageInventoryTree.column("Buy Price", anchor=CENTER, width=90)
StaffManageInventoryTree.column("Sell Price", anchor=CENTER, width=90)
StaffManageInventoryTree.column("Quantity", anchor=CENTER, width=100)
StaffManageInventoryTree.column("Min.Quantity", anchor=CENTER, width=120)
StaffManageInventoryTree.column("Exp.Date", anchor=CENTER, width=140)
StaffManageInventoryTree.column("Category", anchor=CENTER, width=140)
StaffManageInventoryTree.column("Supplier ID", anchor=CENTER, width=140)
StaffManageInventoryTree.column("Expiry Status", anchor=CENTER, width=140)
StaffManageInventoryTree.column("Stock Level", anchor=CENTER, width=140)




#Inventory Alerts treeview for staff
StaffAlertTree = ttk.Treeview(staff_tab2, selectmode="browse", show='headings',
                    columns = ('Product ID', 'Product Name', 'Quantity', 'Stock Level', 'Expiry Status', 'Supplier Name', 'Supplier Phone No.'))

StaffAlertTree.place(relwidth=1.0, relheight=1.0)

Staffx2_scroller= Scrollbar(StaffAlertTree, orient = HORIZONTAL, command =StaffAlertTree.xview)
Staffy2_scroller= Scrollbar(StaffAlertTree, orient = VERTICAL, command =StaffAlertTree.yview)
Staffx2_scroller.pack(side= BOTTOM, fill=X)
Staffy2_scroller.pack(side= RIGHT, fill=Y)

StaffAlertTree.config(yscrollcommand=Staffy2_scroller.set, xscrollcommand=Staffx2_scroller.set)

StaffAlertTree.heading('Product ID', text = 'Product ID', anchor=CENTER)
StaffAlertTree.heading('Product Name', text = 'Product Name', anchor=CENTER)
StaffAlertTree.heading('Quantity', text = 'Quantity', anchor=CENTER)
StaffAlertTree.heading('Stock Level', text = 'Stock Level', anchor=CENTER)
StaffAlertTree.heading('Expiry Status', text = 'Expiry Status', anchor=CENTER)
StaffAlertTree.heading('Supplier Name', text = 'Supplier Name', anchor=CENTER)
StaffAlertTree.heading('Supplier Phone No.', text = 'Supplier Phone No.', anchor=CENTER)


StaffAlertTree.column("Product ID", anchor=CENTER, width=100)
StaffAlertTree.column("Product Name", anchor=CENTER, width=200)
StaffAlertTree.column("Quantity", anchor=CENTER, width=100)
StaffAlertTree.column("Stock Level", anchor=CENTER, width=200)
StaffAlertTree.column("Expiry Status", anchor=CENTER, width=100)
StaffAlertTree.column("Supplier Name", anchor=CENTER, width=200)
StaffAlertTree.column("Supplier Phone No.", anchor=CENTER, width=200)

                            
display_alert_database_staff()


#Supplier Information Treeview for staff
StaffSupplierTree = ttk.Treeview(staff_tab3, selectmode="browse", show='headings',
            columns = ('Supplier ID', 'Supplier Name', 'Phone No.', 'Email', 'Company', 'Company Address'))

StaffSupplierTree.place(relwidth=1.0, relheight=0.85)

Staffx3_scroller= Scrollbar(StaffSupplierTree, orient = HORIZONTAL, command =StaffSupplierTree.xview)
Staffy3_scroller= Scrollbar(StaffSupplierTree, orient = VERTICAL, command =StaffSupplierTree.yview)
Staffx3_scroller.pack(side= BOTTOM, fill=X)
Staffy3_scroller.pack(side= RIGHT, fill=Y)

StaffSupplierTree.config(yscrollcommand=Staffy3_scroller.set, xscrollcommand=Staffx3_scroller.set)

StaffSupplierTree.heading('Supplier ID', text = 'Supplier ID', anchor=CENTER)
StaffSupplierTree.heading('Supplier Name', text = 'Supplier Name', anchor=CENTER)
StaffSupplierTree.heading('Phone No.', text = 'Phone No.', anchor=CENTER)
StaffSupplierTree.heading('Email', text = 'Email', anchor=CENTER)
StaffSupplierTree.heading('Company', text = 'Company', anchor=CENTER)
StaffSupplierTree.heading('Company Address', text = 'Company Address', anchor=CENTER)


StaffSupplierTree.column("Supplier ID", anchor=CENTER, width=80)
StaffSupplierTree.column("Supplier Name", anchor=CENTER, width=80)
StaffSupplierTree.column("Phone No.", anchor=CENTER, width=100)
StaffSupplierTree.column("Email", anchor=CENTER, width=120)
StaffSupplierTree.column("Company", anchor=CENTER, width=100)
StaffSupplierTree.column("Company Address", anchor=CENTER, width=280)


display_supplier_database_staff()



#category treeview for staff
StaffCategoryTree = ttk.Treeview(staff_tab4, selectmode="browse", show='headings',
                    columns = ('Category ID', 'Category Name'))

StaffCategoryTree.place(relwidth=1.0, relheight=0.85)

Staffx4_scroller= Scrollbar(StaffCategoryTree, orient = HORIZONTAL, command =StaffCategoryTree.xview)
Staffy4_scroller= Scrollbar(StaffCategoryTree, orient = VERTICAL, command =StaffCategoryTree.yview)
Staffx4_scroller.pack(side= BOTTOM, fill=X)
Staffy4_scroller.pack(side= RIGHT, fill=Y)

StaffCategoryTree.config(yscrollcommand=Staffy4_scroller.set, xscrollcommand=Staffx4_scroller.set)

StaffCategoryTree.heading('Category ID', text = 'Category ID', anchor=CENTER)
StaffCategoryTree.heading('Category Name', text = 'Category Name', anchor=CENTER)


StaffCategoryTree.column("Category ID", anchor=CENTER, width=100)
StaffCategoryTree.column("Category Name", anchor=CENTER, width=200)


#call function to display list of cateogries for staff                            
display_category_database_staff()


#set the values in edit inventory page according to selected for staff
def view_inventory_staff():
    selected = StaffManageInventoryTree.focus()
    values = StaffManageInventoryTree.item(selected)
    selection = values["values"]
    edit_pro_id_strvar.set(selection[0])
    edit_product_name_strvar.set(selection[1])
    edit_buy_price_strvar.set (selection [2])
    edit_sell_price_strvar.set (selection [3])
    edit_quantity_intvar.set (selection [4])
    edit_min_quantity_intvar.set (selection [5])
    edit_expiry_date_strvar.set (selection [6])
    connect_database()
    category_id_data = cursor.execute('SELECT cat_id FROM category WHERE cat_name LIKE ?', (str(selection [7]),)).fetchone()
    edit_category_id_strvar.set (category_id_data)
    edit_supplier_id_strvar.set (selection [8])
  
#edit inventory values for staff
def edit_inventory_staff():
    ID = edit_pro_id_strvar.get()
    name = edit_product_name_strvar.get()
    category_id= edit_category_id_strvar.get()
    expiry_date= edit_expiry_date_strvar.get()
    quantity = edit_quantity_intvar.get()
    min_quan =  edit_min_quantity_intvar.get()
    supply_price = edit_buy_price_strvar.get()
    selling_price = edit_sell_price_strvar.get()
    supplier_id = edit_supplier_id_strvar.get()
    format = '%Y-%m-%d'
    res = True
     
    if not ID or not name or not category_id or not expiry_date or not quantity or not min_quan or not supply_price or not selling_price or not supplier_id:
            messagebox.showerror('Error', "Please fill in all the fields!")    
    
    else:
        try:
            int(quantity)
        except ValueError:
            messagebox.showerror('Error', "Please insert the Quantity in number form")
        else:
            try:
                int(min_quan)
            except ValueError:
                messagebox.showerror('Error', "Please insert the Minimum Quantity in number form")
            else:
            
                try:
                    res = bool(datetime.strptime(expiry_date, format))
                except ValueError:
                    messagebox.showerror('Error', "Please insert expiry date in YYYY-MM-DD format")
                        
                else:
                    connect_database()
                    cursor.execute("""SELECT product_name FROM product WHERE pro_id = ?""",(ID,))
                    find = cursor.fetchall()
                    if len(find) == 0:
                        messagebox.showerror('Error', "Product ID does not exist!")       
                    else:
                                
                        connect_database()
                        cursor.execute("""UPDATE product SET product_name =?, 
                                            buy_price=?, sell_price =?, quantity =?, min_quantity=?, expiry_date=?, cat_id= ?,
                                            sup_id=? WHERE pro_id = ?""",(name,supply_price, selling_price, quantity, min_quan, expiry_date, category_id,
                                            supplier_id, ID))
                  
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Record added', f"Record of {name} was successfully updated")
                        set_expiry_status()
                        stock_level()
                        display_product_database_staff()
                        display_alert_database_staff()
                        editInventoryWindow.destroy()
#add inventory for staff
def add_inventory_staff():
    ID = add_pro_id_strvar.get()
    name = add_product_name_strvar.get()
    category_id= add_category_id_strvar.get()
    expiry_date= add_expiry_date_strvar.get()
    quantity = add_quantity_intvar.get()
    min_quan =  add_min_quantity_intvar.get()
    supply_price = add_buy_price_strvar.get()
    selling_price = add_sell_price_strvar.get()
    supplier_id = add_supplier_id_strvar.get()
    format = '%Y-%m-%d'
    res = True
     
    if not ID or not name or not category_id or not expiry_date or not quantity or not min_quan or not supply_price or not selling_price or not supplier_id:
            messagebox.showerror('Error', "Please fill in all the fields!")    
    else:
        try:
            pro_image = convert_image_into_binary(get_imagefile)
        except NameError or FileNotFoundError:
            messagebox.showerror('Error', "Please insert product image")
        else:
            try:
                int(quantity)
            except ValueError:
                messagebox.showerror('Error', "Please insert the Quantity in number form")
            else:
                try:
                    int(min_quan)
                except ValueError:
                    messagebox.showerror('Error', "Please insert the Minimum Quantity in number form")
                else:
            
                    try:
                        res = bool(datetime.strptime(expiry_date, format))
                    except ValueError:
                        messagebox.showerror('Error', "Please insert expiry date in YYYY-MM-DD format")
                        
                    else:
                        if ID[0] !="P":
                            messagebox.showerror('Error', "Please insert the ID in format example P001!")    
                        elif len(ID) !=4:
                            messagebox.showerror('Error', "Please insert the ID in format example P001!")
                        else:
                            try:
                                connect_database()
                                conn.execute("""INSERT INTO product (pro_id, product_name, image,
                                            buy_price, sell_price, quantity, min_quantity, expiry_date, cat_id, sup_id)
                                            VALUES(?,?,?,?,?,?,?,?,?,?)""",
                                            (ID, name, pro_image, supply_price, selling_price, quantity, min_quan, expiry_date, category_id,
                                            supplier_id))
                                           
                                
                            except sqlite3.IntegrityError:
                                 messagebox.showerror('Error', "Product ID already exists")
                                
                            else:
                                conn.commit()
                                conn.close()
                                messagebox.showinfo('Record added', f"Record of {name} was successfully added")
                                set_expiry_status()
                                stock_level()
                                display_product_database_staff()
                                display_alert_database_staff()

#close edit inventory page for staff
def close_edit_inventory_staff():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to quit Edit Inventory?')
    if answer:
        editInventoryWindow.destroy()#close Edit Inventory page
        display_product_database_staff()#display list of inventory





#open window to edit inventory records for staff user
def open_edit_inventory_staff():
    global editInventoryWindow
    global edit_productImage_frame
    
    connect_database()
    
    if not StaffManageInventoryTree.selection():
        messagebox.showerror("Error", "Please select an item to edit")
    else:
        editInventoryWindow = Toplevel(window)
        editInventoryWindow.rowconfigure(0, weight=1)
        editInventoryWindow.columnconfigure(0, weight=1)
        editInventoryWindow.state('zoomed')
        editInventoryWindow.configure(bg = '#DFEEFF')
        
        
        editInventory_label = Label(editInventoryWindow, text="EDIT INVENTORY", font=('Arial', 35, 'bold'),bg='#DFEEFF')
        editInventory_label.place(x=600, y=30)
          
        
        productID_label = Label(editInventoryWindow, text="Product ID", font=('Arial', 18),bg='#DFEEFF')
        productID_label.place(x=200, y=115)
        productID_entry = Entry(editInventoryWindow, font=(20), textvariable = edit_pro_id_strvar, width = 30)
        productID_entry.place(x=200, y=150)
            
        productName_label = Label(editInventoryWindow, text="Product Name", font=('Arial', 18),bg='#DFEEFF')
        productName_label.place(x=200, y=200)
        productName_entry = Entry(editInventoryWindow, font=(20), textvariable = edit_product_name_strvar, width = 30)
        productName_entry.place(x=200, y=240)

            
        category_id_label = Label(editInventoryWindow, text="Category ID", font=('Arial', 18),bg='#DFEEFF')
        category_id_label.place(x=200, y=290)
        category_id_data = cursor.execute('SELECT cat_id FROM category')
        category_id_list = [x for x, in category_id_data]
        category_id_combobox =ttk.Combobox(editInventoryWindow, textvariable = edit_category_id_strvar, values = category_id_list, state = "readonly", width = 19, font = 15)
        category_id_combobox.place(x=200, y=330)

            
        expiryDate_label = Label(editInventoryWindow, text="Expiry Date", font=('Arial', 18),bg='#DFEEFF')
        expiryDate_label.place(x=700, y=115)
        expiryDate_entry = Entry(editInventoryWindow, font=(20), textvariable = edit_expiry_date_strvar)
        expiryDate_entry.place(x=700, y=155)

        quantity_label = Label(editInventoryWindow, text="Quantity", font=('Arial', 18),bg='#DFEEFF')
        quantity_label.place(x=700, y=205)
        quantity_entry = Entry(editInventoryWindow, font=(20), textvariable = edit_quantity_intvar)
        quantity_entry.place(x=700, y=245)

        minimumQuantity_label=Label(editInventoryWindow, text="Min. Quantity", font=('Arial', 18),bg='#DFEEFF')
        minimumQuantity_label.place(x=700, y=295)
        minimumQuantity_entry = Entry(editInventoryWindow, font=(20), textvariable = edit_min_quantity_intvar)
        minimumQuantity_entry.place(x=700, y=335)

        supplyPrice_label = Label(editInventoryWindow, text="Supply Price", font=('Arial', 18),bg='#DFEEFF')
        supplyPrice_label.place(x=700, y=385)
        supplyPrice_entry = Entry(editInventoryWindow, font=(20), textvariable = edit_buy_price_strvar)
        supplyPrice_entry.place(x=700, y=425)

        sellingPrice_label = Label(editInventoryWindow, text="Selling Price", font=('Arial', 18),bg='#DFEEFF')
        sellingPrice_label.place(x=700, y=455)
        sellingPrice_entry = Entry(editInventoryWindow, font=(20), textvariable = edit_sell_price_strvar)
        sellingPrice_entry.place(x=700, y=495)

        supplierID_label = Label(editInventoryWindow, text="Supplier ID", font=('Arial', 18),bg='#DFEEFF')
        supplierID_label.place(x=700, y=545)
        supplier_id_data = cursor.execute('SELECT sup_id FROM supplier')
        supplier_id_list = [x for x, in supplier_id_data]
        supplier_id_combobox =ttk.Combobox(editInventoryWindow, textvariable = edit_supplier_id_strvar, values = supplier_id_list, state = "readonly", font = 15, width =19)
        supplier_id_combobox.place(x=700, y=585)

        update_button= Button(editInventoryWindow, text= "UPDATE", font=('Arial', 15, 'bold'), command = edit_inventory_staff)
        update_button.place(x=1100, y=115, height = 40, width = 220)

        cancel_edit_button= Button(editInventoryWindow, text= "QUIT", font=('Arial', 15, 'bold'), command = close_edit_inventory_staff)
        cancel_edit_button.place(x=1100, y=165, height = 40, width = 220)

        view_inventory_staff()

        editInventoryWindow.grab_set()
        editInventoryWindow.mainloop()


#close add inventory page for staff user
def close_add_inventory_staff():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to quit Add Inventory?')
    if answer:
        reset_add_inventory_fields()
        addInventoryWindow.destroy()
        display_product_database_staff()


#open window to add inventory records for staff user
def open_add_inventory_staff():

    connect_database()
    global addInventoryWindow
    global add_productImage_frame
    addInventoryWindow = Toplevel(window)
    addInventoryWindow.rowconfigure(0, weight=1)
    addInventoryWindow.columnconfigure(0, weight=1)
    addInventoryWindow.state('zoomed')
    addInventoryWindow.configure(bg = '#DFEEFF')
    
    
    addInventory_label = Label(addInventoryWindow, text="ADD INVENTORY", font=('Arial', 35, 'bold'),bg='#DFEEFF')
    addInventory_label.place(x=620, y=30)
        
    productID_label = Label(addInventoryWindow, text="Product ID", font=('Arial', 18),bg='#DFEEFF')
    productID_label.place(x=200, y=115)
    productID_entry = Entry(addInventoryWindow, font=(20), textvariable = add_pro_id_strvar)
    productID_entry.place(x=200, y=150)
        
    productName_label = Label(addInventoryWindow, text="Product Name", font=('Arial', 18),bg='#DFEEFF')
    productName_label.place(x=200, y=200)
    productName_entry = Entry(addInventoryWindow, font=(20), textvariable = add_product_name_strvar)
    productName_entry.place(x=200, y=240)

    add_productImage_label = Label(addInventoryWindow, text="Product Image", font=('Arial', 18),bg='#DFEEFF')
    add_productImage_label.place(x=200, y=290)
    add_productImage_frame= Frame(addInventoryWindow, bg='white', highlightbackground='black', highlightthickness=1)
    add_productImage_frame.place(x=200, y=330, height=200,width = 200)
    add_chooseImage_button = Button(addInventoryWindow, text="Select Image", command= upload_image)
    add_chooseImage_button.place(x=200, y=550)
        
    category_id_label = Label(addInventoryWindow, text="Category ID", font=('Arial', 18),bg='#DFEEFF')
    category_id_label.place(x=200, y=600)
    category_id_data = cursor.execute('SELECT cat_id FROM category')
    category_id_list = [x for x, in category_id_data]
    category_id_combobox =ttk.Combobox(addInventoryWindow, textvariable = add_category_id_strvar, values = category_id_list, state = "readonly",  width = 19, font = 15)
    category_id_combobox.place(x=200, y=640)

        
    expiryDate_label = Label(addInventoryWindow, text="Expiry Date", font=('Arial', 18),bg='#DFEEFF')
    expiryDate_label.place(x=700, y=115)
    expiryDate_entry = Entry(addInventoryWindow, font=(20), textvariable = add_expiry_date_strvar)
    expiryDate_entry.place(x=700, y=155)

    quantity_label = Label(addInventoryWindow, text="Quantity", font=('Arial', 18),bg='#DFEEFF')
    quantity_label.place(x=700, y=205)
    quantity_entry = Entry(addInventoryWindow, font=(20), textvariable = add_quantity_intvar)
    quantity_entry.place(x=700, y=245)

    minimumQuantity_label=Label(addInventoryWindow, text="Min. Quantity", font=('Arial', 18),bg='#DFEEFF')
    minimumQuantity_label.place(x=700, y=295)
    minimumQuantity_entry = Entry(addInventoryWindow, font=(20), textvariable = add_min_quantity_intvar)
    minimumQuantity_entry.place(x=700, y=335)

    supplyPrice_label = Label(addInventoryWindow, text="Supply Price", font=('Arial', 18),bg='#DFEEFF')
    supplyPrice_label.place(x=700, y=385)
    supplyPrice_entry = Entry(addInventoryWindow, font=(20), textvariable = add_buy_price_strvar)
    supplyPrice_entry.place(x=700, y=425)

    sellingPrice_label = Label(addInventoryWindow, text="Selling Price", font=('Arial', 18),bg='#DFEEFF')
    sellingPrice_label.place(x=700, y=455)
    sellingPrice_entry = Entry(addInventoryWindow, font=(20), textvariable = add_sell_price_strvar)
    sellingPrice_entry.place(x=700, y=495)

    supplierID_label = Label(addInventoryWindow, text="Supplier ID", font=('Arial', 18),bg='#DFEEFF')
    supplierID_label.place(x=700, y=545)
    supplier_id_data = cursor.execute('SELECT sup_id FROM supplier')
    supplier_id_list = [x for x, in supplier_id_data]
    supplier_id_combobox =ttk.Combobox(addInventoryWindow, textvariable = add_supplier_id_strvar, values = supplier_id_list, state = "readonly",  width = 19, font = 15)
    supplier_id_combobox.place(x=700, y=585)

    add_button= Button(addInventoryWindow, text= "ADD", font=('Arial', 15, 'bold'), command = add_inventory_staff)
    add_button.place(x=1100, y=115, height = 40, width = 220)

    cancel_add_button= Button(addInventoryWindow, text= "QUIT", font=('Arial', 15, 'bold'), command = close_add_inventory_staff)
    cancel_add_button.place(x=1100, y=165, height = 40, width = 220)

    addInventoryWindow.grab_set()
    addInventoryWindow.mainloop()


# Remove inventory records
def remove_inventory_staff():
    if not StaffManageInventoryTree.selection():
        messagebox.showerror("Error", "Please select an item to delete")
        
    else:
    	# Add a little message box for fun
        response = messagebox.askyesno("Delete", "This Will Delete EVERYTHING SELECTED From The Table\nAre You Sure?!")

	#Add logic for message box
        if response == 1:
		# Designate selections
                x = StaffManageInventoryTree.selection()

		# Create List of ID's
                ids_to_delete = []
		
		# Add selections to ids_to_delete list
                for record in x:
                    ids_to_delete.append(StaffManageInventoryTree.item(record, 'values')[0])

                #connect to database
                connect_database()
		

		# Delete Everything From The Table
                cursor.executemany("DELETE FROM product WHERE pro_id = ?", [(a,) for a in ids_to_delete])


		# Reset List
                ids_to_delete = []


		# Commit changes
                conn.commit()


                #display new database values
                display_product_database_staff()
                display_alert_database_staff()
                
		#for fun
                messagebox.showinfo('Status' , 'You have successfully deleted the items!')

#search inventory function for staff 
def search_inventory_staff():
    cb_value1 = search_inventory_by_strvar.get()
    cb_value2 = search_inventory_strvar.get()

    if cb_value1 == "ID":
        connect_database()
        cursor.execute("""SELECT product.pro_id, product.product_name, product.buy_price, product.sell_price,
                        product.quantity, product.min_quantity, product.expiry_date, category.cat_name, supplier.sup_id,
                        product.expiry_status,product.stock_level FROM product JOIN category
                        ON product.cat_id = category.cat_id
                        JOIN supplier ON supplier.sup_id= product.sup_id
                        WHERE product.pro_id LIKE ?""", ('%'+cb_value2+'%',))
        data = cursor.fetchall()
        
        if not cb_value2:            
            messagebox.showerror('Error', 'Please fill in the search field')

        elif len(data) !=0:
            StaffManageInventoryTree.delete(*StaffManageInventoryTree.get_children())
            
            for records in data:
                StaffManageInventoryTree.insert('', END, values= records)
                
            conn.commit()
        else:
            messagebox.showerror('Error', 'Record is not found')
    

    elif cb_value1 == "NAME":
        connect_database()
        cursor.execute("""SELECT product.pro_id, product.product_name, product.buy_price, product.sell_price,
                        product.quantity, product.min_quantity, product.expiry_date, category.cat_name, supplier.sup_id,
                        product.expiry_status,product.stock_level FROM product JOIN category
                        ON product.cat_id = category.cat_id
                        JOIN supplier ON supplier.sup_id= product.sup_id
                        WHERE product.product_name LIKE ?""", ("%" + cb_value2 + "%",))
        data = cursor.fetchall()
        
        if not cb_value2:            
            messagebox.showerror('Error', 'Please fill in the search field')

        elif len(data) !=0:
            StaffManageInventoryTree.delete(*StaffManageInventoryTree.get_children())
            
            for records in data:
                StaffManageInventoryTree.insert('', END, values= records)
                
            conn.commit()
            
        else:
            messagebox.showerror('Error', 'Record is not found')
    else:
        messagebox.showerror('Error', "Please select ID or NAME in the drop down box!")



#clear entries for search fields
def clear_search_inventory_staff():
    display_product_database_staff()
    staff_tab1_search_combobox.current(0)
    for i in ['search_inventory_strvar']:
        exec(f"{i}.set('')")


#call function to display list of inventories for staff
display_product_database_staff()


#set values in edit invetentory page according to selected for staff
def view_supplier_staff():
    selected = StaffSupplierTree.focus()
    values = StaffSupplierTree.item(selected)
    selection = values["values"]
    edit_sup_id_strvar.set(selection [0])
    edit_sup_name_strvar.set(selection [1])
    edit_sup_phone_strvar.set (selection [2])
    edit_sup_email_strvar.set (selection [3])
    edit_sup_company_strvar.set (selection [4])
    edit_sup_address_strvar.set (selection [5])

#function to add supplier for staff
def add_supplier_staff():
    ID = add_sup_id_strvar.get()
    name = add_sup_name_strvar.get()
    phone_no= add_sup_phone_strvar.get()
    email = add_sup_email_strvar.get()
    company = add_sup_company_strvar.get()
    address =  add_sup_address_strvar.get()
    valid_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
         
    if not ID or not name or not phone_no or not email or not company or not address:
        messagebox.showerror('Error', "Please fill in all the fields!")    
    else:
        if ID[0] !="S":
            messagebox.showerror('Error', "Please insert the ID in format example S001!")    
        elif len(ID) !=4:
            messagebox.showerror('Error', "Please insert the ID in format example S001!")
        elif len(phone_no) < 10 or len(phone_no) > 11:
            messagebox.showerror('Error', "Phone number has to be 10 or 11 numbers")
        elif re.search(valid_email, email) is None:
            messagebox.showerror('Error', "Invalid email")

        else:
            try:
                connect_database()
                conn.execute("""INSERT INTO supplier (sup_id, sup_name, sup_phone, sup_email, sup_company, sup_address)
                                VALUES(?,?,?,?,?,?)""",
                                    (ID, name,phone_no,email, company, address))
                                   
            except sqlite3.IntegrityError:
                messagebox.showerror('Error', "Supplier ID already exists")
                        
            else:
                conn.commit()
                conn.close()
                messagebox.showinfo('Record added', f"Record of {name} was successfully added")
                display_supplier_database_staff()
                reset_add_supplier_fields()



#edit values of supplier for staff
def edit_supplier_staff():
    connect_database()
    ID = edit_sup_id_strvar.get()
    name = edit_sup_name_strvar.get()
    phone_no= edit_sup_phone_strvar.get()
    email = edit_sup_email_strvar.get()
    company = edit_sup_company_strvar.get()
    address =  edit_sup_address_strvar.get()
    valid_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    cursor.execute("SELECT * FROM supplier WHERE sup_id = ?", (ID,))
    validate = cursor.fetchall()
     
    if not ID or not name or not phone_no or not email or not company or not address:
            messagebox.showerror('Error', "Please fill in all the fields!")    
    else:
        if ID[0] !="S":
            messagebox.showerror('Error', "Please insert the ID in format example S001!")    
        elif len(ID) !=4:
            messagebox.showerror('Error', "Please insert the ID in format example S001!")
        elif len(phone_no) < 10 or len(phone_no) > 11:
            messagebox.showerror('Error', "Phone number has to be 10 or 11 numbers")
        elif re.search(valid_email, email)is None:
            messagebox.showerror('Error', "Invalid email")
        elif len(validate) == 0:
            messagebox.showerror('Error', "Supplier ID does not exist")
            
        else:

            connect_database()
            cursor.execute("""UPDATE supplier SET sup_name = ?, sup_phone = ?, sup_email = ?, sup_company = ?, sup_address = ? WHERE sup_id = ?"""
                             ,(name,phone_no,email, company,address,ID))
            conn.commit()
                
            messagebox.showinfo('Record added', f"Record of {name} was successfully edited")
            display_supplier_database_staff()
            editSupplierWindow.destroy()


#close add supplier page for staff user
def close_add_supplier_staff():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to quit Add Supplier?')
    if answer:
        reset_add_supplier_fields()
        addSupplierWindow.destroy()
        display_supplier_database_staff()

#open add supplier page for staff user
def open_add_supplier_staff():

    connect_database()
    global add_companyAddress_entry
    global addSupplierWindow
    
    addSupplierWindow = Toplevel(window)
    addSupplierWindow.rowconfigure(0, weight=1)
    addSupplierWindow.columnconfigure(0, weight=1)
    addSupplierWindow.state('zoomed')
    addSupplierWindow.configure(bg = '#DFEEFF')
    
    addSupplier_label = Label(addSupplierWindow, text="ADD SUPPLIER", font=('Arial', 35, 'bold'),bg='#DFEEFF')
    addSupplier_label.place(x=620, y=30)
        
    supplierID_label = Label(addSupplierWindow, text="Supplier ID", font=('Arial', 18),bg='#DFEEFF')
    supplierID_label.place(x=200, y=115)
    supplierID_entry = Entry(addSupplierWindow, font=(20), textvariable = add_sup_id_strvar)
    supplierID_entry.place(x=200, y=150)
        
    supplierName_label = Label(addSupplierWindow, text="Supplier Name", font=('Arial', 18),bg='#DFEEFF')
    supplierName_label.place(x=200, y=200)
    supplierName_entry = Entry(addSupplierWindow, font=(20), textvariable = add_sup_name_strvar)
    supplierName_entry.place(x=200, y=240)
        
    supplierPhone_label = Label(addSupplierWindow, text="Phone No.", font=('Arial', 18),bg='#DFEEFF')
    supplierPhone_label.place(x=200, y=290)
    supplierPhone_entry = Entry(addSupplierWindow, font=(20), textvariable = add_sup_phone_strvar)
    supplierPhone_entry.place(x=200, y=330)

    supplierEmail_label = Label(addSupplierWindow, text="Supplier Email", font=('Arial', 18),bg='#DFEEFF')
    supplierEmail_label.place(x=700, y=115)
    supplierEmail_entry = Entry(addSupplierWindow, font=(20), textvariable = add_sup_email_strvar)
    supplierEmail_entry.place(x=700, y=150)

    supplierCompany_label=Label(addSupplierWindow, text="Supplier Company", font=('Arial', 18),bg='#DFEEFF')
    supplierCompany_label.place(x=700, y=200)
    supplierCompany_entry = Entry(addSupplierWindow, font=(20), textvariable = add_sup_company_strvar)
    supplierCompany_entry.place(x=700, y=240)

    companyAddress_label = Label(addSupplierWindow, text="Company Address", font=('Arial', 18),bg='#DFEEFF')
    companyAddress_label.place(x=700, y=290)
    add_companyAddress_entry = Entry(addSupplierWindow, font=(20), textvariable = add_sup_address_strvar)
    add_companyAddress_entry.place(x=700, y=330,  height = 30, width =700)


    add_button= Button(addSupplierWindow, text= "ADD", font=('Arial', 15, 'bold'), command = add_supplier_staff)
    add_button.place(x=1100, y=115, height = 40, width = 220)

    cancel_add_button= Button(addSupplierWindow, text= "QUIT", font=('Arial', 15, 'bold'), command = close_add_supplier_staff)
    cancel_add_button.place(x=1100, y=165, height = 40, width = 220)

    addSupplierWindow.grab_set()
    addSupplierWindow.mainloop()

#close edit supplier page for staff user
def close_edit_supplier_staff():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to quit EDIT Supplier?')
    if answer:
        editSupplierWindow.destroy()
        display_supplier_database_staff()


#open edit supplier page for staff
def open_edit_supplier_staff():

    connect_database()
    global editSupplierWindow
    global edit_companyAddress_entry

    if not StaffSupplierTree.selection():
        messagebox.showerror("Error", "Please select an item to edit")
    else:

        editSupplierWindow = Toplevel(window)
        editSupplierWindow.rowconfigure(0, weight=1)
        editSupplierWindow.columnconfigure(0, weight=1)
        editSupplierWindow.state('zoomed')
        editSupplierWindow.configure(bg = '#DFEEFF')
        
        editSupplier_label = Label(editSupplierWindow, text="EDIT SUPPLIER", font=('Arial', 35, 'bold'),bg='#DFEEFF')
        editSupplier_label.place(x=620, y=30)
            
        supplierID_label = Label(editSupplierWindow, text="Supplier ID", font=('Arial', 18),bg='#DFEEFF')
        supplierID_label.place(x=200, y=115)
        supplierID_entry = Entry(editSupplierWindow, font=(20), textvariable = edit_sup_id_strvar)
        supplierID_entry.place(x=200, y=150)
            
        supplierName_label = Label(editSupplierWindow, text="Supplier Name", font=('Arial', 18),bg='#DFEEFF')
        supplierName_label.place(x=200, y=200)
        supplierName_entry = Entry(editSupplierWindow, font=(20), textvariable = edit_sup_name_strvar)
        supplierName_entry.place(x=200, y=240)
            
        supplierPhone_label = Label(editSupplierWindow, text="Phone No.", font=('Arial', 18),bg='#DFEEFF')
        supplierPhone_label.place(x=200, y=290)
        supplierPhone_entry = Entry(editSupplierWindow, font=(20), textvariable = edit_sup_phone_strvar)
        supplierPhone_entry.place(x=200, y=330)

        supplierEmail_label = Label(editSupplierWindow, text="Supplier Email", font=('Arial', 18),bg='#DFEEFF')
        supplierEmail_label.place(x=700, y=115)
        supplierEmail_entry = Entry(editSupplierWindow, font=(20), textvariable = edit_sup_email_strvar)
        supplierEmail_entry.place(x=700, y=150)

        supplierCompany_label=Label(editSupplierWindow, text="Supplier Company", font=('Arial', 18),bg='#DFEEFF')
        supplierCompany_label.place(x=700, y=200)
        supplierCompany_entry = Entry(editSupplierWindow, font=(20), textvariable = edit_sup_company_strvar)
        supplierCompany_entry.place(x=700, y=240)

        companyAddress_label = Label(editSupplierWindow, text="Company Address", font=('Arial', 18),bg='#DFEEFF')
        companyAddress_label.place(x=700, y=295)
        edit_companyAddress_entry = Entry(editSupplierWindow, font=(20), textvariable = edit_sup_address_strvar)
        edit_companyAddress_entry.place(x=700, y=335, height = 30, width =700)


        edit_button= Button(editSupplierWindow, text= "EDIT", font=('Arial', 15, 'bold'), command = edit_supplier_staff)
        edit_button.place(x=1100, y=115, height = 40, width = 220)

        cancel_edit_button= Button(editSupplierWindow, text= "QUIT", font=('Arial', 15, 'bold'), command = close_edit_supplier_staff)
        cancel_edit_button.place(x=1100, y=165, height = 40, width = 220)

        view_supplier_staff()

        editSupplierWindow.grab_set()
        editSupplierWindow.mainloop()


# Remove supplier records
def remove_supplier_staff():
    if not StaffSupplierTree.selection():
        messagebox.showerror("Error", "Please select an item to delete")
            
    else:
        connect_database()
            
            # Add a little message box for fun
        response = messagebox.askyesno("Delete", "This Will Delete EVERYTHING SELECTED From The Table\nAre You Sure?!")

            #Add logic for message box
        if response == 1:
                # Designate selections
                x = StaffSupplierTree.focus()
                values = StaffSupplierTree.item(x)
                selection = values ["values"]
                cursor.execute("SELECT product.sup_id, supplier.sup_id FROM product NATURAL JOIN supplier WHERE supplier.sup_id = ?", (str(selection[0]),))
                data = cursor.fetchall()
                if len(data)== 0:
                    cursor.execute("DELETE FROM supplier WHERE sup_id = ?", (str(selection[0]),))
                    conn.commit()
                    display_supplier_database_staff()
                else:
                    messagebox.showerror("Error", "Supplier ID needed for product \nCannot Delete!")

#function to search list of supplier for staff user
def search_supplier_staff():
    cb_value1 = search_supplier_by_strvar.get()
    cb_value2 = search_supplier_strvar.get()

    if cb_value1 == "ID":
        connect_database()
        cursor.execute("""SELECT sup_id, sup_name, sup_phone, sup_email, sup_company, sup_address FROM supplier
                        WHERE sup_id LIKE ?""", ('%'+cb_value2+'%',))
        data = cursor.fetchall()
        
        if not cb_value2:            
            messagebox.showerror('Error', 'Please fill in the search field')

        elif len(data) !=0:
            StaffSupplierTree.delete(*StaffSupplierTree.get_children())
            
            for records in data:
                StaffSupplierTree.insert('', END, values= records)
                
            conn.commit()
        else:
            messagebox.showerror('Error', 'Record is not found')

    elif cb_value1 == "NAME":
            connect_database()
            cursor.execute("""SELECT sup_id, sup_name, sup_phone, sup_email, sup_company, sup_address FROM supplier
                            WHERE sup_name LIKE ?""", ("%" + cb_value2 + "%",))
            data = cursor.fetchall()
            
            if not cb_value2:            
                messagebox.showerror('Error', 'Please fill in the search field')

            elif len(data) !=0:
                StaffSupplierTree.delete(*StaffSupplierTree.get_children())
                
                for records in data:
                    StaffSupplierTree.insert('', END, values= records)
                    
                conn.commit()
                
            else:
                messagebox.showerror('Error', 'Record is not found')
    else:
        messagebox.showerror('Error', "Please select ID or NAME in the drop down box!")

#clear entries for search supplier for staff user
def clear_search_supplier_staff():
    display_supplier_database_staff()
    staff_tab3_search_combobox.current(0)
    for i in ['search_supplier_strvar']:
        exec(f"{i}.set('')")

#set entries in edit category page according to selected values for staff user 
def view_category_staff():
    selected = StaffCategoryTree.focus()
    values = StaffCategoryTree.item(selected)
    selection = values["values"]
    edit_cat_id_strvar.set(selection [0])
    edit_cat_name_strvar.set(selection [1])


#add category of user for staff user
def add_category_staff():
    ID = add_cat_id_strvar.get()
    name = add_cat_name_strvar.get()
         
    if not ID or not name :
        messagebox.showerror('Error', "Please fill in all the fields!")    
    else:
        if ID[0] !="C":
            messagebox.showerror('Error', "Please insert the ID in format example C001!")    
        elif len(ID) !=4:
            messagebox.showerror('Error', "Please insert the ID in format example C001!")

        else:
            try:
                connect_database()
                conn.execute("""INSERT INTO category (cat_id, cat_name)
                                VALUES(?,?)""",
                                (ID, name))
                                   
            except sqlite3.IntegrityError:
                messagebox.showerror('Error', "Category ID already exists")
                        
            else:
                conn.commit()
                conn.close()
                messagebox.showinfo('Record added', f"Record of {name} was successfully added")
                display_category_database_staff()
                reset_add_category_fields()

#edit details of category for staff user
def edit_category_staff():
    connect_database()
    ID = edit_cat_id_strvar.get()
    name = edit_cat_name_strvar.get()
    cursor.execute("SELECT * FROM category WHERE cat_id = ?", (ID,))
    validate = cursor.fetchall()
     
    if not ID or not name:
            messagebox.showerror('Error', "Please fill in all the fields!")    
    else:
        if ID[0] !="C":
            messagebox.showerror('Error', "Please insert the ID in format example S001!")    
        elif len(ID) !=4:
            messagebox.showerror('Error', "Please insert the ID in format example S001!")

        elif len(validate) == 0:
            messagebox.showerror('Error', "Category ID does not exist")
            
        else:
            connect_database()
            cursor.execute("""UPDATE category SET cat_name = ? WHERE cat_id = ?"""
                             ,(name,ID))
            conn.commit()
                
            messagebox.showinfo('Record added', f"Record of {name} was successfully edited")
            display_category_database_staff()
            editCategoryWindow.destroy()

#function to close add category page for staff user
def close_add_category_staff():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to quit Add Category?')
    if answer:
        reset_add_category_fields()
        addCategoryWindow.destroy()
        display_category_database_staff()


#function to open add category page for staff
def open_add_category_staff():

    connect_database()
    global addCategoryWindow
    
    addCategoryWindow = Toplevel(window)
    addCategoryWindow.rowconfigure(0, weight=1)
    addCategoryWindow.columnconfigure(0, weight=1)
    addCategoryWindow.state('zoomed')
    addCategoryWindow.configure(bg = '#DFEEFF')
    
    addCategory_label = Label(addCategoryWindow, text="ADD CATEGORY", font=('Arial', 35, 'bold'),bg='#DFEEFF')
    addCategory_label.place(x=620, y=30)
        
    categoryID_label = Label(addCategoryWindow, text="Category ID", font=('Arial', 18),bg='#DFEEFF')
    categoryID_label.place(x=700, y=115)
    categoryID_entry = Entry(addCategoryWindow, font=(20), textvariable = add_cat_id_strvar)
    categoryID_entry.place(x=700, y=150)
        
    categoryName_label = Label(addCategoryWindow, text="Category Name", font=('Arial', 18),bg='#DFEEFF')
    categoryName_label.place(x=700, y=200)
    categoryName_entry = Entry(addCategoryWindow, font=(20), textvariable = add_cat_name_strvar)
    categoryName_entry.place(x=700, y=240)

    add_button= Button(addCategoryWindow, text= "ADD", font=('Arial', 15, 'bold'), command = add_category_staff)
    add_button.place(x=700, y=290, height = 40, width = 220)

    cancel_add_button= Button(addCategoryWindow, text= "QUIT", font=('Arial', 15, 'bold'), command = close_add_category_staff)
    cancel_add_button.place(x=700, y=340, height = 40, width = 220)

    addCategoryWindow.grab_set()
    addCategoryWindow.mainloop()



#function to close edit category page for staff
def close_edit_category_staff():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to QUIT Edit Category?')
    if answer:
        editCategoryWindow.destroy()
        display_category_database_staff()


#function to open edit category page for staff
def open_edit_category_staff():

    connect_database()
    global editCategoryWindow


    if not StaffCategoryTree.selection():
        messagebox.showerror("Error", "Please select an item to edit")
    else:

        editCategoryWindow = Toplevel(window)
        editCategoryWindow.rowconfigure(0, weight=1)
        editCategoryWindow.columnconfigure(0, weight=1)
        editCategoryWindow.state('zoomed')
        editCategoryWindow.configure(bg = '#DFEEFF')
        
        editCategory_label = Label(editCategoryWindow, text="EDIT CATEGORY", font=('Arial', 35, 'bold'),bg='#DFEEFF')
        editCategory_label.place(x=620, y=30)
            
        categoryID_label = Label(editCategoryWindow, text="Category ID", font=('Arial', 18),bg='#DFEEFF')
        categoryID_label.place(x=700, y=115)
        categoryID_entry = Entry(editCategoryWindow, font=(20), textvariable = edit_cat_id_strvar)
        categoryID_entry.place(x=700, y=150)
            
        categoryName_label = Label(editCategoryWindow, text="Category Name", font=('Arial', 18),bg='#DFEEFF')
        categoryName_label.place(x=700, y=200)
        categoryName_entry = Entry(editCategoryWindow, font=(20), textvariable = edit_cat_name_strvar)
        categoryName_entry.place(x=700, y=240)
            


        edit_button= Button(editCategoryWindow, text= "EDIT", font=('Arial', 15, 'bold'), command = edit_category_staff)
        edit_button.place(x=700, y=290, height = 40, width = 220)

        cancel_edit_button= Button(editCategoryWindow, text= "QUIT", font=('Arial', 15, 'bold'), command = close_edit_category_staff)
        cancel_edit_button.place(x=700, y=340, height = 40, width = 220)

        view_category_staff()

        editCategoryWindow.grab_set()
        editCategoryWindow.mainloop()



# Remove category records
def remove_category_staff():
    if not StaffCategoryTree.selection():
        messagebox.showerror("Error", "Please select an item to delete")
        
    else:
        connect_database()
        
    	# Add a little message box for fun
        response = messagebox.askyesno("Delete", "This Will Delete EVERYTHING SELECTED From The Table\nAre You Sure?!")

	#Add logic for message box
        if response == 1:
		# Designate selections
                x = StaffCategoryTree.focus()
                values = StaffCategoryTree.item(x)
                selection = values ["values"]
                cursor.execute("SELECT product.cat_id, category.cat_id FROM product NATURAL JOIN category WHERE category.cat_id LIKE ?", (str(selection[0]),))
                data = cursor.fetchall()
                if len(data)== 0:
                    cursor.execute("DELETE FROM category WHERE cat_id = ?", (str(selection[0]),))
                    conn.commit()
                    display_category_database_staff()
                else:
                    messagebox.showerror("Error", "Category ID needed for product \nCannot Delete!")


#function to search for list of category for staff
def search_category_staff():
    cb_value1 = search_category_by_strvar.get()
    cb_value2 = search_category_strvar.get()

    if cb_value1 == "ID":
        connect_database()
        cursor.execute("""SELECT cat_id, cat_name FROM category
                        WHERE cat_id LIKE ?""", ('%' + cb_value2 + '%',))
        data = cursor.fetchall()
        
        if not cb_value2:            
            messagebox.showerror('Error', 'Please fill in the search field')

        elif len(data) !=0:
            StaffCategoryTree.delete(*StaffCategoryTree.get_children())
            
            for records in data:
                StaffCategoryTree.insert('', END, values= records)
                
            conn.commit()
        else:
            messagebox.showerror('Error', 'Record is not found')
    

    elif cb_value1 == "NAME":
        connect_database()
        cursor.execute("""SELECT cat_id, cat_name FROM category
                        WHERE cat_name LIKE ?""", ("%" + cb_value2 + "%",))
        data = cursor.fetchall()
        
        if not cb_value2:            
            messagebox.showerror('Error', 'Please fill in the search field')

        elif len(data) !=0:
            StaffCategoryTree.delete(*StaffCategoryTree.get_children())
            
            for records in data:
                StaffCategoryTree.insert('', END, values= records)
                
            conn.commit()
            
        else:
            messagebox.showerror('Error', 'Record is not found')
    else:
        messagebox.showerror('Error', "Please select ID or NAME in the drop down box!")


#function to clear seach category entries for staff
def clear_search_category_staff():
    display_category_database_staff()
    staff_tab4_search_combobox.current(0)
    for i in ['search_category_strvar']:
        exec(f"{i}.set('')")



#place button and entries in inventory tab for staff user
staff_tab1_add_button= Button(staff_tab1, text= "ADD", font=('Arial', 15, 'bold'),command = open_add_inventory_staff)
staff_tab1_add_button.place(x=910, y=620)

staff_tab1_edit_button= Button(staff_tab1, text= "EDIT", font=('Arial', 15, 'bold'),fg = 'blue', command = open_edit_inventory_staff)
staff_tab1_edit_button.place(x=1000, y=620)

staff_tab1_delete_button= Button(staff_tab1, text= "DELETE", font=('Arial', 15, 'bold'), fg = 'red',command = remove_inventory_staff)
staff_tab1_delete_button.place(x=1100, y=620)

staff_tab1_search_button= Button(staff_tab1, text= "SEARCH", font=('Arial', 15, 'bold'), command = search_inventory_staff)
staff_tab1_search_button.place(x=680, y=620)


staff_tab1_search_combobox =ttk.Combobox(staff_tab1, textvariable = search_inventory_by_strvar, values = ["SEARCH BY","ID","NAME"], state = "readonly", font=5)
staff_tab1_search_combobox.place(x=100, y=630)
staff_tab1_search_combobox.current(0)

staff_tab1_search_entry =Entry(staff_tab1, textvariable = search_inventory_strvar, font = 5)
staff_tab1_search_entry.place(x=370, y=630)

staff_tab1_clear_button= Button(staff_tab1, text= "CLEAR", font=('Arial', 15, 'bold'), command = clear_search_inventory_staff)
staff_tab1_clear_button.place(x=800, y=620)



#place button and entries in supplier tab for staff user
staff_tab3_add_button= Button(staff_tab3, text= "ADD", font=('Arial', 15, 'bold'), command= open_add_supplier_staff )
staff_tab3_add_button.place(x=910, y=620)

staff_tab3_edit_button= Button(staff_tab3, text= "EDIT", font=('Arial', 15, 'bold'),fg = 'blue', command = open_edit_supplier_staff)
staff_tab3_edit_button.place(x=1000, y=620)

staff_tab3_delete_button= Button(staff_tab3, text= "DELETE", font=('Arial', 15, 'bold'), fg = 'red',command = remove_supplier_staff)
staff_tab3_delete_button.place(x=1100, y=620)

staff_tab3_search_button= Button(staff_tab3, text="SEARCH", font=('Arial', 15, 'bold'), command = search_supplier_staff)
staff_tab3_search_button.place(x=680, y=620)

staff_tab3_search_combobox =ttk.Combobox(staff_tab3, textvariable = search_supplier_by_strvar, values = ["SEARCH BY","ID","NAME"], state = "readonly", font=5)
staff_tab3_search_combobox.place(x=100, y=630)
staff_tab3_search_combobox.current(0)

staff_tab3_search_entry =Entry(staff_tab3, textvariable = search_supplier_strvar, font=5)
staff_tab3_search_entry.place(x=370, y=630)

staff_tab3_clear_button= Button(staff_tab3, text= "CLEAR", font=('Arial', 15, 'bold'), command = clear_search_supplier_staff)
staff_tab3_clear_button.place(x=800, y=620)




#place button and entries in category tab for staff user
staff_tab4_add_button= Button(staff_tab4, text= "ADD", font=('Arial', 15, 'bold'), command = open_add_category_staff)
staff_tab4_add_button.place(x=910, y=620)

staff_tab4_edit_button= Button(staff_tab4, text= "EDIT", font=('Arial', 15, 'bold'), fg = 'blue',command = open_edit_category_staff)
staff_tab4_edit_button.place(x=1000, y=620)

staff_tab4_delete_button= Button(staff_tab4, text= "DELETE", font=('Arial', 15, 'bold'),fg = 'red', command = remove_category_staff)
staff_tab4_delete_button.place(x=1100, y=620)

staff_tab4_search_button= Button(staff_tab4, text= "SEARCH", font=('Arial', 15, 'bold'), command = search_category_staff)
staff_tab4_search_button.place(x=680, y=620)

staff_tab4_search_combobox =ttk.Combobox(staff_tab4, textvariable = search_category_by_strvar, values = ["SEARCH BY","ID","NAME"], state = "readonly", font=5)
staff_tab4_search_combobox.place(x=100, y=630)
staff_tab4_search_combobox.current(0)

staff_tab4_search_entry =Entry(staff_tab4, textvariable = search_category_strvar, font=5)
staff_tab4_search_entry.place(x=370, y=630)

staff_tab4_clear_button= Button(staff_tab4, text= "CLEAR", font=('Arial', 15, 'bold'), command = clear_search_category_staff)
staff_tab4_clear_button.place(x=800, y=620)




#frame for Home page
staff_HomeFrame = Frame(page3, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
staff_HomeFrame.place(x=150,y=0, height=850, width = 1390)



#frame for "Poh Cheong Tong"                             
staff_HomeTopFrame=Frame(staff_HomeFrame, bg='#492F7C', highlightbackground='white', highlightthickness=1)
staff_HomeTopFrame.place(x=0,y=0, height=100,width = 1550)

staff_HomeBottomFrame=Frame(staff_HomeFrame, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
staff_HomeBottomFrame.place(x=0,y=100, height=750, width = 1390)


#frame for logo    
pg3RectangleFrame1=Frame(page3, bg='#492F7C', highlightbackground='white', highlightthickness=1)
pg3RectangleFrame1.place(x=0,y=0, height=100,width = 150)

#placing logo

pg3Logo = Label(pg3RectangleFrame1, image = img)
pg3Logo.place(x=45, y=18)



#Display "Poh Cheong Tong"
staff_HomeTopLabel = Label(staff_HomeTopFrame, text='Poh Cheong Tong Medical Hall System', font=('Arial', 30), fg='white', bg='#492F7C')
staff_HomeTopLabel.place(x=10, y=30)


staff_HomeWelcomeLabel = Label(staff_HomeBottomFrame, text='Welcome,', font=('Arial', 40, 'bold'), fg='black', bg='#DFEEFF')
staff_HomeWelcomeLabel.place(x=20, y=20)
                   
staff_HomeNameLabel= Label(staff_HomeBottomFrame, textvariable = userName, font=('Arial', 40, 'bold'), fg='black', bg='#DFEEFF')
staff_HomeNameLabel.place(x=280, y=20)

staff_HomeEmail = Label(staff_HomeBottomFrame, text = "Email :", font=('Arial', 25), fg='black', bg='#DFEEFF')
staff_HomeEmail.place(x=20, y=160)

staff_HomeEmailLabel = Label(staff_HomeBottomFrame, textvariable = userEmail, font=('Arial', 25), fg='black', bg='#DFEEFF')
staff_HomeEmailLabel.place(x=220, y=160)

staff_HomeRole = Label(staff_HomeBottomFrame, text = "Role   :", font=('Arial', 25), fg='black', bg='#DFEEFF')
staff_HomeRole.place(x=20, y=210)

staff_HomeRoleLabel = Label(staff_HomeBottomFrame, textvariable = userRole, font=('Arial', 25), fg='black', bg='#DFEEFF')
staff_HomeRoleLabel.place(x=220, y=210)

staff_HomeID= Label(staff_HomeBottomFrame,text = "ID      :", font=('Arial', 25), fg='black', bg='#DFEEFF')
staff_HomeID.place(x=20, y=110)

staff_HomeIDLabel= Label(staff_HomeBottomFrame,textvariable = userId, font=('Arial', 25), fg='black', bg='#DFEEFF')
staff_HomeIDLabel.place(x=220, y=110)


#framing Billing page
staff_BillingFrame = Frame(page3, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
staff_BillingFrame.place(x=150,y=0, height=850, width = 1390)

staff_BillingTopFrame = Frame(staff_BillingFrame, bg='#492F7C', highlightbackground='white', highlightthickness=1)
staff_BillingTopFrame.place(x=0,y=000, height=100,width = 1390)

staff_BillingBottomFrame = Frame(staff_BillingFrame, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
staff_BillingBottomFrame.place(x=0,y=100, height=750,width = 1390)



# ======== Billing Page ===========
#display 'Billing' in billing page
staff_BillingLabel = Label(staff_BillingTopFrame, text='Billing', font=('Arial', 30), fg='white', bg='#492F7C')
staff_BillingLabel.place(x=20, y=30)




# Display table from database
def staff_displayInvoice():
    conn = sqlite3.connect("Poh Cheong Tong.db")
    cur = conn.cursor()
    cur.execute("SELECT invoice_id, date, total FROM invoice GROUP BY invoice_id")
    rows = cur.fetchall()
    for row in rows:  # loop to display all the invoice
        staff_ManageInvoice.insert("", END, values=row)




# Create tree view for Manage Invoice
staff_ManageInvoice = ttk.Treeview(staff_BillingBottomFrame, selectmode="extended", show='headings',
                             columns=('Invoice ID', 'Date Time', 'Total Price'))
staff_ManageInvoice.place(relwidth=1, relheight=0.7)

ttk.Scrollbar(staff_ManageInvoice, orient="vertical", command=ManageInvoice.yview).pack(side=RIGHT, fill=Y)

staff_ManageInvoice.heading('Invoice ID', text='Invoice ID', anchor=CENTER)
staff_ManageInvoice.heading('Date Time', text='Date & Time', anchor=CENTER)
staff_ManageInvoice.heading('Total Price', text='Total Price', anchor=CENTER)

staff_ManageInvoice.column("Invoice ID", anchor=CENTER, width=100)
staff_ManageInvoice.column("Date Time", anchor=CENTER, width=200)
staff_ManageInvoice.column("Total Price", anchor=CENTER, width=140)

staff_displayInvoice()

# ======= Create New Bill ======

def staff_createInvoice():
    addInvoice = Toplevel(window)
    addInvoice.geometry('1400x850')
    addInvoice.configure(bg='#DFEEFF')
    addInvoice.title('Create New Bill')

    conn = sqlite3.connect('Poh Cheong Tong.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM invoice')

    # Heading
    heading_frame = Frame(addInvoice, bd=8, bg="#DFEEFF")
    heading_frame.pack(side=TOP, fill="x")

    heading_label = Label(heading_frame, text="Add New Invoice", font=("times new roman", 18, "bold"), bg="#DFEEFF",
                          fg="black", pady=5)
    heading_label.pack()

    # add items function in create new invoice page
    def add_item_bt():
        if len(add_products.get()) == 0 or inventory.count(add_products.get()) == 0:
            tk.messagebox.showerror("Error", "Product Not Found!")
            return
        else:
            if not pro_stock.get().isdigit():
                tk.messagebox.showerror('Error', 'Invalid quantity!')
                return
            if int(pro_stock.get()) <= 0:
                tk.messagebox.showerror('Error', 'Invalid quantity!')
                return
            cur.execute("SELECT pro_id ,product_name FROM product WHERE product_name = ? ", (add_products.get(),))
            row = cur.fetchall()
            row = [list(row[0])]  # fetch the data from database and put into list
            # get the max ID from invoice table
            cur.execute('select max(ID) from invoice')
            PKid = cur.fetchall()

            if PKid[0][0] is not None:  # if ID is nothing
                for i in range(len(row)):  # each row ID + 1
                    ID_pk = PKid[i][0] + 1
            else:
                ID_pk = 1
            row[0].insert(0, ID_pk)  # row 0 = ID
            ID_pk += 1
            # get the input of product quantity and insert it into list
            row[0].append(int(pro_stock.get()))
            # calculate the product price by multiply unit price and quantity selected
            row[0].append((int(pro_stock.get()) * name_price[add_products.get()]))
            row = [tuple(row[0])]  # convert the row into tuple
            itemID.set(row[0][1])  # value from row 0, column 1 insert into itemID entry
            itemPrice.set(name_price[add_products.get()])  # get the price of selected product
            itemName.set(row[0][2])  # value from row 0, column 2 insert into itemName entry
            cur.execute("SELECT quantity FROM product WHERE pro_id=?", (row[0][1],))  # get the quantity from product id
            qli = cur.fetchall()
            # calculate the actual quantity of product - the quantity of product in the dictionary - quantity input
            if ((qli[0][0] - int(qty_id[row[0][1]])) - int(pro_stock.get())) < 0:
                if li[0][0] != 0:
                    tk.messagebox.showerror('Error', 'Product with this quantity not available!')
                    return
                else:
                    tk.messagebox.showerror('Error', 'Product out of stock!')
                    return

            qty_id[row[0][1]] += int(pro_stock.get())  # quantity of the product in dict(0) + quantity input
            itemQuantity.set(qli[0][0] - qty_id[row[0][1]])  # Left stock = actual quantity - quantity input
            for data in row:
                order_tabel.insert('', 'end', values=data)  # insert the selected product into table

            # convert price into 2dp
            price_product = (float(subtotalPrice.get()) + (float(int(pro_stock.get())) * float(name_price[add_products.get()])))
            price = "{:.2f}".format(price_product)
            subtotalPrice.set(price)
            # clear the entry after the item is successfully add
            pro_stock.set('1')
            add_products.set('')

    def remove_item_bt(event=None):
        re = order_tabel.selection()  # select product to remove from the cart
        if len(re) == 0:  # if not selecting any item
            tk.messagebox.showerror('Error', 'No item are selected')
            return
        if tk.messagebox.askyesno('Alert!', 'Remove Item?'):
            x = order_tabel.get_children()  # get the item id
            re = re[0]
            ol = []  # create empty list
            fi = []  # create empty list
            for n in x:
                if n != re:
                    ol.append(tuple((order_tabel.item(n))['values']))
                else:
                    fi = ((order_tabel.item(n))['values'])  # get the item values
            order_tabel.delete(*order_tabel.get_children())  # delete the products
            for n in ol:
                order_tabel.insert('', 'end', values=n)
            itemQuantity.set('')  # clear the field
            itemName.set('')
            itemID.set('')
            itemPrice.set('')
            add_products.set('')
            pro_stock.set('1')
            qty_id[str(fi[1])] -= fi[3]  # the actual quantity of product - quantity of selected product
            delproprice = float(subtotalPrice.get()) - float(fi[4])  # subtotal price - the item price
            delprice = "{:.2f}".format(delproprice)  # convert the subtotal price into float which is 2dp
            subtotalPrice.set(delprice)
            return

    # clear the entry box
    def clear_bt():
        itemID.set("")
        itemName.set("")
        itemPrice.set("")
        itemQuantity.set("")
        add_products.set("")
        pro_stock.set("1")

    # update the data to database
    def generateInvoice():
        if username_entry == "" or pay_amount_entry == ""  or paymeth_entry == "":
            tk.messagebox.showerror('Error', 'Please fill in the empty fields')
            return
        x = order_tabel.get_children()  # get customer's orders
        if len(x) == 0:
            tk.messagebox.showerror('Error', 'Empty cart!')
            return
        if tk.messagebox.askyesno('Alert!', 'Do you want to proceed?') == False:
            return
        a = []  # create an empty list
        cur.execute("select max(invoice_id) from invoice")
        invoice1 = cur.fetchall()
        invoice1 = invoice1[0][0] + 1  # invoice ID + 1 based on previous id
        for i in x:
            l = order_tabel.item(i)
            a.append(l['values'])  # append the values of order list treeview into the empty list 'a'

        for i in a:  # insert the invoice data into database
            sqlquery = "INSERT INTO invoice " \
                       "(invoice_id, date, user_id, pro_id, quantity, total, paid, change, payment_method) " \
                       "VALUES (?,?,?,?,?,?,?,?,?)"
            values = (
            int(invoice1), str(datetime_entry.get()), str(username_entry.get()), i[1], i[3], str(subtotalPrice.get()),
            str(pay_amount_entry.get()), str(change_entry.get()), str(paymeth_entry.get()))
            cur.execute(sqlquery, values, )
            # update the product quantity after the product is sold
            cur.execute("select quantity from product where pro_id=?", (i[1],))
            pq = cur.fetchall()
            cur.execute("update product set quantity=? where pro_id=?", (pq[0][0] - qty_id[str(i[1])], i[1]))
            conn.commit()
        tk.messagebox.showinfo('Success', 'Transaction Successful!')
        # Update the Billing Page tree view
        staff_ManageInvoice.delete(*staff_ManageInvoice.get_children())
        staff_displayInvoice()

        # Clear create new invoice field
        order_tabel.delete(*order_tabel.get_children())
        itemQuantity.set('')
        itemName.set('')
        itemID.set('')
        itemPrice.set('')
        subtotalPrice.set(0)
        change.set(0)
        payamount.set('')
        PaymentMethod.set('')
        add_products.set('')
        pro_stock.set('1')
        # Re-fetch the products' data from databade
        cur.execute("select pro_id from product")
        l = cur.fetchall()
        for i in range(0, len(l)):
            qty_id[l[i][0]] = 0

    # === Invoice details ===
    invoice_frame1 = Frame(addInvoice, bg="#DFEEFF", relief=FLAT, height=100)
    invoice_frame1.pack(side=TOP, fill="x")

    # Invoice ID
    cur.execute("select max(invoice_id) from invoice")  # get the maximum no of invoice ID
    invoice = cur.fetchall()
    invoice = int(invoice[0][0]) + 1  # new invoice id = maximum invoice ID +1
    Label(invoice_frame1, text="Invoice ID: " + str(invoice), font=("arial", 13), bg="#DFEEFF").grid(row=0, column=0,
                                                                                                     padx=10)

    # Date & Time
    date_label = Label(invoice_frame1, text="Date & Time", font=("arial", 13), bg='#DFEEFF')
    date_label.grid(row=0, column=3, padx=20, pady=10)
    datetime_entry = Entry(invoice_frame1, width=20, font=("arial", 13), bd=1)
    datetime_entry.insert(END, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # get current time
    datetime_entry.grid(row=0, column=4, padx=5, pady=10)

    # declaring cashier name variable
    username = StringVar()
    query = "SELECT user_id FROM user"
    user_data = conn.execute(query)
    user_list = [r for r, in user_data]  # create a user list

    # Cashier Name
    username_label = Label(invoice_frame1, text="Cashier Name", font=("arial", 13), bd=1, bg='#DFEEFF')
    username_label.grid(row=0, column=5, padx=20, pady=10)
    username_entry = ttk.Combobox(invoice_frame1, font=("arial", 12), textvariable=username, values=user_list)
    username_entry.grid(row=0, column=6, padx=5, pady=10)

    # ========= Order Lists (Tree View for Selected Products) ==========
    

    # Create tree view to insert the products added into order lists
    orderList_frame = Frame(addInvoice, width=700, bg='#DFEEFF', relief=RIDGE)
    orderList_frame.place(x=5, y=300, height=400, width=1360)

    order_tabel_frame = Frame(orderList_frame)
    order_tabel_frame.place(x=10, y=25, height=300, width=1345)

    scrollbar_order_x = Scrollbar(order_tabel_frame, orient=HORIZONTAL)
    scrollbar_order_y = Scrollbar(order_tabel_frame, orient=VERTICAL)

    order_tabel = ttk.Treeview(order_tabel_frame, style="Treeview",
                               columns=("id", "product id", "name", 'quantity', 'total price'),
                               selectmode="browse", height=6, yscrollcommand=scrollbar_order_y.set,
                               xscrollcommand=scrollbar_order_x.set)
    order_tabel.heading("id", text="Transaction ID")
    order_tabel.heading("product id", text="Product ID")
    order_tabel.heading("name", text="Product Name")
    order_tabel.heading("quantity", text="Quantity")
    order_tabel.heading("total price", text="Total Price")
    order_tabel["displaycolumns"] = ("id", "product id", "name", "quantity", "total price")
    order_tabel["show"] = "headings"
    order_tabel.column("id", width=200, anchor='center', stretch=NO)
    order_tabel.column("product id", width=200, anchor='center', stretch=NO)
    order_tabel.column("name", width=200, anchor='center', stretch=NO)
    order_tabel.column("quantity", width=200, anchor='center', stretch=NO)
    order_tabel.column("total price", width=200, anchor='center', stretch=NO)

    scrollbar_order_x.pack(side=BOTTOM, fill=X)
    scrollbar_order_x.configure(command=order_tabel.xview)
    scrollbar_order_y.pack(side=RIGHT, fill=Y)
    scrollbar_order_y.configure(command=order_tabel.yview)

    order_tabel.pack(fill=BOTH, expand=1)

    productFrame = Frame(addInvoice, width=700, bg="#DFEEFF", relief=FLAT)
    productFrame.place(x=0, y=105)

    # Quantity input by user
    pro_stock = StringVar(value=1)

    # Variables for product need to add in cart
    add_products = StringVar()
    product_data = conn.execute("SELECT product_name FROM product")
    pro_list = [p for p, in product_data]  # create products list

    # For search frame: Search product entry and buttons
    additem_bt = ttk.Button(productFrame, text="Add Item", command=add_item_bt)
    additem_bt.grid(row=3, column=4, padx=5, pady=10)

    remove_bt = ttk.Button(productFrame, text="Remove Item", command=remove_item_bt)
    remove_bt.grid(row=3, column=5, padx=5, pady=10)

    clear_bt = ttk.Button(productFrame, text="Clear", command=clear_bt)
    clear_bt.grid(row=3, column=6, padx=5, pady=10)

    search_label = Label(productFrame, text="Search Products", font=("arial", 13), bg='#DFEEFF', pady=0)
    search_label.grid(row=1, column=3, padx=10, pady=5)
    product_combobox = ttkwidgets.autocomplete.AutocompleteCombobox(productFrame, width=25, font=("arial", 12),
                                                                    textvariable=add_products, completevalues=pro_list)
    product_combobox.grid(row=1, column=4, columnspan=2, padx=10, pady=5)

    qty_label = Label(productFrame, text="Quantity", font=("arial", 13), bg='#DFEEFF', pady=0)
    qty_label.grid(row=2, column=3, padx=10, pady=5)
    qty_entry = Entry(productFrame, font=("arial", 12), textvariable=pro_stock, width=26)
    qty_entry.grid(row=2, column=4, columnspan=2, padx=10, pady=5)

    # fetch product name and sell price of the product from database
    cur.execute("SELECT product_name, sell_price FROM product")
    li = cur.fetchall()
    inventory = [] # create an empty list
    name_price = dict()  # create dictionary on the product's name and price {product name : product sell price}
    for i in range(0, len(li)):  # looping on the products in range of 0 to the number of products
        if inventory.count(li[i][0]) == 0:
            inventory.append(li[i][0])  # append the sell price of the products into inventory
        name_price[li[i][0]] = li[i][1]  # the product's sell price = the row i column 0(product name) in dictionary
    product_combobox.set_completion_list(inventory)  # set the inventory list into the product combo box
    li = ['Product Id', 'Product Name', 'Price', 'Left Stock']
    for i in range(0, 4):  # looping on the list in range of 0 to 4
        Label(productFrame, text=li[i], font="roboto 14 bold", bg="#FFFFFF")

    # Products id, name, price, stock (Do not editable)
    # selected items variables（Cart）
    itemID = StringVar()
    itemName = StringVar()
    itemPrice = StringVar()
    itemQuantity = StringVar()

    product_label = Label(productFrame, text="Products ID", font=("arial", 13), bg='#DFEEFF', pady=0)
    product_label.grid(row=1, column=0, pady=5)
    product_entry = Entry(productFrame, font=("arial", 12), textvariable=itemID, width=25, state='readonly')
    product_entry.grid(row=1, column=1, pady=5)

    proname_label = Label(productFrame, text="Products Name", font=("arial", 13), bg='#DFEEFF', pady=0)
    proname_label.grid(row=2, column=0, pady=5)
    proname_entry = Entry(productFrame, font=("arial", 12), textvariable=itemName, width=25, state='readonly')
    proname_entry.grid(row=2, column=1, pady=5)

    proprice_label = Label(productFrame, text="Price", font=("arial", 13), bg='#DFEEFF', pady=0)
    proprice_label.grid(row=3, column=0, padx=20, pady=5)
    proprice_entry = Entry(productFrame, font=("arial", 12), textvariable=itemPrice, width=25, state='readonly')
    proprice_entry.grid(row=3, column=1, pady=5)

    stock_label = Label(productFrame, text="Left Stock", font=("arial", 13), bg='#DFEEFF', pady=0)
    stock_label.grid(row=4, column=0, pady=5)
    stock_entry = Entry(productFrame, font=("arial", 12), textvariable=itemQuantity, width=25, state='readonly')
    stock_entry.grid(row=4, column=1, pady=5)

    # Create dictionary to fetch product id from database
    qty_id = dict()
    cur.execute("select pro_id from product")
    pl = cur.fetchall()  #fetch the pro_id from database
    for i in range(0, len(pl)):  # looping on create dictionary for all the products
        qty_id[pl[i][0]] = 0  # set dictionary {product id 1 : price = 0}, {product id 2: price = 0}, ....

    # variable for subtotal price
    subtotalPrice = IntVar(value=0)
    # Sub total
    total_price_label = Label(orderList_frame, text="Sub Total", font=("arial", 13, "bold"), bg="#DFEEFF")
    total_price_label.pack(side=LEFT, anchor=SW, padx=5, pady=15)
    total_price_entry = Entry(orderList_frame, font="arial 12", textvariable=subtotalPrice, state='readonly', width=10)
    total_price_entry.pack(side=LEFT, anchor=SW, padx=5, pady=15)

    # Payment
    paymentframe = Frame(orderList_frame, bg="#DFEEFF", relief=FLAT)
    paymentframe.pack(side=LEFT, anchor=SW, padx=10, pady=5)
    paymentM_label = Label(paymentframe, text="Payment Method", font=("arial", 13, "bold"), bg="#DFEEFF")
    paymentM_label.grid(row=0, column=0, padx=10, pady=10)

    # payment method
    PaymentMethod = StringVar()
    PaymentM = ["Cash", "Debit/Credit Card"]  # Create list for payment method
    paymeth_entry = ttk.Combobox(paymentframe, font="arial 12", textvariable=PaymentMethod, values=PaymentM, width=10)
    paymeth_entry.grid(row=0, column=1, padx=5, pady=5)

    # pay amount by customer
    payamount = IntVar()
    pay_amount_label = Label(paymentframe, text="Amount Paid", font="arial 12", bg="#DFEEFF")
    pay_amount_label.grid(row=0, column=2, padx=10, pady=10)
    pay_amount_entry = Entry(paymentframe, font="arial 12", textvariable=payamount, width=10)
    pay_amount_entry.grid(row=0, column=3, padx=5, pady=5)

    # change amount to customers
    change = IntVar()
    # Calculate the change to customer
    def calculate():
        if float(payamount.get()) < float(subtotalPrice.get()):
            tk.messagebox.showerror("Error", "The pay amount is less than the sub-total price.")
            return
        else:
            Pricechange = float(payamount.get()) - float(subtotalPrice.get())
            changesP = "{:.2f}".format(Pricechange)
            change.set(changesP)

    change_label = Label(paymentframe, text="Change", font="arial 12", bg="#DFEEFF")
    change_label.grid(row=0, column=4, padx=10, pady=5)
    change_entry = Entry(paymentframe, font="arial 12", textvariable=change, state='readonly', width=10)
    change_entry.grid(row=0, column=5, padx=5, pady=5)

    calculate_bt = Button(paymentframe, text='Calculate', font=('Helvetica Neue', 12), relief='raised',
                          command=calculate)
    calculate_bt.grid(row=0, column=7, padx=10, pady=5)

    # Generate invoice
    generate_invoice_bt = Button(paymentframe, text='Generate Invoice', font=('Helvetica Neue', 12), relief='raised',
                                 command=generateInvoice)
    generate_invoice_bt.grid(row=0, column=8, padx=10, pady=5)

    # quit Create Invoice Window
    def quitCreateInvoice():
        if tk.messagebox.askyesno('Close?', 'Are you sure want to quit this window?') == True:
            addInvoice.destroy()

    cancel_close = tk.Button(addInvoice, text='Cancel', width=10, command=lambda: quitCreateInvoice())
    cancel_close.place(x=1100, y=750)


# ========= Delete Invoice ======
def staff_deleteInvoice():
    if not staff_ManageInvoice.selection():  # if not select any row
        tk.messagebox.showerror("Error", "Please select invoice to delete")
    else:  # To confirm the user really want to delete the invoice?
        result = tk.messagebox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                           icon="warning")
        if result == 'yes':
            curItem = staff_ManageInvoice.focus()
            contents = (staff_ManageInvoice.item(curItem))
            selecteditem = contents['values']
            staff_ManageInvoice.delete(curItem)
            cursor = conn.execute("DELETE FROM invoice WHERE invoice_id=?", (str(selecteditem[0]),))
            conn.commit()  # delete data from database
            cursor.close()
            staff_ManageInvoice.delete(*staff_ManageInvoice.get_children())  # clear all rows in tree table
            displayInvoice()  # redisplay the data

def staff_click():  # download bill button function
    if not staff_ManageInvoice.selection():  # if not select a row
        tk.messagebox.showerror(title="Error", message="Please select invoice to download.")
        return
    else:  # Ask user to confirm he/she want to download the receipt
        if tk.messagebox.askyesno('Download invoices', 'Are you sure want to download the invoice?') == True:
            staff_dlpdf()
            tk.messagebox.showinfo("Downloaded", "Invoice is successfully downloaded.")


def staff_dlpdf():
    current_item = staff_ManageInvoice.focus()  # read the selected row
    vl = staff_ManageInvoice.item(current_item, "values")  # get the values on selected row from tree view

    curr = conn.execute(
        "SELECT "
        "i.invoice_id, "
        "i.date, "
        "u.user_name ,"
        "i.payment_method, "
        "i.pro_id, "
        "p.product_name, "
        "p.sell_price, "
        "i.quantity, "
        "i.total, "
        "i.paid, "
        "i.change "
        "FROM invoice i "
        "INNER JOIN product p ON p.pro_id=i.pro_id "
        "LEFT JOIN user u ON u.user_id=i.user_id WHERE invoice_id=?",
        (vl[0],))
    data = curr.fetchall()

    # convert data into dataframe
    df = pd.DataFrame(data, columns=("invoice id", "date", "username", "payment method", "product id", "name",
                                     "sell_price", "quantity", "total price", "paid amount", "change"))

    # Create PDF Template
    pdf = FPDF(orientation='P', unit='mm', format='A5')  # variable pdf to fixed paper orientation, unit and size

    pdf.add_page()  # Add a page
    pdf.set_margins(2, 2, 2)  # set margins(LEFT, TOP, RIGHT)

    pdf.set_font("Times", size=20)  # set style & size of font
    # pdf.cell(width, height, txt, border, Indicates, align)
    pdf.cell(w=125, h=10, txt="Receipt", ln=0, align='C')
    pdf.cell(w=148, h=10, txt='', border=0, ln=1, align='C')  # empty one line

    pdf.set_font("Arial", size=15)
    pdf.cell(w=148, h=10, txt="Poh Cheong Tong Medical Hall", ln=1, align='C')
    pdf.set_font('Helvetica', size=10)
    pdf.cell(w=148, h=5, txt="610-P, Jalan Paya Terubung,", ln=1, align='C')
    pdf.cell(w=148, h=5, txt="Kampung Pisang,", ln=1, align='C')
    pdf.cell(w=148, h=5, txt="11500 Ayer Itam, Pulau Pinang.", ln=1, align='C')

    pdf.set_font('Helvetica', size=13)
    pdf.cell(120, 10, 'Invoice ID: ' + str(df.iloc[0][0]), ln=1, align='L')
    pdf.cell(120, 10, 'Date & Time: ' + str(df.iloc[0][1]), ln=1, align='L')
    pdf.cell(120, 10, 'Cashier Name: ' + str(df.iloc[0][2]), ln=1, align='L')
    pdf.cell(120, 10, 'Payment Method: ' + str(df.iloc[0][3]), ln=1, align='L')
    pdf.cell(120, 6, '', 0, 1, 'C')  # empty one line

    line_height = pdf.font_size * 17.5  # set the line height and column width

    pdf.set_font('Helvetica', 'B', size=10)
    pdf.cell(20, 6, 'Product ID', 0, 0, 'L')  # column 1 heading
    pdf.cell(75, 6, 'Product Name', 0, 0, 'L')  # column 2 heading
    pdf.cell(15, 6, 'Price', 0, 0, 'L')  # column 3 heading
    pdf.cell(15, 6, 'Quantity', 0, 1, 'L')  # column 4 heading

    for i in range(len(df)):  # Create loop to display the products in tables

        pdf.set_font('Helvetica', size=10)
        pdf.cell(20, 6, str(df.loc[0 + i]['product id']), 1, 0, 'L')  # column 1
        pdf.cell(75, 6, str(df.loc[0 + i]['name']), 1, 0, 'L')  # column 2
        pdf.cell(15, 6, str(df.loc[0 + i]['sell_price']), 1, 0, 'L')  # column 3
        pdf.cell(15, 6, str(df.loc[0 + i]['quantity']), 1, 1, 'L')  # column 4

    pdf.cell(80, 6, '', 0, 1, 'C')  # empty line
    pdf.cell(80, 6, '', 0, 1, 'C')  # empty line
    pdf.set_font('Helvetica', size=13)

    pdf.cell(200, 10, 'Sub Total: RM ' + str(df.loc[0]["total price"]), ln=1, align='L')
    pdf.cell(200, 10, 'Paid Amount: RM ' + str(df.loc[0]["paid amount"]), ln=1, align='L')
    pdf.cell(200, 10, 'Change: RM ' + str(df.loc[0]["change"]), ln=1, align='L')

    pdf.output(str(df.loc[0]['invoice id']) + '.pdf', 'F')  # Download file


# Create New Invoice Button
staff_add_button = tk.Button(staff_BillingBottomFrame, text="+ Add", font=('Helvetica Neue', 12), width=10, height=1, relief='raised',
                       command=staff_createInvoice)
staff_add_button.place(x=525, y=600)

# Delete Invoice Button
staff_delete_button = tk.Button(staff_BillingBottomFrame, text="Delete", font=('Helvetica Neue', 12), width=10, height=1,
                          command=staff_deleteInvoice)
staff_delete_button.place(x=775, y=600)

# View Invoice button
staff_download_button = tk.Button(staff_BillingBottomFrame, text="Download\nInvoice", font=('Helvetica Neue', 12), width=10, height=2, relief='raised', command=staff_click)
staff_download_button.place(x=650, y=600)










    
#====== start program ======
window.mainloop()

