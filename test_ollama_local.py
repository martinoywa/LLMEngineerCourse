from ollama import chat, ChatResponse
import argparse


def run_ollama(model: str = "gemma2", stream: bool = False):
    messages = [
        {
            'role': 'user', 
            'content': 'Why is the sky blue?'
        },
    ]

    if stream:
        response = chat(model, messages=messages, stream=True)
        for part in response:
            print(part['message']['content'], end='', flush=True)
    else:
        response: ChatResponse = chat(model, messages=messages)
        print(response['message']['content'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Ollama local chat functionality.")
    parser.add_argument('--stream', action='store_true', help='Enable streaming response')
    parser.add_argument('--model', type=str, default='gemma2', help='Model name to use for chat')

    args = parser.parse_args()
    
    run_ollama(model=args.model, stream=args.stream)
