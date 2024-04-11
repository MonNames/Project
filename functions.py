import sqlite3 as sql
import db
from datetime import datetime
from tkinter import messagebox

connection = sql.connect("dbase.db")
cursor = connection.cursor()

def frameSwitchGeometry(frameLevel, frame, newGeometry):
    """Switches the geometry of a frame."""
    frameLevel.show_frame(frame)
    frameLevel.geometry(newGeometry)

def newCheckPastFuture(self, searchingFor, dropDown, SelectedTournament):
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
    
    menu = dropDown["menu"]
    menu.delete(0, "end")

    for tournament in UpdatedList:
        menu.add_command(label=tournament[1], command=lambda value=tournament[1]: SelectedTournament.set(value))

    self.after(1000, lambda: newCheckPastFuture(self, searchingFor, dropDown, SelectedTournament))

def calculateScore(placement, kills, teamPlacementEntry, teamKillsEntry):
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