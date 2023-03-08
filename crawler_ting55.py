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
for: https://ting55.com/book/4883
"""


def selenium_download_episodes(root_url, folder_path:Path):
    if not folder_path.exists():
        os.mkdir(folder_path)
    urls = []
    with webdriver.Chrome() as driver:
        driver.get(root_url)
        f_class = driver.find_elements(By.CLASS_NAME, 'f')
        for ele in f_class:
            urls.append(ele.get_attribute('href'))

    for url in urls[:2]:
        selenium_parse_and_download(url, folder_path)


def selenium_parse_and_download(page_url, folder_path:Path):
    with webdriver.Chrome() as driver:
        driver.get(page_url)
        wait = WebDriverWait(driver, 10)
        name = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[2]/h1')))
        audio_locator = (By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/div[2]/div[2]/div[1]/audio'")
        _audio = wait.until(EC.presence_of_element_located(audio_locator))
        url = _audio.get_attribute('src')
        download_mp3(url, folder_path.joinpath(f"{name.text}.mp3"))


def download_mp3(url, file_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        

if __name__ == "__main__":
    root_url = 'https://ting55.com/book/4883'
    folder_path = Path('F:/倚天屠龍記/')
    selenium_download_episodes(root_url, folder_path)

    # /html/head/script[3]/text()

