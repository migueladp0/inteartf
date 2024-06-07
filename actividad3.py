# Actividad 3 - Métodos de aprendizaje supervisado
# Miguel Angel Duran Penagos y Diego Fabian Giron Acosta

import networkx as nx
import matplotlib.pyplot as plt
from ipywidgets import interact, Dropdown
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

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

# Generar datos ficticios para el tiempo de viaje entre estaciones
datos = []
for conexion in conexiones:
    estacion_origen, estacion_destino, atributos = conexion
    tiempo_viaje = atributos['weight']  # Utilizamos el peso como tiempo de viaje ficticio
    datos.append([estacion_origen, estacion_destino, tiempo_viaje])

# Convertir los datos a un DataFrame de Pandas
df = pd.DataFrame(datos, columns=['Estacion_Origen', 'Estacion_Destino', 'Tiempo_Viaje'])

# --- BEGIN_SOLUTION
# Codificar las variables categóricas usando One-Hot Encoding
encoder = OneHotEncoder(handle_unknown='ignore')
X = encoder.fit_transform(df[['Estacion_Origen', 'Estacion_Destino']])
# --- END_SOLUTION

# Dividir los datos en conjunto de entrenamiento y prueba
y = df['Tiempo_Viaje']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar un modelo de regresión lineal
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Función para predecir el tiempo de viaje entre dos estaciones
def predecir_tiempo_viaje(estacion_origen, estacion_destino):
    # --- BEGIN_SOLUTION
    # Codificar las estaciones de entrada usando el mismo encoder
    entrada = encoder.transform([[estacion_origen, estacion_destino]])
    # --- END_SOLUTION
    tiempo_predicho = modelo.predict(entrada)
    print("Tiempo de viaje predicho de {} a {}: {:.2f} minutos".format(estacion_origen, estacion_destino, tiempo_predicho[0]))


# Interactividad con widgets
dropdown_inicio = Dropdown(options=estaciones, description='Punto de inicio:')
dropdown_destino = Dropdown(options=estaciones, description='Punto de destino:')
interact(predecir_tiempo_viaje, estacion_origen=dropdown_inicio, estacion_destino=dropdown_destino);