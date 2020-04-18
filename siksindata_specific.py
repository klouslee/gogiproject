from selenium import webdriver
from pymongo import MongoClient


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

for k in range(1,18):
    print(k,'번째 지역 서치')

    #나온 목록에서 국내지역중 하나 클릭
    driver.find_element_by_xpath(next_high_region(k)).click()



    end_num = 2
    while True:
        print(end_num, '번째 세부지역 서치')

        try:
            state = driver.find_element_by_xpath(next_low_region(end_num)).text
        except:
            print('서치오류 서치오류!!')
            break
        region_data = state.split(' ')

        driver.find_element_by_xpath(next_low_region(end_num)).click()
        end_num += 1

        driver.find_element_by_xpath('/html/body/div/div/div/div[3]/div/div/div/div[1]/div[2]/div/ul/li[6]/a').click()

        shop_table = driver.find_element_by_id('tabMove1')
        while True:
            try:
                shop_table.find_element_by_class_name('btn_sMore').click()
            except:
                break
        shop_number=1
        while True:
            shop_name_front = '/html/body/div/div/div/div[3]/div/div/div/div[6]/div/ul/li['
            shop_name_back = ']/div/a/div/div/strong'
            try:
                shop_name=driver.find_element_by_xpath(shop_name_front+str(shop_number)+shop_name_back).text
            except:
                driver.find_element_by_xpath(
                    '/html/body/div/div/div/div[3]/div/div/div/div[1]/div[1]/div/div/a').click()
                break
            shop_number += 1
            print(shop_name)


