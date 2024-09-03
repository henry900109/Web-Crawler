import requests
from bs4 import BeautifulSoup

def get_html(url):
    # Set User-Agent to simulate a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
    }
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# Base URL for the Project Gutenberg Chinese language books
url = "https://www.gutenberg.org/browse/languages/zh"
soup = get_html(url)

# URL components for book pages
head_url = "https://www.gutenberg.org/cache/epub/"
tail_url = "-images.html"

# Find all book links on the page
links = soup.find_all('li', class_="pgdbetext")
number = 0

for link in links:
    # Skip if the text does not contain "(Chinese)"
    if "(Chinese)" not in link.text:
        continue
    # Limit the number of books processed
    if number == 200:
        break
    
    # Extract the book ID from the href and build the full URL
    href = link.find('a').get('href').split("/")[2]
    full_url = f'{head_url}{href}/pg{href}{tail_url}'
    
    # Get the HTML content of the book page
    book = get_html(full_url)
    context = ""
    
    # List of label tags to look for
    label_tag = ["Title", "Author", "Release date"]
    
    # Extract text from <p> tags that contain <strong> tags
    for p_tag in book.find_all('p'):
        strong_tag = p_tag.find('strong')
        if strong_tag:
            if p_tag.text.split(":")[0] in label_tag:
                context += p_tag.text + "\n"
                if p_tag.text.split(":")[0] == "Title":
                    filename = p_tag.text.split(":")[1]

    # Extract text from all <p> tags with an id attribute
    context_list = book.find_all('p', id=True)
    for t in context_list:
        context += t.text + "\n"
    
    # Clean and prepare the filename
    filename = filename.replace("/", "_").replace(" ", "")
    filename = f"Q3/file/{filename}.txt"
    
    # Write the extracted content to a text file
    with open(filename, 'w', encoding='utf8') as f:
        f.write(context)
    
    # print("ok")  
    number += 1
