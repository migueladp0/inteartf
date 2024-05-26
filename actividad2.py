import networkx as nx
import matplotlib.pyplot as plt

# Crear el grafo de estaciones y conexiones.
G = nx.Graph()

estaciones = [
    "portal-norte", "calle-100", "calle-72", "calle-45", "avenida-caracas",
    "calle-19", "portal-sur", "portal-80", "niza-calle-127", "suba-calle-100",
    "suba-calle-95", "suba-av-boyaca", "portal-suba", "avenida-68", "américas-carrera-53"
]

conexiones = [
    ("portal-norte", "calle-100", 10),
    ("calle-100", "calle-72", 5),
    ("calle-72", "calle-45", 5),
    ("calle-45", "avenida-caracas", 3),
    ("avenida-caracas", "calle-19", 4),
    ("calle-19", "portal-sur", 12),
    ("portal-norte", "niza-calle-127", 7),
    ("niza-calle-127", "suba-calle-100", 6),
    ("suba-calle-100", "suba-calle-95", 2),
    ("suba-calle-95", "suba-av-boyaca", 5),
    ("suba-av-boyaca", "portal-suba", 8),
    ("portal-80", "avenida-68", 10),
    ("avenida-68", "américas-carrera-53", 7)
]

G.add_nodes_from(estaciones)
G.add_weighted_edges_from(conexiones)

# Solicitar al usuario los puntos de inicio y fin.
inicio = input("Ingrese el punto de inicio: ").strip().lower().replace(' ', '-')
fin = input("Ingrese el punto de destino: ").strip().lower().replace(' ', '-')

# Calcular la ruta más corta entre dos estaciones
try:
    ruta = nx.shortest_path(G, inicio, fin, weight="weight")
    print("Ruta encontrada:", ruta)

    # Graficar el grafo con la ruta encontrada
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold")
    nx.draw_networkx_edges(G, pos, edgelist=[(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)], width=2.5, edge_color="r")
    plt.show()
except nx.NetworkXNoPath:
    print("No hay ruta entre las estaciones seleccionadas.")

