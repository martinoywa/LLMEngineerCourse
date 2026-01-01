from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    # base_url="http://localhost:11434/v1/",
    # api_key="ollama",
    base_url="https://ollama.com/v1/",
    api_key=os.getenv('OLLAMA_API_KEY')
)

messages = [
    {
        'role': 'user',
        'content': 'Why is the sky blue?',
    },
]

chat_completion = client.chat.completions.create(
    model="gpt-oss:120b",
    messages=[
        {
            'role': 'user',
            'content': 'Why is the sky blue?',
        },
    ]
)

print(chat_completion.choices[0].message.content)
