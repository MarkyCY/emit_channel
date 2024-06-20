import google.generativeai as genai

import os

api_key = os.getenv('GEMINI_API')

async def translate(text, lang):

    input_text = f"Traduce esto al ISO_639-1({lang}): {text}"

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    res = model.generate_content(input_text)

    print(res)

    response = res.text

    return response