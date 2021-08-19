from scraper import *
from collage import *
import sys

def main():
    if (len(sys.argv) != 4):
        print("invalid usage: python3 scraper.py [board url] [collage width] [max image size]")
        return 100
    
    #scrape image urls from pinterest board
    scraper = Scraper(sys.argv[1])
    scraper.log_in()
    scraper.parse()
    imageURLs = scraper.get_image_urls()

    #create collage of images
    collager = Collager(imageURLs, int(sys.argv[2]), int(sys.argv[3]))
    collager.convert_to_images()
    collager.resize_images()
    
    arrangement = collager.arrange_collage()
    collager.create_collage(arrangement)

if __name__ == "__main__":
    main()