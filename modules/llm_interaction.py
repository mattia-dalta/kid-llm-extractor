from openai import OpenAI
from modules.prompts import build_kid_prompt

client = OpenAI()  

def extract_kid_info(text):
    """
    Sends a prompt to GPT to extract structured information from a KID document.

    Args:
        text (str): The full extracted text from the PDF document.

    Returns:
        str: A formatted response with the extracted information.
    """
    prompt = build_kid_prompt(text)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert assistant in KID documents."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1200
    )
    return response.choices[0].message.content.strip()
