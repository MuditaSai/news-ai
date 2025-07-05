import requests
from bs4 import BeautifulSoup
import json
import sys

def fetch_article(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None

    soup = BeautifulSoup(response.content, 'lxml')
    
    # Try multiple strategies to find the title
    title = None
    title_selectors = [
        'h1',
        'title',
        '[class*="title"]',
        '[id*="title"]',
        'h1.title',
        'h1.headline'
    ]
    
    for selector in title_selectors:
        title_element = soup.select_one(selector)
        if title_element and title_element.get_text(strip=True):
            title = title_element.get_text(strip=True)
            break
    
    # Try multiple strategies to find the content
    content = None
    content_selectors = [
        'article',
        '[class*="content"]',
        '[class*="article"]',
        '[class*="body"]',
        '.post-content',
        '.entry-content',
        'main',
        '[role="main"]'
    ]
    
    for selector in content_selectors:
        content_element = soup.select_one(selector)
        if content_element and content_element.get_text(strip=True):
            content = content_element.get_text(strip=True)
            break
    
    # Fallback: try to get all paragraphs if specific selectors fail
    if not content:
        paragraphs = soup.find_all('p')
        if paragraphs:
            content = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
    
    if title and content:
        article_data = {
            'url': url,
            'title': title,
            'content': content
        }
        return article_data
    else:
        print(f"Error: Couldn't extract title and/or content. Title: {bool(title)}, Content: {bool(content)}")
        return None

def save_to_json(data, filename='article.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fetch_article.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    article = fetch_article(url)

    if article:
        save_to_json(article)
        print(f"Article saved to article.json")

