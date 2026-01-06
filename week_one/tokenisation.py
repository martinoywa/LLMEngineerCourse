import tiktoken


def count_tokens(text:str, model_name:str='gpt-3.5-turbo') -> tuple[int, list[int]]:
    """
    Count the number of tokens in the given text for the specified model.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    tokens = encoding.encode(text)

    return len(tokens), tokens


def decode_tokens(token_list:list[int], model_name:str='gpt-3.5-turbo') -> str:
    """
    Decode a list of tokens back into text for the specified model.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    text = encoding.decode(token_list)

    return text


if __name__ == "__main__":
    sample_text = "Mazana ya awali ya AI yalianzishwa na watafiti kama Alan Turing na John McCarthy."
    token_count, token_list = count_tokens(sample_text, model_name='gpt-3.5-turbo')
    print(f"Token Count: {token_count}")
    print(f"Tokens: {token_list}\n")

    decode_tokens_list = decode_tokens(token_list, model_name='gpt-3.5-turbo')
    print(f"Decoded Text: {decode_tokens_list}\n")

    print("Match token_id to text:")
    for token_id in token_list:
        print(f"Token ID: {token_id} -> Text: '{decode_tokens([token_id], model_name='gpt-3.5-turbo')}'")
