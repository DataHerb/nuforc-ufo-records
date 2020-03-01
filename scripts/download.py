# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd


# In[32]:


import logging


# In[33]:


logging.basicConfig()
logger = logging.getLogger('ufo_ext')


# In[2]:


base_url = "http://www.nuforc.org/webreports/ndxevent.html"


# In[3]:


req = requests.get(base_url)


# In[4]:


soup_base = BeautifulSoup(req.content, 'html.parser')


# In[5]:


table_base = soup_base.find(lambda tag: tag.name=='table')
rows_base = table_base.findAll(lambda tag: tag.name=='tr')


# In[91]:


page_links = sum([
    j.findAll("a") for j in sum([i.findAll("td") for i in rows_base], [])
], [])
page_links = list(set([i["href"] for i in page_links]))
page_links.sort()


# In[59]:


logger.info(f"{len(page_links)} pages")


# In[43]:


def extract_table(link):

    try:
        link_req = requests.get(link)
    except Exception as e:
        logger.error("Can not get page content")
        return []

    link_soup = BeautifulSoup(link_req.content, 'html.parser')
    link_table = link_soup.find(lambda tag: tag.name=='table')

    dfs = pd.read_html(str(link_table))
    print(f"retrieved {link} table(s) {len(dfs)}")

    return dfs


# In[60]:


dfs = []
for link in page_links[:2]:
    link = f"http://www.nuforc.org/webreports/{link}"
    dfs.append(
        extract_table(link)
    )


# In[61]:


df_all = pd.concat(
    sum(dfs, [])
)


# In[62]:


df_all.drop_duplicates(inplace=True)


# In[63]:


df_all.to_csv("nuforc_ufo_records.csv", index=False)


# In[67]:


df_all.sort_values(by ="Date / Time")["Date / Time"].values.tolist()
