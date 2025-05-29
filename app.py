import os
import streamlit as st
import base64
from openai import OpenAI
import paho.mqtt.client as paho
import json
import time

# MQTT
def on_publish(client, userdata, result):
    print("📡 Mensaje MQTT publicado")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(f"📨 Mensaje recibido: {message_received}")

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("Usta456")
client1.on_message = on_message

# Imagen → base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# Configuración visual
st.set_page_config(page_title="🔍 Análisis de Imagen", layout="centered")
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: #2ecc71;'>🤖 Análisis de Imágenes con IA</h1>
        <p style='color: #555;'>Sube una imagen y extrae letras o números grandes visibles.</p>
        <hr>
    </div>
""", unsafe_allow_html=True)

# API Key
ke = st.text_input('🔑 Ingresa tu clave API:')
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)

# Imagen
uploaded_file = st.file_uploader("📤 Sube una imagen", type=["jpg", "png", "jpeg"])
if uploaded_file:
    with st.expander("🖼️ Vista previa de la imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# Detalles
show_details = st.toggle("➕ Añadir detalles a la imagen", value=True)
additional_details = "Responde solo con las letras y numero grandes que aparecen en la imagen"

# Botón
analyze_button = st.button("🚀 Analiza la imagen")

if uploaded_file is not None and api_key and analyze_button:
    with st.spinner("🔎 Analizando imagen..."):
        base64_image = encode_image(uploaded_file)
        prompt_text = "Describe what you see in the image in Spanish"
        if show_details and additional_details:
            prompt_text += f"\n\n{additional_details}"

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

            st.markdown("---")

            # Mostrar memes según placa
            if "CKN 364" in full_response.upper():
                st.image("https://media.giphy.com/media/111ebonMs90YLu/giphy.gif", caption="¡Placa reconocida: CKN 364 🎉!", use_container_width=True)
            elif "MXL 931" in full_response.upper():
                st.image("https://media.giphy.com/media/OPU6wzx8JrHna/giphy.gif", caption="Placa reconocida: MXL 931 😿", use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error al analizar: {e}")
            st.image("https://media.giphy.com/media/f7mQvY1MJ0aDC/giphy.gif", caption="Algo salió mal... 😢", use_container_width=True)

else:
    if not uploaded_file and analyze_button:
        st.warning("⚠️ Por favor sube una imagen.")
        st.image("https://media.giphy.com/media/TqiwHbFBaZ4ti/giphy.gif", caption="¿Y la imagen? 🤔", use_container_width=True)
    if not api_key:
        st.warning("⚠️ Por favor ingresa tu API key.")
        st.image("https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif", caption="¡Falta la clave API!", use_container_width=True)

# Botón para mostrar texto completo
if st.button("📤 Enviar respuesta"):
    try:
        st.write(full_response)
        message_placeholder.markdown(full_response)
        st.write(full_response)
    except:
        st.warning("⚠️ Aún no se ha generado ninguna respuesta.")
