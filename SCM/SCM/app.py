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

canvas = None  # Declare the canvas variable outside the function
maximized_graph_window = None  # Variable to store the maximized graph window

def update_graph():
    global canvas, maximized_graph_window  # Add global keyword to access the canvas and maximized_graph_window variables

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

    # Remove existing canvas if it exists
    if canvas is not None:
        canvas.get_tk_widget().destroy()

    # Create a FigureCanvasTkAgg instance to display the graph on the canvas
    canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def maximize_graph(event):
        global maximized_graph_window

        if maximized_graph_window is not None:
            return

        maximized_graph_window = tk.Toplevel(window)
        maximized_graph_window.title('Maximized Graph')
        maximized_graph_window.state('zoomed')  # Set the window to fullscreen

        def close_max_window():
            global maximized_graph_window
            maximized_graph_window.destroy()
            maximized_graph_window = None

        maximized_graph_window.protocol("WM_DELETE_WINDOW", close_max_window)  # Handle window close event

        max_canvas = FigureCanvasTkAgg(plt.gcf(), master=maximized_graph_window)
        max_canvas.draw()
        max_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Bind <Escape> key to close_max_window function
        maximized_graph_window.bind('<Escape>', lambda event: close_max_window())

    canvas.mpl_connect('button_press_event', maximize_graph)


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

    live_graph_window.after(5000, update_live_graph, canvas)

def update_live_graph(canvas):
    data = get_data()
    money = data['resource']['money']

    plt.clf()
    plt.plot([money] * 10)
    plt.xlabel('Time')
    plt.ylabel('Return Rate')
    plt.title('Return Rate Live Time Graph')

    canvas.draw()

    canvas.master.after(5000, update_live_graph, canvas)

def open_detail_page():
    detail_window = tk.Toplevel(window)
    detail_window.title("Show More Detail")
    detail_window.geometry('800x600')

    option_frame = tk.Frame(detail_window)
    option_frame.pack(padx=20, pady=20)

    button_frame = tk.Frame(detail_window)
    button_frame.pack()

    show_detail_button = tk.Button(button_frame, text="Show Detail", width=20, height=2)
    show_detail_button.pack()

    def show_category_detail(*args):
        category = category_var.get().capitalize()
        data = get_data()
        node_mapping = {
            'Factory': 0,
            'Distributor': 1,
            'Retailer': 2
        }

        if category not in node_mapping:
            return

        selected_node = data['node'][node_mapping[category]]

        if category == 'Factory':
            options = ['Production Rate', 'Target Production Rate', 'Reserve']
        elif category == 'Distributor' or category == 'Retailer':
            options = ['Sales Rate', 'Target Sales Rate', 'Reserve']

        def show_data_table():
            selected_option = option_var.get()
            column_names = ['No.', selected_option.title()]
            selected_option = selected_option.replace(' ', '_').lower()
            if selected_option not in selected_node:
                return
            data_list = selected_node[selected_option]
            table_title = selected_option.replace('_', ' ').title()

            for widget in detail_window.winfo_children():
                if isinstance(widget, tk.Frame) and widget != option_frame and widget != button_frame:
                    widget.destroy()

            table_frame = tk.Frame(detail_window)
            table_frame.pack(padx=20, pady=10)

            tree = ttk.Treeview(table_frame, columns=column_names, show='headings', height=10)
            tree.pack(side='left')

            for col in column_names:
                tree.heading(col, text=col)

            tree.column(column_names[0], width=50,anchor='center')  # Adjust the width of the first column
            tree.column(column_names[1], width=550,anchor='center')  # Adjust the width of the second column

            for i, data in enumerate(data_list, start=1):
                tree.insert('', 'end', values=(i, data))

            scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
            scrollbar.pack(side='right', fill='y')

            tree.configure(yscrollcommand=scrollbar.set)

            table_frame.update()
            detail_window.geometry(f'800x{table_frame.winfo_height() + 100}')

        for widget in option_frame.winfo_children():
            widget.destroy()

        option_label = tk.Label(option_frame, text="Select Data:")
        option_label.pack()
        option_var = tk.StringVar()
        option_dropdown = tk.OptionMenu(option_frame, option_var, *options)
        option_dropdown.config(width=30)
        option_dropdown.pack()

        show_detail_button.pack()

        show_detail_button.configure(command=show_data_table, width=20, height=2)

    category_label = tk.Label(detail_window, text="Select Category:")
    category_label.pack()
    category_var = tk.StringVar()
    category_dropdown = tk.OptionMenu(detail_window, category_var, "Factory", "Distributor", "Retailer")
    category_dropdown.config(width=30)
    category_dropdown.pack()

    show_detail_button.pack_forget()

    category_var.trace_add('write', show_category_detail)

window = tk.Tk()
window.title("Supply Chain Management")

graph_frame = tk.Frame(window)
graph_frame.pack(padx=10, pady=10)

figure = plt.figure(figsize=(6, 4))
canvas = FigureCanvasTkAgg(figure, master=graph_frame)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

update_button = tk.Button(window, text="Update Graph", command=update_graph)
update_button.pack(pady=10)

live_graph_button = tk.Button(window, text="Open Live-Time Graph", command=open_live_graph)
live_graph_button.pack(pady=10)

show_detail_button = tk.Button(window, text="Show More Detail", command=open_detail_page)
show_detail_button.pack(pady=10)

window.mainloop()



