import hanja
from hanja import hangul
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

path = 'https://ko.wikisource.org/wiki/%ED%95%98%EB%8A%98%EA%B3%BC_%EB%B0%94%EB%9E%8C%EA%B3%BC_%EB%B3%84%EA%B3%BC_%EC%8B%9C_(1955%EB%85%84)/%EC%84%9C%EC%8B%9C'
driver = webdriver.Chrome('E:\\경희대학교\\2019_1\\데이터베이스(종강)\\중간발표\\chromedriver_win32\\chromedriver')
n = open('poet_name.txt','w')
u = open('poet_url_윤동주.txt','w')

driver.get(path)
hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

for i in range(93):
    ti = str(i)+".txt"
    tmp = open(ti,'w')
    address= driver.current_url
    u.write(address+'\n')

    a = driver.find_element_by_id("header_section_text")
    n.write(a.text+'\n')

    d = driver.find_element_by_class_name("prp-pages-output").text

    rr = hanja.translate(d,'substitution')

    r = hangul.sub('\n',rr)

    tmp.write(r)
    
    tmp.close()
    ss = driver.find_element_by_id("headernext")
    ss.click()

n.close()
u.close()

