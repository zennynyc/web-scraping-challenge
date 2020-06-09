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
    title,paragraph = mars_new(browser)
    data={"title": news_title,
         "paragraph": news_p,
         "feature_image": featured_img(browser),
         "weather": mars_weather_twitter(browswer),
         "fact": mars_facts(browser),
         "hemisphere_image_urls": hemisphere(browser)
    }

    browser.quit()
    return data
def mars_new(broswer):
    url="https://mars.nasa.gov/news"
    browser.visit(url)
    html = browser.html
    #beautifulsoup
    soup = BeautifulSoup(html, 'html.parser')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    try:
      slide=soup.find("li", class_="slide")
      news_title = slide.find("div", class_="content_title").text
      news_p=slide.find("div", class_="article_teaser_body").text
    except AttributeError:
       return None, None
    return  news_title,news_p


 #define a function for featured images
def featured_img(browser):
        url_2="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(url_2)

        browser.click_link_by_partial_text('FULL IMAGE')
        time.sleep(2)
        browser.click_link_by_partial_text('more info')
        time.sleep(2)
        html_2 = browser.html

        soup = BeautifulSoup(html_2, 'html.parser')
        feature_image= soup.find('figure', class_='lede')
        image_url=feature_image.a['href']
        featured_image_url="https://www.jpl.nasa.gov" + image_url
        return featured_img_url

def mars_weather_twitter(browswer):
        url_twitter="https://twitter.com/marswxreport?lang=en"
        browser.visit(url_twitter)
        time.sleep(1)
        html_twitter = browser.html
        soup = BeautifulSoup(html_twitter, 'html.parser')

        result_twitter= soup.findAll("span", {"class":"css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"})

        for result in result_twitter:
            if "Insight sol" in result.text and "low" in result.text:
                mars_weather= result.text
                break
        return mars_weather

#define mars facts
def mars_facts(broswer):
        urlmars="https://space-facts.com/mars/"
        table= pd.read_html(urlmars)
        table_df=table[0]
        table_df.columns=["Description",'value']
        table_df.set_index("Description",inplace=True)
        html_table= table_df.to_html(classes="table table-striped")
        return html_table

#define mars hemispheres

def hemisphere(broswer):
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
    

        

     
    
        