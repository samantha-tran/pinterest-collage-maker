from PIL import Image
import urllib.request

#use Image.open() method to open image
#   to test if it's working, use the storedImage.show() method
# collaging algorithm: credit to 'http://delimitry.blogspot.com/2014/07/picture-collage-maker-using-python.html'

class Collager:
    def __init__(self, imageURLs, maxWidth, maxHeight):
        self.imageURLs = imageURLs
        self.images = []
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight

    def convert_to_images(self):
        for imageURL in self.imageURLs:
            imageName, header = urllib.request.urlretrieve(imageURL)
            self.images.append(Image.open(imageName))

    def create_collage(self):
        pass
        