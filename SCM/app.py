import tkinter as tk
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

    graph = nx.DiGraph()  # Directed graph to represent the relationships

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

window.mainloop()
