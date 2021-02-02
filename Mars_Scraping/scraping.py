# Import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path='chromedriver', headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary 
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_image_urls(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/Users/jessicajohnson/.wdm/drivers/chromedriver/mac64/88.0.4324.96/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

# Scrape Mars news
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Set up the html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images
def featured_image(browser):
    try:
        PREFIX = "https://web.archive.org/web/20181114023740"
        url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        article = browser.find_by_tag('article').first['style']
        article_background = article.split("_/")[1].replace('");',"")
        return f'{PREFIX}_if/{article_background}'
    except:
        return 'https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia22486-main.jpg'
 

# Scrape facts from the Mars facts website
def mars_facts():
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0] #tells pandas to scrape only the first table (index 0)
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars'] #assings columns to the new dataframe
    df.set_index('Description', inplace=True) #sets the description column as the dataframe's index. Inplace=True means the updated index will remain in place
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere_image_urls(browser):

    try:
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        html = browser.html
        img_soup = soup(html, 'html.parser')

        hemisphere_image_urls = []
        img_elem = browser.find_by_tag("h3")

        for x in range(len(img_elem)):
            hemispheres = {}
            browser.find_by_tag("h3")[x].click()
            img_link = browser.links.find_by_text('Sample')[0]
            hemispheres['img_url'] = img_link['href']
            hemispheres['title'] = browser.find_by_css("h2.title").text
            hemisphere_image_urls.append(hemispheres)
            browser.back()
        return hemisphere_image_urls

    except BaseException:
        return None

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())