from ollama import Client, ChatResponse
import dotenv
import os
from scraper import fetch_website_contents


dotenv.load_dotenv()
OLLAMA_API_KEY = os.getenv('OLLAMA_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-oss:120b')
BASE_URL = os.getenv('BASE_URL')
SYSTEM_PROMPT = """You are an expert at summarizing website content. 
Your task is to read the provided text from a website and generate a concise summary that captures the main points and key information. 
Ensure that the summary is clear, coherent, and accurately reflects the content of the website. Return the content in markdown format.
Do not wrap the summary in code blocks.
The summary should be in the Swahili language.
"""

# Ollama Cloud Client
client = Client(
    host="https://ollama.com",
    headers={'Authorization': f'Bearer {OLLAMA_API_KEY}'}
)


def summarize_website_content(website_text: str) -> str:
    """
    Summarize the given website text using the provided system prompt.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": website_text},
    ]

    response: ChatResponse = client.chat(model=MODEL_NAME, messages=messages)
    return response['message']['content']


if __name__ == "__main__":
    content = fetch_website_contents(BASE_URL)
    summary = summarize_website_content(content)
    # print("Website Summary:")
    print(summary)
