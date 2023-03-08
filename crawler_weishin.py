import os
import re
import json
import requests
from tqdm import tqdm
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


"""
for: https://mp.weixin.qq.com/s/N5dBrdC_zvPEZYrxvCliaQ
"""


def download_episodes(root_url, folder_path:Path):
    if not folder_path.exists():
        os.mkdir(folder_path)
    root_response = requests.get(root_url)
    root_soup = BeautifulSoup(root_response.text, 'html.parser')
    a_tags = root_soup.find_all('a', {'textvalue': re.compile('.+集')})
    episode_urls = [a['href'] for a in a_tags]
    for episode_url in tqdm(episode_urls):
        try:                       
            selenium_open_page_and_download(episode_url, folder_path)
        except:
            continue


def selenium_open_page_and_download(url, folder_path:Path):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        span = wait.until(EC.visibility_of_element_located((By.ID, 'voice_play')))
        span.click()
        element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'audio')))
        download_url = element.get_attribute('src')
        download_mp3(download_url, folder_path.joinpath(f'{driver.title}.mp3'))


def download_mp3(url, file_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)


def get_bookname_and_url():
    response = requests.get('https://mp.weixin.qq.com/s/N5dBrdC_zvPEZYrxvCliaQ')
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tags = soup.find_all('a', {'data-linktype': "2"})
    urls = [a['href'] for a in a_tags]
    stop_position = urls.index("https://mp.weixin.qq.com/s?__biz=MzkwNDM0OTA4Nw==&mid=2247487262&idx=1&sn=460eae40c30a789dcd73d2036a1e3d27&chksm=c0891beef7fe92f886d204aa22add71b28b00962e5c1f39f800f7e2519f604f4d6aec4a521d4&scene=21#wechat_redirect")
    urls = urls[:stop_position]
    targets = dict()
    for url in urls:
        response_book = requests.get(url)
        soup_book = BeautifulSoup(response_book.text, 'html.parser')
        title = soup_book.find(id='activity-name').text
        title = re.sub('\s', '', title)
        targets[title] = url
    with open('targest.json', 'w') as f:
        json.dump(targets, f, ensure_ascii=False, indent=4)
        

if __name__ == "__main__":
    # root_url = 'https://mp.weixin.qq.com/s?__biz=MzkwNDM0OTA4Nw==&mid=2247488756&idx=8&sn=6fdb7ea6a54af46109f06a025ede9d82&chksm=c0890004f7fe891223c6de30f90a5acbc88c15e93aaaa0a434ad768b7498565a6b637dfe5f6c&scene=21#wechat_redirect'
    # folder_path = Path('E:/异乡人/')
    # download_episodes(root_url, folder_path)
    targets = get_bookname_and_url()
    print(targets)