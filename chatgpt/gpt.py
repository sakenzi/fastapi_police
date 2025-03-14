from ast import main
import asyncio
from g4f.client import Client
from typing import Optional

client = Client()

def protocol_options(text: str):
    query = (
        f"Вот {text}, по этому тексту составь мне протокол для полиций"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": query
            }
        ],
    )
    print('response', response.choices[0].message.content)
    response_text = response.choices[0].message.content
    
