from selenium import webdriver
from utils import Bot
from config import LOGIN, PASSWORD
from bs4 import BeautifulSoup as BS
import re
from time import sleep

if __name__ == '__main__':
    full_name = 'Егор Дронов'
    browser = webdriver.Firefox()
    bot = Bot(browser=browser)
    bot.get_page('https://www.instagram.com/accounts/login/')
    # разметка
    bot.auth(login_xpath='/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[1]/div/label/input',
             password_xpath='/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label/input',
             enter_xpath='/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button',
             login='vovucho_3149',
             password='porebrik_0987')
    sleep(10)
    browser.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input').send_keys(full_name)
    soup = BS(browser.page_source, 'html.parser')
    pattern = re.compile('//w+/')

    print(soup.prettify())

