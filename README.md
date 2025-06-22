# KID LLM Extractor

This is a Streamlit application that automatically extracts key information from KID (Key Information Document) PDFs using OpenAI's GPT-4o model.

---

## Description

This app allows you to:

- Upload one or more KID PDF files.
- Automatically extract key fields such as:
  - ISIN
  - SRI (Synthetic Risk Indicator)
  - RHP (Recommended Holding Period)
  - Product Name
  - Issuer
  - Target Market (literal text)
  - Performance Scenarios at RHP (only percentages)
- Interact with OpenAI GPT-4o to semantically analyze and summarize the content.
- Download the results as a `.txt` file.

---

## Requirements

Install the required Python packages with:

```bash
pip install -r requirements.txt
```

Make sure you have Python 3.9+ installed.

---

## How to Run

1. Create a `.env` file in the project root with your OpenAI API key:

```
OPENAI_API_KEY=your-api-key-here
```

2. Launch the Streamlit app with:

```bash
streamlit run streamlit_app.py
```

3. Upload one or more PDF files and let the app do the work.

---

## Security

- The `.env` file is excluded from version control via `.gitignore`.
- PDF files are not uploaded or shared and are also ignored by Git.
- API key is **never exposed** in the code or committed.

---

## Output Example

```
ISIN: LU1234567890
SRI: 3
RHP: 5 years
Product Name: ABC Balanced
Issuer: XYZ Asset Management
Target Market: [literal paragraph extracted]
Performance Scenarios at RHP:
- Stress: -12.3%
- Unfavourable: -3.5%
- Moderate: 4.1%
- Favourable: 7.8%
```

---

## Notes

> This tool is for educational and demonstrational purposes only. It is not affiliated with any official financial institution.

---

## Author

**Mattia D'Alta**  
Data & Enthusiast | Bologna, Italy  
GitHub: [mattia-dalta](https://github.com/mattia-dalta)

---

## License

MIT License
