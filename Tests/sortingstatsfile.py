with open("statsfile1g.txt", "r") as file:
    data = file.readlines()
    # Now lets remove the newlines and whitespace
    data = [line.strip() for line in data]
    # Now lets count the number of unique team names, team names in the document are in the format "teamName": "EXAMPLETEAM"
    teamNames = []
    for line in data:
        if "teamName" in line:
            teamNames.append(line)
    
    # Now lets remove the "teamName": part of the string
    teamNames = [teamName.split(":")[1] for teamName in teamNames]
    # Now lets remove the quotation marks
    teamNames = [teamName.replace('"', "") for teamName in teamNames]

    teamNames = set(teamNames)

    # Now lets do the same for each player, format is "playerName": "EXAMPLEPLAYER"
    playerNames = []
    for line in data:
        if "playerName" in line:
            playerNames.append(line)
    
    playerNames = [playerName.split(":")[1] for playerName in playerNames]
    playerNames = [playerName.replace('"', "") for playerName in playerNames]

    playerNames = set(playerNames)

    # Now lets remove all the }, }, and { from the data
    data = [line for line in data if line != "{" and line != "}" and line != "},"]
    # Now lets add a new line in the line before each time we see playerName
    for i in range(len(data)):
        if "playerName" in data[i]:
            data[i] = "\n" + data[i]
    
    # Now lets remove all the new lines between when we see one playerName and the next
    data = "".join(data)
    data = data.split("\n")
    data = [line for line in data if line != ""]
    
    with open("NewStatsFile.txt", "w") as newFile:
        data = "\n".join(data)
        data = data.strip()
        newFile.write(data)
            

    
    
