import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

def get_html(url):
    # Set User-Agent to mimic a real browser and cookies to bypass PTT's age verification.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
    }
    cookies = {
        'over18': '1'  # Bypass the age verification on PTT
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def format_date(input_date):
    # Try to parse the input date assuming it's in MM/DD format.
    try:
        parsed_date = datetime.strptime(input_date, '%m/%d')
        formatted_date = parsed_date.strftime('%m/%d')
        
        # Get today's date and generate a list of dates for the last 7 days, including today.
        today = datetime.now().date()
        dates = [today - timedelta(days=i) for i in range(7)]
        formatted_dates = [date.strftime('%m/%d') for date in dates]

        # Check if the formatted date is within the last 7 days.
        if formatted_date in formatted_dates:
            return True
        else:
            return False
        
    except ValueError:
        return "格式錯誤"  # Return error if date format is incorrect.

def make_file(soup):
    # Extract post metadata including author, title, post time, and content.
    author = soup.find('span', class_="article-meta-value").text
    title = soup.find_all('span', class_="article-meta-value")[2].text
    post_time = soup.find_all('span', class_="article-meta-value")[3].text
    content = soup.find(id="main-content").text.split('\n', 4)[4].rsplit("--", 1)[0].strip()

    # Extract the category, which is often the board name.
    category = soup.find_all('span', class_="article-meta-value")[1].text

    # Extract comments from the post.
    comments = soup.find_all('div', class_="push")
    comment_data = []

    for comment in comments:
        push_userid = comment.find('span', class_="push-userid").text.strip()
        push_content = comment.find('span', class_="push-content").text.strip()[2:]  # Remove the ": " prefix.
        push_time = comment.find('span', class_="push-ipdatetime").text.strip()
        comment_data.append({
            'author': push_userid,
            'content': push_content,
            'time': push_time
        })

    # If there are no comments or comments are disabled, set a default message.
    if not comment_data:
        comment_data = "留言未開放，或尚無留言"
    
    # Save the extracted data into a text file.
    filename = f'./file/{title}.txt'
    filename = filename.replace("\t", "")
    with open(filename, 'w', encoding='utf8') as f:
        f.write(f"作者: {author}\n")
        f.write(f"標題: {title}\n")
        f.write(f"發文時間: {post_time}\n")
        f.write(f"類別: {category}\n")
        f.write(f"內文:\n{content}\n")
        f.write("留言:\n")
        
        if isinstance(comment_data, list):
            for comment in comment_data:
                f.write(f"    作者: {comment['author']}\n")
                f.write(f"    發文時間: {comment['time']}\n")
                f.write(f"    內文: {comment['content']}\n")
                f.write("----\n")
        else:
            f.write(comment_data + "\n")

# URL for the Gossiping board on PTT.
url = "https://www.ptt.cc/bbs/Gossiping/index.html"

# Fetch the main page of the Gossiping board.
soup = get_html(url)

# Find the URL of the previous page using a regular expression.
a_tag = soup.find('a', class_='btn wide', string='‹ 上頁')
pattern = re.compile(r'/bbs/Gossiping/index(\d+)\.html')
match = pattern.search(a_tag.get('href'))
if match:
    number = int(match.group(1))

def search_page(soup, check=True):
    next_page = True
    articles = soup.find_all('div', class_='r-ent')
    base_url = "https://www.ptt.cc"
    
    for article in articles:
        data = article.find('div', class_='date').text.strip()
        
        # Check if the article's date is within the last 7 days.
        if format_date(data):
            title_div = article.find('div', class_='title')
            if title_div:
                a_tag = title_div.find('a')
                if a_tag:
                    href = a_tag.get('href')
                    try:
                        make_file(get_html(f'{base_url}{href}'))
                    except:
                        continue
        elif check:
            next_page = True
        else:
            next_page = False
    
    return next_page

check = True
# Loop through the pages until no more relevant articles are found.
while search_page(soup, check):
    url = f"https://www.ptt.cc/bbs/Gossiping/index{number}.html"
    soup = get_html(url)
    check = False
    number -= 1
