import concurrent
import time
from excelcrawl import excelcrawl
import cv2
import numpy as np
import os
import multiprocessing
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
class hotels_c_crawl: #호텔스 컴바인 크롤링

    def multi_thread(input_list):
        try:
            url = input_list[2].img['src']
        except:
            print("src doesnt have")
            input_list[3].close()
            hotels_c_crawl.again(input_list[4] + 1)
        image_nparray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
        crawl_image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
        print('hotel', crawl_image.shape)
        print(input_list[4])
        cv2.imwrite('/Users/choi/Desktop/datamapping/hotels_combiend/{}/{}.png'.format(input_list[0], input_list[1] + 1), crawl_image)

    def again(ind):
        for index_crawl in range(ind,10000):
            print("hotels : ",index_crawl," crawling ...")
            driver = webdriver.Chrome("/Users/choi/Downloads/chromedriver")
            hotel_name= excelcrawl.search_hotels_name(index_crawl)
            hotel_city = excelcrawl.search_hotels_city(index_crawl)
            url = "https://www.hotelscombined.co.uk"
            response = driver.get(url)
            time.sleep(3)
            try:
                element_popup = driver.find_element_by_xpath("/html/body/div[5]/div/div[3]/div/div/div/div/div[1]/div/div[2]/div[2]/div[2]/button")
                time.sleep(2)
                element_popup.click() #privarcy 팝업 no thanks버튼 클릭
            except:
                print("privacy popup None")
            element_text_box = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[4]/div[1]/div[1]/div/div[1]/div/div/div/div[3]/div/div/div/div/div[1]/div[1]/div/div')
            time.sleep(5)
            try:
                element_text_box.click()
            except:
                driver.close()
                hotels_c_crawl.again(index_crawl+1)
            time.sleep(3)
            element_input = driver.find_element_by_class_name('k_my-input')
            time.sleep(1)
            try:
                element_input.send_keys(hotel_name)
            except:
                print("input hotelname error"+str(index_crawl))
                driver.close()
                hotels_c_crawl.again(index_crawl)
            time.sleep(1)
            try:
                element_submit = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[4]/div[1]/div[1]/div/div[1]/div/div/div/div[3]/div/div/div/div/div[2]/button')
            except:
                driver.close()
                hotels_c_crawl.again(index_crawl+1)
            html = driver.page_source
            soup = BeautifulSoup(html,"html.parser")
            lists= soup.select('.QHyi.QHyi-pres-padding-default')
            for index, list in enumerate(lists):
                for i, tab in enumerate(list):
                    tab_name = tab.select_one('.JyN0-name')
                    tab_city = tab.select_one('.JyN0-subName')
                    #print(tab_city.text)
                    #hotel_city in tab_city.text and
                    #print(hotel_city)
                    #"United States" not in tab_city.text and
                    if hotel_city in tab_city.text:
                        hotel_index = i +1
                        #print("tab_name : " + tab_name.text, "tab_city : " + tab_city.text)
                                #print(hotel_index)
            time.sleep(2)
            try:
                driver_li = driver.find_element_by_xpath('/html/body/div[16]/div/div[2]/div[2]/div/ul/li[{}]'.format(hotel_index)) #리스트중 적합한 요소값을 가져옴
            except:
                print("no list in here"+str(index_crawl))
                driver.close()
                time.sleep(2)
                hotels_c_crawl.again(index_crawl+1)

            time.sleep(2) #nosearchelementerror로 인한 delay
            driver_li.click() # 리스트중 가장 적합한 요소를 클릭
            element_submit.click() #검색 버튼 클릭

            #호텔 사진 가져오기
            time.sleep(5)
            html = driver.page_source
            soup = BeautifulSoup(html,"html.parser")
            driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[4]/div/div[6]/div[1]/section/div[1]').click()
            time.sleep(2)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            images = soup.select('.picture')

            try:
                hotel_name = str(index_crawl)+hotel_name
                os.mkdir('/Users/choi/Desktop/datamapping/hotels_combiend/{}'.format(hotel_name))
            except:
                print("file was already")
                driver.close()
                hotels_c_crawl.again(ind + 1)

            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                executor.map(hotels_c_crawl.multi_thread, [[hotel_name, i, image, driver, ind] for i, image in enumerate(images)])


        #리스트 선택하는거/
        #리스트 없을때 예외처리 x
        #sub호텔은 tripadvisor은 해결 /
        #hotelsuk,trivago 홈페이지 크롤링 ~
        #sub호텔에서 받아온 이미지와 비교해서 정확도 분석
