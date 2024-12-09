from database.database import *
from logs.logs import *
from utils.controller import *
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter.messagebox import showerror


def db_connect():
    connection()
    create_table()
    ok = 'OK DB CONNECTION ESTABLISHED'
    logs(ok)

def main():
    db_connect()
    try:
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
        
        def call_filter_treeview(event):
            filter_treeview(tree, search, option_var)

        search = ttk.Entry(left_frame, width=20, font=('Arial', 13))
        search.grid(row=0, column=0, pady=10, padx=10, sticky=W)
        search.bind('<KeyRelease>', call_filter_treeview)

        option_var = StringVar(value='ID')
        options = ['ID','$','DATE','NAME']

        option_menu = OptionMenu(left_frame, option_var, *options)
        option_menu.grid(row=0, column=1, sticky=E, padx=9)

        def call_validate_input():
            validate_input(option_var, search, validate_num, validate_text)

        option_var.trace_add("write", lambda *args: validate_input(option_var, search, validate_num, validate_text))

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

        def call_edit_element(event):
            edit_element(tree, t, canvas)

        tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=N+S+E+W)
        tree.bind("<Double-1>", call_edit_element)

        button_sell = ttk.Button(root, text='Sell', command=lambda: delete_element(t, canvas, tree))
        button_sell.grid(row=2,column=0, sticky=W, padx=10)

        def call_save_graph():
            save_graph(fig)

        right_down_frame = Frame(right_frame)
        right_down_frame.grid(row=1, column=0, padx=30, pady=5, sticky=S+E+W, columnspan=5)
        right_down_frame.configure(bg="#353535")

        label_down = ttk.Label(right_down_frame, text='Buy a new product', font=('Arial', 20))
        label_down.grid(row=1, column=0, sticky=W, pady=10)
        label_down.configure(background='#353535', foreground='#fff')

        btn_download_graph = ttk.Button(right_down_frame, text='Get Graph', command=call_save_graph)
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

        def call_create_element():
            create_element(tree, label_error, input_name, input_cost, t, canvas)

        button_buy = ttk.Button(right_down_frame, text='comprar', command=call_create_element)
        button_buy.grid(row=7,column=0, sticky=W, pady=5)

        update_treeview(tree)

        root.mainloop()
    except Exception as e:
        print(e)
        logs(f'Error on views - {e}')
        showerror('Ups!', 'Problem trying to rendering the app view...')