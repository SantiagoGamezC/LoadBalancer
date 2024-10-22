#  Load Load Balancer con Flask y NGINX 

## Estructura del Proyecto
NGINX/Openresty: Balanceador de carga y enrutador de solicitudes. Utiliza un script en Lua para decidir a qué backend redirigir cada solicitud.
Flask: Proporciona calculo una puntuación para cada IP basado en su comportamiento.
TensorFlow: Un modelo entrenado para el analisis de comportamiento y asignacion de puntuacion de cada IP.

## Requisitos
Python 3.6+ con las siguientes bibliotecas:
Flask
TensorFlow
NumPy

NGINX 1.24+
Openresty 1.27+
Modelo TensorFlow entrenado

## Configuración
1. Configuración de NGINX
Upstream: Define los servidores backend y sus puertos que manejarán las solicitudes.
Codigo con Lua: Codigo en Lua que consulta al servicio Flask para obtener la puntuación de la IP solicitante, y con este redirigir el trafico.

2. Configuración de Flask
El servicio Flask expone un endpoint (/score_ip) que devuelve una puntuación. El sistema utiliza un modelo de TensorFlow para generar esta puntuación.

3. Uso del Modelo TensorFlow
El modelo scoring_model.h5 se utiliza para analizar el comportamiento de las solicitudes y asignarles una calificacion.

4. Funcionamiento
Cuando una IP hace una solicitud, NGINX consulta el servicio Flask para llamar al modelo tensorflow, asignarle una calificacion y regresarselo al balanceador de cargas. Dependiendo de la puntuación, la solicitud se dirige a uno de los servidores backend.

## Instalacion
NGINX/Openresty:
sudo apt update
sudo apt install nginx
sudo systemctl disable nginx
sudo systemctl stop nginx
sudo apt-get -y install --no-install-recommends wget gnupg ca-certificates lsb-release
wget -O - https://openresty.org/package/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/openresty.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/openresty.gpg] http://openresty.org/package/ubuntu $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/openresty.list > /dev/null
sudo apt-get update
sudo apt-get -y install openresty
sudo systemctl enable openresty
sudo systemctl start openresty
(Configuration file: /usr/local/openresty/nginx/conf/nginx.conf)
Para probar funcionamiento:
sudo openresty -t

Python:
sudo apt install python3-pip
Dentro de directorio para python:
python3 -m venv venv
. ./venv/bin/activate
pip install flask
pip install numpy
pip install tensorflow
Para correr el programa:
python3 pythonipconfig.py


Notas
La configuración actual asume que los servidores backend están en las direcciones IP y puertos especificados.
El modelo scoring_model.h5 debe ser entrenado previamente y disponible en el directorio donde se ejecuta el servidor Flask.
Es necesario descargar las librerias y dependencias necesarias.
El modelo se puede modificar y re-entrenar para satisfacer las necesidades de la red.
Cada se que modifica el archivo de configuracion de Openresty, se debe de correr el comando: sudo systemctl reload openresty
