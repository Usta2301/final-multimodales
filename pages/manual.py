import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Configuración de página
st.set_page_config(page_title="🚪 Control Manual MQTT", layout="centered")

# Encabezado
st.markdown("<h1 style='text-align: center; color: #2E8B57;'>🔧 Control Manual MQTT</h1>", unsafe_allow_html=True)
st.markdown("---")

# Mostrar versión de Python
st.markdown(f"📦 <b>Versión de Python:</b> {platform.python_version()}", unsafe_allow_html=True)

# Variables globales
values = 0.0
act1 = "OFF"

# Funciones MQTT
def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(f"📩 Mensaje recibido: `{message_received}`")

# Configuración MQTT
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("Ustayalejandro")
client1.on_message = on_message

# Botón "Abrir"
if st.button("🟢 Abrir"):
    act1 = "CKN 364"
    client1 = paho.Client("Ustayalejandro")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Gesto": act1})
    ret = client1.publish("Usta", message)

# Espaciado visual
st.markdown("<br>", unsafe_allow_html=True)

# Botón "Cerrar"
if st.button("🔴 Cerrar"):
    act1 = "MXL 931"
    client1 = paho.Client("Ustayalejandro")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Gesto": act1})
    ret = client1.publish("Usta", message)
