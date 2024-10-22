#  Load Load Balancer con Flask y NGINX 

## Estructura del Proyecto
NGINX: Actúa como balanceador de carga y enrutador de solicitudes. Utiliza un script en Lua para decidir a qué backend redirigir cada solicitud en función de la puntuación de la IP obtenida de un servicio Flask.
Flask: Proporciona un servicio REST que calcula una puntuación para cada IP en función de la frecuencia de las solicitudes. La puntuación se utiliza para dirigir las solicitudes a uno de los servidores backend.
TensorFlow: Un modelo entrenado en TensorFlow (scoring_model.h5) se utiliza para predecir la "puntuación" de una IP basada en la cantidad de solicitudes que realiza en los últimos 60 segundos.

## Requisitos
Python 3.6+ con las siguientes bibliotecas:

Flask
TensorFlow
NumPy
NGINX con soporte para Lua. Puedes instalar el paquete nginx-extras que incluye soporte para Lua.

Modelo TensorFlow: Debes tener un archivo scoring_model.h5 que haya sido previamente entrenado para predecir las puntuaciones de las IPs.

## Configuración
1. Configuración de NGINX
El archivo de configuración de NGINX incluye una sección para cada uno de los servidores backend. Aquí un resumen de las configuraciones claves:

Upstream: Define tres servidores backend (puertos 8081, 8082, y 8083 en la IP 192.168.7.157) que manejarán las solicitudes.
Lua Script: NGINX utiliza un script en Lua que consulta al servicio Flask (http://127.0.0.1:5000/score_ip) para obtener la puntuación de la IP solicitante. Dependiendo de la puntuación, la solicitud se dirige a uno de los servidores backend.

 2. Configuración de Flask
El servicio Flask expone un endpoint (/score_ip) que devuelve una puntuación basada en la frecuencia de solicitudes de la IP. El sistema utiliza un modelo de TensorFlow para generar esta puntuación.
3. Uso del Modelo TensorFlow
El modelo scoring_model.h5 debe ser un modelo entrenado que pueda predecir la carga basada en la cantidad de solicitudes recibidas en un período corto (en este caso, 60 segundos).

4. Despliegue
Configurar y ejecutar NGINX con la configuración especificada. Asegúrate de que los servidores backend (8081, 8082, 8083) estén funcionando.
```python
python app.py
```

5. Funcionamiento
Cuando una IP hace una solicitud, NGINX consulta el servicio Flask para obtener una puntuación basada en la frecuencia de solicitudes de esa IP. Dependiendo de la puntuación, la solicitud se dirige a uno de los servidores backend.

Notas
La configuración actual asume que los servidores backend están en las direcciones IP y puertos especificados. Asegúrate de ajustar esto según tu entorno.
El modelo scoring_model.h5 debe ser entrenado previamente y disponible en el directorio donde se ejecuta el servidor Flask.
