import streamlit as st
import hashlib, time, json
from datetime import datetime

st.set_page_config(page_title="Acta Digital", layout="centered")

st.title("Acta Digital")
st.write("Añade puntos al acta y descárgala como texto.")

# Formulario
with st.form("punto_form"):
    punto = st.text_area("Descripción del punto", height=120)
    autor = st.text_input("Autor")
    submit = st.form_submit_button("Añadir punto")

if "puntos" not in st.session_state:
    st.session_state["puntos"] = []

if submit and punto.strip():
    st.session_state["puntos"].append({
        "texto": punto.strip(),
        "autor": autor.strip() or "Anónimo",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

st.subheader("Puntos del acta")
if st.session_state["puntos"]:
    for i, p in enumerate(st.session_state["puntos"], start=1):
        st.markdown(f"**{i}. {p['texto']}**")
        st.caption(f"Autor: {p['autor']} · {p['fecha']}")
else:
    st.info("No hay puntos añadidos aún.")

if st.session_state["puntos"]:
    lines = []
    lines.append("ACTA DIGITAL\n")
    lines.append(f"Generada: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    lines.append("-" * 40 + "\n")
    for i, p in enumerate(st.session_state["puntos"], start=1):
        lines.append(f"{i}. {p['texto']}\n")
        lines.append(f"   Autor: {p['autor']} · {p['fecha']}\n\n")
    txt = "".join(lines)
    st.download_button("Descargar acta (.txt)", txt, file_name="acta-digital.txt", mime="text/plain")



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

