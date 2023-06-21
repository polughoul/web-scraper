import json
import requests
from bs4 import BeautifulSoup


seed = "https://khersonline.net/"

def get_links():
    r = requests.get(seed)
    soup = BeautifulSoup(r.content, "html.parser")
    links = []
    news_elements = soup.find_all("a", class_="featured")
    for element in news_elements:
        link = element["href"]
        links.append(link)
    return links

def get_page_content(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    page_info = {
        "url": link,
        "title": "",
        "body": "",
        "img": "",
        "date": "",
        "time": "",
    }
   
    title_element = soup.find("div", class_="post_title")
    body_element = soup.find("div", class_="post_content")
    date_element = soup.find("time", class_="post_info_item")
    article_img_element = soup.find("div", class_ = "post_content")
        
    if title_element:
        page_info["title"] = title_element.text.strip()
    if body_element:
        page_info["body"] = body_element.text.strip()
    if date_element:
        date_string = date_element.text.strip()  
        date_parts = date_string.split(', ')  
        if len(date_parts) >= 2:
            page_info["date"] = date_parts[0]
            page_info["time"] = date_parts[1]
    if article_img_element:
        img_tag = article_img_element.find("img")
        if img_tag:
            page_info["img"] = img_tag["src"]

    return page_info

def main():
    
    links = get_links()
    top_news = []
    for link in links:
        print(f"Обрабатывается {link}")
        info = get_page_content(link)
        top_news.append(info)

    with open("https-khersonline.json", "wt") as f:
        json.dump(top_news, f, ensure_ascii=False, indent=4)
    print("Работа завершена")

if __name__ == "__main__":
    main()
