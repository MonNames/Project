import sqlite3 as sql
import db
from datetime import datetime

connection = sql.connect("database.db")
cursor = connection.cursor()

def frameSwitchGeometry(controller, frame, newGeometry):
    """Switches the geometry of a frame."""
    controller.show_frame(frame)
    controller.geometry(newGeometry)

def newCheckPastFuture(self, searchingFor, dropDown):
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
        menu.add_command(label=tournament[1], command=lambda value=tournament[1]: dropDown.set(value))

    self.after(1000, lambda: newCheckPastFuture(self, searchingFor, dropDown))

