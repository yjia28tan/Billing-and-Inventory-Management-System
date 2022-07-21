import sqlite3
conn = sqlite3.connect("Poh Cheong Tong.db")
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import pandas as pd  # For data manipulation and analysis
import numpy as np  # For numerical
import matplotlib.pyplot as plt  # Built-in Matplotlib
import seaborn as sns  # For graphical
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import datetime
from datetime import timedelta
from tkcalendar import Calendar, DateEntry
import re
from tkinter import messagebox
#function to connect to database




def open_analysis():

    analysis_window = Tk()
    analysis_window.state("zoomed")
    analysis_window.title("Poh Cheong Tong Medical Hall System")
    analysis_window.configure(bg='#DFEEFF')


    def MouseScrollWheel(event):
        scrollbar.yview("scroll", event.delta, "units")
        return "break"

    # Current Date Chart that show when open sales report
    def bar():
        # Current date and time
        date = datetime.now()
        year_choose = date.strftime('%Y')
        month_choose = date.strftime('%m')
        day_choose = date.strftime('%d')
        # Get data from database
        Bar_Month_Select = pd.read_sql_query("SELECT i.total AS 'Revenue', SUM((p.sell_price - p.buy_price)*i.quantity) AS "
                                             "'Profit' FROM invoice i, product p WHERE i.pro_id = p.pro_id AND strftime("
                                             "'%Y', i.date) = '{}' AND strftime('%m', i.date) = '{}' AND strftime('%d', "
                                             "i.date) = '{}' GROUP BY invoice_id".format(year_choose, month_choose,
                                                                                         day_choose), conn)
        # Change to float
        Bar_Month_Select["Profit"] = Bar_Month_Select["Profit"].astype(float)
        Bar_Month_Select["Revenue"] = Bar_Month_Select["Revenue"].astype(float)
        # Sum up the data value
        Bar_Month_s = Bar_Month_Select['Revenue'].sum()
        Bar_m_s = Bar_Month_Select['Profit'].sum()
        # Set to two decimal place
        R = '{:.2f}'.format(Bar_Month_s)
        P = '{:.2f}'.format(Bar_m_s)
        previous_day = int(day_choose) - 1
        Bar_PMonth_Select = pd.read_sql_query("SELECT i.total AS 'Revenue', SUM((p.sell_price - p.buy_price)*i.quantity) AS"
                                              " 'Profit' FROM invoice i, product p WHERE i.pro_id = p.pro_id AND strftime("
                                              "'%Y', i.date) = '{}' AND strftime('%m', i.date) = '{}' AND strftime('%d', "
                                              "i.date) = '{}' GROUP BY invoice_id".format(year_choose, month_choose,
                                                                                          previous_day), conn)
        Bar_PMonth_Select["Profit"] = Bar_PMonth_Select["Profit"].astype(float)
        Bar_PMonth_Select["Revenue"] = Bar_PMonth_Select["Revenue"].astype(float)
        Bar_PMonth_s = Bar_PMonth_Select['Revenue'].sum()
        Bar_Pm_s = Bar_PMonth_Select['Profit'].sum()
        PR = '{:.2f}'.format(Bar_PMonth_s)
        PP = '{:.2f}'.format(Bar_Pm_s)
        # Form data frame
        data = {'Day': {0: previous_day, 1: int(day_choose)}, 'Revenue': {0: PR, 1: R}, 'Profit': {0: PP, 1: P}}
        b_m_s = pd.DataFrame(data)
        dfl = (b_m_s.melt(id_vars='Day', var_name='Sales', value_name='RM').sort_values('RM', ascending=True)
               .reset_index(drop=True).sort_values('Day', ascending=True))
        dfl['RM'] = dfl['RM'].astype(str).astype(float)
        # Plot bar chart
        fig, ax = plt.subplots(figsize=(9, 6), dpi=100)
        plot = sns.barplot(x='Day', y='RM', data=dfl, hue='Sales', palette="Pastel1", ci=None)
        for c in ax.containers:
            ax.bar_label(c, fmt='%.2f')
        plot.set_ylabel("RM", fontsize=15)
        plot.set_xlabel("Day", fontsize=15)
        plot.set_title("Revenue and Profit Bar Chart in Day", fontsize=21)
        # Convert chart to figure
        canv = FigureCanvasTkAgg(fig, master=scroll_frame)
        canv.draw()
        canv.get_tk_widget().pack(padx=380, pady=100)
        # Add toolbar for the chart
        toolba = NavigationToolbar2Tk(canv, scroll_frame)
        toolba.update()
        toolba.place(x=680, y=780)


    # Pie Product Sold Day
    def pie_product():
        date = datetime.now()
        year_choose = date.strftime('%Y')
        month_choose = date.strftime('%m')
        day_choose = date.strftime('%d')
        Sold_Day = pd.read_sql_query("SELECT p.product_name AS 'Product Name', sum(i.quantity) AS 'Quantity' FROM "
                                     "invoice i JOIN product p ON p.pro_id = i.pro_id WHERE strftime('%Y', i.date) IN "
                                     "('{}') AND strftime('%m', i.date) IN ('{}') AND strftime('%d', i.date) IN ('{}') "
                                     "GROUP BY i.pro_id".format(year_choose, month_choose, day_choose), conn)
        datframe = pd.DataFrame(Sold_Day)
        sold_day_pro = datframe['Product Name'].values.tolist()
        sold_day_quan = datframe['Quantity'].values.tolist()
        colors = sns.color_palette("Pastel1")
        pie_product_day = plt.figure(figsize=(5, 5), dpi=100)
        plt.pie(sold_day_quan, labels=sold_day_pro, autopct='%1.1f%%', colors=colors)
        plt.title("Product Sold in Day", fontsize=18)
        can = FigureCanvasTkAgg(pie_product_day, master=scroll_frame)
        can.draw()
        can.get_tk_widget().pack(padx=180, pady=100)
        toolb = NavigationToolbar2Tk(can, scroll_frame)
        toolb.update()
        toolb.place(x=650, y=1480)


    # Pie Category Sold
    def pie_category():
        date = datetime.now()
        year_choose = date.strftime('%Y')
        month_choose = date.strftime('%m')
        day_choose = date.strftime('%d')
        Sold_Cat_Day = pd.read_sql_query("SELECT c.cat_name AS 'Category', SUM(i.quantity) AS 'Quantity' FROM category "
                                         "c, invoice i, product p WHERE i.pro_id = p.pro_id AND p.cat_id = c.cat_id AND"
                                         " strftime('%Y', i.date) IN ('{}') AND strftime('%m', i.date) IN ('{}') AND "
                                         "strftime('%d', i.date) IN ('{}') GROUP BY c.cat_id"
                                         .format(year_choose, month_choose, day_choose), conn)
        datafram = pd.DataFrame(Sold_Cat_Day)
        sold_cat_day = datafram['Category'].values.tolist()
        sold_cat_day_quan = datafram['Quantity'].values.tolist()
        colors = sns.color_palette("Pastel1")
        pie_category_day = plt.figure(figsize=(5, 5), dpi=100)
        plt.pie(sold_cat_day_quan, labels=sold_cat_day, autopct='%1.1f%%', colors=colors)
        plt.title("Product Sold in Category in Day", fontsize=18)
        ca = FigureCanvasTkAgg(pie_category_day, master=scroll_frame)
        ca.draw()
        ca.get_tk_widget().pack(padx=180, pady=100)
        tool = NavigationToolbar2Tk(ca, scroll_frame)
        tool.update()
        tool.place(x=650, y=2165)


    def sort_year():
        def sales_year():
            # Clear anything that on the frame
            for widget in scroll_frame.winfo_children():
                widget.destroy()
            year_choose = year_chosen.get()
            # Sales Bar Year
            Bar_Month_Select = pd.read_sql_query("SELECT i.total AS 'Revenue', SUM((p.sell_price - p.buy_price)*i.quantity)"
                                                 " AS 'Profit' FROM invoice i, product p WHERE i.pro_id = p.pro_id AND "
                                                 "strftime ('%Y', i.date) = '{}' GROUP BY invoice_id".format(year_choose),
                                                 conn)
            Bar_Month_Select["Profit"] = Bar_Month_Select["Profit"].astype(float)
            Bar_Month_Select["Revenue"] = Bar_Month_Select["Revenue"].astype(float)
            Bar_Month_s = Bar_Month_Select['Revenue'].sum()
            Bar_m_s = Bar_Month_Select['Profit'].sum()
            R = '{:.2f}'.format(Bar_Month_s)
            P = '{:.2f}'.format(Bar_m_s)
            Bar_PMonth_Select = pd.read_sql_query("SELECT i.total AS 'Revenue', SUM((p.sell_price - p.buy_price)*"
                                                  "i.quantity) AS 'Profit' FROM invoice i, product p WHERE i.pro_id = "
                                                  "p.pro_id AND strftime ('%Y', i.date) = '{}' GROUP BY invoice_id".format
                                                  (int(year_choose) - 1), conn)
            Bar_PMonth_Select["Profit"] = Bar_PMonth_Select["Profit"].astype(float)
            Bar_PMonth_Select["Revenue"] = Bar_PMonth_Select["Revenue"].astype(float)
            Bar_PMonth_s = Bar_PMonth_Select['Revenue'].sum()
            Bar_Pm_s = Bar_PMonth_Select['Profit'].sum()
            PR = '{:.2f}'.format(Bar_PMonth_s)
            PP = '{:.2f}'.format(Bar_Pm_s)
            data = {'Year': {0: int(year_choose) - 1, 1: int(year_choose)}, 'Revenue': {0: PR, 1: R},
                    'Profit': {0: PP, 1: P}}
            b_m_s = pd.DataFrame(data)
            dfl = (b_m_s.melt(id_vars='Year', var_name='Sales', value_name='RM').sort_values('RM', ascending=False).
                   reset_index(drop=True).sort_values('Year', ascending=True))
            dfl['RM'] = dfl['RM'].astype(str).astype(float)
            fig, ax = plt.subplots(figsize=(9, 6), dpi=100)
            plot = sns.barplot(x='Year', y='RM', data=dfl, hue='Sales', palette="Pastel1", ci=None)
            for c in ax.containers:
                plot.bar_label(c, fmt='%.2f')
            plot.set_ylabel("RM", fontsize=15)
            plot.set_xlabel("Year", fontsize=15)
            plot.set_title("Revenue and Profit Bar Chart in Year", fontsize=21)
            canv = FigureCanvasTkAgg(fig, master=scroll_frame)
            canv.draw()
            canv.get_tk_widget().pack(padx=380, pady=100)
            toolba = NavigationToolbar2Tk(canv, scroll_frame)
            toolba.update()
            toolba.place(x=680, y=780)
            # Pie Product Sold Year
            Sold_Year = pd.read_sql_query("SELECT p.product_name AS 'Product Name', sum(i.quantity) AS 'Quantity' FROM "
                                          "invoice i JOIN product p ON p.pro_id = i.pro_id WHERE strftime('%Y', i.date) IN "
                                          "('{}') GROUP BY i.pro_id".format(year_choose), conn)
            dframe = pd.DataFrame(Sold_Year)
            sold_year_pro = dframe['Product Name'].values.tolist()
            sold_year_quan = dframe['Quantity'].values.tolist()
            colors = sns.color_palette("Pastel1")
            pie_product_year = plt.figure(figsize=(5, 5), dpi=100)
            plt.pie(sold_year_quan, labels=sold_year_pro, autopct='%1.1f%%', colors=colors)
            plt.title("Product Sold in Year", fontsize=18)
            can = FigureCanvasTkAgg(pie_product_year, master=scroll_frame)
            can.draw()
            can.get_tk_widget().pack(padx=180, pady=100)
            toolb = NavigationToolbar2Tk(can, scroll_frame)
            toolb.update()
            toolb.place(x=650, y=1480)
            # Pie Category Sold Year
            Sold_Cat_Year = pd.read_sql_query("SELECT c.cat_name AS 'Category', SUM(i.quantity) AS 'Quantity' FROM category"
                                              " c, invoice i, product p WHERE i.pro_id = p.pro_id AND p.cat_id = c.cat_id "
                                              "AND strftime('%Y', i.date) IN ('{}') GROUP BY c.cat_id".format(year_choose),
                                              conn)
            datafr = pd.DataFrame(Sold_Cat_Year)
            sold_cat_year = datafr['Category'].values.tolist()
            sold_cat_year_quan = datafr['Quantity'].values.tolist()
            colors = sns.color_palette("Pastel1")
            pie_category_year = plt.figure(figsize=(5, 5), dpi=100)
            plt.pie(sold_cat_year_quan, labels=sold_cat_year, autopct='%1.1f%%', colors=colors)
            plt.title("Product Sold in Category in Year", fontsize=18)
            ca = FigureCanvasTkAgg(pie_category_year, master=scroll_frame)
            ca.draw()
            ca.get_tk_widget().pack(padx=180, pady=100)
            tool = NavigationToolbar2Tk(ca, scroll_frame)
            tool.update()
            tool.place(x=650, y=2165)
            # Destroy the pop up window
            year_window.destroy()

        # Create pop up window
        year_window = Toplevel(analysis_window)
        year_window.geometry("450x225")
        year_window.title("Sales Report in Year")
        year_window.configure(bg='#DFEEFF')
        year_label = Label(year_window, text='Choose a year', font=('Arial', 15), bg='#DFEEFF')
        year_label.pack(pady=20)
        # Get list value from database
        year_value = pd.read_sql_query("SELECT strftime('%Y', date) AS Year FROM invoice GROUP BY strftime('%Y', date)",
                                       conn)
        year_df = pd.DataFrame(year_value)
        year_list = year_df['Year'].values.tolist()
        year_chosen = ttk.Combobox(year_window, width=27, values=year_list, font=('Arial', 12))
        year_chosen.set(datetime.now().year)
        year_chosen.pack(pady=10)
        Button(year_window, text='Confirm', font=('Arial', 15), command=sales_year).pack(pady=20)


    def sort_month():
        def sales_month():
            for widget in scroll_frame.winfo_children():
                widget.destroy()
            year_choose = year_chosen.get()
            month_choose = month_chosen.get()
            # Sales Bar Month
            Bar_Month_Select = pd.read_sql_query("SELECT i.total AS 'Revenue', SUM((p.sell_price - p.buy_price)*i.quantity)"
                                                 " AS 'Profit' FROM invoice i, product p WHERE i.pro_id = p.pro_id AND "
                                                 "strftime('%Y', i.date) = '{}' AND strftime('%m', i.date) = '{}' GROUP "
                                                 "BY invoice_id".format(year_choose, month_choose), conn)
            Bar_Month_Select["Profit"] = Bar_Month_Select["Profit"].astype(float)
            Bar_Month_Select["Revenue"] = Bar_Month_Select["Revenue"].astype(float)
            Bar_Month_s = Bar_Month_Select['Revenue'].sum()
            Bar_m_s = Bar_Month_Select['Profit'].sum()
            R = '{:.2f}'.format(Bar_Month_s)
            P = '{:.2f}'.format(Bar_m_s)
            index = month_list.index(month_choose) - 1
            Bar_PMonth_Select = pd.read_sql_query("SELECT i.total AS 'Revenue', SUM((p.sell_price - p.buy_price)*"
                                                  "i.quantity) AS 'Profit' FROM invoice i, product p WHERE i.pro_id = "
                                                  "p.pro_id AND strftime('%Y', i.date) = '{}' AND strftime('%m', i.date) = "
                                                  "'{}' GROUP BY invoice_id".format(year_choose, month_list[index]), conn)
            Bar_PMonth_Select["Profit"] = Bar_PMonth_Select["Profit"].astype(float)
            Bar_PMonth_Select["Revenue"] = Bar_PMonth_Select["Revenue"].astype(float)
            Bar_PMonth_s = Bar_PMonth_Select['Revenue'].sum()
            Bar_Pm_s = Bar_PMonth_Select['Profit'].sum()
            PR = '{:.2f}'.format(Bar_PMonth_s)
            PP = '{:.2f}'.format(Bar_Pm_s)
            data = {'Month': {0: month_list[index], 1: month_choose}, 'Revenue': {0: PR, 1: R}, 'Profit': {0: PP, 1: P}}
            b_m_s = pd.DataFrame(data)
            dfl = (b_m_s.melt(id_vars='Month', var_name='Sales', value_name='RM').sort_values('RM', ascending=True)
                   .reset_index(drop=True).sort_values('Month', ascending=True))
            dfl['RM'] = dfl['RM'].astype(str).astype(float)
            fig, ax = plt.subplots(figsize=(9, 6), dpi=100)
            plot = sns.barplot(x='Month', y='RM', data=dfl, hue='Sales', palette="Pastel1", ci=None)
            for c in ax.containers:
                ax.bar_label(c, fmt='%.2f')
            plot.set_ylabel("RM", fontsize=15)
            plot.set_xlabel("Month", fontsize=15)
            plot.set_title("Revenue and Profit Bar Chart in Month", fontsize=21)
            canv = FigureCanvasTkAgg(fig, master=scroll_frame)
            canv.draw()
            canv.get_tk_widget().pack(padx=380, pady=100)
            toolba = NavigationToolbar2Tk(canv, scroll_frame)
            toolba.update()
            toolba.place(x=680, y=780)
            # Pie Product Sold Month
            Sold_Month = pd.read_sql_query("SELECT p.product_name AS 'Product Name', sum(i.quantity) AS 'Quantity' FROM "
                                           "invoice i JOIN product p ON p.pro_id = i.pro_id WHERE strftime('%Y', i.date) IN"
                                           " ('{}') AND strftime('%m', i.date) IN ('{}') GROUP BY i.pro_id".format
                                           (year_choose, month_choose), conn)
            daframe = pd.DataFrame(Sold_Month)
            sold_month_pro = daframe['Product Name'].values.tolist()
            sold_month_quan = daframe['Quantity'].values.tolist()
            colors = sns.color_palette("Pastel1")
            pie_product_month = plt.figure(figsize=(5, 5), dpi=100)
            plt.pie(sold_month_quan, labels=sold_month_pro, autopct='%1.1f%%', colors=colors)
            plt.title("Product Sold in Month", fontsize=18)
            can = FigureCanvasTkAgg(pie_product_month, master=scroll_frame)
            can.draw()
            can.get_tk_widget().pack(padx=180, pady=100)
            toolb = NavigationToolbar2Tk(can, scroll_frame)
            toolb.update()
            toolb.place(x=650, y=1480)
            # Pie Category Sold Month
            Sold_Cat_Month = pd.read_sql_query("SELECT c.cat_name AS 'Category', SUM(i.quantity) AS 'Quantity' FROM "
                                               "category c, invoice i, product p WHERE i.pro_id = p.pro_id AND p.cat_id = "
                                               "c.cat_id AND strftime('%Y', i.date) IN ('{}') AND strftime('%m', i.date) IN"
                                               " ('{}') GROUP BY c.cat_id".format(year_choose, month_choose), conn)
            datafra = pd.DataFrame(Sold_Cat_Month)
            sold_cat_month = datafra['Category'].values.tolist()
            sold_cat_month_quan = datafra['Quantity'].values.tolist()
            colors = sns.color_palette("Pastel1")
            pie_category_month = plt.figure(figsize=(5, 5), dpi=100)
            plt.pie(sold_cat_month_quan, labels=sold_cat_month, autopct='%1.1f%%', colors=colors)
            plt.title("Product Sold in Category in Month", fontsize=18)
            ca = FigureCanvasTkAgg(pie_category_month, master=scroll_frame)
            ca.draw()
            ca.get_tk_widget().pack(padx=180, pady=100)
            tool = NavigationToolbar2Tk(ca, scroll_frame)
            tool.update()
            tool.place(x=650, y=2165)
            month_window.destroy()

        month_window = Toplevel(analysis_window)
        month_window.geometry("450x225")
        month_window.title("Sales Report in Month")
        month_window.configure(bg='#DFEEFF')
        month_label = Label(month_window, text='Choose a year and a month', font=('Arial', 15), bg='#DFEEFF')
        month_label.pack(pady=20)
        year_value = pd.read_sql_query("SELECT strftime('%Y', date) AS Year FROM invoice GROUP BY strftime('%Y', date)",
                                       conn)
        year_df = pd.DataFrame(year_value)
        year_list = year_df['Year'].values.tolist()
        year_chosen = ttk.Combobox(month_window, width=27, values=year_list, font=('Arial', 12))
        year_chosen.set(datetime.now().year)
        year_chosen.pack(pady=10)
        month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        month_chosen = ttk.Combobox(month_window, width=27, values=month_list, font=('Arial', 12))
        month_chosen.set('0' + str(datetime.now().month))
        month_chosen.pack()
        Button(month_window, text='Confirm', font=('Arial', 15), command=sales_month).pack(pady=20)


    def sort_day():
        def sales_day():
            for widget in scroll_frame.winfo_children():
                widget.destroy()
            date_chosen = calendar.get_date()
            year_choose = date_chosen.strftime('%Y')
            month_choose = date_chosen.strftime('%m')
            day_choose = date_chosen.strftime('%d')
            # Sales Bar Day
            Bar_Month_Select = pd.read_sql_query("SELECT i.total AS 'Revenue', SUM((p.sell_price - p.buy_price)*i.quantity)"
                                                 " AS 'Profit' FROM invoice i, product p WHERE i.pro_id = p.pro_id AND "
                                                 "strftime('%Y', i.date) = '{}' AND strftime('%m', i.date) = '{}' AND "
                                                 "strftime('%d', i.date) = '{}' GROUP BY invoice_id".format
                                                 (year_choose, month_choose, day_choose), conn)
            Bar_Month_Select["Profit"] = Bar_Month_Select["Profit"].astype(float)
            Bar_Month_Select["Revenue"] = Bar_Month_Select["Revenue"].astype(float)
            Bar_Month_s = Bar_Month_Select['Revenue'].sum()
            Bar_m_s = Bar_Month_Select['Profit'].sum()
            R = '{:.2f}'.format(Bar_Month_s)
            P = '{:.2f}'.format(Bar_m_s)
            previous_day = int(day_choose) - 1
            Bar_PMonth_Select = pd.read_sql_query("SELECT i.total AS 'Revenue', SUM((p.sell_price - p.buy_price)*"
                                                  "i.quantity) AS 'Profit' FROM invoice i, product p WHERE i.pro_id = "
                                                  "p.pro_id AND strftime('%Y', i.date) = '{}' AND strftime('%m', i.date) = "
                                                  "'{}' AND strftime('%d', i.date) = '{}' GROUP BY invoice_id".format
                                                  (year_choose, month_choose, previous_day), conn)
            Bar_PMonth_Select["Profit"] = Bar_PMonth_Select["Profit"].astype(float)
            Bar_PMonth_Select["Revenue"] = Bar_PMonth_Select["Revenue"].astype(float)
            Bar_PMonth_s = Bar_PMonth_Select['Revenue'].sum()
            Bar_Pm_s = Bar_PMonth_Select['Profit'].sum()
            PR = '{:.2f}'.format(Bar_PMonth_s)
            PP = '{:.2f}'.format(Bar_Pm_s)
            data = {'Day': {0: previous_day, 1: int(day_choose)}, 'Revenue': {0: PR, 1: R}, 'Profit': {0: PP, 1: P}}
            b_m_s = pd.DataFrame(data)
            dfl = (b_m_s.melt(id_vars='Day', var_name='Sales', value_name='RM').sort_values('RM', ascending=True)
                   .reset_index(drop=True).sort_values('Day', ascending=True))
            dfl['RM'] = dfl['RM'].astype(str).astype(float)
            fig, ax = plt.subplots(figsize=(9, 6), dpi=100)
            plot = sns.barplot(x='Day', y='RM', data=dfl, hue='Sales', palette="Pastel1", ci=None)
            for c in ax.containers:
                ax.bar_label(c, fmt='%.2f')
            plot.set_ylabel("RM", fontsize=15)
            plot.set_xlabel("Day", fontsize=15)
            plot.set_title("Revenue and Profit Bar Chart in Day", fontsize=21)
            canv = FigureCanvasTkAgg(fig, master=scroll_frame)
            canv.draw()
            canv.get_tk_widget().pack(padx=380, pady=100)
            toolba = NavigationToolbar2Tk(canv, scroll_frame)
            toolba.update()
            toolba.place(x=680, y=780)
            # Pie Product Sold Day
            Sold_Day = pd.read_sql_query("SELECT p.product_name AS 'Product Name', sum(i.quantity) AS 'Quantity' FROM "
                                         "invoice i JOIN product p ON p.pro_id = i.pro_id WHERE strftime('%Y', i.date) IN "
                                         "('{}') AND strftime('%m', i.date) IN ('{}') AND strftime('%d', i.date) IN ('{}') "
                                         "GROUP BY i.pro_id".format(year_choose, month_choose, day_choose), conn)
            datframe = pd.DataFrame(Sold_Day)
            sold_day_pro = datframe['Product Name'].values.tolist()
            sold_day_quan = datframe['Quantity'].values.tolist()
            colors = sns.color_palette("Pastel1")
            pie_product_day = plt.figure(figsize=(5, 5), dpi=100)
            plt.pie(sold_day_quan, labels=sold_day_pro, autopct='%1.1f%%', colors=colors)
            plt.title("Product Sold in Day", fontsize=18)
            can = FigureCanvasTkAgg(pie_product_day, master=scroll_frame)
            can.draw()
            can.get_tk_widget().pack(padx=180, pady=100)
            toolb = NavigationToolbar2Tk(can, scroll_frame)
            toolb.update()
            toolb.place(x=650, y=1480)
            # Pie Category Sold
            Sold_Cat_Day = pd.read_sql_query("SELECT c.cat_name AS 'Category', SUM(i.quantity) AS 'Quantity' FROM category "
                                             "c, invoice i, product p WHERE i.pro_id = p.pro_id AND p.cat_id = c.cat_id AND"
                                             " strftime('%Y', i.date) IN ('{}') AND strftime('%m', i.date) IN ('{}') AND "
                                             "strftime('%d', i.date) IN ('{}') GROUP BY c.cat_id"
                                             .format(year_choose, month_choose, day_choose), conn)
            datafram = pd.DataFrame(Sold_Cat_Day)
            sold_cat_day = datafram['Category'].values.tolist()
            sold_cat_day_quan = datafram['Quantity'].values.tolist()
            colors = sns.color_palette("Pastel1")
            pie_category_day = plt.figure(figsize=(5, 5), dpi=100)
            plt.pie(sold_cat_day_quan, labels=sold_cat_day, autopct='%1.1f%%', colors=colors)
            plt.title("Product Sold in Category in Day", fontsize=18)
            ca = FigureCanvasTkAgg(pie_category_day, master=scroll_frame)
            ca.draw()
            ca.get_tk_widget().pack(padx=180, pady=100)
            tool = NavigationToolbar2Tk(ca, scroll_frame)
            tool.update()
            tool.place(x=650, y=2165)
            day_window.destroy()

        day_window = Toplevel(analysis_window)
        day_window.geometry("450x225")
        day_window.title("Sales Report in Day")
        day_window.configure(bg='#DFEEFF')
        day_label = Label(day_window, text='Choose a date', font=('Arial', 15), bg='#DFEEFF')
        day_label.pack(pady=20)
        calendar = DateEntry(day_window, selectmode='day', year=datetime.now().year,
                             month=datetime.now().month, day=datetime.now().day, font=('Arial', 15))
        calendar.pack()
        Button(day_window, text='Confirm', font=('Arial', 15), command=sales_day).pack(pady=20)


    # Rectangle Frame
    RectangleFrame = Frame(analysis_window, bg='#492F7C', highlightbackground='white', highlightthickness=1)
    RectangleFrame.place(x=0, y=0, height=100, width=1920)
    RectangleFrame2 = Frame(analysis_window, bg='#492F7C', highlightbackground='white', highlightthickness=1)
    RectangleFrame2.place(x=0,y=100, height =700, width = 1533)



    Lab = Label(analysis_window, text='Analysis', font=('Arial', 30), fg='white', bg='#492F7C')
    Lab.place(x=10, y=30)

    # Create notebook
    analysis_notebook = ttk.Notebook(RectangleFrame2)
    analysis_notebook.pack(fill='both', expand = True)

    # Create Frames and Add Scrollbar
    frame1 = Frame(analysis_notebook, bg='#DFEEFF', width=1770, height=840)  # new frame for tab 1
    container = Canvas(frame1, bg='#DFEEFF')
    frame2 = Frame(analysis_notebook, bg='#DFEEFF', width=1770, height=840)  # new frame for tab 2
    frame1.pack(fill='both', expand=True)
    frame2.pack(fill='both', expand=True)
    scrollbar = Scrollbar(frame1, orient=VERTICAL, command=container.yview)
    scroll_frame = Frame(container, bg='#DFEEFF')
    scroll_frame.bind("<Configure>", lambda e: container.configure(scrollregion=container.bbox("all")))
    container.create_window((0, 0), window=scroll_frame, anchor=NW)
    container.configure(yscrollcommand=scrollbar.set)
    container.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    scroll_frame.bind("<MouseWheel>", lambda e: MouseScrollWheel)

    # Add frames to notebook
    analysis_notebook.add(frame1, text="Sales Report")
    analysis_notebook.add(frame2, text="Analytics")
    
    # Analytics
    # Expiry Status Pie
    Expiry = pd.read_sql_query("SELECT expiry_status AS 'Expiry Status', count(expiry_status) AS 'Number of Product' "
                               "FROM product GROUP BY expiry_status", conn)
    dataf = pd.DataFrame(Expiry)
    expiry = dataf['Expiry Status'].values.tolist()
    numpro = dataf['Number of Product'].values.tolist()
    colors = sns.color_palette("Pastel1")
    pie_expiry = plt.figure(figsize=(5, 5), dpi=100)
    plt.pie(numpro, labels=expiry, autopct='%1.1f%%', colors=colors)
    plt.title("Product Expiry Status", fontsize=18)
    canvas = FigureCanvasTkAgg(pie_expiry, master=frame2)
    canvas.draw()
    canvas.get_tk_widget().place(x=150, y=60)
    toolbars = NavigationToolbar2Tk(canvas, frame2)
    toolbars.update()
    toolbars.place(x=220, y=560)
    # Stock Level Status Pie
    Stock = pd.read_sql_query("SELECT stock_level AS 'Stock Level', count(stock_level) AS 'Number of Product' FROM "
                              "product GROUP BY stock_level", conn)
    dataframe = pd.DataFrame(Stock)
    level = dataframe['Stock Level'].values.tolist()
    numproduct = dataframe['Number of Product'].values.tolist()
    pie_stock = plt.figure(figsize=(5, 5), dpi=100)
    plt.pie(numproduct, labels=level, autopct='%1.1f%%', colors=colors)
    plt.title("Stock Level Status", fontsize=18)
    canva = FigureCanvasTkAgg(pie_stock, master=frame2)
    canva.draw()
    canva.get_tk_widget().place(x=850, y=60)
    toolbar = NavigationToolbar2Tk(canva, frame2)
    toolbar.update()
    toolbar.place(x=920, y=560)

    # Sales Report
    Button(frame1, text='Year', font=('Arial', 15), command=sort_year).place(x=100, y=10)
    Button(frame1, text='Month', font=('Arial', 15), command=sort_month).place(x=200, y=10)
    Button(frame1, text='Day', font=('Arial', 15), command=sort_day).place(x=300, y=10)
    # Show current day chart
    bar()
    pie_product()
    pie_category()

    analysis_window.mainloop()


