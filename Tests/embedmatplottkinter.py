import tkinter as tk 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.title("Embedding in Tk")
root.geometry("1200x400")

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

root.mainloop()
