import networkx as nx
import matplotlib.pyplot as plt
from ipywidgets import interact, Dropdown

# Crear el grafo de estaciones y conexiones
G = nx.Graph()

# Lista de estaciones del sistema de transporte masivo
estaciones = [
    "portal-norte", "calle-100", "calle-72", "calle-45", "avenida-caracas",
    "calle-19", "portal-sur", "portal-80", "niza-calle-127", "suba-calle-100",
    "suba-calle-95", "suba-av-boyaca", "portal-suba", "avenida-68", "américas-carrera-53"
]

# Lista de conexiones entre las estaciones con pesos (distancias)
conexiones = [
    ("portal-norte", "calle-100", {'weight': 10, 'distancia': '10 km'}),
    ("calle-100", "calle-72", {'weight': 5, 'distancia': '5 km'}),
    ("calle-72", "calle-45", {'weight': 5, 'distancia': '5 km'}),
    ("calle-45", "avenida-caracas", {'weight': 3, 'distancia': '3 km'}),
    ("avenida-caracas", "calle-19", {'weight': 4, 'distancia': '4 km'}),
    ("calle-19", "portal-sur", {'weight': 12, 'distancia': '12 km'}),
    ("portal-norte", "niza-calle-127", {'weight': 7, 'distancia': '7 km'}),
    ("niza-calle-127", "suba-calle-100", {'weight': 6, 'distancia': '6 km'}),
    ("suba-calle-100", "suba-calle-95", {'weight': 2, 'distancia': '2 km'}),
    ("suba-calle-95", "suba-av-boyaca", {'weight': 5, 'distancia': '5 km'}),
    ("suba-av-boyaca", "portal-suba", {'weight': 8, 'distancia': '8 km'}),
    ("portal-80", "avenida-68", {'weight': 10, 'distancia': '10 km'}),
    ("avenida-68", "américas-carrera-53", {'weight': 7, 'distancia': '7 km'})
]

# Agregar nodos (estaciones) al grafo
G.add_nodes_from(estaciones)
# Agregar aristas (conexiones) con atributos al grafo
G.add_edges_from(conexiones)

# Crear listas desplegables para seleccionar la estación de inicio y destino
dropdown_inicio = Dropdown(options=estaciones, description='Punto de inicio:')
dropdown_destino = Dropdown(options=estaciones, description='Punto de destino:')

# Definir la función de cálculo de ruta
def calcular_ruta(inicio, fin):
    # Calcular la ruta más corta entre dos estaciones
    try:
        ruta = nx.shortest_path(G, inicio, fin, weight="weight")
        print("Ruta encontrada:", ruta)
        distancia_total = nx.shortest_path_length(G, inicio, fin, weight="weight")
        print("Distancia total:", distancia_total, "km")

        # Graficar el grafo con la ruta encontrada
        pos = nx.circular_layout(G)  # Disposición circular de las estaciones
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray")
        labels = nx.get_edge_attributes(G, 'distancia')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)  # Etiquetas de distancia en las aristas
        nx.draw_networkx_edges(G, pos, edgelist=[(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)], width=3, edge_color="blue", alpha=0.5)
        plt.title('Ruta más corta desde {} hasta {}'.format(inicio, fin), fontsize=15)
        plt.show()
    except nx.NetworkXNoPath:
        print("No hay una ruta directa entre las estaciones seleccionadas.")
        try:
            # Calcular una ruta alternativa entre dos estaciones si no hay ruta directa
            ruta_alternativa = nx.shortest_path(G, inicio, fin)
            print("Ruta alternativa encontrada:", ruta_alternativa)
            distancia_total_alternativa = nx.shortest_path_length(G, inicio, fin)
            print("Distancia total de la ruta alternativa:", distancia_total_alternativa, "km")

            # Graficar el grafo con la ruta alternativa encontrada
            nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray")
            nx.draw_networkx_edges(G, pos, edgelist=[(ruta_alternativa[i], ruta_alternativa[i+1]) for i in range(len(ruta_alternativa)-1)], width=3, edge_color="red", alpha=0.5)
            plt.title('Ruta alternativa desde {} hasta {}'.format(inicio, fin), fontsize=15)
            plt.show()
        except nx.NetworkXNoPath:
            print("No hay una ruta entre las estaciones seleccionadas.")

# Interactividad con widgets
interact(calcular_ruta, inicio=dropdown_inicio, fin=dropdown_destino);
