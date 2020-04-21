from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class Instagram():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    def close(self):

        self.driver.close()

    def login(self):
        #odpalenie strony startowej
        driver = self.driver
        driver.get("https://www.instagram.com/")
        assert 'Instagram' in driver.title

        #logowanie
        time.sleep(1)
        login_button = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]")
        login_button.click()


        user_elem = driver.find_element_by_xpath("//input[@name='username']")
        password_elem = driver.find_element_by_xpath("//input[@name='password']")

        user_elem.clear()
        user_elem.send_keys(self.username)

        password_elem.clear()
        password_elem.send_keys(self.password)
        password_elem.send_keys(Keys.RETURN)

        #wyłączenie powiadomienia
        time.sleep(10)
        context = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[2]")
        time.sleep(3)
        context.click()

    def count_photo(self, hashtag):
        #przekierowanie do zdjęć z danym hasztagiem
        time.sleep(1)
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")

        #przewijaj stronę 3 razy i zrób każdej zdjęcie
        for i in range(1, 4):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.save_screenshot(hashtag + str(i) + '.png')
            time.sleep(1)

        #wyliczenie wyświetlanych zdjęć
        element = driver.find_elements_by_tag_name('a')
        picture_href = [a.get_attribute('href') for a in element]

        #łączna ilośc hasztagów
        all_photo = driver.find_element_by_xpath("/html/body/div[1]/section/main/header/div[2]/div[1]/div[2]/span/span")
        print(hashtag + " displays " + str(len(picture_href)) + " photos with " + str(all_photo.text))

        #powiązane hasztagi
        related_hashtag = driver.find_element_by_xpath('/html/body/div[1]/section/main/header/div[2]/div[2]/span/span[2]')
        print('Related hashtag: ' + str(related_hashtag.text))

        #przewijanie po powiązanych hasztagach
        for o in picture_href:
            driver.get(o)
            print(o)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
            if o == 'https://www.instagram.com/explore/tags/pusto/':
                return


if __name__ == '__main__':

    user = 'thasente99'
    passw = 'fie5aeMu0'

    #wywołanie
    user = Instagram(username=user, password=passw)
    user.login()
    user.count_photo('Noc')
    user.close()