import networkx as nx
import matplotlib.pyplot as plt
from ipywidgets import interact, Dropdown
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder

# Crear el grafo de estaciones y conexiones
G = nx.Graph()

# Lista de estaciones del sistema de transporte masivo
estaciones = [
    "Portal Norte", "Calle 100", "Calle 72", "Calle 45", "Avenida Caracas",
    "Calle 19", "Portal Sur", "Portal 80", "Niza Calle 127", "Suba Calle 100",
    "Suba Calle 95", "Suba Av. Boyacá", "Portal Suba", "Avenida 68", "Américas Carrera 53"
]

# Lista de conexiones entre las estaciones con pesos (distancias)
conexiones = [
    ("Portal Norte", "Calle 100", {'weight': 10, 'distancia': '10 km'}),
    ("Calle 100", "Calle 72", {'weight': 5, 'distancia': '5 km'}),
    ("Calle 72", "Calle 45", {'weight': 5, 'distancia': '5 km'}),
    ("Calle 45", "Avenida Caracas", {'weight': 3, 'distancia': '3 km'}),
    ("Avenida Caracas", "Calle 19", {'weight': 4, 'distancia': '4 km'}),
    ("Calle 19", "Portal Sur", {'weight': 12, 'distancia': '12 km'}),
    ("Portal Norte", "Niza Calle 127", {'weight': 7, 'distancia': '7 km'}),
    ("Niza Calle 127", "Suba Calle 100", {'weight': 6, 'distancia': '6 km'}),
    ("Suba Calle 100", "Suba Calle 95", {'weight': 2, 'distancia': '2 km'}),
    ("Suba Calle 95", "Suba Av. Boyacá", {'weight': 5, 'distancia': '5 km'}),
    ("Suba Av. Boyacá", "Portal Suba", {'weight': 8, 'distancia': '8 km'}),
    ("Portal 80", "Avenida 68", {'weight': 10, 'distancia': '10 km'}),
    ("Avenida 68", "Américas Carrera 53", {'weight': 7, 'distancia': '7 km'}),
    ("Portal Sur", "Portal 80", {'weight': 9, 'distancia': '9 km'}),
    ("Américas Carrera 53", "Portal 80", {'weight': 11, 'distancia': '11 km'})
]

# Agregar nodos (estaciones) al grafo
G.add_nodes_from(estaciones)
# Agregar aristas (conexiones) con atributos al grafo
G.add_edges_from(conexiones)

# Generar datos ficticios para el tiempo de viaje entre estaciones
datos = []
for conexion in conexiones:
    estacion_origen, estacion_destino, atributos = conexion
    tiempo_viaje = atributos['weight']  # Utilizamos el peso como tiempo de viaje ficticio
    datos.append([estacion_origen, estacion_destino, tiempo_viaje])

# Crear un DataFrame de Pandas con datos ficticios más grandes
df = pd.DataFrame(datos * 3, columns=['Estacion_Origen', 'Estacion_Destino', 'Tiempo_Viaje'])

# Codificar las variables categóricas usando One-Hot Encoding
encoder = OneHotEncoder(handle_unknown='ignore')
X = encoder.fit_transform(df[['Estacion_Origen', 'Estacion_Destino']])

# Dividir los datos en conjunto de entrenamiento y prueba
y = df['Tiempo_Viaje']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar un modelo de regresión lineal
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Función para predecir el tiempo de viaje entre dos estaciones
def predecir_tiempo_viaje(estacion_origen, estacion_destino):
    """
    Función para predecir el tiempo de viaje entre dos estaciones.
    
    Parameters:
        estacion_origen (str): Nombre de la estación de origen.
        estacion_destino (str): Nombre de la estación de destino.
    """
    if estacion_origen not in estaciones or estacion_destino not in estaciones:
        print("Error: Estación no válida. Por favor, seleccione estaciones válidas.")
        return
    entrada = encoder.transform([[estacion_origen, estacion_destino]])
    tiempo_predicho = modelo.predict(entrada)
    print("Tiempo de viaje predicho de {} a {}: {:.2f} minutos".format(estacion_origen, estacion_destino, tiempo_predicho[0]))

# Visualizar el grafo de estaciones y conexiones de manera más estética
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
labels = nx.get_edge_attributes(G, 'distancia')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Red de Transporte Masivo - Estaciones y Conexiones")
plt.show()

# Interactividad con widgets para predecir el tiempo de viaje
dropdown_inicio = Dropdown(options=estaciones, description='Punto de inicio:')
dropdown_destino = Dropdown(options=estaciones, description='Punto de destino:')
interact(predecir_tiempo_viaje, estacion_origen=dropdown_inicio, estacion_destino=dropdown_destino);
