import os
import dotenv
from openai import OpenAI
from scraper import fetch_website_links, fetch_website_contents
import json


dotenv.load_dotenv()
LARGE_MODEL_NAME = os.getenv('LARGE_MODEL_NAME', 'gpt-oss:120b')
SMALL_MODEL_NAME = os.getenv('SMALL_MODEL_NAME', 'deepseek-r1:1.5b')

local_client = OpenAI(
    base_url="http://localhost:11434/v1/",
    api_key="ollama",
)

cloud_client = OpenAI(
    base_url="https://ollama.com/v1/",
    api_key=os.getenv('OLLAMA_API_KEY')
)

LINKS_SYSTEM_PROMPT = """
You have been provided with a list of links found on a website.
You're able to identify which links are most relevant to include in a brochure about the company, 
such as links to product pages, service descriptions, about us pages, and contact information.
You should respond in a JSON as in the example below:

{
    "relevant_links": [
        {"type": "about us page", "url": "https://example.com/about"},
        {"type": "services page", "url": "https://example.com/services"},
        {"type": "contact page", "url": "https://example.com/contact"}
    ]
}
"""

BROCHURE_SYSTEM_PROMPT = """
You are an expert brochure generator.
Using the provided relevant links about a company, generate a concise and engaging brochure.
The brochure should highlight the company's key offerings, values, and contact information.
Ensure the brochure is clear, coherent, and appealing to potential customers.
Return the brochure in markdown format.
Do not wrap the brochure in code blocks.
"""


def get_relevant_links(website:str, links: list, client):
    """
    Identify and return relevant links for brochure generation.
    """

    response = local_client.chat.completions.create(
        model=SMALL_MODEL_NAME, 
        messages=[
            {"role": "system", "content": LINKS_SYSTEM_PROMPT},
            {"role": "user", "content": f"Here are the links: {links} from the website: {website}."},
        ],
        response_format={"type": "json_object"}
    )

    relevant_links = response.choices[0].message.content
    return relevant_links


def combine_all_content(relevant_links) -> str:
    """
    Combine all relevant link content into a single string.
    """
    links = json.loads(relevant_links)
    combined_content = ""
    for link_info in links["relevant_links"]:
        url = link_info["url"]
        if url:
            content = fetch_website_contents(url)
            combined_content += f"\n\nContent from {url}:\n{content}"
    return combined_content


def generate_brochure(combined_content: str, client) -> None:
    """
    Generate a brochure using all the content.
    """
    messages = [
        {"role": "system", "content": BROCHURE_SYSTEM_PROMPT},
        {"role": "user", "content": f"{relevant_links}"},
    ]

    for part in client.chat(model=LARGE_MODEL_NAME, messages=messages, stream=True):
        print(part['message']['content'], end='', flush=True)


if __name__ == "__main__":
    website = "https://www.edwarddonner.com"
    links = fetch_website_links(website)
    print(f"Fetched Links Count: {len(links)}, Examples: {links[:5]}\n")
    relevant_links = get_relevant_links(website, links, local_client)
    print(f"Relevant Links: {relevant_links}\nType: {type(relevant_links)}\n")
    combined_content = combine_all_content(relevant_links)
    print(f"Combined Content Length: {len(combined_content)} characters\n")
    # generate_brochure(relevant_links, client)
