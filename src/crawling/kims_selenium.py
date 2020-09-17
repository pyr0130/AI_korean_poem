import hanja
from hanja import hangul
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

path = 'https://ko.wikisource.org/wiki/%EC%A7%84%EB%8B%AC%EB%9E%98%EA%BD%83_(%EC%8B%9C%EC%A7%91)'
driver = webdriver.Chrome('E:\\경희대학교\\2019_1\\데이터베이스(종강)\\중간발표\\chromedriver_win32\\chromedriver')

u = open('poet_url_김소월.txt','w')

driver.get(path)
hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

sampe = driver.find_elements_by_tag_name('a')

i = 235
for k in range(75,165):
    if sampe[k].text == '편집':
        continue
    else:
        target = sampe[k]

        target.send_keys(Keys.CONTROL + "\n")

        driver.switch_to.window(driver.window_handles[1])
        address= driver.current_url
        u.write(address+'\n')

        ti = str(i)+".txt"
        tmp = open(ti,'w')
        try:
            d = driver.find_element_by_class_name("poem").text
        except:
            try:
                d = driver.find_element_by_class_name("mw-parser-output").text
            except:
                continue
        rr = hanja.translate(d,'substitution')

        r = hangul.sub('\n',rr)

        tmp.write(r)
        
        tmp.close()

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        i+=1

u.close()

