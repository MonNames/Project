import sqlite3 as sql
import db
from datetime import datetime
from tkinter import messagebox, ttk
import tkinter as tk
from tkinter import messagebox
from idlelib.tooltip import Hovertip

connection = sql.connect("dbase.db")
cursor = connection.cursor()

def frameSwitchGeometry(frameLevel, frame, newGeometry):
    """Switches the geometry of a frame."""
    frameLevel.show_frame(frame)
    frameLevel.geometry(newGeometry)

def newCheckPastFuture(self, searchingFor, dropDown, SelectedTournament):
    """Checks if the user is searching for past, future or all tournaments."""
    UpdatedList = []
    allTournaments = db.getAllRows(cursor, "tbl_Tournaments")
    currentDate = datetime.now()

    if searchingFor == "past":
        for row in allTournaments:
            if datetime.strptime(row[2], "%d-%m-%Y") < currentDate:
                UpdatedList.append(row)
    
    elif searchingFor == "future":
        for row in allTournaments:
            if datetime.strptime(row[2], "%d-%m-%Y") > currentDate:
                UpdatedList.append(row)
    
    elif searchingFor == "all":
        for row in allTournaments:
            UpdatedList.append(row)
    
    menu = dropDown["menu"]
    menu.delete(0, "end")

    for tournament in UpdatedList:
        menu.add_command(label=tournament[1], command=lambda value=tournament[1]: SelectedTournament.set(value))

    self.after(1000, lambda: newCheckPastFuture(self, searchingFor, dropDown, SelectedTournament))

def calculateScore(placement, kills, teamPlacementEntry, teamKillsEntry):
    """Calculates the score of a team based on their placement and kills."""
    OverallScore = 0
    validPlacement = False
    validKills = False

    try:
        placement = int(placement)
        # Calculates score based on placement (ALGS Scoring System based)
        if placement == 1:
            OverallScore += 12
            validPlacement = True
        elif placement == 2:
            OverallScore += 9
            validPlacement = True
        elif placement == 3:
            OverallScore += 7
            validPlacement = True
        elif placement == 4:
            OverallScore += 5
            validPlacement = True
        elif placement == 5:
            OverallScore += 4
            validPlacement = True
        elif placement >= 6 and placement <= 10:
            OverallScore += 2
            validPlacement = True
        elif placement >= 11 and placement <= 15:
            OverallScore += 1
            validPlacement = True
        elif placement >= 16 and placement <= 20:
            OverallScore += 0
            validPlacement = True
        else:
            # If the user enters a placement that is not within the range of 1-20
            messagebox.showerror("Error", "Please enter a valid team placement.")
            validPlacement = False
    except ValueError:
        # If the user enters a non-integer value
        messagebox.showerror("Error", "Please enter a valid team placement.")

    try:
        # Calculates score based on kills (1 kill = 1 point)
        kills = int(kills)
        if kills >= 0:
            validKills = True
        else:
            # If the user enters a negative number of kills
            messagebox.showerror("Error", "Please enter a valid number of team kills.")
            validKills = False
    except ValueError:
        # If the user enters a non-integer value
        messagebox.showerror("Error", "Please enter a valid number of team kills.")

    if validPlacement and validKills:
        OverallScore += kills
        messagebox.showinfo("Score", "Your team scored " + str(OverallScore) + " points!")

    teamPlacementEntry.delete(0, "end")
    teamKillsEntry.delete(0, "end")

def show_and_hide(PasswordEntry, ConfirmPasswordEntry):
    """Shows and hides the password."""
    if PasswordEntry["show"] == "":
        PasswordEntry["show"] = "*"
    else:
        PasswordEntry["show"] = ""

    if ConfirmPasswordEntry != "None":
        if ConfirmPasswordEntry["show"] == "":
            ConfirmPasswordEntry["show"] = "*"
        else:
            ConfirmPasswordEntry["show"] = ""

def makeBackButton(frame, backTo, controller):
    """Creates a back button in the top left corner."""
    backIcon = tk.PhotoImage(file="Images and Icons/Leave_Icon.png")
    BackButton = ttk.Button(frame, image = backIcon, compound="left", style="Toolbutton", takefocus=False,
                            command=lambda: controller.show_frame(backTo))
    BackButton.image = backIcon
    BackButton.place(relx=0.05, rely=0.03, anchor="center")

class CreateToolTip(object):
    """create a tooltip for a given widget"""
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
