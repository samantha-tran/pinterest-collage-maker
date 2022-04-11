from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

try:
    from details import EMAIL, PASSWORD
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
        self.driver = webdriver.Firefox()
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
        sleep(randint(5,8))
    
    def parse(self):
        self.driver.get(self.boardURL)

        images = wait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//img[@alt!='' and @srcset!='']")))
        
        previousImages = images[:]

        self._add_URLs(images)
        
        while True:
            #scroll to last image of list and wait for new images to load
            self.driver.execute_script('arguments[0].scrollIntoView();', images[-1])
            sleep(randint(5,8))

            try:
                images = wait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//img[@alt!='']")))
                self._add_URLs(images)

                #if new parsed images are the same as the old ones, end of board reached
                if (images[-1].id == previousImages[-1].id):
                    print("Reached the end of the board!")
                    raise TimeoutException
                
                #if images are new, append to list of previously stored images
                previousImages = images[:]

            except TimeoutException:
                break
            
    def get_image_urls(self):
        return list(self.imageURLs.values())

    def _add_URLs(self, images):
        for image in images:
            #only add distinct URLS
            if (image.id not in self.imageURLs):
                self.imageURLs[image.id] = image.get_attribute("src")
