from PIL import Image   # need for image manipulation
import os               # need for path finding

def resolution(path, newPath, newW, newH, flip=False):
    image = Image.open(path)    # opens the img file

    # flips the image horizontally
    if flip:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)

    # change resolution of iamge
    newImg = image.resize((newW, newH))

    # sends new image to specified directory
    newImg.save(newPath)

# checks if the script is being run directly or if run from
# somewhere else
if __name__ == "__main__":

    # prompts user for file, desire width, and desire height
    fileName = str(input("What is the name of the picture include file type extension:"))

    width = int(input("What do you want the new width to be:"))

    height = int(input("What do you want the new height to be:"))

    # Gives home path of user i.e C:Users\Natck\
    homePath = os.path.expanduser("~")

    # variable for directory of image being resized
    imgPath = os.path.join(homePath, "Downloads", fileName)

    # renames the image after being resized
    resizedImg = f"resized{fileName}"

    # directory where the resized image is sent
    newPath = os.path.join(homePath, "OneDrive", "Pictures", "Saved Pictures", resizedImg)

    # calling the function
    resolution(imgPath, newPath, width, height)

