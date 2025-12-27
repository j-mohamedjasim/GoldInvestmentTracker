from tkinter import *
from tkinter import Tk, ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import Button, Tk, Label, Entry
from datetime import datetime, timedelta
import sqlite3
import requests
import json

con = sqlite3.connect('databse.db')
c = con.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS dataentries(
          date TEXT,
          company TEXT,
          address TEXT,
          description TEXT,
          unit INTEGER,
          price REAL,
          pricePerUnit REAL,
          gram REAL,
          pricePerGram REAL,
          status TEXT,
          product TEXT,
          purpose TEXT,
          whom TEXT,
          purity TEXT
          )""")

con.commit()
con.close()



def insert(event=None):
    date = dateEntry.get()
    if len(date) == 10:
        pass
    else:
        messagebox.showerror('Error', 'Please input date in correct format.')
        dateEntry.focus_set()
        return
    
    company = companyEntry.get()
    if company == '':
        messagebox.showerror('Error', 'Please input company name.')
        companyEntry.focus_set()
        return
    else:
        pass

    address = addressEntry.get()
    if address == '':
        messagebox.showerror('Error', 'Please input address for the company.')
        addressEntry.focus_get()
        return
    else:
        pass

    invoice = invoiceEntry.get()
    if invoice == '':
        messagebox.showerror('Error', 'Please input invoice ID.')
        invoiceEntry.focus_set()
        return
    else:
        pass

    unit = unitEntry.get()
    if unit == '':
        messagebox.showerror('Error', 'Please input number of unit you have purchased for this item you are entering.')
        unitEntry.focus_set()
        return
    else:
        pass

    price = priceEntry.get()
    if price == '':
        messagebox.showerror('Error', 'Please input the price you have purchased this unit.')
        priceEntry.focus_set()
        return
    else:
        pass

    pricePerUnit = pricePerUnitEntry.get()
    if pricePerUnit == '':
        messagebox.showerror('Error', 'Please input the price per unit.')
        pricePerUnitEntry.focus_set()
        return
    else:
        pass

    gram = gramEntry.get()
    if gram == '':
        messagebox.showerror('Error', 'Please input gram you have purchased.')
        gramEntry.focus_set()
        return
    else:
        pass

    pricePerGram = pricePerGramEntry.get()
    if pricePerGram == '':
        messagebox.showerror('Error', 'Please input price per gram.')
        pricePerGramEntry.focus_set()
        return
    else:
        pass

    status = statusEntry.get()
    product = productEntry.get()
    purpose = purposeEntry.get()
    whom = whomEntry.get()
    purity = purityEntry.get()

    con = sqlite3.connect('databse.db')
    c = con.cursor()
    c.execute("INSERT INTO dataentries VALUES(:date, :company, :address, :description, :unit, :price, :pricePerUnit, :gram, :pricePerGram, :status, :product, :purpose, :whom, :purity)",
              {
                  'date': date,
                  'company': company.title(),
                  'address': address.upper(),
                  'description': invoice.upper(),
                  'unit': int(unit),
                  'price': float(price),
                  'pricePerUnit': float(pricePerUnit),
                  'gram': float(gram),
                  'pricePerGram': float(pricePerGram),
                  'status': status,
                  'product': product,
                  'purpose': purpose,
                  'whom': whom,
                  'purity': purity,
              })
    
    con.commit()
    con.close()

    unitEntry.delete(0, 'end')
    priceEntry.delete(0, 'end')
    pricePerUnitEntry.config(state='active')
    pricePerUnitEntry.delete(0, 'end')
    pricePerUnitEntry.config(state='readonly')
    gramEntry.delete(0, 'end')
    pricePerGramEntry.config(state='active')
    pricePerGramEntry.delete(0, 'end')
    pricePerGramEntry.config(state='readonly')
    statusEntry.set('Active')
    productEntry.set('Coin')
    purposeEntry.set('Savings')
    whomEntry.set('Savings')
    purityEntry.set('22K')

con = sqlite3.connect('databse.db')
c = con.cursor()

root = Tk()
root.geometry('700x700')
root.title('Entry')

def table(event=None):

    global tables

    try:
        if tables.winfo_exists():
            tables.deiconify()
            tables.lift()
            return
    except:
        pass

    status = {
        'active': '',
        'sold': ''
    }

    price = {
        'k22': 0.0,
        'k18': 0.0,
        'k24': 0.0
    }

    totalAmount = 0.00
    totalCoin = 0
    totalValue = 0.00
    totalGram = 0.00

    def status_update():
        active = status_var.get()
        sold = status_var1.get()

        totalAmount = 0.00
        totalCoin = 0
        totalValue = 0.00
        totalGram = 0.00

        if active == 1:
            status['active'] = 'Yes'
        else:
            status['active'] = 'No'

        if sold == 1:
            status['sold'] = 'Yes'
        else:
            status['sold'] = 'No'

        if status['sold'] == 'Yes' and status['active'] == 'Yes':
            con = sqlite3.connect('databse.db')
            c = con.cursor()
            c.execute("SELECT * FROM dataentries")

            datas = c.fetchall()

            con.close()

            for item in tree.get_children():
                tree.delete(item)

            for data in datas:

                ppg = data[8] #Price Per Gram

                if data[13] == '24K':
                    tppg = (price['k24'] * data[7]) - (ppg * data[7]) #tppg means Today Price Per Gram
                elif data[13] == '22K':
                    tppg = (price['k22'] * data[7]) - (ppg * data[7])
                else:
                    tppg = (price['k18'] * data[7]) - (ppg * data[7])

                totalAmount += float(data[5])
                totalCoin += float(data[4])
                totalValue += float(tppg)
                totalGram += data[7]

                tree.insert('', 'end', values=[data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], f'{tppg: .2f}'])

            if totalValue < 0.00:
                priceLbl3.config(foreground='red')
            else:
                priceLbl3.config(foreground='green')

            priceLbl1.config(text=f'Total Amount: £{totalAmount: .2f}')
            priceLbl2.config(text=f'Total Coin: {round(totalCoin)}')
            priceLbl3.config(text=f'Total Value: £{totalValue: .2f}')
            priceLbl4.config(text=f'Total Gram: {totalGram: .2f}')

        elif status['active'] == 'Yes':
            con = sqlite3.connect('databse.db')
            c = con.cursor()
            c.execute("SELECT * FROM dataentries WHERE status = ?",('Active',))

            datas = c.fetchall()

            con.close()

            for item in tree.get_children():
                tree.delete(item)

            for data in datas:

                ppg = data[8] #Price Per Gram

                if data[13] == '24K':
                    tppg = (price['k24'] * data[7]) - (ppg * data[7]) #tppg means Today Price Per Gram
                elif data[13] == '22K':
                    tppg = (price['k22'] * data[7]) - (ppg * data[7])
                else:
                    tppg = (price['k18'] * data[7]) - (ppg * data[7])

                totalAmount += float(data[5])
                totalCoin += float(data[4])
                totalValue += float(tppg)
                totalGram += data[7]

                tree.insert('', 'end', values=[data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], f'{tppg: .2f}'])

            if totalValue < 0.00:
                priceLbl3.config(foreground='red')
            else:
                priceLbl3.config(foreground='green')

            priceLbl1.config(text=f'Total Amount: £{totalAmount: .2f}')
            priceLbl2.config(text=f'Total Coin: {round(totalCoin)}')
            priceLbl3.config(text=f'Total Value: £{totalValue: .2f}')
            priceLbl4.config(text=f'Total Gram: {totalGram: .2f}')

        elif status['sold'] == 'Yes':
            con = sqlite3.connect('databse.db')
            c = con.cursor()
            c.execute("SELECT * FROM dataentries WHERE status = ?",('Sold',))

            datas = c.fetchall()

            con.close()

            for item in tree.get_children():
                tree.delete(item)

            for data in datas:

                ppg = data[8] #Price Per Gram

                if data[13] == '24K':
                    tppg = (price['k24'] * data[7]) - (ppg * data[7]) #tppg means Today Price Per Gram
                elif data[13] == '22K':
                    tppg = (price['k22'] * data[7]) - (ppg * data[7])
                else:
                    tppg = (price['k18'] * data[7]) - (ppg * data[7])

                totalAmount += float(data[5])
                totalCoin += float(data[4])
                totalValue += float(tppg)
                totalGram += data[7]

                tree.insert('', 'end', values=[data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], f'{tppg: .2f}'])

            if totalValue < 0.00:
                priceLbl3.config(foreground='red')
            else:
                priceLbl3.config(foreground='green')

            priceLbl1.config(text=f'Total Amount: £{totalAmount: .2f}')
            priceLbl2.config(text=f'Total Coin: {round(totalCoin)}')
            priceLbl3.config(text=f'Total Value: £{totalValue: .2f}')
            priceLbl4.config(text=f'Total Gram: {totalGram: .2f}')

        

        else:
            con = sqlite3.connect('databse.db')
            c = con.cursor()
            c.execute("SELECT * FROM dataentries ORDER BY date ASC")

            datas = c.fetchall()

            con.close()

            for item in tree.get_children():
                tree.delete(item)

            for data in datas:

                ppg = data[8] #Price Per Gram

                if data[13] == '24K':
                    tppg = (price['k24'] * data[7]) - (ppg * data[7]) #tppg means Today Price Per Gram
                elif data[13] == '22K':
                    tppg = (price['k22'] * data[7]) - (ppg * data[7])
                else:
                    tppg = (price['k18'] * data[7]) - (ppg * data[7])

                totalAmount += float(data[5])
                totalCoin += float(data[4])
                totalValue += float(tppg)
                totalGram += data[7]

                tree.insert('', 'end', values=[data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], f'{tppg: .2f}'])

            if totalValue < 0.00:
                priceLbl3.config(foreground='red')
            else:
                priceLbl3.config(foreground='green')

            priceLbl1.config(text=f'Total Amount: £{totalAmount: .2f}')
            priceLbl2.config(text=f'Total Coin: {round(totalCoin)}')
            priceLbl3.config(text=f'Total Value: £{totalValue: .2f}')
            priceLbl4.config(text=f'Total Gram: {totalGram: .2f}')
    

    def make_gapi_request():
        api_key = "goldapi-jasimjs-io"
        symbol = "XAU"
        curr = "GBP"
        date = ""

        url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"
        
        headers = {
            "x-access-token": api_key,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()

            gold_24k = data["price_gram_24k"] 
            gold_22k = data["price_gram_22k"] 
            gold_18k = data["price_gram_18k"]

            label_24k.config(text=f'24K: £{gold_24k: .2f}')
            label_18k.config(text=f'18K: £{gold_18k: .2f}')
            label_22k.config(text=f'22K: £{gold_22k: .2f}')

            

            price['k24'] = float(gold_24k)
            price['k22'] = float(gold_22k)
            price['k18'] = float(gold_18k)
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror('Error', e)    

    
    tables = Toplevel(root)
    tables.geometry('900x700')
    tables.title('Table')

    mainframe = ttk.Frame(tables)
    mainframe.pack()

    status_var = IntVar()
    status_var1 = IntVar()
    status1 = ttk.Checkbutton(mainframe, text='Active', variable=status_var, command=status_update)
    status1.pack(side='left', padx=(10,0), pady=(10,0))
    status_var.set(1)

    status2 = ttk.Checkbutton(mainframe, text='Sold', variable=status_var1, command=status_update)
    status2.pack(side='left', padx=(10,0), pady=(10,0))
    status_var1.set(1)

    label_18k = ttk.Label(mainframe, text='18K:')
    label_18k.pack(side='right', padx=(10,10), pady=(10,0))

    label_22k = ttk.Label(mainframe, text='22K:')
    label_22k.pack(side='right', padx=(10,10), pady=(10,0))

    label_24k = ttk.Label(mainframe, text='24K:')
    label_24k.pack(side='right', padx=(50,10), pady=(10,0))

    mainframe1 = ttk.Frame(tables)
    mainframe1.pack()

    priceLbl1 = ttk.Label(mainframe1, text=('Total amount:'))
    priceLbl1.pack(side='left', padx=(10,0), pady=(10,10))

    priceLbl2 = ttk.Label(mainframe1, text='Total Coin:')
    priceLbl2.pack(side='left', padx=(10,0), pady=(10,10))

    priceLbl3 = ttk.Label(mainframe1, text='Total Value: ')
    priceLbl3.pack(side='left', padx=(10,0), pady=(10,10))

    priceLbl4 = ttk.Label(mainframe1, text='Total Gram: ')
    priceLbl4.pack(side='left', padx=(10,0), pady=(10,10))


    make_gapi_request()

    def sold_def():
        selected_items = tree.selection()

        if selected_items:

            for item in selected_items:
                item_values = tree.item(item)['values']
                invoice = item_values[3]
                price_value = item_values[5]
                

            con = sqlite3.connect('databse.db')
            c = con.cursor()
            c.execute("UPDATE dataentries SET status = ? WHERE description = ? AND price = ?",('Sold', invoice, price_value))

            con.commit()
            con.close()

            for item in tree.get_children():
                tree.delete(item)

            con = sqlite3.connect('databse.db')
            c = con.cursor()
            c.execute("SELECT * FROM dataentries ORDER BY date ASC")

            datas = c.fetchall()

            con.close()

            totalAmount = 0.00
            totalCoin = 0
            totalValue = 0.00
            totalGram = 0.00

            for data in datas:

                ppg = data[8] #Price Per Gram

                if data[13] == '24K':
                    tppg = (price['k24'] * data[7]) - (ppg * data[7]) #tppg means Today Price Per Gram
                elif data[13] == '22K':
                    tppg = (price['k22'] * data[7]) - (ppg * data[7])
                else:
                    tppg = (price['k18'] * data[7]) - (ppg * data[7])

                totalAmount += float(data[5])
                totalCoin += float(data[4])
                totalValue += float(tppg)
                totalGram += data[7]

                tree.insert('', 'end', values=[data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], f'{tppg: .2f}'])

            if totalValue < 0.00:
                priceLbl3.config(foreground='red')
            else:
                priceLbl3.config(foreground='green')

            priceLbl1.config(text=f'Total Amount: £{totalAmount: .2f}')
            priceLbl2.config(text=f'Total Coin: {round(totalCoin)}')
            priceLbl3.config(text=f'Total Value: £{totalValue: .2f}')
            priceLbl4.config(text=f'Total Gram: {totalGram: .2f}')
            

        else:
            messagebox.showerror("Error", "There is no item selected.")
            return
        
    def active_def():

        selected_items = tree.selection()

        if selected_items:
           

            for item in selected_items:
                item_values = tree.item(item)['values']
                invoice = item_values[3]
                price_value = item_values[5]
                

            con = sqlite3.connect('databse.db')
            c = con.cursor()
            c.execute("UPDATE dataentries SET status = ? WHERE description = ? AND price = ?",('Active', invoice, price_value))

            con.commit()
            con.close()

            for item in tree.get_children():
                tree.delete(item)

            con = sqlite3.connect('databse.db')
            c = con.cursor()
            c.execute("SELECT * FROM dataentries ORDER BY date ASC")

            datas = c.fetchall()

            con.close()

            totalAmount = 0.00
            totalCoin = 0
            totalValue = 0.00
            totalGram = 0.00

            for data in datas:

                ppg = data[8] #Price Per Gram

                if data[13] == '24K':
                    tppg = (price['k24'] * data[7]) - (ppg * data[7]) #tppg means Today Price Per Gram
                elif data[13] == '22K':
                    tppg = (price['k22'] * data[7]) - (ppg * data[7])
                else:
                    tppg = (price['k18'] * data[7]) - (ppg * data[7])

                totalAmount += float(data[5])
                totalCoin += float(data[4])
                totalValue += float(tppg)
                totalGram += data[7]

                tree.insert('', 'end', values=[data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], f'{tppg: .2f}'])

            if totalValue < 0.00:
                priceLbl3.config(foreground='red')
            else:
                priceLbl3.config(foreground='green')

            priceLbl1.config(text=f'Total Amount: £{totalAmount: .2f}')
            priceLbl2.config(text=f'Total Coin: {round(totalCoin)}')
            priceLbl3.config(text=f'Total Value: £{totalValue: .2f}')
            priceLbl4.config(text=f'Total Gram: {totalGram: .2f}')
        else:
            messagebox.showerror('Error', 'You did not select any item.')
            return

    def delete_def():

        selected_items = tree.selection()

        if selected_items:
            response = messagebox.askokcancel("Confirmation", "Are you sure you want to delete this item?")
            if response:
                

                for item in selected_items:
                    item_values = tree.item(item)['values']
                    invoice = item_values[3]
                    price_value = item_values[5]
                    

                    tree.delete(item)

                con = sqlite3.connect('databse.db')
                c = con.cursor()
                c.execute("DELETE FROM dataentries WHERE description = ? AND price = ?",(invoice, price_value))

                con.commit()
                con.close()

                for item in tree.get_children():
                    tree.delete(item)

                con = sqlite3.connect('databse.db')
                c = con.cursor()
                c.execute("SELECT * FROM dataentries ORDER BY date ASC")

                datas = c.fetchall()

                con.close()

                totalAmount = 0.00
                totalCoin = 0
                totalValue = 0.00
                totalGram = 0.00

                for data in datas:

                    ppg = data[8] #Price Per Gram

                    if data[13] == '24K':
                        tppg = (price['k24'] * data[7]) - (ppg * data[7]) #tppg means Today Price Per Gram
                    elif data[13] == '22K':
                        tppg = (price['k22'] * data[7]) - (ppg * data[7])
                    else:
                        tppg = (price['k18'] * data[7]) - (ppg * data[7])

                    totalAmount += float(data[5])
                    totalCoin += float(data[4])
                    totalValue += float(tppg)
                    totalGram += data[7]

                    tree.insert('', 'end', values=[data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], f'{tppg: .2f}'])

                if totalValue < 0.00:
                    priceLbl3.config(foreground='red')
                else:
                    priceLbl3.config(foreground='green')

                priceLbl1.config(text=f'Total Amount: £{totalAmount: .2f}')
                priceLbl2.config(text=f'Total Coin: {round(totalCoin)}')
                priceLbl3.config(text=f'Total Value: £{totalValue: .2f}')
                priceLbl4.config(text=f'Total Gram: {totalGram: .2f}')
            else:
                return
        else:
            messagebox.showerror('Error', 'You did not select any item.')
            return

    con = sqlite3.connect('databse.db')
    c = con.cursor()
    c.execute("SELECT * FROM dataentries ORDER BY date ASC")

    datas = c.fetchall()

    con.close()

    column = ('date', 'company', 'address', 'description', 'unit', 'price', 'pricePerUnit', 'gram', 'pricePerGram', 'status', 'product', 'purpose', 'whom', 'purity', 'varience')

    tree = ttk.Treeview(tables, column = column, show= 'headings', height=10)
    tree.pack(fill='both', expand=True, pady=(10,10))

    tree.heading('date', text= 'Date')
    tree.heading('company', text='Company')
    tree.heading('address', text='Address')
    tree.heading('description', text='Description')
    tree.heading('unit', text='Unit')
    tree.heading('price', text='Price')
    tree.heading('pricePerUnit', text='£ Per Unit')
    tree.heading('gram', text='Gram')
    tree.heading('pricePerGram', text='£ Per Gram')
    tree.heading('status', text='Status')
    tree.heading('product', text='Product')
    tree.heading('purpose', text='Purpose')
    tree.heading('whom', text='Whom')
    tree.heading('purity', text='Purity')
    tree.heading('varience', text='Varience')

    tree.column('date', width=20)
    tree.column('company', width=20)
    tree.column('address', width=20)
    tree.column('description', width=20)
    tree.column('unit', width=20)
    tree.column('price', width=20)
    tree.column('pricePerUnit', width=20)
    tree.column('gram', width=20)
    tree.column('pricePerGram', width=20)
    tree.column('status', width=20)
    tree.column('product', width=20)
    tree.column('purpose', width=20)
    tree.column('whom', width=20)
    tree.column('purity', width=20)
    tree.column('varience', width=20)

    for data in datas:

        ppg = data[8] #Price Per Gram

        if data[13] == '24K':
            tppg = (price['k24'] * data[7]) - (ppg * data[7]) #tppg means Today Price Per Gram
        elif data[13] == '22K':
            tppg = (price['k22'] * data[7]) - (ppg * data[7])
        else:
            tppg = (price['k18'] * data[7]) - (ppg * data[7])

        totalAmount += float(data[5])
        totalCoin += float(data[4])
        totalValue += float(tppg)
        totalGram += data[7]

        tree.insert('', 'end', values=[data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], f'{tppg: .2f}'])

    if totalValue < 0.00:
        priceLbl3.config(foreground='red')
    else:
        priceLbl3.config(foreground='green')

    priceLbl1.config(text=f'Total Amount: £{totalAmount: .2f}')
    priceLbl2.config(text=f'Total Coin: {round(totalCoin)}')
    priceLbl3.config(text=f'Total Value: £{totalValue: .2f}')
    priceLbl4.config(text=f'Total Gram: {totalGram: .2f}')

    mainframe2 = ttk.Frame(tables, )
    mainframe2.pack()
    soldButton = ttk.Button(mainframe2, text="Sold", command=sold_def)
    soldButton.pack(side='left', padx=(10,0), pady=(10,10))

    activeButton = ttk.Button(mainframe2, text="Active", command=active_def)
    activeButton.pack(side='left', padx=(10,0), pady=(10,10))

    deleteButton  = ttk.Button(mainframe2, text='Delete 🗑', command=delete_def)
    deleteButton.pack(side='left', padx=(10,0), pady=(10,10))


#================================================================================================================
menubar = tk.Menu(root)
function_menu = tk.Menu(menubar, tearoff=0)
function_menu.add_command(label='Table', command=table, accelerator="Command+T")
menubar.add_cascade(label='Chart', menu=function_menu)

root.config(menu=menubar)

root.bind('<Command-t>', table)

today = datetime.today()
tdate = today.strftime('%Y-%m-%d')

dateEntry = ttk.Entry(root, width=11)
dateEntry.grid(row=0, column=0, padx=(10,0), pady=(10,0), columnspan=2, sticky='w')
dateEntry.delete(0,'end')
dateEntry.insert(0,tdate)

companyLbl = ttk.Label(root, text='Company')
companyLbl.grid(row=1, column=0, padx=(10,0), pady=(10,0), sticky='w')

companyEntry = ttk.Entry(root)
companyEntry.grid(row=1, column=1, padx=(10,0), pady=(10,0), sticky='w')

listWidget = Listbox(root, height=5)
listWidget.grid(row=1, column=2, padx=(10,0), pady=(10,0), sticky='ne', rowspan=5)
listWidget.grid_remove()

def searchCompany(event): #bring company name as typing in companyEntry.
    typed = companyEntry.get()

    if typed == '':
        listWidget.grid_remove()
        return
    
    

    c.execute("SELECT company FROM dataentries WHERE company LIKE ?", (typed + "%", ))
    results = c.fetchall()

    listWidget.delete(0, 'end')

    if results:
        unique_name = sorted({row[0] for row in results})
        for name in unique_name:
            listWidget.insert(END, name)
        listWidget.grid()

    else:
        listWidget.grid_remove()

def fill_entry(event):
    selected = listWidget.get(ACTIVE)
    companyEntry.delete(0, END)
    companyEntry.insert(0, selected)
    listWidget.grid_remove()
    addressEntryAuto()

companyEntry.bind("<KeyRelease>", searchCompany)
listWidget.bind("<<ListboxSelect>>", fill_entry)
listWidget.bind("<ButtonRelease-1>", fill_entry)

addressLbl = ttk.Label(root, text='Address')
addressLbl.grid(row=2, column=0, padx=(10,0), pady=(10,0), sticky='w')

def addressEntryAuto():#Auto complete address entry
    company = companyEntry.get()
    con = sqlite3.connect('databse.db')
    c = con.cursor()
    c.execute("SELECT address FROM dataentries WHERE company = ?",(company, ))

    address = c.fetchone()

    con.close()
    if address:
        addressEntry.delete(0, END)
        addressEntry.insert(0, address[0])

addressEntry = ttk.Entry(root)
addressEntry.grid(row=2, column=1, padx=(10,0), pady=(10,0), sticky='w')

invoiceLbl = ttk.Label(root, text='Invoice Number')
invoiceLbl.grid(row=3, column=0, padx=(10,0), pady=(10,0), sticky='w')

invoiceEntry = ttk.Entry(root)
invoiceEntry.grid(row=3, column=1, padx=(10,0), pady=(10,0), sticky='w')

unitLbl = ttk.Label(root, text='Unit Purchased')
unitLbl.grid(row=4, column=0, padx=(10,0), pady=(10,0), sticky='w')

unitEntry = ttk.Spinbox(root, from_=1, to=100, width=3)
unitEntry.grid(row=4, column=1, padx=(10,0), pady=(10,0), sticky='w')

priceLbl = ttk.Label(root, text='Price')
priceLbl.grid(row=5, column=0, padx=(10,0), pady=(10,0), sticky='w')

priceEntry = ttk.Spinbox(root, from_=0.00, to=10000.00, width=7)
priceEntry.grid(row=5, column=1, padx=(10,0), pady=(10,0), sticky='w')


pricePerUnitLbl = ttk.Label(root, text='Price Per Unit')
pricePerUnitLbl.grid(row=6, column=0, padx=(10,0), pady=(10,0), sticky='w')

def pricePerUnit(event=None):
    unit = unitEntry.get().strip()
    price = priceEntry.get().strip()

    if unit == '':
        return
    if price == '':
        return

    try:
        uni = float(unit)
        
    except ValueError:
        messagebox.showerror('Error', 'Price should be in numbers.')
        unitEntry.focus_set()
        return
    
    try:
        pri = float(price)
        
    except ValueError:
        messagebox.showerror('Error', 'Unit should be in numbers.')
        priceEntry.focus_set()
        return
    try:
        divide = f'{pri / uni: .2f}'
    except ZeroDivisionError:
        divide = 0.00

    pricePerUnitEntry.config(state=ACTIVE)
    pricePerUnitEntry.delete(0, END)
    pricePerUnitEntry.insert(0, divide)
    pricePerUnitEntry.config(state=DISABLED)

pricePerUnitEntry = ttk.Spinbox(root, from_=0.00, to=10000.00, width=7)
pricePerUnitEntry.grid(row=6, column=1, padx=(10,0), pady=(10,0), sticky='w')
priceEntry.bind("<KeyRelease>", pricePerUnit)
priceEntry.bind("<<Increment>>", pricePerUnit)
priceEntry.bind("<<Decrement>>", pricePerUnit)
pricePerUnitEntry.config(state=DISABLED)

gramLbl = ttk.Label(root, text='Gram')
gramLbl.grid(row=7, column=0, padx=(10,0),pady=(10,0), sticky='w')

gramEntry = Spinbox(root, from_=0.00, to=1000.00, width=7)
gramEntry.grid(row=7, column=1, padx=(10,0), pady=(10,0), sticky='w')

def gramCalculation(event=None):
    gram = gramEntry.get().strip()
    price = pricePerUnitEntry.get().strip()

    if gram == '':
        return

    if price == '':
        return

    try:
        gra = float(gram)
    except ValueError:
        
        messagebox.showerror('Error', 'Gram should be in numbers.')
        gramEntry.focus_set()
        return
    
    try:
        pri = float(price)
    except ValueError:
        messagebox.showerror('Error', 'Price should be in numbers.')
        pricePerUnitEntry.focus_set()
        return
    
    try:
        divide = f'{pri / gra: .2f}'
    except ZeroDivisionError:
        divide = 0.00
    pricePerGramEntry.config(state=ACTIVE)
    pricePerGramEntry.delete(0, END)
    pricePerGramEntry.insert(0, divide)
    pricePerGramEntry.config(state=DISABLED)

pricePerGramLbl = ttk.Label(root, text='Price Per Gram')
pricePerGramLbl.grid(row=8, column=0, padx=(10,0), pady=(10,0), sticky='w')

pricePerGramEntry = ttk.Spinbox(root, from_=0.00, to=10000.00, width=7)
pricePerGramEntry.grid(row=8, column=1, padx=(10,0), pady=(10,0), sticky='w')
pricePerGramEntry.config(state=DISABLED)
gramEntry.bind("<KeyRelease>", gramCalculation)
gramEntry.bind("<<Increment>>", gramCalculation)
gramEntry.bind("<<Decrement>>", gramCalculation)

statusLbl = ttk.Label(root, text='Status')
statusLbl.grid(row=9, column=0, padx=(10,0), pady=(10,0), sticky='w')

statusEntry = ttk.Combobox(root, values=['Active', 'Sold'], width=7, state='readonly')
statusEntry.grid(row=9, column=1, padx=(10,0), pady=(10,0), sticky='w')
statusEntry.set('Active')

productLbl = ttk.Label(root, text='Product')
productLbl.grid(row=10, column=0, padx=(10,0), pady=(10,0), sticky='w')

productEntry = ttk.Combobox(root, values=['Biscuit', 'Coin', 'Jewels'], state='readonly')
productEntry.grid(row=10, column=1, padx=(10,0), pady=(10,0), sticky='w')
productEntry.set('Coin')

purposeLbl = ttk.Label(root, text='Purpose')
purposeLbl.grid(row=11, column=0, padx=(10,0), pady=(10,0), sticky='w')

def purposeValidation(event=None):
    purpose = purposeEntry.get()

    if purpose == 'Pleasure':
        whomEntry.set('Shafana Shaeen')
    elif purpose == 'Savings':
        whomEntry.set('Savings')
    else:
        pass

purposeEntry = ttk.Combobox(root, values=['Savings', 'Pleasure'], state='readonly')
purposeEntry.grid(row=11, column=1, padx=(10,0), pady=(10,0), sticky='w')
purposeEntry.set('Savings')
purposeEntry.bind("<<ComboboxSelected>>", purposeValidation)

whomLbl = ttk.Label(root, text='For Whom')
whomLbl.grid(row=12, column=0, padx=(10,0), pady=(10,0), sticky='w')

whomEntry = ttk.Combobox(root, values=['Shafana Shaeen', 'Afizah', 'Relatives', 'Gift', 'Savings'], state='readonly')
whomEntry.grid(row=12, column=1, padx=(10,0), pady=(10,0), sticky='w')
whomEntry.set('Savings')

purityLbl = ttk.Label(root, text='Purity')
purityLbl.grid(row=13, column=0, padx=(10,0), pady=(10,0), sticky='w')

purityEntry = ttk.Combobox(root, values=['18K', '22K', '24K'], state='readonly', width=4, foreground='purple')
purityEntry.grid(row=13, column=1, padx=(10,0), pady=(10,0), sticky='w')
purityEntry.set('22K')
purityEntry.bind('<Return>', insert)

insertButton = ttk.Button(root, text='Submit', width=6, command=insert)
insertButton.grid(row=14, column=1, padx=(10,0), pady=(20,0))
insertButton.bind('<Return>', insert)


root.mainloop()
