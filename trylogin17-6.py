import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3


window = Tk()
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.state('zoomed')

page1 = Frame(window)
page2 = Frame(window)
page3 = Frame(window)
page4 = Frame(window)

for frame in (page1, page2, page3, page4):
    frame.grid(row=0, column=0, sticky='nsew')

def show_frame(frame):
    frame.tkraise()

show_frame(page1)

# ============= Page 1 (Log in) =============
page1.config(background='#DFEEFF')

conn = sqlite3.connect('C:/Users/user/OneDrive/Documents/PohCheongTong/Poh Cheong Tong.db')
cursor = conn.cursor()

#code for login
def login():
    '''userID = user_id_strvar.get()
    pw = password_strvar.get()
    userRole = role_strvar.get()
    
    try:
        """"conn = sqlite3.connect('F:/Documents/PohCheongTong/Poh Cheong Tong.db.db')"""
        conn = sqlite3.connect('C:/Users/user/OneDrive/Documents/PohCheongTong/Poh Cheong Tong.db')
        cursor =conn.cursor()
        cursor.execute('SELECT * FROM user WHERE role=? AND user_id =? AND password=?', [userRole, userID, pw])
        login = cursor.fetchall()            
            
    except Exception as ep:
        messagebox.showerror("Error",ep)            
    
        
    if userID == '' or pw == '' or userRole =='':
            messagebox.showerror('Login Error','You are required to fill in all the fields.')
    else:
        if login:
            messagebox.showinfo('Login Status' , 'You have successfully Logged In!')
            show_frame(page2)
            
        else:
            messagebox.showerror('Login Status', 'Invalid username or password')'''
    show_frame(page2)
        
    
                                  
user_id_strvar = tk.StringVar()
password_strvar= tk.StringVar()
role_strvar = tk.StringVar()        

bigimg = ImageTk.PhotoImage(Image.open("Logo.jpeg"))
pg1_img = Label(page1, image = bigimg)
pg1_img.place(x=300, y=280)


pg1_label = Label(page1, text='ID', font=('Arial', 30, 'bold'), bg='#DFEEFF')
pg1_label.place(x=700, y=300)

pg1_entryID = Entry(page1, font=(20), textvariable = user_id_strvar)
pg1_entryID.place(x=910, y=313)

pg1_label1 = Label(page1, text="Log In", font=('Arial', 70),bg='#DFEEFF')
pg1_label1.place(x=700, y=50)

pg1_label2 = Label(page1, text='Password', font=('Arial', 30, 'bold'),bg='#DFEEFF')
pg1_label2.place(x=700, y=400)

pg1_entryPassword = Entry(page1, font=(20), textvariable = password_strvar)
pg1_entryPassword.place(x=910, y=413)

pg1_label3 = Label(page1, text='Role', font=('Arial', 30, 'bold'),bg='#DFEEFF')
pg1_label3.place(x=700, y=500)

pg1_entryRole = Entry(page1, font=(20), textvariable = role_strvar)
pg1_entryRole.place(x=910, y=513)


pg1_button2 = Button(page1, text='Forgot Password', font=('Arial', 10, 'bold', 'underline'), bg='#DFEEFF',fg='#4BD4FF', command=lambda: show_frame(page4))
pg1_button2.place(x=976, y=610)


pg1_button = Button(page1, text='Submit', font=('Arial', 20, 'bold'), bg='#8AC1FF',fg='white', command=login)
pg1_button.place(x=976, y=550)

# ======== Page 2 (home) ===========
page2.config(background='#DFEEFF')

                             
pg2RectangleFrame=Frame(page2, bg='#492F7C', highlightbackground='white', highlightthickness=1)
pg2RectangleFrame.place(x=0,y=0, height=100,width = 1550)
    
pg2RectangleFrame2=Frame(page2, bg='#492F7C', highlightbackground='white', highlightthickness=1)
pg2RectangleFrame2.place(x=0,y=0, height=100,width = 150)


img = ImageTk.PhotoImage(Image.open("miniLogo.jpeg"))
pg2Logo = Label(page2, image = img)
pg2Logo.place(x=45, y=18)


pg2Label = Label(page2, text='Poh Cheong Tong Medical Hall System', font=('Arial', 30), fg='white', bg='#492F7C')
pg2Label.place(x=160, y=30)


# ========== Create side menu bar ==========

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


