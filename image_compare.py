import time

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import excelcrawl
import os
class image_compare:
    def image_compare_linterarea(index):
            sub_hotel_name = excelcrawl.excelcrawl.search_subhotel_name(index)##엑셀파일 에서 가져와야함 배열 로 넣을떄 하나씩 넣을껏
            hotel_name = str(index) + excelcrawl.excelcrawl.search_hotels_name(index)
            score_list=[]
            try:
                hotel_list = os.listdir('/Users/choi/Desktop/datamapping/hotels_combiend/{}'.format(hotel_name))
            except:
                print("hotel_name not crawl", hotel_name)
                image_compare.image_compare_linterarea(index+1)
            try:
                sub_hotel_list = os.listdir('/Users/choi/Desktop/datamapping/sub_hotels/{}'.format(sub_hotel_name))
            except:
                print("sub_hotel_name not crawl", hotel_name)
                image_compare.image_compare_linterarea(index + 1)
            print("sub_hotel : ", sub_hotel_name, "hotel :", hotel_name)
            for loop in range(1,len(hotel_list)):
                before = cv2.imread('/Users/choi/Desktop/datamapping/hotels_combiend/{}/{}.png'.format(hotel_name, loop))
                for sub_loop in range(1, len(sub_hotel_list)):
                    after = cv2.imread('/Users/choi/Desktop/datamapping/sub_hotels/{}/{}.png'.format(sub_hotel_name,sub_loop))
                    score = image_compare.compare_ssim(before,after,hotel_name,sub_hotel_name,loop,sub_loop,index)
                    score_list.append(score)
            print(score_list)
            try:
                max_score = max(score_list)
                print(max_score)
            except ValueError:
                print("no list")
            excelcrawl.excelcrawl.active_csv(index,max_score)
            time.sleep(5)
            image_compare.image_compare_linterarea(index+1)


    def compare_ssim(before,after, hotel_name, sub_hotel_name, loop, sub_loop,index):
        score = None
        # Convert images to grayscale
        before = cv2.resize(before, dsize=(256, 256), interpolation=cv2.INTER_AREA)
        after = cv2.resize(after, dsize=(256, 256), interpolation=cv2.INTER_AREA)
        before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
        after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)
        # Compute SSIM between two images
        # score = cv2.compare(before_gray,after_gray,cv2.CMP_GT)
        (score, diff) = ssim(before_gray, after_gray, full=True)
        if (score > 0.5):
            #print("hotel_name : {} sub_hotel_name : {} hotel_pic_num : {} sub_hotel_pic_num : {}".format(hotel_name, sub_hotel_name, loop, sub_loop))
            print("Image similarity", score)
        return score




        #else:
          #pass
        time.sleep(2)

