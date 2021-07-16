import time
#import excelcrawl
import cv2
import numpy as np
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
class hotels_c_crawl: #호텔스 컴바인 크롤링
    def __init__(self):
        pass
    driver = webdriver.Chrome("/Users/choi/Downloads/chromedriver")
    #addr =excelcrawl.excelcrawl.search_hotels_name()##엑셀파일 에서 가져와야함 배열 로 넣을떄 하나씩 넣을껏
    hotel_name= 'Grasmere Court'
    hotel_city = 'Keynsham'
    url = "https://www.hotelscombined.co.uk/"
    response = driver.get(url)
    time.sleep(3)
    try:
        element_popup = driver.find_element_by_xpath("/html/body/div[5]/div/div[3]/div/div/div/div/div[1]/div/div[2]/div[2]/div[2]/button")
        #print(element_popup)
        element_popup.click() #privarcy 팝업 no thanks버튼 클릭
    except:
        print("privacy popup None")
        pass
    element_text_box = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[4]/div[1]/div[1]/div/div[1]/div/div/div/div[3]/div/div/div/div/div[1]/div[1]/div/div')

    element_text_box.click()
    time.sleep(3)
    element_input = driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/div[1]/div[2]/div[1]/input')
    time.sleep(1)
    try:
        element_input.send_keys(hotel_name)
    except:
        driver.close()
    time.sleep(1)
    element_submit = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[4]/div[1]/div[1]/div/div[1]/div/div/div/div[3]/div/div/div/div/div[2]/button')
    #element_submit.click() # 입력한 주소/호텔이름과 ul에 나오는 값과 매칭을 안시켜주면 검색불가


    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    try:
        lists= soup.select('.QHyi.QHyi-pres-padding-default')
        for index, list in enumerate(lists):
            for i, tab in enumerate(list):
                tab_name = tab.select('.JyN0-name')
                tab_city = tab.select('.JyN0-subName')
                print("tab_name : "+tab_name,"tab_city : "+tab_city)
                if tab_name == hotel_name: #정규표현식이나, 문자열비교 알고리즘(kmp)쓸것
                    if tab_city == hotel_city: #정규표현식이나, 문자열비교 알고리즘(kmp)쓸것
                        index = index
                        print(index)
                        drive_city = tab_city
                    else:
                        print("city name wasn't matching") #수정 필요
    except:
        pass
    index = 1 #적합한 요소값 (test)
    time.sleep(2)
    driver_li = driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/div[2]/div/ul/li[{}]'.format(index)) #리스트중 적합한 요소값을 가져옴
    #print(driver_li)
    time.sleep(2) #nosearchelementerror로 인한 delay
    driver_li.click() # 리스트중 가장 적합한 요소를 클릭
    element_submit.click() #검색 버튼 클릭

    #호텔 사진 가져오기
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    images = soup.select('.carouselDotWrapper')
    #print(images)
    for image in images:
        url = image.img['src']
        print(url)
        image_nparray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
        image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
        print(image.shape)
        cv2.imshow('Image from url', image)
        cv2.waitKey(5000)  # 이미지 가져오기 성공

    #element_tab_click.click()
        #호텔이름과 도시이름을 매칭해보고 가장 맞는 쪽으로 선택
        #만약 리스트가 없을 경우를 봐서 예외처리 필요

   # WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@src='https://unodc.shinyapps.io/GSH_App/']")))
   # WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//ul[@class="nav navbar-nav"]//a[text()="National Data"]'))).click()

    #driver.close()




id="vMgI-accept"