from ollama import Client
import dotenv
import os


dotenv.load_dotenv()
OLLAMA_API_KEY = os.getenv('OLLAMA_API_KEY')


client = Client(
    host="https://ollama.com",
    headers={'Authorization': f'Bearer {OLLAMA_API_KEY}'}
)

messages = [
    {
        'role': 'user',
        'content': 'Why is the sky blue?',
    },
]

for part in client.chat('gpt-oss:120b', messages=messages, stream=True):
    print(part['message']['content'], end='', flush=True)
