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
      messages=[
        {
          "role": "system",
          "content": f"Devuélve la traducción del idioma original al ISO_639-1({lang})"
        },
        {
          "role": "user",
          "content": text
        }
      ],
    )

    print(res.choices[0].message.content)

    return res.choices[0].message.content

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