from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time as tm
import random
from user_agent import generate_user_agent, generate_navigator
import pandas as pd
from tqdm.notebook import tqdm
from selenium.webdriver.common.by import By
import os
from datetime import datetime
import re
import pandas as pd
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException


options = webdriver.ChromeOptions()
options.add_argument('--incognito')

#Specify CWD here.
PATH = ''

def lazy_scroll(driver):
    current_height = driver.execute_script('return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        tm.sleep(3)
        new_height = driver.execute_script('return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );')
        if new_height == current_height:
            html = driver.page_source
            break
        current_height = new_height
    return html

def reddit_scrape(subreddit,driver):
    url = subreddit
    try : 
        driver.get(url)
    except WebDriverException:
        tm.sleep(10)
        driver.quit()
        driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
        driver.get(url)

    tm.sleep(5)
    try:
        driver.maximize_window()
    except WebDriverException as e:
        # Handle the specific exception when the window is already maximized
        print("WebDriverException occurred while maximizing window:", e)
    
    tm.sleep(5)
    lazy_scroll(driver)
    tm.sleep(5)
    post_links = driver.find_elements(By.TAG_NAME, 'shreddit-post')

    print('PostLinks: ' + str(post_links))

    post_data = []
    if(len(post_links) > 0):
        for post in post_links:
            href_attribute = post.get_attribute("permalink")
            print(f"Element Href: {href_attribute}")
            post_data.append({'Permalink': href_attribute})

        # Create a DataFrame from the list of dictionaries
        df = pd.concat([pd.DataFrame(post_data)], ignore_index=True)
        
        result_df = pd.DataFrame(columns=['post_detail', 'platform', 'genre', 'post_like', 'post_created_time', 'post_source'])

        postNum = 1

        for post in df['Permalink']:
            print("Post: " + str(postNum))
            postNum = postNum + 1
            url = 'https://old.reddit.com' + post
            print(url)
            try : 
                driver.get(url)
            except WebDriverException:
                tm.sleep(10)
                driver.quit()
                #Depending on your OS, you may need to update creating the Driver instance!!
                driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
                driver.get(url)

                
            tm.sleep(3)
            lazy_scroll(driver)
            tm.sleep(2)
            parent = driver.find_elements(By.CLASS_NAME, 'comment')

            for element in parent:
                comment = element.find_element(By.CLASS_NAME, 'tagline')
                try:
                    votescore = comment.find_element(By.CLASS_NAME, 'unvoted')
                    score = votescore.get_attribute('title')
                    print(score)
                except:
                    score = 0

                time = comment.find_element(By.TAG_NAME, 'time')
                orgTime = time.get_attribute('datetime')
                original_time = datetime.strptime(orgTime, "%Y-%m-%dT%H:%M:%S%z")
                formatted_time_str = original_time.strftime("%Y-%m-%d %H:%M:%S")

                commentBox = element.find_element(By.CLASS_NAME, 'usertext-body')
                commentText = commentBox.find_elements(By.TAG_NAME, 'p')
                resultText = ''

                for text in commentText:
                    resultText = resultText + ' ' + text.text
                print(resultText)
                # Set values directly using loc accessor
                result_df.loc[len(result_df)] = {
                    'post_detail': resultText,
                    'platform': 'Reddit',
                    'post_like': score,
                    'post_created_time': formatted_time_str,
                    'post_source': url
                }

        result_df['post_detail'].replace('', np.nan, inplace=True)
        result_df['post_detail'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
        result_df = result_df.dropna(subset=['post_detail'])
        return result_df
    
subs = pd.read_excel(PATH + 'SubredditList.xlsx')
subreddits = subs['url']
final_df = pd.DataFrame(columns=['post_detail', 'platform', 'genre', 'post_like', 'post_created_time', 'post_source'])
for sub in subreddits:
    driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
    # Construct the URL for the subreddit. You may need to update this if Reddit changes the form of their URL. Also update week to hour, day, year, or all depending on what you need.
    subreddit_url = f'{sub}/top/?t=week'
    print(subreddit_url)
    # Call the 'reddit_scrape' function for the current subreddit
    subreddit_df = reddit_scrape(subreddit_url,driver)
    # Append the resulting DataFrame to the final DataFrame
    final_df = pd.concat([final_df, subreddit_df], ignore_index=True)
    driver.quit()
final_df.to_csv(PATH + 'RedditCrawlerResults.csv', index=False)

