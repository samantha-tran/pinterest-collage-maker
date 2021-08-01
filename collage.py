from PIL import Image
import urllib.request

#use Image.open() method to open image
#   to test if it's working, use the storedImage.show() method
# collaging algorithm: credit to 'http://delimitry.blogspot.com/2014/07/picture-collage-maker-using-python.html'

MARGIN_SIZE = 2

class Collager:
    def __init__(self, imageURLs, maxCollageWidth, initialImageHeight):
        self.imageURLs = imageURLs
        self.imageSizes = {}
        self.maxWidth = maxCollageWidth
        self.initialImageHeight = initialImageHeight

    def convert_to_images(self):
        for imageURL in self.imageURLs:
            imageName, header = urllib.request.urlretrieve(imageURL)
            with Image.open(imageName) as image:
                self.imageSizes[imageURL] = [image.size[0], image.size[1]]

    def resize_images(self):
        for imageURL in self.imageSizes:

            heightRatio = (self.initialImageHeight / float(self.imageSizes[imageURL][1]))

            width = int((float(self.imageSizes[imageURL][0]) * float(heightRatio)))

            self.imageSizes[imageURL] = [width, self.initialImageHeight]

    def arrange_collage(self):

        row = [] #images that make up a row
        collageRows = [] #((float)resizing coefficient, row)
        currentWidth = 0

        for imageURL in self.imageSizes:
            currentWidth += self.imageSizes[imageURL][0] + MARGIN_SIZE
            row.append(imageURL)

            if ((currentWidth >= self.maxWidth)):
                collageRows.append((float(currentWidth) / float(self.maxWidth), row[:]))
                row = []
                currentWidth = 0
        
        #add last line
        collageRows.append((float(currentWidth) / float(self.maxWidth), row[:]))
        
        return collageRows[:]

    def create_collage(self, collageRows):

        #create collage base
        height = self._get_collage_height(collageRows)
        collageImage = Image.new('RGB', (self.maxWidth, height), (255, 255, 255))

        y = 0 #offset of image on the y-axis

        for (coefficient, imageRow) in collageRows:

            x = 0 #offset of image on the x-axis

            for imageURL in imageRow:

                imageName, header = imageName, header = urllib.request.urlretrieve(imageURL)
                image = Image.open(imageName)

                dimensions = self.imageSizes[imageURL]

                ratio = (self.initialImageHeight / coefficient) / dimensions[1]
                if (ratio > 1):
                    #enlarge image
                    image = image.resize((int(dimensions[0] * ratio), int(dimensions[1] * ratio)), Image.ANTIALIAS)
                else:
                    #minimise image
                    image.thumbnail((int(self.maxWidth / coefficient), int(self.initialImageHeight / coefficient)), Image.ANTIALIAS)
                collageImage.paste(image, (int(x), int(y)))

                x += image.size[0] + MARGIN_SIZE

            y += int(self.initialImageHeight / coefficient) + MARGIN_SIZE

        collageImage.show()

    def _get_collage_height(self, collageRows):
        height = 0
        for (coefficient, imageRow) in collageRows:
            height += int(self.initialImageHeight / coefficient) + MARGIN_SIZE
        return height

