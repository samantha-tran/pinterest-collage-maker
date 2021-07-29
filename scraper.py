from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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

class Scraper:
    def __init__(self, boardURL):
        self.driver = webdriver.Chrome()
        self.boardURL = boardURL
        self.imageURLs = {}

    def log_in(self):
        self.driver.maximize_window()
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
        
        images = wait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//img[@alt!='' and @srcset!='']")))
        
        previousImages = images[:]

        self._add_URLs(images)
        
        while True:
            self.driver.execute_script('arguments[0].scrollIntoView();', images[-1])
            sleep(randint(3,5))

            try:
                images = wait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//img[@alt!='' and @srcset!='']")))
                self._add_URLs(images)

                if (images[-1].id == previousImages[-1].id):
                    print("Reached the end of the board!")
                    raise TimeoutException

                previousImages = images[:]

            except TimeoutException:
                break
        
        for key in self.imageURLs:
            print(self.imageURLs[key])
        print(len(self.imageURLs))

    def get_image_urls(self):
        imageURLs = []
        for key in self.imageURLs:
            imageURLs.append(self.imageURLs[key])
        return imageURLs

    def _add_URLs(self, images):
        for image in images:
            if (image.id not in self.imageURLs):
                self.imageURLs[image.id] = image.get_attribute("src")
