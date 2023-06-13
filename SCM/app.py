import tkinter as tk
import requests
import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

def get_data():
    
    response = requests.get("API_URL")
    data = json.loads(response.text)
    return data

def update_graph():
    
    data = get_data()

    graph.clear()

    for node in data['nodes']:
        graph.add_node(node['id'], production_rate=node['production_rate'], sale_rate=node['sale_rate'],
                       kpi_production=node['kpi_production'], kpi_sale=node['kpi_sale'])

    for edge in data['edges']:
        graph.add_edge(edge['from'], edge['to'])

    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue')
    plt.title('Supply Chain Network')
    plt.axis('off')
    canvas.draw()

#Function to add relationship
def add_relationship():
    
    add_window = tk.Toplevel(window)
    add_window.title("Add Relationship")

    def handle_add():
        category = category_var.get()
        name = name_entry.get()

        if category == 'Manufacturer':
            new_relationship = {'from': name, 'to': 'warehouse'}
        elif category == 'Warehouse':
            new_relationship = {'from': 'manufacturer', 'to': name}
        else:  
            new_relationship = {'from': 'warehouse', 'to': name}

        data['edges'].append(new_relationship)

        update_graph()

        add_window.destroy()

    category_label = tk.Label(add_window, text="Select Category:")
    category_label.pack()

    category_var = tk.StringVar(add_window)
    category_var.set("Manufacturer")
    category_dropdown = tk.OptionMenu(add_window, category_var, "Manufacturer", "Warehouse", "Shop")
    category_dropdown.pack()

    name_label = tk.Label(add_window, text="Enter Name:")
    name_label.pack()

    name_entry = tk.Entry(add_window)
    name_entry.pack()

    add_button = tk.Button(add_window, text="Add", command=handle_add)
    add_button.pack()

# Function to show manufacturer data
def show_manufacturer_data():
   
    manufacturer_window = tk.Toplevel(window)
    manufacturer_window.title("Show Manufacturer Data")

    def handle_show():
        manufacturer_id = manufacturer_entry.get()

        manufacturer = None
        for node in data['nodes']:
            if node['id'] == manufacturer_id:
                manufacturer = node
                break

        if manufacturer:
            production_rate = manufacturer['production_rate']
            kpi_production = manufacturer['kpi_production']

            result_label.config(text=f"Production Rate: {production_rate}\nKPI (Production): {kpi_production}")
        else:
            result_label.config(text="Manufacturer not found")

    manufacturer_label = tk.Label(manufacturer_window, text="Enter Manufacturer ID:")
    manufacturer_label.pack()

    manufacturer_entry = tk.Entry(manufacturer_window)
    manufacturer_entry.pack()

    show_button = tk.Button(manufacturer_window, text="Show", command=handle_show)
    show_button.pack()

    result_label = tk.Label(manufacturer_window, text="")
    result_label.pack()

# Function to show shop data
def show_shop_data():
    
    shop_window = tk.Toplevel(window)
    shop_window.title("Show Shop Data")

    def handle_show():
        shop_id = shop_entry.get()

        shop = None
        for node in data['nodes']:
            if node['id'] == shop_id:
                shop = node
                break

        if shop:
            sale_rate = shop['sale_rate']
            kpi_sale = shop['kpi_sale']

            result_label.config(text=f"Sale Rate: {sale_rate}\nKPI (Sale): {kpi_sale}")
        else:
            result_label.config(text="Shop not found")

    shop_label = tk.Label(shop_window, text="Enter Shop ID:")
    shop_label.pack()

    shop_entry = tk.Entry(shop_window)
    shop_entry.pack()

    show_button = tk.Button(shop_window, text="Show", command=handle_show)
    show_button.pack()

    result_label = tk.Label(shop_window, text="")
    result_label.pack()

window = tk.Tk()
window.title("Supply Chain Management")

graph_frame = tk.Frame(window)
graph_frame.pack(padx=10, pady=10)

figure = plt.figure(figsize=(6, 4))
canvas = FigureCanvasTkAgg(figure, master=graph_frame)
canvas.get_tk_widget().pack()

update_button = tk.Button(window, text="Update Graph", command=update_graph)
update_button.pack(pady=10)

add_relationship_button = tk.Button(window, text="Add Relationship", command=add_relationship)
add_relationship_button.pack(pady=10)

manufacturer_button = tk.Button(window, text="Show Manufacturer Data", command=show_manufacturer_data)
manufacturer_button.pack(pady=10)

shop_button = tk.Button(window, text="Show Shop Data", command=show_shop_data)
shop_button.pack(pady=10)

graph = nx.Graph()

data = get_data()

update_graph()

window.mainloop()
