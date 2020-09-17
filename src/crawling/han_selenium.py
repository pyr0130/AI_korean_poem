import hanja
from hanja import hangul
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

path = 'https://ko.wikisource.org/wiki/%EB%8B%98%EC%9D%98_%EC%B9%A8%EB%AC%B5/%EB%8B%98%EC%9D%98_%EC%B9%A8%EB%AC%B5'
driver = webdriver.Chrome('E:\\경희대학교\\2019_1\\데이터베이스(종강)\\중간발표\\chromedriver_win32\\chromedriver')
#n = open('poet_name.txt','w')
u = open('poet_url_한용운.txt','w')

driver.get(path)
hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

for i in range(93,184):
    ti = str(i)+".txt"
    tmp = open(ti,'w')
    address= driver.current_url
    u.write(address+'\n')

    d = driver.find_element_by_class_name("poem").text
    
    rr = hanja.translate(d,'substitution')

    r = hangul.sub('\n',rr)

    tmp.write(r)
    
    tmp.close()
    ss = driver.find_element_by_id("headernext")
    ss.click()


#n.close()
u.close()
