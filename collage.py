from PIL import Image
import urllib.request

#use Image.open() method to open image
#   to test if it's working, use the storedImage.show() method
# collaging algorithm: credit to 'http://delimitry.blogspot.com/2014/07/picture-collage-maker-using-python.html'

MARGIN_SIZE = 5

class Collager:
    def __init__(self, imageURLs, maxCollageWidth, maxCollageHeight, initialImageHeight):
        self.imageURLs = imageURLs
        self.images = []
        self.maxWidth = maxCollageWidth
        self.maxHeight = maxCollageHeight
        self.initialImageHeight = initialImageHeight

    def convert_to_images(self):
        for imageURL in self.imageURLs:
            imageName, header = urllib.request.urlretrieve(imageURL)
            image = Image.open(imageName)
            self.images.append(image)

    def resize_images(self):
        for i in range(0, len(self.images)):
            image = self.images[i]
            heightRatio = (self.initialImageHeight / float(image.size[1]))
            width = int((float(image.size[0]) * float(heightRatio)))
            self.images[i] = image.resize((width, self.initialImageHeight), Image.LANCZOS)

    def create_collage(self):
        """ fixed_height = 420
        image = Image.open('1.jpeg')
        height_percent = (fixed_height / float(image.size[1]))
        width_size = int((float(image.size[0]) * float(height_percent)))
        image = image.resize((width_size, fixed_height), PIL.Image.NEAREST)
        image.save('resized_nearest.jpg') """
        for image in self.images:
            pass
