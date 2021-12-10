'''
Weibo posts within each topic
topic name_posts.txt * 168    
'''

from selenium import webdriver
import time
from bs4 import BeautifulSoup

# Open Chrome and ask the user to login in [loginWaitSeconds] seconds, no explainations one more time.
chromeDriver = webdriver.Chrome()
chromeDriver.get("https://www.weibo.com")
loginWaitSeconds = 45
for i in range(loginWaitSeconds):
    print("Please login your Weibo account in the page loaded in Chrome in", loginWaitSeconds - i, "seconds...")
    time.sleep(1)

# Read topic names and links from the files saved previously.
links = open("result_links.txt", "r").read().split("\n")
topics = open("result_names.txt", "r", encoding="utf-8").read().split("\n")

# This time, use index of each topic for the loops instead of using itself.
# The reason to do so is that here the index is also being used to get the corresponding topic name in another list,
# which can only be done once having the index, not the link.
for link_index in range(len(links)):

    # Get the link and name of current index of topic.
    link = links[link_index]
    topic = topics[link_index].replace("#", "")

    # To avoid the last line of the file read above is empty, check it before going on processing.
    if topic == "":
        break

    # Prepare several containers for the information to be collected~
    poster_name = []
    poster_personal_page_link = []
    poster_certifications = []
    post_content = []
    post_equipment = []

    # Give a message.
    print("Start topic " + link + " now.")

    # Do the collecting on each of the (at most) 50 pages of the post list of each topic.
    for page_num in range(50):

        # Same operation as before. Suitable page numbers are 1-50, not 0-49, which is the list that range(50) provides.
        current_page_num = page_num + 1
        print("Opening page no." + str(current_page_num))

        # Open current page of post list in Chrome, create a BS for it.
        chromeDriver.get(link + "&typeall=1&suball=1&timescope=custom:2009-08-16-0:2021-11-14-23&Refer=SWeibo_box&page=" + str(current_page_num))
        soup = BeautifulSoup(chromeDriver.page_source, "lxml")

        # Check if this is the final page of current topic. If it is, break the loops of current topic immediately - no need to load more pages for this topic.
        if "您可以尝试更换关键词，再次搜索。" in chromeDriver.page_source:
            print("This topic contains less than 50 pages of results, stop this topic now.")
            break

        # If it is not the final page of the post lists currently, go on.
        else: # This page contains posts.

            # All posts are in tags named "p" with class "txt". Find them.
            data_useful = soup.find_all("p", class_="txt")

            # Do processes on each of them.
            for each_data_useful in data_useful:

                # Collect all posts except the folded long posts.
                if "展开全文" not in each_data_useful.text[1:]:

                    # Poster name, post content and also the post equipment are all here.
                    poster_name.append(each_data_useful.get("nick-name")) # poster name
                    post_content.append(each_data_useful.text[1:]) # post content
                    post_equipment.append(each_data_useful.find_parent("div").find_parent("div").find_all("p", class_="from")[0].text.strip())

                    # Check the Weibo verification level of current poster.
                    poster_info_data = each_data_useful.find_parent("div", class_="content").find_all("div", class_="info")[0].find_all("div")[1].find_all("a")

                    # Verified users have 2 items in there poster_info_data. The name of the verification is in the attribute "title".
                    if len(poster_info_data) == 2:
                        poster_personal_page_link.append(poster_info_data[0].get("href"))
                        poster_certifications.append(poster_info_data[1].get("title"))

                    # Normal users have 1 item in there poster_info_data. Manually give them the verification name "普通用户".
                    elif len(poster_info_data) == 1:
                        poster_personal_page_link.append(poster_info_data[0].get("href"))
                        poster_certifications.append("普通用户")

                    # The poster of forwarded original posts have 3 or even more items in there poster_info_data.
                    else:
                        poster_personal_page_link.append(poster_info_data[0].get("href"))
                        poster_certifications.append("转载自的用户")

    # Here create a file to save all posts collected in this topic, with the topic name as part of the name of the file.
    output_file = open("./results/" + topic + "_posts.txt", "w", encoding="utf-8")
    for i in range(len(poster_name)):
        output_file.write(str(poster_name[i]) + "||" + str(poster_certifications[i]) + "||" + str(poster_personal_page_link[i]) + "||" + str(post_content[i].replace("\n", "\\n").replace("\r", "\\r")) + "||" + str(post_equipment[i]).strip().replace("\n", "").replace("\r", ""))
        output_file.write("\n")
    output_file.flush()
    output_file.close()

# Close the Chrome window created on the beginning.
chromeDriver.quit()