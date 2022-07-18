import sqlite3
import tkinter as tk
import tkinter.messagebox
from _datetime import datetime
from tkinter import *
from tkinter import ttk
import ttkwidgets.autocomplete
from PIL import Image, ImageTk
from fpdf import FPDF
import pandas as pd

window = tk.Tk()
window.title("Poh Cheong Tong Medical Hall System")
window.configure(bg='#DFEEFF')
window.state('zoomed')

page1 = Frame(window)  # Log-in
page2 = Frame(window)  # Home
page3 = Frame(window)  # Inventory
page4 = Frame(window)  # Billing
page5 = Frame(window)  # Analysis

for screen in (page1, page2, page3, page4, page5):
    screen.grid(row=0, column=0, sticky='nsew')


def show_frame(frame):
    frame.tkraise()


show_frame(page4)

# === Connect Database ===
conn = sqlite3.connect('Poh Cheong Tong.db')
cur = conn.cursor()

# =============================================== Page 4 Billing Page ==============================================
page4.update()
# ========== Add heading and frame ==========

Frame(window, bg='#492F7C', highlightbackground='white', highlightthickness=1, width=window.winfo_width(),
      height=100).place(x=0, y=0)

Frame(window, bg='#DFEEFF', highlightbackground='white', highlightthickness=1, width=1385,
      height=730).place(x=150, y=100)

logo = ImageTk.PhotoImage(Image.open('Logo.png').resize((50, 50), resample=Image.LANCZOS))
Label(window, image=logo, bg='#492F7C').place(x=45, y=18)

Label(window, text='Billing', font=('Arial', 30), fg='white', bg='#492F7C', justify='center').place(x=160,
                                                                                                    y=20)

# ========== Create site menu bar ==========

min_w = 145  # Minimum width of the frame
max_w = 145  # Maximum width of the frame
cur_width = min_w  # Increasing width of the frame
expanded = False  # Check if it is completely expanded


def expand():
    global cur_width, expanded
    cur_width += 0  # Increase the width by 0
    rep = page4.after(5, expand)  # Repeat this func every 5 ms
    frame.config(width=cur_width)  # Change the width to new increase width
    if cur_width >= max_w:  # If width is greater than maximum width
        expanded = True  # Frame is expended
        page4.after_cancel(rep)  # Stop repeating the function
        fill()


def contract():
    global cur_width, expanded
    cur_width -= 0  # Reduce the width by 0
    rep = page4.after(5, contract)  # Call this func every 5 ms
    frame.config(width=cur_width)  # Change the width to new reduced width
    if cur_width <= min_w:  # If it is back to normal width
        expanded = False  # Frame is not expanded
        page4.after_cancel(rep)  # Stop repeating the function
        fill()


def fill():
    if expanded:  # If the frame is expanded
        # Show the label, and remove the image
        logout_b.config(text='Log-Out', image='', font=('Lucida Fax', 12), fg='#EFE2E2')
        home_b.config(text='Home', image='', font=('Lucida Fax', 12), fg='#EFE2E2')
        billing_b.config(text='Billing', image='', font=('Lucida Fax', 12), fg='#EFE2E2')
        inventory_b.config(text='Inventory', image='', font=('Lucida Fax', 12), fg='#EFE2E2')
        analysis_b.config(text='Analysis', image='', font=('Lucida Fax', 12), fg='#EFE2E2')
        register_b.config(text='Register\n New User', image='', font=('Lucida Fax', 12), fg='#EFE2E2')
    else:
        # Bring the image back
        logout_b.config(image=logout, font=(0, 30))
        home_b.config(image=home, font=(0, 30))
        billing_b.config(image=billing, font=(0, 30))
        inventory_b.config(image=inventory, font=(0, 30))
        analysis_b.config(image=analysis, font=(0, 30))
        register_b.config(image=register, font=(0, 30))


