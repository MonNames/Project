#Create a tkinter window with a drop down

import tkinter as tk
from tkinter import *

def Main():

    def UpdateValue(Value):
        Value += 1
        DisplayValueLabel.config(text="Value: " + str(Value))
        root.after(1000, UpdateValue, Value)
        
    root = tk.Tk()
    root.geometry("30x30")
    root.title("Tournament Management System")

    Value = 0
    DisplayValueLabel = Label(root, text="Value: " + str(Value))
    DisplayValueLabel.pack()

    # Recursively update the value every second
    UpdateValue(Value)

    root.mainloop()

Main()

