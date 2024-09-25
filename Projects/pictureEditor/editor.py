from PIL import Image

def resolution(path, newPath, newW, newH):
    image = Image.open(path)

    newImg = image.resize((newW, newH))

    newImg.save(newPath)


if __name__ == "__main__":
    imgPath = "C:\Users\Natck\Downloads\reiFla.jpeg"
