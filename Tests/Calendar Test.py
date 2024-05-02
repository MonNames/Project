from tkcalendar import Calendar, DateEntry
from tkinter import *

root = Tk()
root.geometry("400x400")

calendar = DateEntry(root, selectmode="day", year=2008, month=1, day=1, date_pattern="dd-mm-yyyy")
calendar.pack(pady=20)

def grad_date():
    date.config(text="Selected Date is: " + calendar.get())

button1 = Button(root, text="Get Date", command=grad_date)
button1.pack()

date = Label(root, text="")
date.pack(pady=20)

root.mainloop()
