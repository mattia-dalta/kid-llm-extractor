import streamlit as st
import fitz  # PyMuPDF è una libreria per la manipolazione di PDF
from openai import OpenAI
from io import BytesIO
from dotenv import load_dotenv
import os

# Carica la chiave API dal file .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ API key non trovata. Controlla che il file .env sia nella stessa cartella e correttamente scritto.")
    st.stop()

# Inizializza il client OpenAI
client = OpenAI(api_key=api_key)


# Estrazione testo PDF
def estrai_testo_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        return "\n".join([page.get_text() for page in doc])

# Prompt a GPT
def estrai_info_kid(testo):
    prompt = f"""
Sei un assistente esperto in documenti KID (Key Information Document).
Estrai le seguenti informazioni dal testo fornito. Segui le istruzioni esattamente:

1. ISIN: riportalo esattamente come nel testo.
2. SRI: numero da 1 a 7, se presente.
3. RHP: orizzonte di detenzione raccomandato, copia testuale.
4. Nome del prodotto: prendi solo la **prima parte del nome**, prima di "Prodotto Standard", "Classe di attivi", ecc.
5. Emittente: nome esatto.
6. Target Market: copia **letteralmente** il paragrafo del target market, senza parafrasi.
7. Scenari a RHP: estrai **solo le percentuali** indicate per:
   - Stress
   - Sfavorevole
   - Moderato
   - Favorevole

Se una percentuale non è presente, scrivi "non disponibile".

Formato di risposta:
ISIN: ...
SRI: ...
RHP: ...
Nome del prodotto: ...
Emittente: ...
Target Market: ...
Scenari di performance a RHP:
- Stress: ...
- Sfavorevole: ...
- Moderato: ...
- Favorevole: ...

Testo documento:
{testo}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sei un assistente esperto in documenti KID."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1200
    )
    return response.choices[0].message.content.strip()

# UI Streamlit
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
            testo = estrai_testo_pdf(file)
            risultato = estrai_info_kid(testo)
            estrazioni.append((file.name, risultato))

    for nome_file, risultato in estrazioni:
        st.markdown(f"<h3 style='color:#0d29ce;'>📁 Risultato per: {nome_file}</h3>", unsafe_allow_html=True)
        for linea in risultato.splitlines():
            if ":" in linea:
                chiave, valore = linea.split(":", 1)
                st.markdown(f"<span style='color:black'><b>{chiave.strip()}</b>: {valore.strip()}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:black'>{linea}</span>", unsafe_allow_html=True)
        st.markdown("<hr style='border: 1px solid #41db5e;'>", unsafe_allow_html=True)

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