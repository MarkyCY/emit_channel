from openai import OpenAI
#import google.generativeai as genai
from dotenv import load_dotenv

import os
load_dotenv()

iso_lang_es = {
    'ab': 'Abjasio', 'aa': 'Afar', 'af': 'Afrikáans', 'ak': 'Akan', 'sq': 'Albanés',
    'am': 'Amárico', 'ar': 'Árabe', 'an': 'Aragonés', 'hy': 'Armenio', 'as': 'Asamés',
    'av': 'Avárico', 'ae': 'Avéstico', 'ay': 'Aimara', 'az': 'Azerbaiyano', 'ba': 'Baskir',
    'bm': 'Bambara', 'be': 'Bielorruso', 'bn': 'Bengalí', 'bh': 'Bhojpuri', 'bi': 'Bislama',
    'bo': 'Tibetano', 'bs': 'Bosnio', 'br': 'Bretón', 'bg': 'Búlgaro', 'ca': 'Catalán',
    'ch': 'Chamorro', 'ce': 'Checheno', 'cv': 'Chuvash', 'kw': 'Córnico', 'co': 'Corso',
    'cr': 'Cree', 'cs': 'Checo', 'da': 'Danés', 'de': 'Alemán', 'dv': 'Maldivo', 'dz': 'Dzongkha',
    'el': 'Griego', 'en': 'Inglés', 'eo': 'Esperanto', 'et': 'Estonio', 'eu': 'Euskera',
    'ee': 'Ewe', 'fo': 'Feroés', 'fa': 'Persa', 'fj': 'Fiyiano', 'fi': 'Finés', 'fr': 'Francés',
    'fy': 'Frisón', 'ff': 'Fulah', 'gl': 'Gallego', 'ka': 'Georgiano', 'gd': 'Gaélico Escocés',
    'ga': 'Irlandés', 'gv': 'Manés', 'gn': 'Guaraní', 'gu': 'Guyaratí', 'ht': 'Criollo Haitiano',
    'ha': 'Hausa', 'he': 'Hebreo', 'hz': 'Herero', 'hi': 'Hindi', 'ho': 'Hiri Motu', 'hu': 'Húngaro',
    'is': 'Islandés', 'io': 'Ido', 'ig': 'Igbo', 'id': 'Indonesio', 'ia': 'Interlingua', 'ie': 'Interlingue',
    'iu': 'Inuktitut', 'ik': 'Inupiaq', 'xh': 'Xhosa', 'zu': 'Zulú', 'it': 'Italiano', 'jv': 'Javanés',
    'ja': 'Japonés', 'kl': 'Groenlandés', 'kn': 'Canarés', 'kr': 'Kanuri', 'ks': 'Cachemiro', 'kk': 'Kazajo',
    'km': 'Khmer', 'ki': 'Kikuyu', 'rw': 'Kinyarwanda', 'ky': 'Kirguís', 'kv': 'Komi', 'kg': 'Kongo',
    'ko': 'Coreano', 'kj': 'Kuanyama', 'ku': 'Kurdo', 'lo': 'Lao', 'la': 'Latín', 'lv': 'Letón', 'li': 'Limburgués',
    'ln': 'Lingala', 'lt': 'Lituano', 'lb': 'Luxemburgués', 'lu': 'Luba-Katanga', 'lg': 'Ganda', 'mk': 'Macedonio',
    'mg': 'Malgache', 'ms': 'Malayo', 'ml': 'Malayalam', 'mt': 'Maltés', 'mi': 'Maorí', 'mr': 'Maratí', 'mh': 'Marshalés',
    'mn': 'Mongol', 'na': 'Nauruano', 'nv': 'Navajo', 'nd': 'Ndebele del Norte', 'ne': 'Nepalí', 'ng': 'Ndonga', 'nb': 'Noruego Bokmål',
    'nn': 'Noruego Nynorsk', 'no': 'Noruego', 'ii': 'Yi', 'nr': 'Ndebele del Sur', 'oc': 'Occitano', 'oj': 'Ojibwa', 'cu': 'Eslavo Eclesiástico',
    'om': 'Oromo', 'or': 'Odia', 'os': 'Osetio', 'pa': 'Panyabí', 'pi': 'Pali', 'pl': 'Polaco', 'ps': 'Pastún', 'pt': 'Portugués', 'qu': 'Quechua',
    'rm': 'Romanche', 'rn': 'Kirundi', 'ro': 'Rumano', 'ru': 'Ruso', 'sa': 'Sánscrito', 'sc': 'Sardo', 'sd': 'Sindhi', 'se': 'Sami Septentrional',
    'sm': 'Samoano', 'sg': 'Sango', 'sr': 'Serbio', 'sn': 'Shona', 'si': 'Cingalés', 'sk': 'Eslovaco', 'sl': 'Esloveno', 'so': 'Somalí', 'st': 'Sesotho',
    'es': 'Español', 'su': 'Sundanés', 'sw': 'Suajili', 'ss': 'Suazi', 'sv': 'Sueco', 'ta': 'Tamil', 'te': 'Telugu', 'tg': 'Tayiko', 'th': 'Tailandés',
    'ti': 'Tigriña', 'tk': 'Turcomano', 'tl': 'Tagalo', 'tn': 'Setsuana', 'to': 'Tongano', 'tr': 'Turco', 'ts': 'Tsonga', 'tt': 'Tártaro', 'tw': 'Twi',
    'ty': 'Tahitiano', 'ug': 'Uigur', 'uk': 'Ucraniano', 'ur': 'Urdu', 'uz': 'Uzbeko', 've': 'Venda', 'vi': 'Vietnamita', 'vo': 'Volapük', 'wa': 'Valón',
    'cy': 'Galés', 'wo': 'Wolof', 'yi': 'Yidis', 'yo': 'Yoruba', 'za': 'Chuan', 'zu': 'Zulú'
}

def get_language_name(iso_code):
    return iso_lang_es.get(iso_code, "Error: Código de idioma no válido")

api_key = os.getenv('OPENAI_API')

client = OpenAI(api_key=api_key)

async def translate(text, lang):
    res = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": f"""Traduce el siguiente texto al idioma {get_language_name(lang)}, dejando en inglés las palabras técnicas como 'crypto', 'blockchain', 'trading', y otras relacionadas con este mundo. Asegúrate de mantener las palabras, el contexto y el tono lo más parecido posible al original, de forma que la traducción sea un clon de la original pero en otro idioma. No traduzcas palabras técnicas al {get_language_name(lang)}. A continuación el texto:"""
        },
        {
          "role": "user",
          "content": text
        }
      ],
    )

    print("lang:", lang, res.choices[0].message.content)

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