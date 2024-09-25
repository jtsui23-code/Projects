from PIL import Image
import os

def resolution(path, newPath, newW, newH):
    image = Image.open(path)

    newImg = image.resize((newW, newH))

    newImg.save(newPath)


if __name__ == "__main__":

    fileName = str(input("What is the name of the picture include file type extension:"))

    # Gives home path of user i.e C:Users\Natck\
    homePath = os.path.expanduser("~")

    imgPath = os.path.join(homePath, "Downloads", fileName)

    newPath = os.path.join(homePath, "OneDrive", "Pictures", "Saved Pictures")

