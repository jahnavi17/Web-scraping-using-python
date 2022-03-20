#!/usr/bin/env python
# coding: utf-8

# ## Web Scraping using python libraries requests and BeautifulSoup

# Goodreads is a website which lets users across the world to rate the books and to write down reviews. Every year, Goodreads conduct choice awards where users can vote to their favorite book in each genre. Based on the number of votes each book received, one book will be declared winner from each genre. 

# Here, I used python to scrape the goodreads website and collect 2021 winner details like the category, title of the book, number of votes received and the author of the book. 

# ### Importing the needed libraries

# In[1]:


import requests 
from bs4 import BeautifulSoup as bs
import pandas as pd


# ### Getting the page needed using requests library

# In[2]:


page=requests.get("https://www.goodreads.com/choiceawards/best-books-2021")
soup=bs(page.content,'html.parser')
print(soup.prettify())


# ### Getting required fields for one record

# In[3]:


sample_data=soup.find(class_="category clearFix")
print(sample_data.prettify())


# In[4]:


sample_cat=sample_data.find("h4").get_text()
print(sample_cat)


# In[5]:


sample_title=sample_data.find("img")["alt"]
print(sample_title)


# In[6]:


sample_a=sample_data.find("a")
print(sample_a.prettify())


# In[7]:


print(sample_a["href"])


# ### Getting child page from the parent page for one record

# In[8]:


sample_page=requests.get("https://www.goodreads.com"+sample_a["href"])
sample_soup=bs(sample_page.content,'html.parser')
print(sample_soup.prettify())


# In[9]:


sample_votes=sample_soup.find(class_="greyText gcaNumVotes").get_text()
print(sample_votes)


# In[10]:


sample_author=sample_soup.find(class_="authorName__container")
print(sample_author.prettify())


# In[11]:


sample_author_name=sample_author.find("span").get_text()
print(sample_author_name)


# In[12]:


print(sample_cat,sample_title,sample_votes,sample_author_name)


# ### Getting all the records using css selectors

# In[13]:


categories=[t.get_text().strip("\n") for t in soup.select(".clearFix.category h4")]
categories


# In[14]:


titles=[t["alt"] for t in soup.select(".category__winnerImageContainer img")]
titles


# In[15]:


child_soups=[]
child_a=soup.select(".clearFix.category a")
child_href=[a["href"] for a in child_a]
print(child_href)


# In[16]:


child_href=[i for i in child_href if i!='#']
print(child_href)


# In[17]:


print(len(child_href))


# In[18]:


print(len(titles))


# In[19]:


votes=[]
authors=[]
for i,href in enumerate(child_href):
    child_page=requests.get("https://www.goodreads.com"+href)
    child_soup=bs(child_page.content,'html.parser')
    no_votes=child_soup.find(class_="greyText gcaNumVotes").get_text()
    votes.append(no_votes)
    author=child_soup.find("span",itemprop="name").get_text()
    authors.append(author)
print(len(votes))
print(len(authors))


# In[20]:


print(votes)


# In[21]:


votes=[t.strip("\n") for t in votes]
votes=[t.replace("\n","") for t in votes]
print(votes)


# In[22]:


print(authors)


# ### Creating a dataframe

# In[23]:


winners=pd.DataFrame({"category":categories,"title":titles,"votes":votes,"author":authors})
print(winners)


# In[24]:


winners.head()


# ### Saving the dataframe as a .csv file 

# In[29]:


winners.to_csv("Goodreads choice awards.csv")


# In[ ]:




