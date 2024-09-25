from PIL import Image
import os

def resolution(path, newPath, newW, newH):
    image = Image.open(path)

    newImg = image.resize((newW, newH))

    newImg.save(newPath)


if __name__ == "__main__":

    fileName = str(input("What is the name of the picture include file type extension:"))

    width = int(input("What do you want the new width to be:"))

    height = int(input("What do you want the new height to be:"))
    # Gives home path of user i.e C:Users\Natck\
    homePath = os.path.expanduser("~")

    imgPath = os.path.join(homePath, "Downloads", fileName)

    resizedImg = f"resized{fileName}"
    newPath = os.path.join(homePath, "OneDrive", "Pictures", "Saved Pictures", resizedImg)

    resolution(imgPath, newPath, width, height)

