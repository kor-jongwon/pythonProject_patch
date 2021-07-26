import concurrent
import os
import time
import numpy as np
import cv2
import requests
from excelcrawl import excelcrawl
from threading import Timer
from concurrent import futures
from bs4 import BeautifulSoup
from selenium import webdriver

class crawl:
    def __init__(self):
        pass

    def multi_thread(input_list):
            url = input_list[2]['src']
            image_nparray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
            crawl_image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
            print('sub_hotel', crawl_image.shape)
            cv2.imwrite('/Users/choi/Desktop/datamapping/sub_hotels/{}/{}.png'.format(input_list[0], input_list[1] + 1), crawl_image)

    def sub_hotel_crawl(ind):
        for index_crawl in range(ind, 10000):
            driver = webdriver.Chrome("/Users/choi/Downloads/chromedriver")
            hotel_name =excelcrawl.search_subhotel_name(index_crawl)##엑셀파일 에서 가져와야함 배열 로 넣을떄 하나씩 넣을껏
            hotel_city = excelcrawl.search_subhotel_city(index_crawl)
            try:
                os.mkdir('/Users/choi/Desktop/datamapping/sub_hotels/{}'.format(hotel_name))
            except:
                print("file was already : ", hotel_name)
                driver.close()
                crawl.sub_hotel_crawl(ind + 1)
            print()
            print("sub-hotels : ",ind," crawling...")
            time.sleep(10)
            url = "https://www.google.com/" # 접속할 url
            driver.get(url) # 접속 시도
            element = driver.find_element_by_name('q') #q테그찾기
            element.send_keys(hotel_name) #주소값 입력
            time.sleep(3)
            element.submit() #검색
            time.sleep(3)
            html = driver.page_source
            soup = BeautifulSoup(html,"html.parser")
            hotel_url_div = soup.select('.yuRUbf') # 호텔 url가져옴 (span껴있음)

            for hotel_url in hotel_url_div:
                for hotel_url_span in hotel_url:
                    for i, hotel_url_cite in enumerate(hotel_url_span.cite):
                        #hotel_url.span.decompose() #span태크 제거
                        time.sleep(3)
                        #print(hotel_url_cite)
                        if hotel_url_cite == 'https://hotels.com' or hotel_url_cite == 'https://uk.hotels.com' or hotel_url_cite == 'https://kr.hotels.com':
                            #index = i + 1
                            #print(str(i) + "hotels")
                            time.sleep(3)
                            element_find_sub_hotel_url = hotel_url_span['href']
                            driver.get(element_find_sub_hotel_url)
                            time.sleep(5)
                            html = driver.page_source
                            soup = BeautifulSoup(html, "html.parser")
                            images  = soup.select('._3vohxN._2kg-Bh')
                            #print(images)
                            try:
                                with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                                    executor.map(crawl.multi_thread, [[hotel_name, i, image] for i, image in enumerate(images[:30])])
                                driver.close()
                                crawl.sub_hotel_crawl(ind + 1)
                            except:
                                print("there was no picture")
                                crawl.sub_hotel_crawl(ind + 1)



                        elif hotel_url_cite == 'https://www.tripadvisor.co.uk' or hotel_url_cite == 'https://www.tripadvisor.com':
                            #print(str(i)+ "tripadvisor")
                            try:
                                print(hotel_url_span)
                                element_find_sub_hotel_url = hotel_url_span['href']
                            except KeyError:
                                print("href error")
                                driver.close()
                                crawl.sub_hotel_crawl(ind)


                            driver.get(element_find_sub_hotel_url)
                            time.sleep(5)
                            html = driver.page_source
                            soup = BeautifulSoup(html, "html.parser")
                            try:
                                images = soup.select('._1a4WY7aS.RcPVTgNb')
                            except:
                                print("no such images")
                                driver.close()
                                crawl.sub_hotel_crawl(ind+1)
                            #print(images)
                                with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                                    executor.map(crawl.multi_thread, [[hotel_name,i,image] for i, image in enumerate(images[:30])])
                                driver.close()
                                crawl.sub_hotel_crawl(ind+1)



                        elif hotel_url_cite == 'https://ar.trivago.com':
                            time.sleep(3)
                            #index = i + 1
                            #print(str(i) + "ar.trivago")
                            element_find_sub_hotel_url = hotel_url_span['href']
                            driver.get(element_find_sub_hotel_url)
                            html = driver.page_source
                            soup = BeautifulSoup(html, "html.parser")
                            time.sleep(3)
                            try:
                                element_input = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div/div[1]/div[2]/form/div/div[1]/div/input')
                            except:
                                driver.close()
                                crawl.sub_hotel_crawl(ind)
                            element_input.click()
                            html = driver.page_source
                            soup = BeautifulSoup(html, "html.parser")
                            lists = soup.select('.ssg-subtitle')
                            #print(lists)
                            for index, tab in enumerate(lists):
                                tab.mark.decompose()
                                tab_city = tab.text
                                if tab_city.find(hotel_city) != -1:
                                    hotel_index = index +1
                                    #print("ffffff")
                                    #print("tab_name : " + hotel_name, "tab_city : " + tab_city.text)

                            time.sleep(2)
                            try:
                                driver_li = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div/div[1]/div[2]/form/div/div[1]/div/div/div/ul/li[{}]'.format(hotel_index))  # 리스트중 적합한 요소값을 가져옴
                            except:
                                print("no list in here " + str(index_crawl))
                                driver.close()
                                time.sleep(2)
                                crawl.sub_hotel_crawl(ind + 1)
                            time.sleep(2)  # nosearchelementerror로 인한 delay
                            driver_li.click()  # 리스트중 가장 적합한 요소를 클릭
                            time.sleep(3)
                            html = driver.page_source
                            soup = BeautifulSoup(html, "html.parser")
                            hotel_name_list = soup.select(".item-link.name__copytext")
                            for index, hotel_list in enumerate(hotel_name_list):
                                for i, hotel in enumerate(hotel_list):
                                    if hotel_name in hotel:
                                        hotel_index = i +1
                                        print("tab_name : " + hotel_name, "tab_city : " + tab_city)
                            try:
                                hotel_li = driver.find_element_by_xpath('/html/body/div[2]/main/div[1]/div[1]/div[3]/div/div[1]/div[2]/div[1]/div/section/ol/li[1]/div/article/div[{}]/div[2]/div/div/h3/span'.format(hotel_index))
                            except:
                                print("no list in here" + str(index_crawl))
                                driver.close()
                                time.sleep(2)
                                crawl.sub_hotel_crawl(ind+1)
                            hotel_li.click()
                            images_buttton = driver.find_elements_by_class_name('tabs__label')
                            print(images_buttton)

                            driver.find_element_by_xpath('/html/body/div[2]/main/div[1]/div[1]/div[3]/div/div[1]/div[2]/div[1]/div/section/ol/li[1]/div/article/div[2]/div/div[1]/div/ul/li[3]/button')
                            try:

                                os.mkdir('/Users/choi/Desktop/datamapping/sub_hotels/{}'.format(hotel_name))
                            except:
                                print("file was already")
                                driver.close()
                                crawl.sub_hotel_crawl(ind +1)
                            try:
                                with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                                    executor.map(crawl.multi_thread,[[hotel_name, i, image] for i, image in enumerate(images[:30])])
                                driver.close()
                                crawl.sub_hotel_crawl(ind+1)
                                    # cv2.destroyWindow(crawl_image) close image
                            except:
                                print("there was no picture")
                                driver.close()
                                crawl.sub_hotel_crawl(ind+1)



