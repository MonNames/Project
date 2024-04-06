import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
root.geometry("400x400")
root.title("ScrolledText Widget")

def get_text():
    text = input_area.get("1.0", tk.END)
    print(text)
    input_area.delete("1.0", tk.END)

input_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
input_area.pack(pady=20)

button = tk.Button(root, text="Get Text", command=get_text)
button.pack(pady=20)

root.mainloop()