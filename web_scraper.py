import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    """
    Scrape website and return DOM content.
    
    Args:
        url (str): URL to scrape
        
    Returns:
        str: HTML content of the webpage
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error scraping the website: {str(e)}"

def extract_body_content(dom_content):
    """
    Extract body content from DOM.
    
    Args:
        dom_content (str): Full HTML content
        
    Returns:
        str: Body content of the HTML
    """
    soup = BeautifulSoup(dom_content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()
        
    # Get the body if it exists, otherwise use the whole document
    body = soup.body if soup.body else soup
    return str(body)

def clean_body_content(body_content):
    """
    Clean the body content by removing extra whitespace and unnecessary tags.
    
    Args:
        body_content (str): Body content to clean
        
    Returns:
        str: Cleaned body content
    """
    soup = BeautifulSoup(body_content, 'html.parser')
    
    # Extract text
    text = soup.get_text(separator='\n', strip=True)
    
    # Remove excessive newlines
    import re
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

def split_dom_content(dom_content, chunk_size=4000):
    """
    Split DOM content into chunks to avoid token limits in AI models.
    
    Args:
        dom_content (str): DOM content to split
        chunk_size (int): Maximum size of each chunk
        
    Returns:
        list: List of content chunks
    """
    words = dom_content.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        # Add word length plus a space
        word_length = len(word) + 1
        
        if current_length + word_length > chunk_size:
            # If adding this word would exceed chunk size, start a new chunk
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            # Add word to current chunk
            current_chunk.append(word)
            current_length += word_length
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks