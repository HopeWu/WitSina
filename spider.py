from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pyquery import PyQuery as pc
from config import *
import pymongo
import urllib.request

cap = webdriver.DesiredCapabilities.PHANTOMJS
cap["phantomjs.page.settings.resourceTimeout"] = 1000
cap["phantomjs.page.settings.loadImages"] = True
cap["phantomjs.page.settings.disk-cache"] = True
cap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0"
cap["phantomjs.page.customHeaders.User-Agent"] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0'

browser = webdriver.PhantomJS(service_args=SERVICE_ARGS, desired_capabilities=cap)
#browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

imageNum = 0

wait = WebDriverWait(browser, 20)
browser.set_window_size(1400, 900)

browser2 = webdriver.PhantomJS(service_args=SERVICE_ARGS, desired_capabilities=cap)
#browser2 = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait2 = WebDriverWait(browser2, 20)
browser2.set_window_size(1400, 900)

MAX_PAGE = 9
'''
def savePicSet(set_addr):
    next_pic_addr = set_addr + '#p=2'
    browser2.get(next_pic_addr)
    wait2.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#imgTotal'))
    )
    html = browser2.page_source
    doc = pc(html)
    total = doc('#imgTotal').text()
    #print(total)
    for page in range(3, int(total) +1):
        tail = '#p=' + str(page)
        next_pic_addr = set_addr + tail
        print('  '+next_pic_addr)
        browser2.get(next_pic_addr)
        html = browser2.page_source
        doc = pc(html)
        img_addr = doc('div')
'''

def savePicSet(set_addr):
    next_pic_addr = set_addr + '#p=2'
    print(next_pic_addr )
    browser2.get(next_pic_addr)
    '''
    wait2.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#imgTotal'))
    )
    '''
    html = browser2.page_source
    doc = pc(html)
    items = doc('.scroll-section > .scroll-item').items()
    for item in items:
        print(item.find('.img-wrap img').attr('src'))
        image_url = item.find('.img-wrap img').attr('src')
        if(image_url):
            global imageNum
            f = open('./image/image'+str(imageNum)+'.jpg','wb')
            imageNum = imageNum + 1
            f.write((urllib.request.urlopen(image_url)).read())
            #print((urllib.request.urlopen(image_url)).read())
            f.close()



def getPicSet():
    print(" in get pic set")
    next_page = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#pagebar > input.enter'))
    )
    next_page = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.See_layer > div.See_main'))
    )
    html = browser.page_source
    doc = pc(html)
    items = doc('#cover-list > li').items()
    for item in items:
        set_addr = item.find('div > a').attr('href')
        print(item.find('div > a').attr('href'))
        savePicSet(set_addr)
        print('\n')

def nextPage(page_num):
    print('next page processing', page_num)
    _input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#pagebar > input.pg_text'))
    )
    submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#pagebar > input.enter'))
    )
    _input.clear()
    _input.send_keys(page_num)
    submit.click()
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#pagebar > span.current'), str(page_num)))
    getPicSet()



def main():
    browser.get("http://photo.sina.com.cn/wit/")
    getPicSet()
    for page_num in range(2, MAX_PAGE + 1):
        nextPage(page_num)

if __name__ =='__main__':
    main()
