from selenium import webdriver
from pymongo import MongoClient

url = 'https://www.siksinhot.com/taste?hpSchCate=4&hpAreaId=33&isBestOrd=N&upHpAreaId=9'
driver = webdriver.Chrome('D:/finalproject/chromedriver.exe')
client = MongoClient('localhost', 27017)
db = client.dbsparta
driver.get(url)
driver.implicitly_wait(2)


db.sample.insert_one({'양념소갈비살(1,4kg)': '44,000'})