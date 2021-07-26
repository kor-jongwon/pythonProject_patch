import os

import numpy as np
import requests
from bs4 import BeautifulSoup
from cv2 import cv2
from selenium import webdriver
from webdriver_manager import driver

class image:
    driver = webdriver.Chrome("/Users/choi/Downloads/chromedriver")
    driver.get("https://www.tripadvisor.co.uk/Hotel_Review-g190816-d1846337-Reviews-Douneside_House-Aboyne_Aberdeenshire_Scotland.html")
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    images = soup.select('._1a4WY7aS.RcPVTgNb')
    try:
        hotel_name = str(12) + "Douneside House"
        os.mkdir('/Users/choi/Desktop/datamapping/sub_hotels/{}'.format(hotel_name))
    except:
        print("file was already")
    for i, image in enumerate(images):
        url = image['src']
        print(url)
        image_nparray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
        crawl_image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
        print(crawl_image.shape)
        cv2.imshow('Image from url', crawl_image)
        cv2.waitKey(5000)  # 이미지 가져오기 성공
        cv2.imwrite('/Users/choi/Desktop/datamapping/sub_hotels/{}/{}.png'.format(hotel_name, i + 1),
                                    crawl_image)
                        # cv2.destroyWindow(crawl_image) close image
