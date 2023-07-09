import requests
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import base64
from io import BytesIO
from PIL import Image
import os
import time
import logging
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def ImageCrawl(search_term, log_file, dir):
    # directory where images will be downloaded   
    # savedir = dir+'\\'+search_term
    savedir = r"C:\Users\user\OneDrive\바탕 화면\Data\Aucuba japonica  var. variegata"
    if not os.path.exists(savedir):
        os.makedirs(savedir)

    # log 설정
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    logger = logging.getLogger(f"{search_term}_{now}")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file, mode="w")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info("***%s",search_term)


    start_time = time.time()

    # chrome driver path 수정
    driverpath = r'C:\Users\user\Desktop\chromedriver.exe'

    num_images = 1000   # 필요한 이미지 개수 수정
    logger.info("***Num of images to crawl:%d",num_images)
    # create directory to store images
    path = r'C:\Users\user\OneDrive\Desktop' #path 수정


    chrome_options = Options()
    chrome_options.add_argument('--headless') #background 창
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(driverpath, chrome_options=chrome_options)
    driver.get(f"https://www.google.com/search?q={search_term}&tbm=isch")


    # SCROLL down the page to load more images
    countn = 0
    while len(driver.find_elements_by_tag_name("img")) < 2.5*num_images:
        # print("countn:",countn)
        last_height = driver.execute_script("return document.body.scrollHeight") #gets the height of the page
        # 'show more' button 클릭
        if (countn != 0 and countn%5==0) : 
            try:
                # print('try')
                wait = WebDriverWait(driver, 10)
                button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input')))
                button.click()
                time.sleep(3)
            except Exception as e:
                logger.error(f"An error occurred in click xpath: {e}")
                pass
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scrolls down 
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        logger.info("img len:%s",len(driver.find_elements_by_tag_name("img")))

        
        if new_height == last_height:   # means it hit the bottom of the page 
            print("hit the bottom of page.")
            break
        last_height = new_height
        countn+=1

    # parse HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # find all image tags on the page
    img_tags = soup.find_all('img')
    logger.info("len of img tags:%d",len(img_tags))



   
    num_saved = 953
    count = 0
    # loop through the image tags and save the images
    for img_tag in img_tags:
        logger.info("%d",count)
        try:
            if(img_tag.has_attr('src')):
                img_url = img_tag['src']
            elif(img_tag.has_attr('data-src')):
                img_url = img_tag['data-src']

            try: #base64 아닌 이미지
                img_data = requests.get(img_url).content

                # 웹사이트 로고 저장 하지 않도록 사이즈로 필터링 하기
                img_file = BytesIO(img_data)
                img = Image.open(img_file)
                width, height = img.size
                if width < 80 or height < 80:
                    logger.info("logo picture. Abort.")
                    count+=1
                    continue
                #이미지 저장
                # with open(os.path.join(savedir, f"{num_saved}.jpg"), 'wb') as f:
                #     f.write(img_data)
                response = requests.get(img_url, stream=True)
                if response.status_code == 200:
                    with open(savedir, 'wb') as file:
                        file.write(response.content)
                    num_saved += 1
                    logger.info(f"Downloaded image {num_saved} of {num_images}")
                count+=1
            except: #base64
                    # Decode the base64 data
                    img_binary = base64.b64decode(img_url.split(',')[1])

                    # get the dimensions of the image
                    img_file = BytesIO(img_binary)
                    img = Image.open(img_file)
                    width, height = img.size
                    # 웹사이트 로고 저장 하지 않도록 사이즈로 필터링 하기
                    if width < 80 or height < 80:
                        logger.info("too small picture. Abort.")
                        count+=1
                        continue
                    #이미지 저장
                    # with open(os.path.join(savedir, f"{num_saved}.jpg"), 'wb') as f:
                    #     f.write(img_binary)
                    response = requests.get(img_url, stream=True)
                    if response.status_code == 200:
                        with open(savedir, 'wb') as file:
                            file.write(response.content)
                        num_saved += 1
                        logger.info(f"Downloaded image {num_saved} of {num_images}")
                    count+=1

        except Exception as e:
            logger.error("An error occurred:%s", e)
            count+=1
            continue
        

    # close webdriver
    driver.close()


    end_time = time.time()
    logger.info("%f seconds",end_time - start_time)