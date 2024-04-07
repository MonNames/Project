# Lets start by going through the file and reading the data
with open("NewStatsFile.txt", "r") as file:
    data = file.readlines()
    # Now lets go through each line and split the line by the comma
    playerDetailsList = []
    for line in data:
        line = line.split(",")
        playerNameLine = line[0]
        playerTeamLine = line[1]
        # Now lets create a variable that stores both the player name and the team name
        playerDetails = playerNameLine + " " + playerTeamLine
        playerDetailsList.append(playerDetails)

# Now lets delete the first index of the list as it does not contain any useful information
del playerDetailsList[0]


