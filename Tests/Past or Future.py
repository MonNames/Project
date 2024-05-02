from tkcalendar import Calendar
from tkinter import *
from datetime import datetime

root = Tk()
root.geometry("400x400")

calendar = Calendar(root, selectmode="day", year=2008, month=1, day=1)
calendar.pack(pady=20)

def grad_date():
    def past_or_future():
        if datetime.strptime(calendar.get_date(), "%m/%d/%y") < datetime.now():
            return "past"
        else:
            return "future"
    date.config(text="Selected Date is: " + calendar.get_date() + " Date is in the " + past_or_future())

button1 = Button(root, text="Get Date", command=grad_date)
button1.pack()

date = Label(root, text="")
date.pack(pady=20)

root.mainloop()