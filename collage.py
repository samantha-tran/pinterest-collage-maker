from PIL import Image
import urllib.request

#use Image.open() method to open image
#   to test if it's working, use the storedImage.show() method
# collaging algorithm: credit to 'http://delimitry.blogspot.com/2014/07/picture-collage-maker-using-python.html'

MARGIN_SIZE = 2

class Collager:
    def __init__(self, imageURLs, maxCollageWidth, initialImageHeight):
        self.imageURLs = imageURLs
        self.images = []
        self.maxWidth = maxCollageWidth
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

    def arrange_collage(self):

        row = [] #images that make up a row
        collageRows = [] #((float)resizing coefficient, row)
        currentWidth = 0
        images = self.images[:]

        while images:
            image = images.pop()
            currentWidth += image.size[0] + MARGIN_SIZE
            row.append(image)

            if ((currentWidth >= self.maxWidth)):
                collageRows.append((float(currentWidth) / float(self.maxWidth), row[:]))
                row = []
                currentWidth = 0
        
        #add last line
        collageRows.append((float(currentWidth) / float(self.maxWidth), row[:]))
        
        return collageRows[:]

    def create_collage(self, collageRows):

        height = self._get_collage_height(collageRows)

        collageImage = Image.new('RGB', (self.maxWidth, height), (255, 255, 255))

        y = 0 #offset of image on the y-axis

        for (coefficient, imageRow) in collageRows:

            x = 0 #offset of image on the x-axis

            for image in imageRow:

                ratio = (self.initialImageHeight / coefficient) / image.size[1]

                if (ratio > 1):
                    #enlarge image
                    image = image.resize((int(image.size[0] * ratio), int(image.size[1] * ratio)), Image.ANTIALIAS)
                elif (coefficient < 1):
                    #minimise image
                    image = image.thumbnail((int(self.maxWidth / coefficient), int(self.initialImageHeight / coefficient)), Image.ANTIALIAS)
                
                collageImage.paste(image, (int(x), int(y)))

                x += image.size[0] + MARGIN_SIZE

            y += int(self.initialImageHeight / coefficient) + MARGIN_SIZE

        collageImage.show()

    def _get_collage_height(self, collageRows):
        height = 0
        for (coefficient, imageRow) in collageRows:
            height += int(self.initialImageHeight / coefficient) + MARGIN_SIZE
        return height

