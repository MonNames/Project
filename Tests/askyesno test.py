import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.geometry("30x30")
root.title("Tournament Management System")

def doFunction():
    shouldContinue = messagebox.askyesno("Continue?", "Do you want to continue?")
    if shouldContinue:
        print("Continuing")
    else:
        print("Not continuing")

testButton = tk.Button(root, text="Confirm", command=lambda: doFunction())
testButton.pack()

root.mainloop()