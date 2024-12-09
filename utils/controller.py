import pandas as pd
import os
import re
from datetime import datetime
from database.database import *
from logs.logs import *
from tkinter.messagebox import showerror, showinfo
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *


def buy(label_error, input_name, input_cost):
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

        label_error.config(text='Product registred correctly', foreground='green')

        ok = f'OK TO BUY PRODUCT {product_name}'
        logs(ok)
        
        return product
    except Exception as e:
        error = 'Error: Name or Date invalid'
        label_error.config(text=error, foreground='red')
        logs(f'{error} - {e}')


def create_element(tree, label_error, input_name, input_cost, t, canvas):
    producto_dict = buy(label_error, input_name, input_cost)
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
        update_graph(t, canvas)

        input_name.delete(0, tk.END)
        input_cost.delete(0, tk.END)

        ok = f'OK TO CREATE {producto}'
        logs(ok)
    except Exception as e:
        error = f'Error to create object {producto}: {e}'
        logs(error)
        showerror('Error', f'Problem with creating the product {producto}')


def delete_element(t, canvas, tree):
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
        update_graph(t, canvas)
        ok = f'OK TO DELETE #{my_id} ELEMENT'
        logs(ok)
    except Exception as e:
        error = f'Error to delete object #{my_id}: {e}'
        logs(error)
        showerror('Errpr', f'Problem when deleting object #{my_id}')
    

def edit_element(tree, t, canvas):
    for item in tree.selection():
        item_text = tree.item(item, "values")
        entry_name = ttk.Entry(tree, width=10)
        entry_name.insert(0, item_text[0])
        entry_name.grid(row=tree.index(item), column=2)
        
        entry_cost = ttk.Entry(tree, width=10)
        entry_cost.insert(0, item_text[2])
        entry_cost.grid(row=tree.index(item), column=4)
        
        entry_name.bind("<Return>", lambda e: save_edit(item, tree, entry_name, entry_cost, t, canvas))
        entry_cost.bind("<Return>", lambda e: save_edit(item, tree, entry_name, entry_cost, t, canvas))


def save_edit(item, tree, entry_name, entry_cost, t, canvas):
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
        update_graph(t, canvas)
        ok = 'GRAPH UPDATED'
        logs(ok)
    except Exception as e:
        error = f'Error: problen when trying to save changes - {e}'
        logs(error)
        showerror('Error', 'Problem when trying to save changes')


def export_to_excel():

    file_path = validate_export(extension='xlsx', type='XLSX')
    con = connection()
    query = "SELECT * FROM productos"

    try:
        df = pd.read_sql_query(query, con)
        df.to_excel(file_path, index=False)
        con.close()
        showinfo("Export Complete", f"File saved in: {file_path}")
        ok = 'OK EXPORT TO EXCEL'
        logs(ok)
    except Exception as e:
        error = f'Error: Problem trying to export to Excel'
        logs(f'{error} - {e}')
        showerror("Incomplete Export", f"{error}")


def export_to_csv():
    file_path = validate_export(extension='csv', type='CSV')
    con = connection()
    query = "SELECT * FROM productos"

    try:
        df = pd.read_sql_query(query, con)
        df.to_csv(file_path, index=False)
        con.close()
        showinfo("Export Complete", f"File saved in: {file_path}")
        ok = 'OK TO EXPORT CSV'
        logs(ok)
    except Exception as e:
        error = f'Error: Problem trying to export to CSV'
        logs(f'{error} - {e}')
        showerror("Incomplete Export", f"{error}")


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
    except Exception as e:
        error = f'Error: Problem tying to graph data - {e}'
        logs(error)
        showerror('Error', 'Problem trying to graph data')


def save_graph(fig):

    file_path = asksaveasfilename(
        title='Save Graph Image',
        defaultextension='.png',
        filetypes=[('PNG files', '*.png')],
        initialdir=os.path.join(os.path.expanduser('~'), 'Downloads'),
        initialfile='expenses_graph'
    )

    if not file_path:
        showinfo('Save Cancelled', 'Not file selected')
        return

    fig.savefig(file_path)
    showinfo("Image Downloaded", f"You can go to {file_path} folder to view it!")


def filter_treeview(tree, search, option_var):
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
    except Exception as e:
        error = f'Error: Cannot complete the filter action - {e}'
        logs(error)
        showerror('Error', 'Problem when trying to filter')


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
    except Exception as e:
        error = f'Error: Problen when trying to update TreeView - {e}'
        logs(error)
        showerror('Error', 'Problem when trying to update the TreeView')


def update_graph(t, canvas):
    info = graph()
    t.clear()
    t.set_title('Expenses graph')
    t.plot(info['count'], info['altitud'], color='red')
    canvas.draw()


def validate_export(extension, type):

    file_path = asksaveasfilename(
        title='Save Export',
        defaultextension=f'.{extension}',
        filetypes=[(f'{type} files', f'*.{extension}')],
        initialdir=os.path.join(os.path.expanduser('~'), 'Downloads'),
        initialfile='export'
    )

    if not file_path:
        showinfo('Save Cancelled', 'No name provided')

    with open(file_path, 'w') as file:
        file.write('')

    return file_path
    

def validate_name(name):
    try:
        if not re.match(r'^(([a-z]+)(-?)([a-zA-Z]*)){4,}$', name):
            raise ValueError('Name not allowed')
        
        return True
    except ValueError as e:
        logs(e)


def validate_cost(number):
    try:
        if not re.match(r'^(\d+)$', str(number)):
            raise ValueError('Cost patron not allowed')
        
        return True
    except ValueError as e:
        logs(e)
    

def validate_is_numeric(value):
    try:
        if not value.isdigit():
            raise ValueError('Value is not a digit')
        
        return True
    except ValueError as e:
        logs(e)


def validate_is_text(value):
    try:
        if not value.isalpha():
            raise ValueError('Value is not a text')
        
        return True
    except ValueError as e:
        logs(e)


def validate_input(option_var, search, validate_num, validate_text):
    selection = option_var.get()

    if selection == 'ID' or selection == '$':
        search.configure(validate='key', validatecommand=(validate_num, '%P'))

    if selection == 'NAME':
        search.configure(validate='key', validatecommand=(validate_text, '%P'))
