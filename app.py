# app.py
import streamlit as st
import hashlib, time, json, secrets

# =========================
# Prompt 3 — Función de hash
# =========================
def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

st.title("🔐 Registro y Votación de Documentos Digitales")

# Campo para probar el hash
st.subheader("🧩 Prueba de Hash")
text_to_hash = st.text_input("Escribe algo para calcular su hash:")
if text_to_hash:
    st.write("Hash generado:", get_hash(text_to_hash))

# =========================
# Prompt 4 — Interfaz de registro
# =========================
st.header("📜 Registro de Documentos")
owner = st.text_input("Propietario del documento")
content = st.text_area("Contenido del documento")

if st.button("Registrar"):
    if content.strip():
        record = {"owner": owner or "Anónimo", "hash": get_hash(content), "time": time.time()}
        with open("blockchain.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        st.success("✅ Documento registrado con éxito")
    else:
        st.warning("Por favor, escribe contenido antes de registrar.")

# =========================
# Prompt 5 — Verificación de integridad
# =========================
def verify(content):
    h = get_hash(content)
    try:
        with open("blockchain.json", "r", encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                if r["hash"] == h:
                    return True
    except FileNotFoundError:
        return False
    return False

st.subheader("🔍 Verificar integridad")
verify_content = st.text_area("Escribe el contenido para verificar:")
if st.button("Verificar"):
    if verify_content.strip():
        if verify(verify_content):
            st.success("✅ Este documento ya estaba registrado.")
        else:
            st.error("❌ No se encontró este documento en la cadena.")
    else:
        st.warning("Escribe contenido para verificar.")

# =========================
# Prompt 6 — Firma digital
# =========================
st.header("🖋️ Firma Digital")
private_key = secrets.token_hex(16)
public_key = get_hash(private_key)

st.write("Tu clave pública (identifica al usuario):")
st.code(public_key)
st.info("La clave pública identifica; la privada da poder para firmar documentos.")

# =========================
# Prompt 7 — Sistema de votación simple
# =========================
st.header("🗳️ Votación de validez")
doc_hash = st.text_input("Hash del documento a votar")
vote = st.radio("¿Consideras que este documento es válido?", ["Sí", "No"])

if st.button("Votar"):
    if doc_hash.strip():
        with open("votes.json", "a", encoding="utf-8") as f:
            f.write(json.dumps({"hash": doc_hash, "vote": vote}) + "\n")
        st.success("🗳️ Voto registrado correctamente.")
    else:
        st.warning("Introduce el hash del documento antes de votar.")

# =========================
# Prompt 8 — Resultado de la votación
# =========================
def count_votes():
    yes, no = 0, 0
    try:
        with open("votes.json", "r", encoding="utf-8") as f:
            for line in f:
                v = json.loads(line)
                if v["vote"] == "Sí":
                    yes += 1
                else:
                    no += 1
    except FileNotFoundError:
        pass
    return yes, no

if st.button("Ver resultado"):
    y, n = count_votes()
    st.write(f"🟢 Sí: {y} | 🔴 No: {n}")
    st.caption("El código ejecuta la decisión, pero no analiza si es justa.")

# =========================
# Prompt 9 — Subir y desplegar
# =========================
st.divider()
st.markdown("""st.markdown("""
""")
