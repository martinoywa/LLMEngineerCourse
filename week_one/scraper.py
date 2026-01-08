from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

import requests
from dotenv import load_dotenv
import os


load_dotenv()
BASE_URL = os.getenv('BASE_URL')


# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_contents(url: str, timeout: int = 15_000) -> str:
    """
    Fetch fully rendered website content (JS executed).
    Returns title + visible text, truncated to 2,000 characters.
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Use domcontentloaded instead of networkidle
            page.goto(url, timeout=timeout, wait_until="domcontentloaded")

            # Optional: give JS a short moment to populate content
            page.wait_for_timeout(1_500)

        except PlaywrightTimeout:
            print(f"[WARN] Timeout loading {url}, continuing with partial content")

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"

    for tag in soup(["script", "style", "noscript", "img", "svg", "input"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)

    return ((title + "\n\n" + text)[:2_000])


def fetch_website_links(url):
    """
    Return the links on the webiste at the given url
    I realize this is inefficient as we're parsing twice! This is to keep the code in the lab simple.
    Feel free to use a class and optimize it!
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]



# if __name__ == "__main__":
#     test_url = BASE_URL
#     print("Website Contents:")
#     print(fetch_website_contents(test_url))
#     print("\nWebsite Links:")
#     print(fetch_website_links(test_url))
