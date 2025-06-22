from openai import OpenAI
import fitz  # PyMuPDF
import sys
from dotenv import load_dotenv
import os

# Carico la variabile d'ambiente dal file .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Inizializzo il client OpenAI
client = OpenAI(api_key=api_key)

# Prendo il path del PDF da terminale
if len(sys.argv) < 2:
    print("Uso: python extract_kid_llm.py sample_data/KID1.pdf")
    sys.exit()

pdf_path = sys.argv[1]

# Estrazione del testo dal PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text() for page in doc])

text = extract_text_from_pdf(pdf_path)

# Prompt per GPT
prompt = f"""
Sei un assistente esperto in documenti KID (Key Information Document).

Il tuo compito è estrarre le seguenti informazioni. Segui attentamente queste istruzioni:

1. ISIN: riportalo così come appare nel testo.
2. SRI: numero da 1 a 7, se presente.
3. Orizzonte di detenzione raccomandato (RHP): esattamente come scritto nel documento.
4. Nome del prodotto: estrai solo la **prima parte** del titolo del prodotto, prima di eventuali diciture come “Prodotto Standard”, “Classe di attivi”, “Categoria”, ecc. Esempio: da “CNP STRATEGY BALANCE - Prodotto Standard (Tar. U03D-U03E)” ➤ prendi solo “CNP STRATEGY BALANCE”.
5. Nome dell’emittente: così com'è scritto.
6. Target Market: copia **esattamente** il paragrafo o la sezione in cui viene descritto, **senza riassunti o riformulazioni**.
7. Scenari di performance a RHP (orizzonte di detenzione raccomandato): estrai **solo le percentuali** indicate per:
   - Stress
   - Sfavorevole
   - Moderato
   - Favorevole

Se una percentuale non è presente, scrivi "non disponibile". Formatta il risultato così:

ISIN: ...
SRI: ...
RHP: ...
Nome del prodotto: ...
Nome dell’emittente: ...
Target Market: ...
Scenari di performance a RHP:
- Stress: ...
- Sfavorevole: ...
- Moderato: ...
- Favorevole: ...

Testo del documento:
{text}
"""

# Invio la richiesta al modello GPT
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Sei un assistente esperto in documenti KID."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2,
    max_tokens=1200
)

# Pulizia e stampa della risposta
response_text = response.choices[0].message.content
cleaned_response = "\n".join(line for line in response_text.splitlines() if line.strip() != "")
print("\n--- RISPOSTA GPT-4O ---\n")
print(cleaned_response)