# Define and resize the icons to be shown in Menu bar
logout = ImageTk.PhotoImage(Image.open('Logout.png').resize((40, 40), resample=Image.LANCZOS))
home = ImageTk.PhotoImage(Image.open('Home.png').resize((40, 40), resample=Image.LANCZOS))
billing = ImageTk.PhotoImage(Image.open('Bill.png').resize((40, 40), resample=Image.LANCZOS))
inventory = ImageTk.PhotoImage(Image.open('Inventory.png').resize((40, 40), resample=Image.LANCZOS))
analysis = ImageTk.PhotoImage(Image.open('Analysis.png').resize((40, 40), resample=Image.LANCZOS))
register = ImageTk.PhotoImage(Image.open('Register.png').resize((40, 40), resample=Image.LANCZOS))

page4.update()  # For the width to get updated

frame = Frame(window, bg='#492F7C', width=150, height=window.winfo_height(), highlightbackground='white',
              highlightthickness=1)
frame.place(x=0, y=100)

# Defining the buttons for menu bar in Home page
logout_b = Button(frame, image=logout, bg='#252B61', relief='ridge')
home_b = Button(frame, image=home, bg='#252B61', relief='ridge')
billing_b = Button(frame, image=billing, bg='#252B61', relief='ridge', command=lambda: show_frame(page3))
inventory_b = Button(frame, image=inventory, bg='#252B61', relief='ridge', command=lambda: show_frame(page3))
analysis_b = Button(frame, image=analysis, bg='#252B61', relief='ridge')
register_b = Button(frame, image=register, bg='#252B61', relief='ridge')

# Placing button in menu bar
logout_b.place(x=25, y=10, width=100)
home_b.place(x=25, y=70, width=100)
billing_b.place(x=25, y=130, width=100)
inventory_b.place(x=25, y=190, width=100)
analysis_b.place(x=25, y=250, width=100)
register_b.place(x=25, y=310, width=100)

# Bind to the frame, if centered or left
frame.bind('<Enter>', lambda e: expand())
frame.bind('<Leave>', lambda e: contract())

# So that it does not depend on the widgets inside the frame
frame.pack_propagate(False)

# ====================== Manage Invoice ====================
# Frame for tree view
treeFrame = Frame(window, bg='#DFEEFF', width=1350, height=750)
treeFrame.place(x=150, y=105)


# Display table from database
def displayInvoice():
    conn = sqlite3.connect("Poh Cheong Tong.db")
    cur = conn.cursor()
    cur.execute("SELECT invoice_id, date, total FROM invoice GROUP BY invoice_id")
    rows = cur.fetchall()
    for row in rows:  # loop to display all the invoice
        ManageInvoice.insert("", END, values=row)


# Create tree view for Manage Invoice
ManageInvoice = ttk.Treeview(treeFrame, selectmode="extended", show='headings',
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
    """
    def clicktranstable():
        cur = order_tabel.selection()  # select row from the table
        cur = order_tabel.item(cur)
        selc_item = cur['values']  # get the valus of the row
        print(selc_item)
        if len(selc_item) == 7:
            itemID.set((selc_item[1]))
            itemName.set((selc_item[2]))
            # get the price and quantity of selected item with product id
            cur.execute("select sell_price,quantity from product where pro_id=?", (selc_item[1],))
            selc_item = cur.fetchall()
            itemPrice.set(selc_item[0][0])
            itemQuantity.set(selc_item[0][1] - qty_id[itemID.get()]) """

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
        if tkinter.messagebox.askyesno('Close?', 'Are you sure want to quit this window?') == True:
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
add_button = tk.Button(window, text="+ Add", font=('Helvetica Neue', 12), width=10, height=1, relief='raised',
                       command=createInvoice)
add_button.place(x=625, y=700)

# Delete Invoice Button
delete_button = tk.Button(window, text="Delete", font=('Helvetica Neue', 12), width=10, height=1,
                          command=deleteInvoice)
delete_button.place(x=875, y=700)

# View Invoice button
download_button = tk.Button(window, text="Download\nInvoice", font=('Helvetica Neue', 12), width=10, height=2, relief='raised', command=click)
download_button.place(x=750, y=695)

window.mainloop()
