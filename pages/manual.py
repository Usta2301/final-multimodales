import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Configuración general de la página
st.set_page_config(
    page_title="🚦 Control de Acceso Manual",
    page_icon="🔐",
    layout="centered"
)

# Encabezado atractivo
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="color:#2c3e50;">🔧 Panel de Control Manual</h1>
        <p style="color:#555;">Controla manualmente el acceso enviando señales MQTT</p>
        <hr style="margin-top:20px; margin-bottom:30px;">
    </div>
""", unsafe_allow_html=True)

# Mostrar versión de Python
st.markdown(f"<span style='color: #888;'>🧪 Versión de Python:</span> <b>{platform.python_version()}</b>", unsafe_allow_html=True)
st.markdown("---")

# Variables
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
    st.success(f"📨 Mensaje recibido: `{message_received}`")

# Configuración MQTT
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("Ustayalejandro")
client1.on_message = on_message

# Contenedor visual con botones grandes
with st.container():
    st.markdown("<h4 style='color:#34495e;'>📲 Enviar Comando:</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🟢 Abrir Acceso", use_container_width=True):
            act1 = "CKN 364"
            client1 = paho.Client("Ustayalejandro")
            client1.on_publish = on_publish
            client1.connect(broker, port)
            message = json.dumps({"Gesto": act1})
            ret = client1.publish("Usta", message)
            st.success("✅ Comando 'Abrir' enviado correctamente.")

    with col2:
        if st.button("🔴 Cerrar Acceso", use_container_width=True):
            act1 = "MXL 931"
            client1 = paho.Client("Ustayalejandro")
            client1.on_publish = on_publish
            client1.connect(broker, port)
            message = json.dumps({"Gesto": act1})
            ret = client1.publish("Usta", message)
            st.success("✅ Comando 'Cerrar' enviado correctamente.")
