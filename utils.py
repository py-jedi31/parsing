from selenium.webdriver import Firefox, Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import random, randint, randrange
from selenium.common.exceptions import NoSuchElementException
class Bot(object):

    def __init__(self, browser: webdriver):
        self.browser = browser

    def get_page(self, url: str) -> None:
        self.browser.get(url)
        sleep(randint(1, 5))

    def _fill_field(self, xpath: str, keys: str) -> None:
        field = self.browser.find_element_by_xpath(xpath)
        field.clear()
        field.send_keys(keys)

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def like_photo_by_hashtag(self, hashtag: str, n: int) -> None:

        self.browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        sleep(5)

        for i in range(1, n):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(random.randrange(3, 5))

        links = self.browser.find_elements_by_tag_name('a')
        posts_urls = [link.get_attribute('href') for link in links if "/p/" in link.get_attribute('href')]

        for url in posts_urls:
            try:
                self.browser.get(url)
                sleep(3)
                like_button = self.browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                sleep(random.randrange(80, 100))
            except Exception as error:
                print(error)
                self.close_browser()

    def _xpath_exists(self, url: str) -> bool:

        try:
            self.browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False

        return exist

    def auth(self, login_xpath: str, password_xpath: str, enter_xpath: str, login: str, password: str) -> None:
        self._fill_field(login_xpath, login)
        sleep(random() * 3)

        self._fill_field(password_xpath, password)
        sleep(random() * 3)

        '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button'
        self.browser.find_element_by_xpath(enter_xpath).send_keys(Keys.ENTER)

    def put_like_to_post(self, userpost: str) -> None:

        self.browser.get(userpost)
        sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"

        if self._xpath_exists(wrong_userpage):
            print("Такого поста не существует, проверьте URL")
            self.close_browser()

        else:
            print("Пост успешно найден, ставим лайк!")
            sleep(2)

            like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
            self.browser.find_element_by_xpath(like_button).click()
            sleep(2)

            print(f"Лайк на пост: {userpost} поставлен!")
            self.close_browser()


    def put_likes_to_user(self, userpage: str) -> None:

        self.browser.get(userpage)
        sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self._xpath_exists(wrong_userpage):
            print("Такого пользователя не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пользователь успешно найден, ставим лайки!")
            sleep(2)

            posts_count = int(self.browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/a/span").text)
            loops_count = int(posts_count / 12) + 1
            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                urls: list = self.browser.find_elements_by_tag_name('a')
                urls: list = [url.get_attribute('href') for url in urls if "/p/" in url.get_attribute('href')]

                url = None

                for url in urls:
                    posts_urls.append(url)

                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(randrange(2, 4))
                print(f"Итерация #{i}")

            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            set_posts_urls = list(set(posts_urls))

            with open(f'{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

            with open(f'{file_name}_set.txt') as file:
                urls_list = file.readlines()

                for post_url in urls_list:
                    try:
                        self.browser.get(post_url)
                        sleep(2)

                        like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
                        self.browser.find_element_by_xpath(like_button).click()
                        # time.sleep(random.randrange(80, 100))
                        sleep(2)

                        print(f"Лайк на пост: {post_url} успешно поставлен!")
                    except Exception as error:
                        print(error)
                        self.close_browser()

            self.close_browser()