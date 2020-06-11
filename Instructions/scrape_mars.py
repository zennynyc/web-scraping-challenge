from bs4 import BeautifulSoup
import requests
import pprint
from splinter import Browser
import time 
import pandas as pd

# define an overal function
def scrape_all():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title,news_p = mars_new(browser)
    data={"title": news_title,
         "paragraph": news_p,
         "featured_image": featured_img(browser),
        # "weather": mars_weather_twitter(browser),
         "fact": mars_facts(browser),
         "hemisphere_image_urls": hemisphere(browser)
    }

    browser.quit()
    return data
def mars_new(browser):
    url="https://mars.nasa.gov/news"
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    #beautifulsoup
    soup = BeautifulSoup(html, 'html.parser')

    try:
      slide= soup.find("div", class_="list_text")
      news_title = slide.find("div", class_="content_title").text
      news_p= slide.find("div", class_="article_teaser_body").text

    except AttributeError:
       return None, None
    return  news_title,news_p


 #define a function for featured images
def featured_img(browser):
        url_2="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(url_2)

        browser.click_link_by_partial_text('FULL IMAGE')
        time.sleep(1)
        browser.click_link_by_partial_text('more info')
        time.sleep(1)
        html_2 = browser.html

        soup = BeautifulSoup(html_2, 'html.parser')
        feature_image= soup.find('figure', class_='lede')
        image=feature_image.a['href']
        featured_image_url= "https://jpl.nasa.gov" + image
        return featured_image_url


#define mars facts
def mars_facts(browser):
        urlmars="https://space-facts.com/mars/"
        table= pd.read_html(urlmars)
        table_df=table[0]
        table_df.columns=["Description",'value']
        table_df.set_index("Description",inplace=True)
        html_table= table_df.to_html(classes="table table-striped")
        return html_table

#define mars hemispheres

def hemisphere(browser):
    url_4="https://astrogeology.usgs.gov/search/results?    q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_4)
    time.sleep(3)

    html_4=browser.html
    soup=BeautifulSoup(html_4, "html.parser")
    hemisphere= soup.findAll("div", class_="description")
    Hemispheres_list= []
    base_url= "https://astrogeology.usgs.gov"

    for record in hemisphere:
        title=record.find('a', class_="itemLink product-item").text
        browser.click_link_by_partial_text(title)
        time.sleep(2)
        html6 = browser.html
        soup6 = BeautifulSoup(html6, 'html.parser')
        # full size picture
        image_url = soup6.find('img', class_='wide-image')['src']
        # add the base_url
        url=base_url+image_url
        #title and url in list
        Hemispheres_summary={}
        Hemispheres_summary['title']=title
        Hemispheres_summary['url']=url
        Hemispheres_list.append(Hemispheres_summary)
        browser.visit(url_4)
        time.sleep(2)
    return(Hemispheres_list)
    

        

     
    
        