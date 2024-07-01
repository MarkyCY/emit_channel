from openai import OpenAI
#import google.generativeai as genai
from dotenv import load_dotenv

import os
load_dotenv()

#api_key = os.getenv('GEMINI_API')
api_key = os.getenv('OPENAI_API')

client = OpenAI(api_key=api_key)

async def translate(text, lang):
    res = client.chat.completions.create(
      model="gpt-3.5-turbo",
      prompt = f"Devuélveme la traducción de esto al ISO_639-1({lang}): {text}"
    )

    print(res)

    return res

#async def translate(text, lang):
#
#    input_text = f"Traduce esto al ISO_639-1({lang}): {text}"
#
#    genai.configure(api_key=api_key)
#    model = genai.GenerativeModel('gemini-pro')
#    res = model.generate_content(input_text)
#
#    print(res)
#
#    response = res.text
#
#    return response