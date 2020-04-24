from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys

import time

url = 'https://www.siksinhot.com/taste'
driver = webdriver.Chrome('D:/finalproject/chromedriver.exe')
client = MongoClient('localhost',27017)
db = client.dbsparta
driver.get(url)
driver.implicitly_wait(1)

driver.find_element_by_xpath('/html/body/div/div/div/div[3]/div/div/div/div[1]/div[1]/div/div/a').click()
#먼저 맛집 지역 클릭


def next_low_region(end_num):
    low_text_front = '/html/body/div/div/div/div[3]/div/div/div/div['
    middle_num = 9
    low_text_middle = ']/div[2]/div[2]/div/div/div[2]/ul/li['
    low_text_end = ']/a'
    try:
        driver.find_element_by_class_name("area_recommand_tag")
    except:
        middle_num -= 1
    try:
        driver.find_element_by_class_name("sub_cont_gray01")
    except:
        middle_num -= 1
    try:
        driver.find_element_by_class_name("sub_cont_white01")
    except:
        middle_num -= 1
    try:
        driver.find_element_by_class_name("sub_cont_white02")
    except:
        middle_num -= 1
    return low_text_front+str(middle_num)+low_text_middle+str(end_num)+low_text_end

def next_high_region(end_num):
    high_text_front = '/html/body/div/div/div/div[3]/div/div/div/div['
    middle_num = 9
    high_text_middle = ']/div[2]/div[2]/div/div/div[1]/ul/li['
    high_text_end = ']/a'
    try:
        driver.find_element_by_class_name("area_recommand_tag")
    except:
        middle_num -= 1
    try:
        driver.find_element_by_class_name("sub_cont_gray01")
    except:
        middle_num -= 1
    try:
        driver.find_element_by_class_name("sub_cont_white01")
    except:
        middle_num -= 1
    try:
        driver.find_element_by_class_name("sub_cont_white02")
    except:
        middle_num -= 1
    return high_text_front+str(middle_num)+high_text_middle+str(end_num)+high_text_end
count1=0
count2=0

def get_src(storenum):
    src_front = '/html/body/div/div/div/div[3]/div/div/div/div[6]/div/ul/li['
    src_back = ']/div/a/span/img'
    try:
        src = driver.find_element_by_xpath(src_front+str(storenum)+src_back)
        gogi_src = src.get_attribute("src")
        return gogi_src
    except:
        return "없음"





for k in range(1,18):
    print(k,'번째 지역 서치')

    #나온 목록에서 국내지역중 하나 클릭
    driver.find_element_by_xpath(next_high_region(k)).click()



    end_num = 2
    if count1 == 0:
        count1 += 1
        end_num =2
        ##중간에 터지면 지역번호 지정 ㄱㄱ
    while True:
        print(end_num, '번째 세부지역 서치')

        try:
            state = driver.find_element_by_xpath(next_low_region(end_num)).text
        except:
            print('터짐')
            break
        region_data = state.split(' ')

        driver.find_element_by_xpath(next_low_region(end_num)).click()
        end_num += 1

        driver.find_element_by_xpath('/html/body/div/div/div/div[3]/div/div/div/div[1]/div[2]/div/ul/li[6]/a').send_keys(Keys.ENTER)

        shop_table = driver.find_element_by_id('tabMove1')
        while True:
            try:
                shop_table.find_element_by_class_name('btn_sMore').click()
            except:
                break
        shop_number=1
        if count2==0 :
            count2+=1
            shop_number=1
            #이건 샵번호 지정하자 중간에 터졌을 경우
        while True:
            shop_name_front = '/html/body/div/div/div/div[3]/div/div/div/div[6]/div/ul/li['
            shop_name_back = ']/div/a/div/div'
            shop_name_text = '/strong'
            shop_name_star = ']/div/a/div/em'
            shop_name_full = shop_name_front+str(shop_number)+shop_name_back
            try:
                shop_name=driver.find_element_by_xpath(shop_name_full+shop_name_text).text
                shop_name = shop_name.replace(".", ",") #가게제목. 있을경우 ,로 바꿔줌
                print(shop_name)
                star = driver.find_element_by_xpath(shop_name_front+str(shop_number)+shop_name_star).text

            except:
                driver.find_element_by_xpath(
                    '/html/body/div/div/div/div[3]/div/div/div/div[1]/div[1]/div/div/a').click()
                break

            gogisrc =get_src(shop_number)

            shop_information = []
            shop_information.append({'지역':region_data[0]})
            shop_information.append({'가게이름':shop_name})
            shop_information.append({'이미지':gogisrc})
            shop_information.append({'별점': star})
            total_info = {'이미지':shop_information}
            db.PicStar.insert_one(total_info)

            shop_number += 1