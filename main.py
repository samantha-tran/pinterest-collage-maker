from scraper import *
from collage import *
import sys

def main():
    if (len(sys.argv) != 2):
        print("invalid usage: python3 scraper.py [board url]")
        return 100
    
    #scrape image urls from pinterest board
    scraper = Scraper(sys.argv[1])
    scraper.log_in()
    scraper.parse()
    imageURLs = scraper.get_image_urls()

    #create collage of images
    collager = Collager(imageURLs)
    collager.convert_to_images()

    while 1:
        pass

if __name__ == "__main__":
    main()