# Placing buttons in menu bar Home Page
logout_b.place(x=25, y=10, width = 100)
home_b.place(x=25, y=70, width = 100)
billing_b.place(x=25, y=130, width = 100)
inventory_b.place(x=25, y=190, width = 100)
analysis_b.place(x=25, y=250, width = 100)
register_b.place(x=25, y=310, width = 100)

# Bind to the frame, if centered or left
menuFrame.bind('<Enter>', lambda e: expandForHome())
menuFrame.bind('<Leave>', lambda e: contractForHome())

# So that Frame does not depend on the widgets inside the frame
menuFrame.grid_propagate(False)



# ======== Page 3 (Inventory) ===========
page3.config(background='#DFEEFF')

                             
pg3RectangleFrame=Frame(page3, bg='#492F7C', highlightbackground='white', highlightthickness=1)
pg3RectangleFrame.place(x=0,y=0, height=100,width = 1550)
    
pg3RectangleFrame2=Frame(page3, bg='#492F7C', highlightbackground='white', highlightthickness=1)
pg3RectangleFrame2.place(x=0,y=0, height=100,width = 150)


pg3RectangleFrame3=Frame(page3, bg='#492F7C', highlightbackground='white', highlightthickness=1)
pg3RectangleFrame3.place(x=150,y=100, height=600,width = 1390)

pg3RectangleFrame4=Frame(page3, bg='#DFEEFF', highlightbackground='white', highlightthickness=1)
pg3RectangleFrame4.place(x=150,y=700, height=120,width = 1390)




pg3Logo = Label(page3, image = img)
pg3Logo.place(x=45, y=18)


pg3Label = Label(page3, text='Poh Cheong Tong Medical Hall System', font=('Arial', 30), fg='white', bg='#492F7C')
pg3Label.place(x=160, y=30)


menuFrameInventory = Frame(page3, bg='#492F7C', width=150, height=window.winfo_height(),highlightbackground='white', highlightthickness=1 )
menuFrameInventory.place(x=0, y=100)

def expandForInventory():
    global cur_width, expanded
    cur_width += 10  # Increase the width by 10
    rep = window.after(5, expandForInventory)  # Repeat this func every 5 ms
    frame.config(width=cur_width)  # Change the width to new increase width
    if cur_width >= max_w:  # If width is greater than maximum width
        expanded = True  # Frame is expended
        window.after_cancel(rep)  # Stop repeating the function
        fillForInventory()


def contractForInventory():
    global cur_width, expanded
    cur_width -= 10  # Reduce the width by 10
    rep = window.after(5, contractForInventory)  # Call this func every 5 ms
    frame.config(width=cur_width)  # Change the width to new reduced width
    if cur_width <= min_w:  # If it is back to normal width
        expanded = False  # Frame is not expanded
        window.after_cancel(rep)  # Stop repeating the function
        fillForInventory()



