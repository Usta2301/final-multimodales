import os
import streamlit as st
import base64
from openai import OpenAI
import paho.mqtt.client as paho
import json
import time
from IPython.display import Audio

def on_publish(client, userdata, result):
    print("El dato ha sido publicado\n")

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)
    if message_received == "Sonido":
        sound_file = 'hum_high.mp3'
        display(Audio(sound_file, autoplay=True))

# MQTT Config
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("Usta456")
client1.on_message = on_message

# Función para codificar imagen
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# Configuración de página
st.set_page_config(
    page_title="🔍 Análisis de Imagen Inteligente",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Encabezado
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 Análisis de Imagen</h1>", unsafe_allow_html=True)
st.markdown("---")

# Entrada de clave API
with st.sidebar:
    st.markdown("### 🔑 Ingresa tu API Key")
    ke = st.text_input('Clave de OpenAI', type="password")
    os.environ['OPENAI_API_KEY'] = ke
    api_key = os.environ['OPENAI_API_KEY']

# Subida de imagen
uploaded_file = st.file_uploader("📤 Sube una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.expander("🖼️ Vista previa de la imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# Toggle para detalles adicionales
show_details = st.toggle("➕ Añadir detalles sobre la imagen", value=True)
additional_details = "Responde solo con las letras y número grandes que aparecen en la imagen"

# Botón para analizar
analyze_button = st.button("🚀 Analizar imagen")

# Lógica principal
if uploaded_file is not None and api_key and analyze_button:
    with st.spinner("🔍 Analizando imagen..."):
        base64_image = encode_image(uploaded_file)

        prompt_text = "Describe what you see in the image in Spanish"

        if show_details and additional_details:
            prompt_text += f"\n\nContexto adicional proporcionado por el usuario:\n{additional_details}"

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ],
            }
        ]

        try:
            full_response = ""
            message_placeholder = st.empty()

            for completion in client.chat.completions.create(
                model="gpt-4o", messages=messages,
                max_tokens=1200, stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

                    client1 = paho.Client("Usta456")
                    client1.on_publish = on_publish
                    client1.connect(broker, port)
                    message = json.dumps({"Gesto": full_response})
                    ret = client1.publish("Usta", message)

        except Exception as e:
            st.error(f"🚨 Ocurrió un error: {e}")

else:
    if not uploaded_file and analyze_button:
        st.warning("⚠️ Por favor sube una imagen.")
    if not api_key:
        st.warning("⚠️ Por favor ingresa tu API Key.")

# Mostrar resultado final
if st.button("📤 Enviar respuesta"):
    try:
        st.write(full_response)
        message_placeholder.markdown(full_response)
    except:
        st.warning("⚠️ Aún no se ha generado ninguna respuesta.")
