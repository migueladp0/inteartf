# Actividad 4 - Métodos de aprendizaje no supervisado
# Miguel Angel Duran Penagos y Diego Fabian Giron Acosta

import networkx as nx
import matplotlib.pyplot as plt
from ipywidgets import interact, Dropdown
import pandas as pd
from sklearn.cluster import KMeans

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

# Agregar nodos (estaciones) al grafo
G.add_nodes_from(estaciones)
# Agregar aristas (conexiones) con atributos al grafo
G.add_edges_from(conexiones)

# Generar datos para el tiempo de viaje entre estaciones
datos = []
for conexion in conexiones:
    estacion_origen, estacion_destino, atributos = conexion
    tiempo_viaje = atributos['weight']  # Utilizamos el peso como tiempo de viaje
    datos.append([estacion_origen, estacion_destino, tiempo_viaje])

# Convertir los datos a un DataFrame de Pandas
df = pd.DataFrame(datos, columns=['Estacion_Origen', 'Estacion_Destino', 'Tiempo_Viaje'])

# Agrupar las estaciones en clusters utilizando K-Means
X = df[['Tiempo_Viaje']]
kmeans = KMeans(n_clusters=3, random_state=42).fit(X)
df['Cluster'] = kmeans.labels_

# Visualización de clusters
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G)
colors = ['r', 'g', 'b']
for cluster in set(df['Cluster']):
    nodes = df[df['Cluster'] == cluster]['Estacion_Origen'].tolist()
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=colors[cluster], label=f'Cluster {cluster}')
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)
plt.legend()
plt.show()

# Función para predecir el tiempo de viaje entre dos estaciones
def predecir_tiempo_viaje(estacion_origen, estacion_destino):
    if estacion_origen not in estaciones or estacion_destino not in estaciones:
        print("Una o ambas estaciones seleccionadas no existen en los datos.")
        return

    # Filtrar filas donde la estación de origen es igual a la estación origen seleccionada
    filtro_origen = df['Estacion_Origen'] == estacion_origen
    # Filtrar filas donde la estación de destino es igual a la estación destino seleccionada
    filtro_destino = df['Estacion_Destino'] == estacion_destino

    if filtro_origen.any() and filtro_destino.any():
        cluster_origen = df.loc[filtro_origen, 'Cluster'].values[0]
        cluster_destino = df.loc[filtro_destino, 'Cluster'].values[0]

        if cluster_origen == cluster_destino:
            tiempo_predicho = df.loc[(filtro_origen) & (filtro_destino), 'Tiempo_Viaje'].values[0]
            print(f"Tiempo de viaje predicho de {estacion_origen} a {estacion_destino}: {tiempo_predicho:.2f} minutos")
        else:
            # Alternativamente podrías implementar una predicción para estaciones en diferentes clusters
            print("Las estaciones seleccionadas no están en el mismo cluster. No se puede hacer una predicción.")
    else:
        print("Una o ambas estaciones seleccionadas no existen en los datos.")

# Interactividad con widgets
dropdown_inicio = Dropdown(options=estaciones, description='Punto de inicio:')
dropdown_destino = Dropdown(options=estaciones, description='Punto de destino:')
interact(predecir_tiempo_viaje, estacion_origen=dropdown_inicio, estacion_destino=dropdown_destino);
