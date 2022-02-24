# %%
from selenium import webdriver
import requests
import os
import json
import chromedriver_autoinstaller
import sys
# %%
url = 'https://www.kidsnote.com/login/'
with open('student_data.json','r', encoding='utf-8') as f:
    json_data = json.load(f)
    child_name = json_data['name']
    child_profile = json_data['profile']
    user_id = json_data['id']
    user_password = json_data['password']
    print('loading id, password is completed')
foldername = './kidsnote_download'
try:
    os.mkdir(foldername)
except:
    print('all ready exist')


# %%
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver_path = f'./{chrome_ver}/chromedriver.exe'
if os.path.exists(driver_path):
    print(f"chrom driver is insatlled: {driver_path}")
else:
    print(f"install the chrome driver(ver: {chrome_ver})")
    chromedriver_autoinstaller.install(True)
driver = webdriver.Chrome(executable_path=driver_path)
driver.get(url=url)

# %%
from selenium.webdriver.common.by import By
#id, password
driver.find_element(By.NAME, 'username').send_keys(user_id)
driver.find_element(By.NAME, 'password').send_keys(user_password)
submit_forms = driver.find_elements(By.TAG_NAME,'input')
for form in submit_forms:
    if form.get_attribute('type') == 'submit':
        print('find login button')
        form.click()
        break

# %%
try:
    driver.find_element(By.CSS_SELECTOR, 'body > header > div.header-inner > ul > li > a').click()
    chr_list = driver.find_element(By.CSS_SELECTOR, 'body > header > div.header-inner > ul > li > ul')
except:
    print('login failed')
    sys.exit()


# %%
# 리스트 수정 필요

# %%
albums = []
for chr in chr_list.find_elements(By.TAG_NAME, 'a'):
    if (child_name in chr.text):
        albums.append(chr)
    

# %%
albums[child_profile].click()

# %%
try:
    driver.find_element(By.CLASS_NAME,'close_btn').click()
except:
    print('no popup')

# %%
sidebar = driver.find_element(By.ID,'side-menu')
sidebar_items = sidebar.find_elements(By.TAG_NAME, 'a')
for item in sidebar_items:
    try:
        if ('albums' in item.get_attribute('href')):
             item.click()
    except:
        print('dont have albums in sidebar')

# %%

def img_download(links):
    for link in links:
        try:
            res = requests.get(link)
        except:
            print(f'{link} is not available')
        file_name = link.split('/')[-2]
        total_name= f'{foldername}/{file_name}.jpg'
        with open(total_name, 'wb') as f:
            f.write(res.content)

# %%
ad_xpath = '//*[@id="content-inner"]/div/div/div[2]/form'
def get_album(id):
    album_list_wrapper = driver.find_element(By.CLASS_NAME, 'album-list-wrapper')
    albums = album_list_wrapper.find_elements(By.TAG_NAME, 'a')
    driver.get(albums[id].get_attribute('href'))
    try:
        driver.find_element(By.XPATH, ad_xpath).click()
    except:
        a = 1 
    imgs = driver.find_element(By.ID, 'img-grid-container')
    img_links = imgs.find_elements(By.TAG_NAME, 'a')
    img_links = list(map(lambda x: x.get_attribute('href'), img_links))
    img_download(img_links)

# %%
while(True):
    album_list_wrapper = driver.find_element(By.CLASS_NAME, 'album-list-wrapper')
    albums = album_list_wrapper.find_elements(By.TAG_NAME, 'a')
    album_length = len(albums)
    print('start album download')
    for i in range(album_length):
        get_album(i)
        driver.back()
        try:
            driver.find_element(By.XPATH, ad_xpath)
            driver.back()
        except:
            a = 1 
    try:
        next_link = driver.find_element(By.CLASS_NAME, 'next')
        next_link.find_element(By.TAG_NAME, 'a').click()
    except:
        print('download finished')
        break

# %%
driver.close()

# %%



