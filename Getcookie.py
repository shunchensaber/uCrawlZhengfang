from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import urllib.request
import requests
from bs4 import BeautifulSoup
def getcookie(userName,password):
    chrome_options = Options()

    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    #登录vpn
    driver.get('https://vpn.njit.casbs.cn/client/#/login')
    #driver.find_element_by_class_name('userName').send_keys('202170811')
    driver.find_element_by_name('userName').send_keys(userName)
    driver.find_element_by_name('password').send_keys(password)
    #driver.find_element_by_class_name('el-button btn el-button--button').click()
    driver.find_element_by_tag_name('button').click()
    time.sleep(1)

    #driver.find_elements_by_class_name('el-tabs__item')[2].click()
    #driver.find_elements_by_class_name('aimg')[11].click()
    #登录正方管理系统
    cookie_part = driver.get_cookie('web_vpn_user_token')
    cookie = cookie_part['value']
    url = 'https://jwjs.njit.casbs.cn/'
    headers_cookie = "web_vpn_user_token=%s" % (cookie)
    return headers_cookie












