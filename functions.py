import db

def RefreshTournaments(cursor, TournamentsAvailable, SelectedTournament):
    #First we need to get the updated tournaments list
    UpdatedTournaments = []
    allTournaments = db.getAllRows(cursor, "tbl_Tournaments")
    for row in allTournaments:
        UpdatedTournaments.append(row[1])
    
    # Wipe the details from the current Option Menu
    menu = TournamentsAvailable["menu"]
    menu.delete(0, "end")

    # Now we need to add the updated tournaments to the Option Menu
    for tournament in UpdatedTournaments:
        menu.add_command(label=tournament, command=lambda value=tournament: SelectedTournament.set(value))
