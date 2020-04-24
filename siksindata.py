from selenium import webdriver
from pymongo import MongoClient


url = 'https://www.siksinhot.com/taste'
driver = webdriver.Chrome('D:/finalproject/chromedriver.exe')
client = MongoClient('localhost',27017)
db = client.dbsparta
driver.get(url)

driver.find_element_by_xpath('/html/body/div/div/div/div[3]/div/div/div/div[1]/div[1]/div/div/a').click()
for k in range(1,18):
    high_text_front='/html/body/div/div/div/div[3]/div/div/div/div[9]/div[2]/div[2]/div/div/div[1]/ul/li['
    high_text_back=']/a'
    high_full_text=high_text_front+str(k)+high_text_back

    driver.find_element_by_xpath(high_full_text).click()
    high_region = driver.find_element_by_xpath(high_full_text+'/span').text
    middle=2
    low_text_front='/html/body/div/div/div/div[3]/div/div/div/div[9]/div[2]/div[2]/div/div/div[2]/ul/li['
    low_text_middle=']/a'
    while True:

        try:
            state = driver.find_element_by_xpath(low_text_front+str(middle)+low_text_middle).text
        except:
            break;
        middle+=1

        region_data = state.split(' ')
        for char in region_data[1]:
            if char in '()':
                region_data[1]=region_data[1].replace(char,'')
        region_info = {
            'state':str(high_region),
            'region': region_data[0],
            'shop_num': region_data[1]
        }
        db.region.insert_one(region_info)