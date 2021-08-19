from PIL import Image
import urllib.request

# collaging algorithm: credit to 'http://delimitry.blogspot.com/2014/07/picture-collage-maker-using-python.html'

MARGIN_SIZE = 2

class Collager:
    def __init__(self, imageURLs, maxCollageWidth, initialImageHeight):
        self.imageURLs = imageURLs
        self.imageSizes = {}
        self.maxWidth = maxCollageWidth
        self.initialImageHeight = initialImageHeight

    def convert_to_images(self):
        print("fetching images")
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

        print("Creating your collage!")
        row = [] #images that make up a row
        collageRows = [] #((float)resizing coefficient, row)
        currentWidth = 0

        for imageURL in self.imageSizes:
            #start new row if over max collage width
            if ((currentWidth >= self.maxWidth)):
                collageRows.append((float(self.maxWidth) / float(currentWidth), row[:]))
                row = []
                currentWidth = 0
            
            currentWidth += self.imageSizes[imageURL][0] + MARGIN_SIZE
            row.append(imageURL)
        
        #add last line
        collageRows.append((1, row[:]))
        
        return collageRows[:]

    def create_collage(self, collageRows):

        #create collage base
        height = self._get_collage_height(collageRows)
        collageImage = Image.new('RGB', (self.maxWidth, height), (255, 255, 255))

        y = 0 #offset of image on the y-axis

        for (coefficient, imageRow) in collageRows:

            x = 0 #offset of image on the x-axis

            for imageURL in imageRow:

                dimensions = self.imageSizes[imageURL]
                imageName, header = imageName, header = urllib.request.urlretrieve(imageURL)
                image = Image.open(imageName)

                ratio = float(self.initialImageHeight * coefficient) / float(dimensions[1])
                image = image.resize((int(dimensions[0] * ratio), int(dimensions[1] * ratio)), Image.ANTIALIAS)
                collageImage.paste(image, (int(x), int(y)))
                x += image.size[0] + MARGIN_SIZE

            y += int(self.initialImageHeight * coefficient) + MARGIN_SIZE

        print("Collage is done!")
        collageImage.show()
        collageImage.save("collage.png")

    def _get_collage_height(self, collageRows):
        height = 0
        for (coefficient, imageRow) in collageRows:
            height += int(self.initialImageHeight * coefficient) + MARGIN_SIZE
        return height

