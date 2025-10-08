import requests
from bs4 import BeautifulSoup

#url = "https://pixelford.com/blog/"
#response = requests.get(url, headers = {'user-agent': "Haloo"})
#print(response.content)

url = "https://pixelford.com/blog/"
response = requests.get(url, headers = {'user-agent': "haloo"})
html = response.content
soup = BeautifulSoup(html, 'html.parser')
blogs = soup.find_all('article', class_="type-post")

for blog in blogs:
    title = blog.find('a', class_="entry-title-link").get_text
    print(title)

    time_tag = blog.find('time', class_="entry-time").get('datetime')
    print(time_tag)