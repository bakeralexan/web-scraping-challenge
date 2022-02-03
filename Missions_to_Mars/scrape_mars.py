import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Visit url
    mars_news_url = "https://redplanetscience.com/"
    browser.visit(mars_news_url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Get the reference div
    news = soup.find('div', class_='list_text')
    # Get the news title
    news_title = news.find_all('div', class_='content_title')[0].text
    # Get the news paragraph
    news_p = news.find_all('div', class_='article_teaser_body')[0].text

    featured_image_url = "https://spaceimages-mars.com/"
    browser.visit(featured_image_url)

    html = browser.html
    soup = bs(html, "html.parser")
    images = soup.find_all('img', class_="headerimage fade-in")
    for item in  images:
        featured_image_src = item['src']
    featured_image = featured_image_url + featured_image_src

    astropedia_url = "https://marshemispheres.com/"
    browser.visit(astropedia_url)
    html = browser.html
    soup = bs(html, "html.parser")
    results = soup.find_all('a', class_="itemLink product-item", href=True)
    html_list = []
    for result in results:

        url = result["href"]
        if url not in html_list and url != "#":
            html_list.append(url) 

    title_list = []
    img_list = []
    for x in html_list:

        browser.visit(astropedia_url + x)
        html = browser.html
        soup = bs(html, "html.parser")
        relative_image_path = soup.find('img', class_='wide-image')["src"]
        title = soup.find('h2', class_='title').get_text()
        img = astropedia_url + relative_image_path

        title_list.append(title)
        img_list.append(img)
    # Close the browser after scraping
    browser.quit()
    final_dictionary = {"News_Title": news_title, "News_Paragragh": news_p, "Featured_Image": featured_image, "Hemisphere_Title_1": title_list[0], "Hemisphere_URL_1": img_list[0], "Hemisphere_Title_2": title_list[1], "Hemisphere_URL_2": img_list[1], "Hemisphere_Title_3": title_list[2], "Hemisphere_URL_3": img_list[2], "Hemisphere_Title_4": title_list[3], "Hemisphere_URL_4": img_list[3]}

    # Return results
    return final_dictionary

