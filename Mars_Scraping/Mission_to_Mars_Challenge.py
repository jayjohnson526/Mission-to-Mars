#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars Challenge

# ### Import Dependencies and Set up ChromeDriver

# In[1]:


# Import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re


# In[2]:


# Path to chromedriver
get_ipython().system('which chromedriver')


# In[3]:


# Set the executable path and initialize the chrome browser in splinter
#executable_path = {'executable_path': '/Users/jessicajohnson/.wdm/drivers/chromedriver/mac64/88.0.4324.96/chromedriver'}
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[4]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[5]:


# Set up the html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[6]:


slide_elem.find("div", class_='content_title')


# In[7]:


# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[9]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[10]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### Mars Facts

# In[14]:


# Scrape facts from the Mars facts website
df = pd.read_html('http://space-facts.com/mars/')[0] #tells pandas to scrape only the first table (index 0)
df.columns=['description', 'value'] #assings columns to the new dataframe
df.set_index('description', inplace=True) #sets the description column as the dataframe's index. Inplace=True means the updated index will remain in place
df


# In[15]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[63]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[64]:


html = browser.html
img_soup = soup(html, 'html.parser')


# In[65]:


# Extract image titles
image_titles = []
for heading in img_soup.find_all(["h3"]):
    image_titles.append(heading.text.strip())
image_titles


# In[136]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
img_elem = browser.find_by_tag("h3")

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for x in range(len(img_elem)):
    hemisphere = {}
    browser.find_by_tag("h3")[x].click()
    img_link = browser.links.find_by_text('Sample')[0]
    hemisphere['img_url'] = img_link['href']
    hemisphere['title'] = browser.find_by_css("h2.title").text
    hemisphere_image_urls.append(hemisphere)
    browser.back()


# In[141]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[140]:


# 5. Quit the browser
browser.quit()

