#Create a tkinter window with a drop down

import tkinter as tk
from tkinter import *

def Main():

    def RefreshOptions():
        NewOption = EntryVar.get()
        Options.append(NewOption)

        menu = DropDown["menu"]
        menu.delete(0, "end")

        menu.add_command(label="Select an Option", command=lambda value="Select an Option": EntryVar.set(value))


    MainWindow = Tk()
    MainWindow.title("Tournament Management System")
    MainWindow.geometry("400x400")

    #Create a drop down menu

    Options = ["Option 1", "Option 2", "Option 3", "Option 4"]
    DropDown = tk.OptionMenu(MainWindow, "Select an Option", *Options)

    EntryVar = StringVar()
    EntryBox = Entry(MainWindow, textvariable=EntryVar)
    EntryBox.pack()

    RefreshButton = Button(MainWindow, text="Refresh Options", command=RefreshOptions)
    RefreshButton.pack()

    DropDown.pack()

    MainWindow.mainloop()

Main()