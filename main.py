import streamlit as st
from io import BytesIO
from modules.file_loader import extract_text_from_pdf
from modules.llm_interaction import extract_kid_info

# UI base
st.set_page_config(page_title="Estrazione KID", layout="centered")
st.image("prometeia_logo.jpg", width=200)

st.markdown("""
    <h1 style='text-align: center; color: #0d29ce;'>Estrazione Dati Strutturati da Documenti KID</h1>
    <p style='text-align: center; font-size: 16px; color: black;'>Carica uno o più file PDF per estrarre i dati</p>
    """, unsafe_allow_html=True)

uploaded_files = st.file_uploader("Seleziona uno o più documenti KID", type="pdf", accept_multiple_files=True)

estrazioni = []

if uploaded_files:
    for file in uploaded_files:
        with st.spinner(f"Elaborazione di: {file.name}"):
            testo = extract_text_from_pdf(file)
            risultato = extract_kid_info(testo)
            estrazioni.append((file.name, risultato))

    # Visualizza i risultati
    for nome_file, risultato in estrazioni:
        st.markdown(f"<h3 style='color:#0d29ce;'>📁 Risultato per: {nome_file}</h3>", unsafe_allow_html=True)
        for linea in risultato.splitlines():
            if ":" in linea:
                chiave, valore = linea.split(":", 1)
                st.markdown(f"<span style='color:black'><b>{chiave.strip()}</b>: {valore.strip()}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:black'>{linea}</span>", unsafe_allow_html=True)
        st.markdown("<hr style='border: 1px solid #41db5e;'>", unsafe_allow_html=True)

    # Prepara il file di output
    tutto_il_testo = "\n\n".join([
        f"==== {nome_file} ====\n{risultato}" for nome_file, risultato in estrazioni
    ])
    file_buffer = BytesIO(tutto_il_testo.encode("utf-8"))

    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Scarica estrazioni",
        data=file_buffer,
        file_name="estrazioni_kid.txt",
        mime="text/plain"
    )
