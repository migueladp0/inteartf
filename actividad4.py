# Actividad 4 - Métodos de aprendizaje no supervisado
# Miguel Angel Duran Penagos y Diego Fabian Giron Acosta

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans

# Lista de estaciones del sistema de transporte masivo
estaciones = [
    "portal-norte", "calle-100", "calle-72", "calle-45", "avenida-caracas",
    "calle-19", "portal-sur", "portal-80", "niza-calle-127", "suba-calle-100",
    "suba-calle-95", "suba-av-boyaca", "portal-suba", "avenida-68", "américas-carrera-53"
]

# Lista de coordenadas de las estaciones (ejemplo, reemplázalas con las coordenadas reales)
coordenadas = {
    "portal-norte": (10, 20),
    "calle-100": (15, 25),
    "calle-72": (20, 30),
    "calle-45": (25, 35),
    "avenida-caracas": (30, 40),
    "calle-19": (35, 45),
    "portal-sur": (40, 50),
    "portal-80": (45, 55),
    "niza-calle-127": (50, 60),
    "suba-calle-100": (55, 65),
    "suba-calle-95": (60, 70),
    "suba-av-boyaca": (65, 75),
    "portal-suba": (70, 80),
    "avenida-68": (75, 85),
    "américas-carrera-53": (80, 90)
}

# Convertir las coordenadas a DataFrame
df_coord = pd.DataFrame(list(coordenadas.values()), columns=['Coord_X', 'Coord_Y'], index=coordenadas.keys())

# Agrupar las estaciones en clusters utilizando K-Means
kmeans = KMeans(n_clusters=3, random_state=42).fit(df_coord)
df_coord['Cluster'] = kmeans.labels_

# Mostrar el DataFrame con las coordenadas y los clusters asignados
print("Coordenadas y clusters asignados a las estaciones:")
print(df_coord)

# Crear el grafo de estaciones y conexiones
G = nx.Graph()

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
    ("avenida-68", "américas-carrera-53", {'weight': 7, 'distancia': '7 km'}),
    # Añadimos las conexiones inversas
    ("calle-100", "portal-norte", {'weight': 10, 'distancia': '10 km'}),
    ("calle-72", "calle-100", {'weight': 5, 'distancia': '5 km'}),
    ("calle-45", "calle-72", {'weight': 5, 'distancia': '5 km'}),
    ("avenida-caracas", "calle-45", {'weight': 3, 'distancia': '3 km'}),
    ("calle-19", "avenida-caracas", {'weight': 4, 'distancia': '4 km'}),
    ("portal-sur", "calle-19", {'weight': 12, 'distancia': '12 km'}),
    ("niza-calle-127", "portal-norte", {'weight': 7, 'distancia': '7 km'}),
    ("suba-calle-100", "niza-calle-127", {'weight': 6, 'distancia': '6 km'}),
    ("suba-calle-95", "suba-calle-100", {'weight': 2, 'distancia': '2 km'}),
    ("suba-av-boyaca", "suba-calle-95", {'weight': 5, 'distancia': '5 km'}),
    ("portal-suba", "suba-av-boyaca", {'weight': 8, 'distancia': '8 km'}),
    ("avenida-68", "portal-80", {'weight': 10, 'distancia': '10 km'}),
    ("américas-carrera-53", "avenida-68", {'weight': 7, 'distancia': '7 km'})
]

# Agregar aristas (conexiones) con atributos al grafo
G.add_edges_from(conexiones)

# Visualización del grafo
plt.figure(figsize=(10, 6))
nx.draw(G, pos=coordenadas, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
plt.title("Grafo de Estaciones de Transporte Masivo")
plt.show()
