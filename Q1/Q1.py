import requests
from bs4 import BeautifulSoup

# Set User-Agent and cookies
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
}

# URL for the PTT hot boards page
url = "https://www.ptt.cc/bbs/hotboards.html"

# Send request with headers
response = requests.get(url, headers=headers)
html = response.text

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all <a> elements with class "board"
board_links = soup.find_all('a', class_="board")

# Base URL to append to relative links
base_url = "https://www.ptt.cc"

# Write the board names and URLs to a file
with open("question1.txt", "w", encoding='utf8') as f:
    for link in board_links:
        href = link.get('href')  # Get the href attribute (URL)
        text = link.text.split("\n")[1]  # Extract the board name
        f.write(f"列表名稱 : {text}, 網址: {base_url}{href}\n")
