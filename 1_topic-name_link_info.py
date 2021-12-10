'''
Weibo topic names, descriptions and hyperlinks 
result_names.txt, result_links.txt, result_infos.txt  
'''

from selenium import webdriver
import time
from bs4 import BeautifulSoup

# Open a new Chrome window and open the main page of Weibo for the user to login.
chromeDriver = webdriver.Chrome()
chromeDriver.get("https://www.weibo.com")

# Count down [loginWaitSeconds] seconds with tips showing up here to guide the user to login on this page.
loginWaitSeconds = 45
for i in range(loginWaitSeconds):
    print("Please login your Weibo account in the page loaded in Chrome in", loginWaitSeconds - i, "seconds...")
    time.sleep(1)

# Prepare 3 empty containers for the collected data later.
topic_names = []
topic_links = []
topic_infos = []

# There are 25 pages of topic lists in the search result, collect topics on these pages one by one.
for i in range(25):

    # "range(25)" provides values from 0 to 24, to get values we need (which are 1 to 25), each number should be added by 1.
    page_number = i + 1

    # Here comes the link of pages of the search result.
    # - The first part contains the search key word (which is "%E6%9D%A8%E7%AC%A0", refers to Chinese word "杨笠").
    # - Then the link ended by page number, which should be converted to a String type (by using str() ) to be added to the link.
    # i.e. The final link should be like "https://s.weibo.com/topic?q=%E6%9D%A8%E7%AC%A0&pagetype=topic&topic=1&Refer=weibo_topic&page=1", for the example of the first page.
    url = "https://s.weibo.com/topic?q=%E6%9D%A8%E7%AC%A0&pagetype=topic&topic=1&Refer=weibo_topic&page=" + str(page_number)

    # Open the link above in the Chrome window created before, then use BS to collect the code of the page.
    chromeDriver.get(url)
    soup = BeautifulSoup(chromeDriver.page_source, "lxml")

    # The names of topics come as tags named "a" with class "name", find them in BeautifulSoup.
    # Get the topic names (get_text directly) and links(the attribute "href" of the name) and put them into the containers.
    topic_names_sources = soup.find_all("a", class_="name")
    for i in range(len(topic_names_sources)):
        topic_names.append(topic_names_sources[i].get_text())
        topic_links.append(topic_names_sources[i]["href"])

    # The detail information of each topic comes as tags named "div" with class "info", find them in BeautifulSoup.
    # Since further processing is needed for the codes in each of these "div" tags, build new BeautifulSoups for each of them, saved to container topic_soups.
    topic_sources = soup.find_all("div", class_="info")
    topic_soups = []
    for i in range(len(topic_sources)):
        topic_soups.append(BeautifulSoup(topic_sources[i].text, "lxml"))

    # Then for each of the BeautifulSoups of the codes in the "div" tags, get the first ([0]) tag "p" in it, where is the detail information of each topic comes. Put them into the container.
    for i in range(len(topic_soups)):
        topic_infos.append(topic_soups[i].find_all("p")[0].get_text().replace("\n\n\n\n", "|"))

    # Give a message out that the current page of search results is over.
    print("page no." + str(page_number) + " finished, " + str(len(topic_names_sources)) + " topics collected. Wait 5 seconds then go on to the next page.")
    time.sleep(5)

# After the 25 loops above, those three containers are full of topic informations.

# Create three files to save them.
names_file = open("result_names.txt", "w", encoding="utf-8", errors="ignore")
links_file = open("result_links.txt", "w", encoding="utf-8", errors="ignore")
infos_file = open("result_infos.txt", "w", encoding="utf-8", errors="ignore")

for i in range(len(topic_names)):
    names_file.write(str(topic_names[i]) + "\n")

for i in range(len(topic_links)):
    links_file.write(str(topic_links[i]) + "\n")

for i in range(len(topic_infos)):
    infos_file.write(str(topic_infos[i]) + "\n")

# Files writing finished, close those three files.
names_file.flush()
names_file.close()
links_file.flush()
links_file.close()
infos_file.flush()
infos_file.close()

# Close the Chrome window created on the beginning.
chromeDriver.quit()