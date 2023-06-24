import tkinter as tk
from tkinter import ttk
import requests
import json
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def get_data():
    response = requests.get('https://gist.githubusercontent.com/lobakkang/c74c810ccd86c78d543ebd5fead15fa3/raw/bc1bb87cff745521ca73180ebf885eafba3f08c1/gistfile1.txt')
    data = json.loads(response.text)
    return data


def update_graph():
    data = get_data()
    plt.clf()

    graph = nx.DiGraph()

    node_mapping = {
        0: 'factory',
        1: 'distributor',
        2: 'retailer'
    }

    for node in data['node']:
        node_type = node['type']
        if node_type in node_mapping.values():
            graph.add_node(node_type)

    for edge in data['edge']:
        direction = edge['direction']
        if direction[0] in node_mapping and direction[1] in node_mapping:
            provider = node_mapping[direction[0]]
            receiver = node_mapping[direction[1]]
            graph.add_edge(provider, receiver)

    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue')
    plt.title('Supply Chain Network')
    plt.axis('off')
    canvas.draw()


def open_live_graph():
    global live_graph_window

    live_graph_window = tk.Toplevel(window)
    live_graph_window.title("Return Rate Live Time Graph")
    live_graph_window.geometry('800x600')

    data = get_data()
    money = data['resource']['money']

    figure = plt.figure(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(figure, master=live_graph_window)
    canvas.get_tk_widget().pack()

    plt.plot([money] * 10)
    plt.xlabel('Time')
    plt.ylabel('Return Rate')
    plt.title('Return Rate Live Time Graph')

    canvas.draw()

def open_detail_page():
    detail_window = tk.Toplevel(window)
    detail_window.title("Show More Detail")
    detail_window.geometry('800x600')

    def show_category_detail(category):
        
        data = get_data()
        node_mapping = {
            'factory': 0,
            'distributor': 1,
            'retailer': 2
        }

        selected_node = data['node'][node_mapping[category]]

        if category == 'factory':
            options = ['production_rate', 'target_production_rate', 'reserve']
        elif category == 'distributor' or category == 'retailer':
            options = ['sales_rate', 'target_sales_rate', 'reserve']

        for widget in detail_window.winfo_children():
            widget.destroy()

        option_frame = tk.Frame(detail_window)
        option_frame.pack(padx=20, pady=20)

        option_label = tk.Label(option_frame, text="Select Data:")
        option_label.pack()
        option_var = tk.StringVar()
        option_dropdown = tk.OptionMenu(option_frame, option_var, *options)
        option_dropdown.pack()

        def show_data_table():
            selected_option = option_var.get()
            column_names = ['No.', selected_option.title()]
            data_list = selected_node[selected_option]
            table_title = selected_option.title()

            table_frame = tk.Frame(detail_window)
            table_frame.pack(padx=20, pady=10)

            tree = ttk.Treeview(table_frame, columns=column_names, show='headings')
            tree.pack(side='left')

            for col in column_names:
                tree.heading(col, text=col)

            for i, data in enumerate(data_list, start=1):
                tree.insert('', 'end', values=(i, data))

            scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
            scrollbar.pack(side='right', fill='y')

            tree.configure(yscrollcommand=scrollbar.set)

            table_frame.update()
            tree.config(height=table_frame.winfo_height() // 20)

            detail_window.geometry(f'800x{table_frame.winfo_height() + 100}')

        show_detail_button = tk.Button(option_frame, text="Show Detail", command=show_data_table)
        show_detail_button.pack()

    category_label = tk.Label(detail_window, text="Select Category:")
    category_label.pack()
    category_var = tk.StringVar()
    category_dropdown = tk.OptionMenu(detail_window, category_var, "factory", "distributor", "retailer")
    category_dropdown.pack()

    show_detail_button = tk.Button(detail_window, text="Show Detail", command=lambda: show_category_detail(category_var.get()))
    show_detail_button.pack()


window = tk.Tk()
window.title("Supply Chain Management")

graph_frame = tk.Frame(window)
graph_frame.pack(padx=10, pady=10)

figure = plt.figure(figsize=(6, 4))
canvas = FigureCanvasTkAgg(figure, master=graph_frame)
canvas.get_tk_widget().pack()

update_button = tk.Button(window, text="Update Graph", command=update_graph)
update_button.pack(pady=10)

live_graph_button = tk.Button(window, text="Open Live-Time Graph", command=open_live_graph)
live_graph_button.pack(pady=10)

graph = nx.Graph()

data = get_data()

update_graph()

option_var = tk.StringVar()

show_detail_button = tk.Button(window, text="Show More Detail", command=open_detail_page)
show_detail_button.pack(pady=10)

window.mainloop()


