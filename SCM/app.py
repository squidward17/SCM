import tkinter as tk
import requests
import json
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_data():
    response = requests.get('https://raw.githubusercontent.com/lobakkang/TruLogic/main/data/scenario/scene1.json')
    data = json.loads(response.text)
    return data

def update_graph():
    data = get_data()
    plt.clf()

    for node in data['node']:
        graph.add_node(node['id'], production_rate=node['production_rate'], sale_rate=node['sale_rate'],
                       kpi_production=node['kpi_production'], kpi_sale=node['kpi_sale'])

    for edge in data['edge']:
        graph.add_edge(edge['from'], edge['to'])

    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue')
    plt.title('Supply Chain Network')
    plt.axis('off')
    canvas.draw()

def show_manufacturer_data():
    manufacturer_window = tk.Toplevel(window)
    manufacturer_window.title("Show Manufacturer Data")

    def handle_show():
        manufacturer_id = manufacturer_entry.get()

        manufacturer = None
        for node in data['node']:
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

def show_shop_data():
    shop_window = tk.Toplevel(window)
    shop_window.title("Show Shop Data")

    def handle_show():
        shop_id = shop_entry.get()

        shop = None
        for node in data['node']:
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

def open_live_graph():
    global live_graph_window

    live_graph_window = tk.Toplevel(window)
    live_graph_window.title("Live-Time Rate of Return")
    live_graph_window.geometry('800x600')

    data = get_data()
    rates = data['rates']

    figure = plt.figure(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(figure, master=live_graph_window)
    canvas.get_tk_widget().pack()

    plt.plot(rates)
    plt.xlabel('Time')
    plt.ylabel('Rate of Return')
    plt.title('Live-Time Rate of Return')

    canvas.draw()

window = tk.Tk()
window.title("Supply Chain Management")

graph_frame = tk.Frame(window)
graph_frame.pack(padx=10, pady=10)

figure = plt.figure(figsize=(6, 4))
canvas = FigureCanvasTkAgg(figure, master=graph_frame)
canvas.get_tk_widget().pack()

update_button = tk.Button(window, text="Update Graph", command=update_graph)
update_button.pack(pady=10)

manufacturer_button = tk.Button(window, text="Show Manufacturer Data", command=show_manufacturer_data)
manufacturer_button.pack(pady=10)

shop_button = tk.Button(window, text="Show Shop Data", command=show_shop_data)
shop_button.pack(pady=10)

live_graph_button = tk.Button(window, text="Open Live-Time Graph", command=open_live_graph)
live_graph_button.pack(pady=10)

graph = nx.Graph()

data = get_data()

update_graph()

window.mainloop()

