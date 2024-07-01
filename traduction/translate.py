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
          "content": f"""You are an expert translator. Your task is to translate the given sentence into {lang} while maintaining the original tone, style, and meaning as closely as possible. Use appropriate vocabulary and grammar to ensure the translation is natural and accurate. 

IMPORTANT: Do not translate technical terms such as 'trading', 'blockchain', 'algorithm', etc.

Here is the sentence to translate:"""
        },
        {
          "role": "user",
          "content": text
        }
      ],
    )

    print("lang: ", lang, res.choices[0].message.content)

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