from back import musicPlayer   #import musicPlayer class from backend
import tkinter as tk
from tkinter import filedialog #used for selecting songs in file explorer

class musicPlayerApp:
    def __init__(self,root):
        self.root = root
        self.root.title("Music Player")

        #This creates instance/object of musicPlayer Class from backen
        self.player = musicPlayer()

        #makes a variable start that stores the tkinter button for loading song
        self.load = tk.Button(self.root, text="Load Song", command=self.loadSong)

        #makes a variable start that stores the tkinter button for playing song
        self.start = tk.Button(self.root, text="Play", command=self.playSong)

        #makes a variable start that stores the tkinter button for pausing song
        self.pause = tk.Button(self.root,text="Pause", command=self.pause)

        #makes a variable start that stores the tkinter button for ending song
        self.end = tk.Button(self.root,text="End", command=self.end)

        #makes a variable start that stores the tkinter button for resuming song
        self.resume = tk.Button(self.root,text="Resume", command=self.resume)



        #puts the buttons on the window called root
        self.load.pack()
        self.start.pack()
        self.pause.pack()
        self.end.pack()
        self.resume.pack()

    def loadSong(self):
        #this variable stores the path of the mp3 file selected
        # filedialog is from tkinter library and used to prompt the user to 
        # select file
        song = filedialog.askopenfilename(filetypes=[("Audio File", "*.mp3")])

        #checks if user selected a song
        if song:
            #the object of the musicPlayer class uses its method for loading song
            # song contains the path of the mp3 
            self.player.loadSong(song)


    def playSong(self):
        print("Playing Music")

        #the object of the musicPlayer class uses its method for starting song 
        self.player.startSong()

    def pause(self):
        print("Pause Song")

        #the object of the musicPlayer class uses its method for starting song 
        self.player.pauseSong()

    def resume(self):
        print("Resuming Song")

        #the object of the musicPlayer class uses its method for resuming song 
        self.player.unpauseSong()

    def end(self):
        print("End Song")

        #the object of the musicPlayer class uses its method for ending song 
        self.player.endSong()
    
#Checks if this is the main python program that is running or if this program is 
#being imported as a header file to another program
# if this is the main program that runs everything __name__ will equal __main__
# if this file is being imported then __name__ will be something else
# __name__ is a special python variable for scripts
if __name__ == "__main__":

    #This creates the tkinter object that is the window for GUI to be placed on
    root = tk.Tk()

    #creates class object and passes the tkinter window to
    app = musicPlayerApp(root)

    #keeps the window running
    root.mainloop()