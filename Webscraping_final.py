from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import json
import requests
import io
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service("C:\\Users\\Abdul Rahim\\Self Projects\\Deepfakes\\Webscraping\\Webscraping\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

def scroll_to_bottom():
        '''Scroll to the bottom of the page
        '''
        last_height = driver.execute_script('return document.body.scrollHeight')
        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(2)

            new_height = driver.execute_script('return document.body.scrollHeight')
            try:
                element = driver.find_element(
                    by=By.CSS_SELECTOR,
                    value='.YstHxe input'
                )
                element.click()
                time.sleep(2)
            except:
                pass

            if new_height == last_height:
                break

            last_height = new_height

url = 'https://images.google.com/'

driver.get(
    url=url
)

box = driver.find_element(By.NAME, "q")
box.send_keys("cats")
box.send_keys(Keys.ENTER)
time.sleep(2)

scroll_to_bottom()
time.sleep(2)

img_results = driver.find_elements(By.CLASS_NAME, "rg_i.Q4LuWd")
print(f'total images {len(img_results)}')

image_urls = set()
for img_result in img_results[0:10]:
        try:
            WebDriverWait(
                driver,
                15
            ).until(
                EC.element_to_be_clickable(
                    img_result
                )
            )
            img_result.click()
            time.sleep(2)

            actual_img = driver.find_element(By.CLASS_NAME,"sFlh5c.pT0Scc.iPVvYb")

            src = actual_img.get_attribute('src')
            image_urls.add(src)

            if 'https://' in src:
                print(src)
            else:
                print('Base 64 in source.')
        except:
            print('Image is not clickable.')


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        os.makedirs(download_path, exist_ok=True)
        file_path = os.path.join(download_path, file_name)  # Use os.path.join

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)


download_path = "imgs/"


for i, url in enumerate(image_urls):
    download_image(download_path, url, str(i) + ".jpg")
    print(i)
    print(url)      



     
