from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False) 

    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')[1]. get_text()
    news_p = soup.find_all('div', class_='article_teaser_body')[1].get_text()


    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)

    browser.find_by_tag("button")[1].click()

    featured_image = browser.find_by_css("img.fancybox-image")[0]["src"]

    mars_fact_url = 'https://galaxyfacts-mars.com/'

    # Make pandas to get the html
    tables = pd.read_html(mars_fact_url)

    mars_fact_df = tables[1]
    mars_fact_df.columns = ['Description', 'Fact']
    mars_fact_df.set_index('Description', inplace=True)
    html_table = mars_fact_df.to_html()

    base_url = 'https://marshemispheres.com/'
    browser.visit(base_url)
    all_hemi = []
    for i in range(4):
        browser.find_by_css("a.product-item img")[i].click()
        hemi = {}
        hemi["title"] = browser.find_by_css("h2.title")[0].text
        hemi["img_url"] = browser.find_by_text("Sample")[0]["href"]
        all_hemi.append(hemi)
        browser.back()

    data = {"news_title":news_title,
            "news_p":news_p,
            "featured":featured_image,
            "facts":html_table,
            "hemispheres":all_hemi
    }

    browser.quit()
    return data
