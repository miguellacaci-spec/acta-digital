import streamlit as st
import hashlib, time, json

# Configuración inicial
st.set_page_config(page_title="Acta Digital con Hash", layout="centered")
st.title("📜 Acta Digital con Registro Seguro")

# Archivo donde se guardan los registros
DATA_FILE = "acta_registros.json"

# 1️⃣ Cargar datos previos si existen
def cargar_registros():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# 2️⃣ Guardar datos nuevos
def guardar_registros(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# 3️⃣ Calcular hash de cada punto (texto + tiempo)
def calcular_hash(texto, timestamp):
    bloque = f"{texto}{timestamp}".encode("utf-8")
    return hashlib.sha256(bloque).hexdigest()

# Cargar registros previos
registros = cargar_registros()

# 4️⃣ Formulario para crear un punto nuevo
st.subheader("Añadir nuevo punto al acta")
with st.form("nuevo_punto"):
    punto = st.text_area("Escribe el contenido del punto:", height=120)
    autor = st.text_input("Autor")
    enviar = st.form_submit_button("Guardar punto")

# 5️⃣ Guardar el punto si se envía
if enviar and punto.strip():
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    hash_punto = calcular_hash(punto, timestamp)
    nuevo = {
        "texto": punto.strip(),
        "autor": autor.strip() or "Anónimo",
        "fecha": timestamp,
        "hash": hash_punto
    }
    registros.append(nuevo)
    guardar_registros(registros)
    st.success("✅ Punto añadido correctamente.")

# 6️⃣ Mostrar los registros existentes
st.subheader("📚 Historial del acta")
if registros:
    for i, r in enumerate(registros, start=1):
        st.markdown(f"**{i}. {r['texto']}**")
        st.caption(f"Autor: {r['autor']} · Fecha: {r['fecha']}")
        st.code(r["hash"], language="text")
else:
    st.info("Todavía no hay puntos registrados.")
