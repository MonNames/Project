import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("30x30")
root.title("Tournament Management System")

my_img = ImageTk.PhotoImage(Image.open("Images and Icons/editicon.png"))

testButton = tk.Button(root, image=my_img, height = 1, width = 5, command=lambda: print("Test"))
testButton.pack()

root.mainloop()