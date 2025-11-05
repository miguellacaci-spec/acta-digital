import streamlit as st
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
