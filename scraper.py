from random import randint
from time import sleep
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image

try:
    from test_details import EMAIL, PASSWORD
except Exception as e:
    print(e)

# get image urls from pinterest board link
# for image url of each image
#   write URL in urllib.request.urlretrieve() method
#   use Image.open() method to open image
#   to test if it's working, use the storedImage.show() method
# collaging algorithm: credit to 'http://delimitry.blogspot.com/2014/07/picture-collage-maker-using-python.html'

#python3 
class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.boardURL = sys.argv[1]
        self.imageURLs = []

    def log_in(self):
        self.driver.get("https://www.pinterest.com.au/login/")

        #get log in elements
        emailElement = self.driver.find_element_by_id('email')
        passwordElement = self.driver.find_element_by_id('password')

        #enter log in details
        emailElement.send_keys(EMAIL)
        passwordElement.send_keys(PASSWORD)
        passwordElement.send_keys(Keys.RETURN)

        #wait for successful sign in
        sleep(randint(3,5))
    
    def parse(self):
        self.driver.get(self.boardURL)
        #wait for page to load - for larger boards, increase sleep time
        sleep(10)
        imgs = self.driver.find_elements_by_xpath("//img[@alt!='']")
        print(len(imgs))
        for img in imgs:
            imageURL = img.get_attribute("src")
            sleep(2)
            self.imageURLs.append(img.get_attribute("src"))
        print(self.imageURLs)
        print(len(self.imageURLs))


    def _get_scroll_amount(self):
        scrollHeight =  self.driver.execute_script("return document.body.scrollHeight")
        windowSize = self.driver.get_window_size()["height"]
        return scrollHeight // windowSize


def main():
    if (len(sys.argv) != 2):
        print("invalid usage: python3 scraper.py [board url]")
        return 100
    scraper = Scraper()
    scraper.log_in()
    scraper.parse()
    while 1:
        pass

if __name__ == "__main__":
    main()