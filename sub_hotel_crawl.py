import numpy as np
import requests
from selenium import webdriver
import cv2
import re
#import excelcrawl
from bs4 import BeautifulSoup
class crawl:
    def __init__(self):
        pass

    def tripavisor(self): #tirpavisor에서 이미지 가져오기
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        images = soup.select('._1a4WY7aS.RcPVTgNb')
        for image in images:
            url = image['src']
            image_nparray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
            image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
            print(image.shape)
            cv2.imshow('Image from url', image)
            cv2.waitKey(5000)  # 이미지 가져오기 성공

    driver = webdriver.Chrome("/Users/choi/Downloads/chromedriver")
    #addr =excelcrawl.excelcrawl.search_subhotel_addr()##엑셀파일 에서 가져와야함 배열 로 넣을떄 하나씩 넣을껏
    addr = '3 Lisles Hill Road, Aughafatten   BT42 4LJ'
    url = "https://www.google.com/" # 접속할 url
    response = driver.get(url) # 접속 시도
    element = driver.find_element_by_name('q') #q테그찾기
    print(element)
    element.send_keys(addr) #주소값 입력
    element.submit() #검색
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    textline = soup.select('.VwiC3b.yXK7lf.MUxGbd.yDYNvb.lyLwlc')
    text_arr = list()

    for text in textline: #검색한 단어와 같은 단어 추출
        tag = text.find_all("em")
        append_list = list()
        for j in tag: #
            append_list.append(j.string)
        text_arr.append(append_list)
    print(text_arr)
    for i, text_arr_list in enumerate(text_arr): #각 홈페이지별로 em태그에 있는 값을 가져와 검색할려는 검색어와 비교
        addr_replace = addr.replace(" ","")

        print(addr_replace) #검색어의 빈칸을 없애기
        for text_arr_list_element in text_arr_list:
            text_arr_list_element = text_arr_list_element.replace(" ", "")
            if text_arr_list_element in addr_replace:
                print(str(i)+"true"+ text_arr_list_element)
            else:
                print("false"+text_arr_list_element)

    #driver.close()
    hotel_name = soup.select('.iUh30.Zu0yb.qLRx3b.tjvcx') # 호텔 url가져옴 (span껴있음)

    hotel_arr = list()
    for hotel_url in hotel_name:  #em 태그에서 걸러진 사이트를 중에 www.tripadvisor.com 홈페이지 주소 추출해서 맞으면 그사이트로 이동
        hotel_url.span.decompose() #span태크 제거
        # print(hotel_url.text)
        if hotel_url.text == 'https://www.tripadvisor.com':
            print(hotel_url.find('.yuRUbf')) #if 로 걸러진 사이트중에


    #<em>테그에 있는 문자열 배열에 저장.
    #엑셀에서 가져온 sub_hotel_addr과 em 테그안에 값을 비교하여 가장 높은 정확도가 높은 사이트에 들어갈 알고리즘 필요

    for upperlist in text_arr:
        for lowerlist in upperlist:
            print(lowerlist)
    links = soup.select('.yuRUbf')
    link_arr = list()
    for link in links:
        print(link.select_one('.LC20lb.DKV0Md').text)  # 제목
        print(link.a.attrs['href'])  # 링크
        print()
        link_arr.append(link.a.attrs['href'])
        #높은 확률이 나온 링크매칭해서 그 링크로 들어감

    #response = driver.get(link_arr[i])  ## /www.tripadvisor.com 에 해당 각 홈페이지에 테그 클래스 네임에 맞게 함수 필요

    #3개사이트를 다 들어가서 확인하는게 아니라 3개중에 있는 사이트로 들어감
    #홈페이지별로 필요 (booking, tripadvisor, ) booking(구현 필요)


