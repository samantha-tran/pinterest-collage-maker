from random import randint
from time import sleep
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image

try:
    from test_details import EMAIL, PASSWORD
except Exception as e:
    print(e)

MAX_SCROLLS = 20

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
        for i in range(0, MAX_SCROLLS):
            imgs = self.driver.find_elements_by_tag_name("img")
            for img in imgs:
                imageURL = img.get_attribute("src")
                if (imageURL in self.imageURLs):
                    break
                else:
                    self.imageURLs.append(img.get_attribute("src"))
            self.driver.execute_script("window.scrollTo(0,{0})".format(i * (self.driver.get_window_size()["height"])))

    def _find_element(self):
        element = self.driver.find_elements_by_id("data")
        if element:
            return element
        else:
            return False

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