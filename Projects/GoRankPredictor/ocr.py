#This program runs a GUI for an OCR used to extract text from a snipped image
# Process OCR Works for English and Japanese Horizontal text However doesn't 
# Properly copy text with vertical Japanese text

#try: is used to state attempt to run the code below it
#However if the code under try: causes an error than go to 
#except:
try:
    #this gets the ctypes library which contains librarys from C
    # windll this is an object from the ctypes library
    # windll gives you access to DLL's in window
    # DLL's are a type of libraries that can be accessed
    # by multiple applications at the same time 
    # and even be changed while other applications are using the DLL

    from ctypes import windll

    #this line accesses the shcore.DLL through windll
    #SetProcessDpiAwareness(1) makes the computer aware the screen is a 
    # HiDPI
    # DPI (Dot Per Inch) i.e number of pixals on the screen
    # higher resolution screen has a high DPI
    # if SetProcessDpiAwareness() was 0 instead then there is no DPI awareness
    # if set to 2 then Per monitor awareness for multiple monitors
    #Without DPI awareness the snip image will be scaled down because 
    # the program does not know how good the display is 
    windll.shcore.SetProcessDpiAwareness(1)  # Set process as DPI aware

#execpt: states what to do if the code under try: fails to work
# in this case if the code under try: fails then the program would run normally
# try-expect is used when dealing with anything that may fail because of OS or DLL 
# in this case since DLL can cause errors if they are updated and no longer compatible
# with the program that was relying on the DLL
except:
    pass


#This library is used for OCR and text extraction and is compatitible with many languages
import pytesseract

# This library allows to parse through strings using pattern
# recongition
import re

#This library deals with copy/paste system clipboard
import pyperclip

#This accesses the Pillow library(image capturing) and gets the ImageGrab function from it
from PIL import ImageGrab, ImageEnhance

#This accesses the tkinter library(makes GUI) and writes an abreviation ttk for using it
import tkinter as ttk



# gives access to the path for tesseract program 
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Natck\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# this gets the simpledialog function from tkinter
# simpledialog is used for displaying a prompt for user input
# messagebox is used for display just text for like warnings or confirmation
from tkinter import simpledialog, messagebox

ocrData = {
    'winHi': 0,
    'winLo':0,
    'lostHi':0,
    'lostLo':0,
    'rank':''
}

def addData(text):
    pass


