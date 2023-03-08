import os
import re
import time
import opencc
import requests
from tqdm import tqdm
from pathlib import Path


"""
for: https://www.bilibili.com/video/BV1tM4y1k7qN?p=1
"""


def loop_all_episodes(root_url, folder_path:Path, missing):
    if not folder_path.exists():
        os.mkdir(folder_path)
    
    for i in tqdm(missing):
        parse_and_download(f'{root_url}?p={i}', folder_path, i)
        time.sleep(10)

    # with webdriver.Chrome() as driver:
    #     driver.get(root_url)
    #     waits = WebDriverWait(driver, 20)
    #     a_list = waits.until(
    #         EC.presence_of_element_located(
    #             (By.CLASS_NAME, 'router-link-exact-active router-link-active')))
    #     print(len(a_list))

    # for a in tqdm(a_list):
    #     print(a['href'])
    #     parse_and_download(a['href'], folder_path)


def parse_and_download(page_url, folder_path:Path, i):
    response = requests.get(page_url)
    pattern_title = '<title data-vue-meta="true">(.+)</title>'
    pattern_url = '"base_url":"([^"]+)"'
    name = re.search(pattern_title, response.text).group(1).split('_')[0]
    converter = opencc.OpenCC('s2t')
    name = converter.convert(name)
    new_name = re.sub(' ', '_', name)
    new_name = re.sub('章', '回', new_name)
    full_path = folder_path.joinpath(f'{i:03}_{name}.mp3')
    url = re.findall(pattern_url, response.text)[-1]
    download_mp3(url, full_path)


def download_mp3(url, file_name):
    for _ in range(5):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=128):
                    f.write(chunk)
            break
        time.sleep(5)
        

def find_missing():
    dir_path = Path('倚天屠龍記')
    done = os.listdir(dir_path)
    done_num = {int(epi.split('_')[0]) for epi in done}
    all = set(list(range(1, 201)))
    missing = list(all - done_num)
    return missing


def rename_files():
    dir_path = Path('倚天屠龍記')
    for file_path in dir_path.iterdir():
        new_name = re.sub('__', '_', file_path.name)
        file_path.rename(dir_path.joinpath(new_name))
        

if __name__ == "__main__":
    root_url = 'https://www.bilibili.com/video/BV1tM4y1k7qN'
    folder_path = Path('倚天屠龍記/')
    missing = find_missing()
    # loop_all_episodes(root_url, folder_path, missing)
    rename_files()
    # parse_and_download(root_url, folder_path)
