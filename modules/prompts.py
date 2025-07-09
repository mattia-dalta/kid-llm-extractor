def build_kid_prompt(text: str) -> str:
    return f"""
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
{text}
"""
