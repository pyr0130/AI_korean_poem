import hanja
from hanja import hangul
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

path = 'https://ko.wikisource.org/wiki/%EC%98%81%EB%9E%91%EC%8B%9C%EC%A7%91'

u = open('poet_url_김영랑.txt','w')

driver.get(path)
hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

sampe = driver.find_elements_by_tag_name('a')

i = 184
for k in range(4,57):
    target = sampe[k] 
    target.send_keys(Keys.CONTROL + "\n")

    driver.switch_to.window(driver.window_handles[1])
    address= driver.current_url
    u.write(address+'\n')

    ti = str(i)+".txt"
    tmp = open(ti,'w')

    d = driver.find_element_by_class_name("poem").text
    rr = hanja.translate(d,'substitution')

    r = hangul.sub('\n',rr)

    tmp.write(r)
    
    tmp.close()

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    i+=1


u.close()

