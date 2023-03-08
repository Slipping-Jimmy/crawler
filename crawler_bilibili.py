import os
import re
import requests
from tqdm import tqdm
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


"""
for: https://www.bilibili.com/video/BV1UB4y137m1?p=1
"""


def loop_all_episodes_human_intellengence(folder_path:Path):
    urls = [
        
    ]



def loop_all_episodes(root_url, folder_path:Path):
    if not folder_path.exists():
        os.mkdir(folder_path)
    
    for i in tqdm(range(1, 37)):
        parse_and_download(f'{root_url}?p={i}', folder_path)

    # with webdriver.Chrome() as driver:
    #     driver.get(root_url)
    #     waits = WebDriverWait(driver, 20)
    #     a_list = waits.until(
    #         EC.presence_of_element_located(
    #             (By.CLASS_NAME, 'router-link-exact-active router-link-active')))

    # for a in tqdm(a_list):
    #     print(a['href'])
    #     parse_and_download(a['href'], folder_path)


def parse_and_download(page_url, folder_path:Path):
    response = requests.get(page_url)
    pattern_title = '<title data-vue-meta="true">(.+)</title>'
    pattern_url = '"base_url":"([^"]+)"'
    name = re.search(pattern_title, response.text).group(1).split('_')[0]
    url = re.findall(pattern_url, response.text)[-1]
    print(name, url)
    download_mp3(url, folder_path.joinpath(name+'.mp3'))


def download_mp3(url, file_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        

if __name__ == "__main__":
    root_url = 'https://www.bilibili.com/video/BV1UB4y137m1'
    folder_path = Path('F:/倚天屠龍記/')
    loop_all_episodes(root_url, folder_path)
    # parse_and_download(root_url, folder_path)
