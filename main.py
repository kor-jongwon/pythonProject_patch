
from hotels_c_crawl import hotels_c_crawl
from sub_hotel_crawl import crawl
from image_compare import image_compare
from multiprocessing import Process

def main():
   process_hotels = Process(target=hotels_c_crawl.again, args=(2,))
   process_subhotel = Process(target=crawl.sub_hotel_crawl, args=(4,))

if __name__ == "__main__":
    #process_hotels_1 = Process(target=hotels_c_crawl.again, args=(9491,))
   # process_subhotel_1 = Process(target=crawl.sub_hotel_crawl, args=(9521,))
    process_image_compare = Process(target=image_compare.image_compare_linterarea, args=(9485,))
    #process_hotels_1.start()
    process_image_compare.start()
    #process_subhotel_1.start()
    #process_hotels_1.join()
    process_image_compare.join()
    #process_subhotel_1.join()