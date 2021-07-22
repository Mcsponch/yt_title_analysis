from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
import pandas as pd
import time

# X PATHS
X_CHAN_NAME = '//yt-formatted-string[@class="style-scope ytd-channel-name"]'
X_VIDEO_TITLES = '//h3[@class="style-scope ytd-grid-video-renderer"]/a'


def _start_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)
    driver.get(url)
    print('Page loaded, getting ready to scrape')
    return driver

def _get_channel_name(driver, xpath_to_name):
    chan_name = driver.find_element_by_xpath(X_CHAN_NAME).text
    print('Scraping video titles from:', chan_name)
    return chan_name


def _get_titles(driver, xpath_to_videotitle):
    delay = 3
    video_titles_i = driver.find_elements_by_xpath(X_VIDEO_TITLES)
    
    webdriver.ActionChains(driver).move_to_element(video_titles_i[-1]).perform()
    time.sleep(delay)

    video_titles_f = driver.find_elements_by_xpath(X_VIDEO_TITLES)
    while len(video_titles_f) > len(video_titles_i):
        print('Scrolling to load more video miniatures...')
        video_titles_i = video_titles_f

        webdriver.ActionChains(driver).move_to_element(video_titles_i[-1]).perform()
        time.sleep(delay)
            
        video_titles_f = driver.find_elements_by_xpath(X_VIDEO_TITLES)

    print('Done')
    print(len(video_titles_f), ' Videos found')
    print('Getting text from all the titles...')
    titles_text = [title.get_attribute('title') for title in video_titles_f]
    title_url = [url.get_attribute('href') for url in video_titles_f]
    print('Done')

    return titles_text , title_url



def run():
    # scraping
    channel_videos_url = input('Please enter the URL')
    driver = _start_driver(channel_videos_url)
    source = _get_channel_name(driver, X_CHAN_NAME)
    titles, urls = _get_titles(driver, X_VIDEO_TITLES)
    driver.close()

    # making database
    print('Building data frame')
    df = pd.DataFrame()
    df['video_titles'] = titles
    df['video_url'] = urls
    df['source'] = source.lower()
    

    print('First 5 elements of the data frame')
    print(df.head(5))

    df.to_csv(f'{source}_title_database_dirty.csv' , index=False)

    print('Saving dataframe as :', f'{source}_title_database_dirty.csv' )
    print('Script finished')



if __name__ == '__main__':
    run()