#This is a function that will be used for snipping images used in the OCR
def ocr():

    #root is the GUI interface for the snip tool
    # adding .withdraw() to root hides the interface while the user is snipping an image
    root.withdraw()

    #this creates a mini window for selecting a snipped area
    selectScreen = ttk.Toplevel(root)

    #this makes the snip screen cover the whole screen
    selectScreen.attributes("-fullscreen", True)

    #this makes the window semi-transparent
    #alpha is a keey word for transparency in tkinter
    # if alpha is set to 0.0 then the window is invisible
    # if alpha is set to 1.0 than it is completely solid
    selectScreen.attributes("-alpha", 0.3)

    #This makes everything but the selected area black to make it easier for the user to snip the highlighted area
    selectScreen.config(bg='black')


    #This makes it to where the selection Screen that the snip rectangle is place upon
    # is at the top of EVERY window open even on hiden so the snip can happen properly

    selectScreen.lift()
    
    #This makes it to where any action done by keyboard or mouse is 
    # applied directly to the selectScreen and not any of the windows behind it
    selectScreen.focus_force()

    #IntVar() is a class in the tkinter library that holds the corindates of where mouse movement
    #This stores the x and y cordinate when the mouse is first clicked in IntVar()
    #This also stores the x and y cordinates of when the mouse is released 

    x_start, y_start, x_end, y_end = ttk.IntVar(), ttk.IntVar(), ttk.IntVar(), ttk.IntVar()

    #This function takes in a special parameter called event which is imported from tkinter
    #event is like the activator of the GUI ex) mouse click, key press, etc

    # the name of the event in tkinter for left mouse click is <ButtonPress-1>
    # the name for the event for the mouse scroller click is <ButtonPress-2>
    # the name for the event for the right mouse click would be <ButtonPress-3>
    def mouseClicked (event):

        #the inital x corindate of when the mouse is clicked in represented as 
        # event.x this is stored in the IntVariable x_start
        x_start.set(event.x)


        #the inital y corindate of when the mouse is clicked is represented by 
        #event.y and this is stored inside IntVariable called y_start
        y_start.set(event.y)

    #This function takes a special event parameter from tkinter
    # This function tracks the x and y cordinates of the mouse movement
    def mouseMovement(event):
        
        #This makes constantly updates the end point of where the mouse is being dragged to
        x_end.set(event.x)
        y_end.set(event.y)


        #this uses the coords() method from the Canvas funtion imported from tkinter
        # using coords( (box's name) x,y,x2,y2) allows you to set cordinates of the 
        # canvas(snip rectangle) this is constantly being updated while the mouse
        #  moving and being pressed
        canvas.coords(snipBox, x_start.get(), y_start.get(), x_end.get(), y_end.get())

    

    #This function takes an event parameter that is special to the tkinter library
    # This function sets the final cordinates of the snip rectangle when the mouse 
    # is released
    def mouseRelease(event):

        # this picks the smallest number out of the two x corindates and sets 
        # the intial x cordinate in x1
        # this is needed because if the user drags the snip rectangle left
        # then then x_end would be smaller then x_start
        #this makes it to where the top left corner will always have x1 cordinate
        # of the snip box
        x1 = min(x_start.get(), x_end.get())

        #this gets the bigger x cordinate out of the two varibles
        # .get() is needed to get the x values because 
        # x_start and x_end are variables inside of a class like strucutre so 
        # using .get() is needed to access their data
        x2 = max(x_start.get(), x_end.get())

        #this does the same thing for the y cordinates 
        y1 = min(y_start.get(),y_end.get())

        y2 = max(y_start.get(), y_end.get())

        #this closes the snip rectangle
        selectScreen.destroy()

        #this makes the snip GUI reappear 
        root.deiconify()


        #screenshot is a new varialbe created
        #the function ImageGrab from the pillow library is used
        #ImageGrab.grab() functions as a screenshot mechinism 
        #bbox stands for bounding box is the region of the snip rectangle
        #the cordinates created above are then put into the bounding box
        screenshot = ImageGrab.grab(bbox=(x1,y1,x2,y2))


        #this function takes an image as a parameter
        # this function makes the image it recieves into gray scale
        # 'L' stands for luminance and is used instead of RGB because
        # it is faster 
        def conTrasting(image):

            #This creates an obect called enhancer using Pill's ImageEnhance
            enhancer = ImageEnhance.Contrast(image)

            #the object then uses the method .enhance()
            # 1 means there is no change in the contrast
            # values greater than 1 increase contrast
            return enhancer.enhance(1.2)
        
        contrastedImage = conTrasting(screenshot)

        #this shows the contents of the screenshot
        contrastedImage.show()



        #this function recieves an image file as a parameter
        # this function extracts japanese text from an image and stores the text as a string
        # the string is return 
        def extractText(image):

            #this uses pytesseract OCR library to extract japanese text from snip
            # psm is page segmentation mode
            # different types of --psm
            # psm 11 - looks for as much text as possible
            # psm  6 - used for single block or paragraph
            # psm  7 - used for single line of text
            # psm 12 - like psm 11 but considers orientation of text 
            text = pytesseract.image_to_string(image, lang='jpn', config='--psm 6')

            return text 
        
        #this calls the extractText function and sends the screenshot/snip as a parameter
        # then stores the string/text in a varaible
        jpText = extractText(contrastedImage)

        pyperclip.copy(jpText)

        #HEREHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        #HEREHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        #HEREHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        #HEREHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        #HEREHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        #HEREHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH

        print("Text was extracted from snip")

    

    #this creates a canvas(small snip rectangle) using the Canvas() function in tkinter
    # the snip canvas is placed ontop of the selectScreen which contains the whole screen
    #this also makes the cursor become a cross to indicate snipping is occuring 
    canvas = ttk.Canvas(selectScreen, cursor="cross")


    #this makes it to where the canvas(snip rectangle) have access to the whole screen
    #fill means to fill up the whole selectScreen which was initlized earlier to be the 
    # ful screen and ttk.BOTH is a shortcut for doing both ttk.x and ttk.y
    canvas.pack(fill=ttk.BOTH, expand=True)
    
    snipBox = canvas.create_rectangle(0,0,0,0 , outline='red', width=2)


    #canvas.bind() makes it to where a specific event is bounded to a function
    # so <ButtonPress-1> is the event for mouse left click
    # <B1-Motion> is the event for mouse movement while left click on mouse is held
    # <ButtonRelease-1> is the event for releasing the left click on mouse
    canvas.bind("<ButtonPress-1>", mouseClicked)
    canvas.bind("<B1-Motion>", mouseMovement)
    canvas.bind("<ButtonRelease-1>", mouseRelease)




#This uses the function called Tk() which creates a window for the snip GUI
root = ttk.Tk()

root.title("OCR")



#this creates a button using the Button function in tkinter on the root interface
#The button as the word Snip on it
# The functionality of the button is determined by whatever comes after command= 
# so in this case whenever the button is pressed the ocr function is called
button = ttk.Button(root, text="OCR", command=ocr)

#This positions the button to be correctly sized on the root GUI
button.pack()

#This makes the snip tool wait for interaction or until the program is closed
root.mainloop()

