from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
import sqlite3
import pandas as pd
import os
import re
import logging

logging.basicConfig(
    filename='logs.log',
    encoding='utf-8',
    filemode='a',
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def logs(report):
    logging.info(report)

def export_to_excel():
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    con = connection()
    query = "SELECT * FROM productos"

    try:
        df = pd.read_sql_query(query, con)
        archive_path = os.path.join(download_path, 'products.xlsx') 
        df.to_excel(archive_path, index=False)
        con.close()
        showinfo("Export Complete", f"File saved in: {archive_path}")
        ok = 'OK EXPORT TO EXCEL'
        logs(ok)
    except:
        error = f'Error: Problem trying to export to Excel'
        logs(error)
        showinfo("Incomplete Export", f"{error}")

def export_to_csv():
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    con = connection()
    query = "SELECT * FROM productos"

    try:
        df = pd.read_sql_query(query, con)
        archive_path = os.path.join(download_path, 'products.csv')
        df.to_csv(archive_path, index=False)
        con.close()
        showinfo("Export Complete", f"File saved in: {archive_path}")
        ok = 'OK TO EXPORT CSV'
        logs(ok)
    except:
        error = f'Error: Problem trying to export to CSV'
        logs(error)
        showinfo("Incomplete Export", f"{error}")


def graph():
    con = connection()
    cursor = con.cursor()
    query = 'SELECT * FROM productos'

    try:
        cursor.execute(query)
        data = cursor.fetchall()

        objects = {}

        for i, row in enumerate(data):
            object = {}
            for j, element in enumerate(row):
                object[f'{j}'] = element
            objects[f'{i}'] = object
        
        count = []
        altitud = []
        for i, key in enumerate(objects):
            count.append(i)
            obj = objects[key]
            for k, v in obj.items():
                if k == '3':
                    altitud.append(v)

        info = {
            'count': count,
            'altitud': altitud
        }

        ok = 'OK GRAPHING DATA'
        logs(ok)

        return info
    except:
        error = 'Error: Problem tying to graph data'
        logs(error)

def save_graph():
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    save_path = os.path.join(downloads_path, 'expenses_graph.png')
    fig.savefig(save_path)
    showinfo("Image Downloaded", "You can go to your Downloads folder to view it!")

def connection():
    con = sqlite3.connect('productos.db')
    return con

def create_table():
    con = connection()
    cursor = con.cursor()
    table_name = 'productos'
    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name}
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto varchar(20) NOT NULL,
    fecha TEXT,
    precio REAL)
    """
    cursor.execute(query)
    con.commit()

try:
    connection()
    create_table()
    ok = 'OK CONNECT ESTABLISHED'
    logs(ok)
except ConnectionError:
    error = f'Error: {ConnectionError}'
    logs(error)

def buy():
    try:
        label_error.config(text='')
        product_name = input_name.get()
        product_cost = int(input_cost.get())

        if not validate_name(product_name) or not validate_cost(product_cost):
            raise ValueError
        
        product = {
            'producto': product_name,
            'precio': product_cost
        }

        ok = f'OK TO BUY PRODUCT {product_name}'
        logs(ok)

        return product
    except ValueError:
        error = 'Error: Name or Date invalid'
        label_error.config(text=error, foreground='red')
        logs(error)

def create_element(tree):
    producto_dict = buy()
    producto = producto_dict['producto']
    precio = producto_dict['precio']
    fecha = str(datetime.now().date())
    con = connection()
    cursor = con.cursor()
    data = (producto, fecha, precio)

    query = 'INSERT INTO productos(producto, fecha, precio) VALUES(?, ?, ?)'
    try:
        cursor.execute(query, data)
        con.commit()
        update_treeview(tree)
        update_graph()

        ok = f'OK TO CREATE {producto}'
        logs(ok)
    except SystemError as e:
        error = f'Error to create object {producto}: {e}'
        logs(error)

def delete_element():
    value = tree.selection()
    item = tree.item(value)
    my_id = item['text']

    con = connection()
    cursor = con.cursor()
    data = (my_id,)

    query = 'DELETE FROM productos WHERE id = ?'
    try:
        cursor.execute(query, data)
        con.commit()
        tree.delete(value)
        update_graph()
        ok = f'OK TO DELETE #{my_id} ELEMENT'
        logs(ok)
    except SystemError as e:
        error = f'Error to delete object #{my_id}: {e}'
        logs(error)
    
def edit_element(event):
    for item in tree.selection():
        item_text = tree.item(item, "values")
        entry_name = ttk.Entry(tree, width=10)
        entry_name.insert(0, item_text[0])
        entry_name.grid(row=tree.index(item), column=2)
        
        entry_cost = ttk.Entry(tree, width=10)
        entry_cost.insert(0, item_text[2])
        entry_cost.grid(row=tree.index(item), column=4)
        
        entry_name.bind("<Return>", lambda e: save_edit(item, entry_name, entry_cost))
        entry_cost.bind("<Return>", lambda e: save_edit(item, entry_name, entry_cost))

def save_edit(item, entry_name, entry_cost):
    name = entry_name.get()
    cost = entry_cost.get()
    tree.item(item, values=(name, cost))
    con = connection()
    cursor = con.cursor()
    query = 'UPDATE productos SET producto = ?, precio = ? WHERE id = ?'

    try:
        cursor.execute(query, (name, cost, tree.item(item, "text")))
        con.commit()
        con.close()
        update_treeview(tree)
        entry_name.destroy()
        entry_cost.destroy()
        update_graph()
        ok = 'GRAPH UPDATED'
        logs(ok)
    except:
        error = f'Error: problen when trying save changes'
        logs(error)

def update_treeview(treeview):
    records = treeview.get_children()

    for element in records: 
        treeview.delete(element)

    query = 'SELECT * FROM productos ORDER BY id ASC'

    con = connection()
    cursor = con.cursor()

    try:
        data = cursor.execute(query)

        result = data.fetchall()

        for fila in result:
            treeview.insert('', 0, text=fila[0], values=(fila[1], fila[2], fila[3]))
    except:
        error = f'Error: Problen when trying to update TreeView'
        logs(error)

def update_graph():
    info = graph()
    t.clear()
    t.set_title('Expenses graph')
    t.plot(info['count'], info['altitud'], color='red')
    canvas.draw()

def filter_treeview(event):
    entry_value = search.get()

    con = connection()
    cursor = con.cursor()

    selection = option_var.get()

    try:
        if entry_value=='':
            query = 'SELECT * FROM productos ORDER BY id ASC'
            cursor.execute(query)
        else:
            if selection == 'ID':
                query = "SELECT * FROM productos WHERE id LIKE ?"
                cursor.execute(query, (f'%{entry_value}%',))
            elif selection == '$':
                query = "SELECT * FROM productos WHERE precio >= ?"
                cursor.execute(query, (entry_value,))
            elif selection == 'NAME':
                query = "SELECT * FROM productos WHERE producto LIKE ?"
                cursor.execute(query, (f'%{entry_value}%',))
            elif selection == 'DATE':
                query = "SELECT * FROM productos WHERE fecha LIKE ?"
                cursor.execute(query, (f'%{entry_value}%',))

        result = cursor.fetchall()
        con.close()

        for row in tree.get_children():
            tree.delete(row)
        
        for row in result:
            tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3]))
    except:
        error = f'Error: Cannot complete the filter action'
        logs(error)

# def validate_password(password):
#     validation = re.match(r'^(?=.*[A-Z])(?=.*[a-z]{3,})(?=.*[0-9]{3,})(?=.*[!@#$%^&]).{8,}$', password)
#     if validation:
#         return True
#     return False

def validate_name(name):
    if not re.match(r'^([a-z]+)(-?)([a-zA-Z]*){4,}$', name):
        return False
    return True

def validate_cost(number):
    if not re.match(r'^(\d+)$', str(number)):
        return False
    return True
    
def validate_is_numeric(value):
    if value.isdigit():
        return True
    return False

def validate_is_text(value):
    if value.isalpha():
        return True
    return False

def validate_input(*args):
    selection = option_var.get()
    if selection == 'ID' or selection == '$':
        search.configure(validate='key', validatecommand=(validate_num, '%P'))
    if selection == 'NAME':
        search.configure(validate='key', validatecommand=(validate_text, '%P'))


root = Tk()
root.geometry('890x620')
root.configure(bg='#353535')
root.title('Venta y compra de productos')

validate_num = (root.register(validate_is_numeric), '%P')
validate_text = (root.register(validate_is_text), '%P')

root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=2)

left_frame = Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky=N+S+E+W)

left_frame.grid_rowconfigure(1, weight=1)
left_frame.grid_columnconfigure(0, weight=1)

right_frame = Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky=N+S+E+W)
right_frame.configure(bg='#353535')

right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(1, weight=0)
right_frame.grid_columnconfigure(0, weight=1)

right_frame.grid_rowconfigure(0, weight=1) 
right_frame.grid_rowconfigure(1, weight=0) 
right_frame.grid_columnconfigure(0, weight=2)

search = ttk.Entry(left_frame, width=20, font=('Arial', 13))
search.grid(row=0, column=0, pady=10, padx=10, sticky=W)
search.bind('<KeyRelease>', filter_treeview)

option_var = StringVar(value='ID')
options = ['ID','$','DATE','NAME']

option_menu = OptionMenu(left_frame, option_var, *options)
option_menu.grid(row=0, column=1, sticky=E, padx=9)

option_var.trace_add("write", validate_input)

tree = ttk.Treeview(left_frame)
tree['columns'] = ('col1', 'col2', 'col3')

tree.heading('#0', text='ID')
tree.heading('col1', text='NAME')
tree.heading('col2', text='DATE SOLD')
tree.heading('col3', text='COST')

tree.column('#0', width=20, minwidth=20, anchor=W)
tree.column('col1', width=50, minwidth=50, anchor=W)
tree.column('col2', width=50, minwidth=50, anchor=W)
tree.column('col3', width=50, minwidth=50, anchor=W)

entry_width = search.winfo_reqwidth()
tree.column('#0', width=int(entry_width / 4), minwidth=20, anchor=W)
tree.column('col1', width=int(entry_width / 4), minwidth=50, anchor=W)
tree.column('col2', width=int(entry_width / 4), minwidth=50, anchor=W)
tree.column('col3', width=int(entry_width / 4), minwidth=50, anchor=W)

tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=N+S+E+W)
tree.bind("<Double-1>", edit_element)

button_sell = ttk.Button(root, text='Sell', command=delete_element)
button_sell.grid(row=2,column=0, sticky=W, padx=10)

button_excel = ttk.Button(root, text='Export excel', command=export_to_excel)
button_excel.grid(row=2,column=0, padx=100, sticky=E)

button_csv = ttk.Button(root, text=' Export csv', command=export_to_csv)
button_csv.grid(row=2,column=0, sticky=E, padx=10, pady=5)

fig = Figure(figsize=(5, 3), dpi=100)
t = fig.add_subplot(111)
t.plot(graph()['count'], graph()['altitud'], color='red')
t.set_title('Expenses graph')

canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, padx=10, sticky=E)

right_down_frame = Frame(right_frame)
right_down_frame.grid(row=1, column=0, padx=30, pady=5, sticky=S+E+W, columnspan=5)
right_down_frame.configure(bg="#353535")

label_down = ttk.Label(right_down_frame, text='Buy a new product', font=('Arial', 20))
label_down.grid(row=1, column=0, sticky=W, pady=10)
label_down.configure(background='#353535', foreground='#fff')

btn_download_graph = ttk.Button(right_down_frame, text='Get Graph', command=save_graph)
btn_download_graph.grid(row=0, column=0, sticky=W)

label_name = ttk.Label(right_down_frame, text='Name')
label_name.grid(row=2, column=0, sticky=W, pady=2)
label_name.configure(background='#353535', foreground='#fff')

input_name = ttk.Entry(right_down_frame, width=30, font=('Arial', 13))
input_name.grid(row=3, column=0, sticky=W, pady=5)

label_cost = ttk.Label(right_down_frame, text='Cost')
label_cost.grid(row=4, column=0, sticky=W, pady=2)
label_cost.configure(background='#353535', foreground='#fff')

input_cost = ttk.Entry(right_down_frame, width=30, font=('Arial', 13))
input_cost.grid( row=5, column=0, sticky=W)

label_error = ttk.Label(right_down_frame, text='', font=('Arial', 8))
label_error.grid(row=6, column=0, sticky=N+W)
label_error.configure(background='#353535')

button_buy = ttk.Button(right_down_frame, text='comprar', command=lambda:create_element(tree))
button_buy.grid(row=7,column=0, sticky=W, pady=5)

update_treeview(tree)

root.mainloop()