def fillForInventory(): 
    if expanded:  #If the frame is expanded
        # Show the label, and remove the image
        logoutInventory_b.config(text='Log-Out', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        homeInventory_b.config(text='Home', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        billingInventory_b.config(text='Billing', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        inventoryInventory_b.config(text='Inventory', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        analysisInventory_b.config(text='Analysis', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
        registerInventory_b.config(text='Register\n New User', image='', font=('Lucida Fax', 12), fg=('#EFE2E2'))
    else:
        # Bring the image back
        logoutInventory_b.config(image=logout, font=(0, 30))
        homeInventory_b.config(image=home, font=(0, 30))
        billingInventory_b.config(image=billing, font=(0, 30))
        inventoryInventory_b.config(image=inventory, font=(0, 30))
        analysisInventory_b.config(image=analysis, font=(0, 30))
        registerInventory_b.config(image=register, font=(0, 30))
        
window.update()  # For the width to get updated

# Defining the buttons for menu bar in Inventory page
logoutInventory_b = Button(menuFrameInventory, image=logout, bg='#252B61', relief='ridge')
homeInventory_b = Button(menuFrameInventory, image=home, bg='#252B61', relief='ridge', command = lambda: show_frame(page2))
billingInventory_b = Button(menuFrameInventory, image=billing, bg='#252B61', relief='ridge')
inventoryInventory_b = Button(menuFrameInventory, image=inventory, bg='#252B61', relief='ridge', command=lambda: show_frame(page3))
analysisInventory_b = Button(menuFrameInventory, image=analysis, bg='#252B61', relief='ridge')
registerInventory_b = Button(menuFrameInventory, image=register, bg='#252B61', relief='ridge')


# Placing button in menu bar for Inventory page
logoutInventory_b.place(x=25, y=10, width = 100)
homeInventory_b.place(x=25, y=70, width = 100)
billingInventory_b.place(x=25, y=130, width = 100)
inventoryInventory_b.place(x=25, y=190, width = 100)
analysisInventory_b.place(x=25, y=250, width = 100)
registerInventory_b.place(x=25, y=310, width = 100)


# Bind to the frame, if centered or left
menuFrameInventory.bind('<Enter>', lambda e: expandForInventory())
menuFrameInventory.bind('<Leave>', lambda e: contractForInventory())

# So that it does not depend on the widgets inside the frame
menuFrameInventory.grid_propagate(False)



# ======= Create tab ==========
#widget that manages a collection of windows/displays
notebook = ttk.Notebook(pg3RectangleFrame3) 

# Create frame for tabs
tab1 = Frame(notebook, bg = '#DFEEFF') #new frame for tab 1
tab2 = Frame(notebook, bg = '#DFEEFF') #new frame for tab 2
tab3 = Frame(notebook, bg = '#DFEEFF') #new frame for tab 3

tab1.pack(fill='both', expand=True)
tab2.pack(fill='both', expand=True)
tab3.pack(fill='both', expand=True)

notebook.add(tab1,text="Manage Inventory")
notebook.add(tab2,text="Inventory Alert")
notebook.add(tab3,text="Supplier Information")

notebook.pack(expand=True,fill= "both") #expand = expand to fill any space not otherwise used
                                       #fill = fill space on x and y axis


for row in cursor.execute('SELECT * FROM user'):
    product= row[0]
    user_name = row[1]
    user_email = row[2]
    role = row[3]
    password = row[4]

def display_product_database():
    conn = sqlite3.connect('C:/Users/user/OneDrive/Documents/PohCheongTong/Poh Cheong Tong.db')
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM product")
    data = cursor.fetchall()
	
    # Add our data to the screen
    for records in data:
            ManageInventoryTree.insert('', END, values=records)
		
    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()

def display_supplier_database():
    conn = sqlite3.connect('C:/Users/user/OneDrive/Documents/PohCheongTong/Poh Cheong Tong.db')
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM supplier")
    data = cursor.fetchall()
	
    # Add our data to the screen
    for records in data:
        SupplierTree.insert('', END, values=records)
		
    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()


#manage inventory treeview
ManageInventoryTree = ttk.Treeview(tab1, selectmode="extended", show='headings',
                    columns = ('Product ID', 'Name', 'Image', 'Buy Price', 'Sell Price', 'B.code', 'Quantity', 'Min.Quantity', 'Exp.Date', 'Category ID', 'Supplier ID'))

ManageInventoryTree.place(relwidth=1.0, relheight=1.0)

x_scroller= Scrollbar(ManageInventoryTree, orient = HORIZONTAL, command =ManageInventoryTree.xview)
y_scroller= Scrollbar(ManageInventoryTree, orient = VERTICAL, command =ManageInventoryTree.yview)
x_scroller.pack(side= BOTTOM, fill=X)
y_scroller.pack(side= RIGHT, fill=Y)

ManageInventoryTree.config(yscrollcommand=y_scroller.set, xscrollcommand=x_scroller.set)

ManageInventoryTree.heading('Product ID', text = 'Product ID', anchor=CENTER)
ManageInventoryTree.heading('Name', text = 'Name', anchor=CENTER)
ManageInventoryTree.heading('Image', text = 'Image', anchor=CENTER)
ManageInventoryTree.heading('Buy Price', text = 'Buy Price', anchor=CENTER)
ManageInventoryTree.heading('Sell Price', text = 'Sell Price', anchor=CENTER)
ManageInventoryTree.heading('B.code', text = 'B.code', anchor=CENTER)
ManageInventoryTree.heading('Quantity', text = 'Quantity', anchor=CENTER)
ManageInventoryTree.heading('Min.Quantity', text = 'Min. Quantity', anchor=CENTER)
ManageInventoryTree.heading('Exp.Date', text = 'Exp. Date', anchor=CENTER)
ManageInventoryTree.heading('Category ID', text = 'Category ID', anchor=CENTER)
ManageInventoryTree.heading('Supplier ID', text = 'Supplier ID', anchor=CENTER)

ManageInventoryTree.column("Product ID", anchor=CENTER, width=100)
ManageInventoryTree.column("Name", anchor=CENTER, width=200)
ManageInventoryTree.column("Image", anchor=CENTER, width=140)
ManageInventoryTree.column("Buy Price", anchor=CENTER, width=90)
ManageInventoryTree.column("Sell Price", anchor=CENTER, width=90)
ManageInventoryTree.column("B.code", anchor=CENTER, width=140)
ManageInventoryTree.column("Quantity", anchor=CENTER, width=100)
ManageInventoryTree.column("Min.Quantity", anchor=CENTER, width=120)
ManageInventoryTree.column("Exp.Date", anchor=CENTER, width=140)
ManageInventoryTree.column("Category ID", anchor=CENTER, width=140)
ManageInventoryTree.column("Supplier ID", anchor=CENTER, width=140)

display_product_database()


#Supplier Information Treeview
SupplierTree = ttk.Treeview(tab3, selectmode="extended", show='headings',
            columns = ('Supplier ID', 'Supplier Name', 'Phone No.', 'Email', 'Company', 'Company Address'))

SupplierTree.place(relwidth=1.0, relheight=1.0)

x2_scroller= Scrollbar(SupplierTree, orient = HORIZONTAL, command =SupplierTree.xview)
y2_scroller= Scrollbar(SupplierTree, orient = VERTICAL, command =SupplierTree.yview)
x2_scroller.pack(side= BOTTOM, fill=X)
y2_scroller.pack(side= RIGHT, fill=Y)

SupplierTree.config(yscrollcommand=y2_scroller.set, xscrollcommand=x2_scroller.set)

SupplierTree.heading('Supplier ID', text = 'Supplier ID', anchor=CENTER)
SupplierTree.heading('Supplier Name', text = 'Supplier Name', anchor=CENTER)
SupplierTree.heading('Phone No.', text = 'Phone No.', anchor=CENTER)
SupplierTree.heading('Email', text = 'Email', anchor=CENTER)
SupplierTree.heading('Company', text = 'Company', anchor=CENTER)
SupplierTree.heading('Company Address', text = 'Company Address', anchor=CENTER)

SupplierTree.column("Supplier ID", anchor=CENTER, width=80)
SupplierTree.column("Supplier Name", anchor=CENTER, width=80)
SupplierTree.column("Phone No.", anchor=CENTER, width=100)
SupplierTree.column("Email", anchor=CENTER, width=120)
SupplierTree.column("Company", anchor=CENTER, width=100)
SupplierTree.column("Company Address", anchor=CENTER, width=170)

display_supplier_database()




#convert to string
pro_id_strvar = tk.StringVar()
product_name_strvar= tk.StringVar()
buy_price_strvar = tk.StringVar()
sell_price_strvar = tk.StringVar()
quantity_strvar = tk.StringVar()
min_quantity_strvar = tk.StringVar()
expiry_date_strvar = tk.StringVar()
category_strvar = tk.StringVar()
supplier_name_strvar = tk.StringVar()



#File dialog to select files
def upload_image():
    global get_image
    get_image = filedialog.askopenfilenames(title="SELECT IMAGE", filetypes=( ("png", "*.png"), ("jpg" , "*.jpg")))
    image=Image.open(get_image)
    image_resized= image.resize((200,200))
    image = ImageTk.PhotoImage(image_resized)
    display_image = Label(imageFrame, image = image)
    display_image.place(x=0, y=0)
    

'''#Image need to be convert into binary before insert into database
def convert_image_into_binary(filename):
    with open(filename, 'rb') as file:
        photo_image = file.read()
    return photo_image

def insert_image():
    image_database = sqlite3.connect("'C:/Users/user/OneDrive/Documents/PohCheongTong/Poh Cheong Tong.db')
    data = image_database.cursor()
    
    for image in get_image:
       insert_photo   = convert_image_into_binary(image)
       data.execute("INSERT INTO Image Values(:image)", 
                 {'image': insert_photo })

    image_database.commit()
    image_database.close()'''



#open window to edit inventory records
def open_edit_inventory():
    editInventoryWindow = Toplevel(window)
    editInventoryWindow.rowconfigure(0, weight=1)
    editInventoryWindow.columnconfigure(0, weight=1)
    editInventoryWindow.state('zoomed')
    editInventoryWindow.configure(bg = '#DFEEFF')
    
    


    addInventory_label = Label(editInventoryWindow, text="EDIT INVENTORY", font=('Arial', 35, 'bold'),bg='#DFEEFF')
    addInventory_label.place(x=600, y=50)
    
    productID_label = Label(editInventoryWindow, text="Product ID", font=('Arial', 18),bg='#DFEEFF')
    productID_label.place(x=200, y=115)
    productID_entry = Entry(editInventoryWindow, font=(20), textvariable = pro_id_strvar)
    productID_entry.place(x=200, y=150)
    
    productName_label = Label(editInventoryWindow, text="Product Name", font=('Arial', 18),bg='#DFEEFF')
    productName_label.place(x=200, y=200)
    productName_entry = Entry(editInventoryWindow, font=(20), textvariable = product_name_strvar)
    productName_entry.place(x=200, y=240)

    productImage_label = Label(editInventoryWindow, text="Product Image", font=('Arial', 18),bg='#DFEEFF')
    productImage_label.place(x=200, y=290)
    productImage_frame= Frame(editInventoryWindow, bg='white', highlightbackground='black', highlightthickness=1)
    productImage_frame.place(x=200, y=330, height=200,width = 200)
    chooseImage_button = Button(editInventoryWindow, text="Select Image", command=upload_image)
    chooseImage_button.place(x=200, y=550)
    
    category_label = Label(editInventoryWindow, text="Category", font=('Arial', 18),bg='#DFEEFF')
    category_label.place(x=200, y=600)
    category_entry = Entry(editInventoryWindow, font=(20), textvariable = category_strvar)
    category_entry.place(x=200, y=640)
    
    barcode_label = Label(editInventoryWindow, text="Bar Code", font=('Arial', 18),bg='#DFEEFF')
    barcode_label.place(x=700, y=115)
    barcode_frame= Frame(editInventoryWindow, bg='white', highlightbackground='black', highlightthickness=1)
    barcode_frame.place(x=700, y=150, height=200,width = 200)

    expiryDate_label = Label(editInventoryWindow, text="Expiry Date", font=('Arial', 18),bg='#DFEEFF')
    expiryDate_label.place(x=700, y=355)
    expiryDate_entry = Entry(editInventoryWindow, font=(20), textvariable = expiry_date_strvar)
    expiryDate_entry.place(x=700, y=395)

    quantity_label = Label(editInventoryWindow, text="Quantity", font=('Arial', 18),bg='#DFEEFF')
    quantity_label.place(x=700, y=445)
    quantity_entry = Entry(editInventoryWindow, font=(20), textvariable = expiry_date_strvar)
    quantity_entry.place(x=700, y=485)

    minimumQuantity_label=Label(editInventoryWindow, text="Min. Quantity", font=('Arial', 18),bg='#DFEEFF')
    minimumQuantity_label.place(x=700, y=535)
    minimumQuantity_entry = Entry(editInventoryWindow, font=(20), textvariable = min_quantity_strvar)
    minimumQuantity_entry.place(x=700, y=575)

    supplyPrice_label = Label(editInventoryWindow, text="Supply Price", font=('Arial', 18),bg='#DFEEFF')
    supplyPrice_label.place(x=1100, y=115)
    supplyPrice_entry = Entry(editInventoryWindow, font=(20), textvariable = buy_price_strvar)
    supplyPrice_entry.place(x=1100, y=155)

    sellingPrice_label = Label(editInventoryWindow, text="Selling Price", font=('Arial', 18),bg='#DFEEFF')
    sellingPrice_label.place(x=1100, y=205)
    sellingPrice_entry = Entry(editInventoryWindow, font=(20), textvariable = sell_price_strvar)
    sellingPrice_entry.place(x=1100, y=245)

    supplierName_label = Label(editInventoryWindow, text="Selling Price", font=('Arial', 18),bg='#DFEEFF')
    supplierName_label.place(x=1100, y=295)
    supplierName_entry = Entry(editInventoryWindow, font=(20), textvariable = supplier_name_strvar)
    supplierName_entry.place(x=1100, y=335)

    save_edit_button= Button(editInventoryWindow, text= "SAVE", font=('Arial', 15, 'bold'),command = open_add_inventory)
    save_edit_button.place(x=1100, y=385, height = 40, width = 220)

    cancel_edit_button= Button(editInventoryWindow, text= "CANCEL", font=('Arial', 15, 'bold'),command = open_add_inventory)
    cancel_edit_button.place(x=1100, y=435, height = 40, width = 220)

    


    
        
    

    editInventoryWindow.mainloop()
    


#open window to add inventory records
def open_add_inventory():
    addInventoryWindow = Toplevel(window)
    addInventoryWindow.mainloop()

        
# Remove inventory records
def remove_inventory():
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

		# Delete From Treeview
                for record in x:
                    ManageInventoryTree.delete(record)

		# Create a database or connect to one that exists
                conn = sqlite3.connect('C:/Users/user/OneDrive/Documents/PohCheongTong/Poh Cheong Tong.db')

		# Create a cursor instance
                c = conn.cursor()
		

		# Delete Everything From The Table
                c.executemany("DELETE FROM product WHERE pro_id = ?", [(a,) for a in ids_to_delete])
		

		# Reset List
                ids_to_delete = []


		# Commit changes
                conn.commit()

		# Close our connection
                conn.close()
		
		#for fun
                messagebox.showinfo('Status' , 'You have successfully deleted the items!')

                '''# Clear entry boxes if filled
                clear_entries()'''

'''# Select Record
def select_record(e):
	# Clear entry boxes
	fn_entry.delete(0, END)
	ln_entry.delete(0, END)
	id_entry.delete(0, END)
	address_entry.delete(0, END)
	city_entry.delete(0, END)
	state_entry.delete(0, END)
	zipcode_entry.delete(0, END)

	# Grab record Number
	selected = ManageInventoryTree.focus()
	# Grab record values
	values = ManageInventoryTree.item(selected, 'values')

	# outpus to entry boxes
	fn_entry.insert(0, values[0])
	ln_entry.insert(0, values[1])
	id_entry.insert(0, values[2])
	address_entry.insert(0, values[3])
	city_entry.insert(0, values[4])
	state_entry.insert(0, values[5])
	zipcode_entry.insert(0, values[6])'''


'''# Update inventory records
def update_record():
	# Grab the record number
	selected = ManageInventoryTree.focus()
	# Update record
	ManageInventoryTree.item(selected, text="", values=(fn_entry.get(), ln_entry.get(), id_entry.get(), address_entry.get(), city_entry.get(), state_entry.get(), zipcode_entry.get(),))

	# Create a database or connect to one that exists
	conn = sqlite3.connect('C:/Users/user/OneDrive/Documents/PohCheongTong/Poh Cheong Tong.db')

	# Create a cursor instance
	c = conn.cursor()
	
	# Update the database
	c.execute("""UPDATE product SET
		first_name = :first,
		last_name = :last,
		address = :address,
		city = :city,
		state = :state,
		zipcode = :zipcode

		WHERE oid = :oid""",
		{
			'first': fn_entry.get(),
			'last': ln_entry.get(),
			'address': address_entry.get(),
			'city': city_entry.get(),
			'state': state_entry.get(),
			'zipcode': zipcode_entry.get(),
			'oid': id_entry.get(),
		})
	


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()


	# Clear entry boxes
	fn_entry.delete(0, END)
	ln_entry.delete(0, END)
	id_entry.delete(0, END)
	address_entry.delete(0, END)
	city_entry.delete(0, END)
	state_entry.delete(0, END)
	zipcode_entry.delete(0, END)'''



















tab1_add_button= Button(pg3RectangleFrame4, text= "ADD", font=('Arial', 15, 'bold'),command = open_add_inventory)
tab1_add_button.place(x=600, y=20)


tab1_edit_button= Button(pg3RectangleFrame4, text= "EDIT", font=('Arial', 15, 'bold'),command = open_edit_inventory)
tab1_edit_button.place(x=600, y=20)

tab1_delete_button= Button(pg3RectangleFrame4, text= "DELETE", font=('Arial', 15, 'bold'),command = remove_inventory)
tab1_delete_button.place(x=500, y=20)


#======== Page 4=============
page4.config(background='gray')
pag4_label = Label(page4, text='WELCOME TO PAGE 4', font=('Arial', 30, 'bold'))
pag4_label.place(x=50, y=100)

pg4_button = Button(page4, text='NEXT', font=('Arial', 13, 'bold'), command=lambda: show_frame(page1))
pg4_button.place(x=190, y=400)
#====== start program ======
window.mainloop()
