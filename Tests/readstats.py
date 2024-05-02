import pandas as pd
import tkinter as tk
from tkinter import ttk

fileread = pd.read_excel("Stats Files/StatsFile.xlsx")

# Write the PlayerName 3 rows down into a playername variable

root = tk.Tk()
root.title("Stats")
root.geometry("1200x400")

# Create a treeview

spacelabel = tk.Label(root, text=" ")
spacelabel.pack(pady=5)

tree = ttk.Treeview(root, show="headings")
tree["columns"] = ("PlayerName", "TeamName", "DamageDone", "Placement", "Kills")
tree.heading("PlayerName", text="PlayerName")
tree.heading("TeamName", text="TeamName")
tree.heading("DamageDone", text="DamageDone")
tree.heading("Placement", text="Placement")
tree.heading("Kills", text="Kills")
tree.pack()

# Insert the data into the treeview

for index, row in fileread.iterrows():
    tree.insert("", "end", values=(row["PlayerName"], row["TeamName"], row["DamageDone"], row["Placement"], row["Kills"]))

root.mainloop()



