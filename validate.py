import db
import sqlite3 as sql

connection = sql.connect("database.db")
cursor = connection.cursor()

def emailIsValid(Email, Role):
    """Validates an email address."""
    validEmail = False
    # Start by checking if the email is valid (it must contain an @ symbol and a .) and cannot contain spaces
    if "@" in Email and "." in Email:
        validEmail = True

        if any(i.isspace() for i in Email):
            validEmail = False
        else:
            validEmail = True
    else:
        validEmail = False

    takenEmail = False
    getAllRowsAdmin = db.getAllRows(cursor, "tbl_Administrators")
    getAllRowsParticipants = db.getAllRows(cursor, "tbl_Participants")
    if Role == "Admin":
        for row in getAllRowsAdmin:
            if Email == row[5]:
                takenEmail = True
    
    elif Role == "Participant":
        for row in getAllRowsParticipants:
            if Email == row[2]:
                takenEmail = True
    
    if takenEmail == True and validEmail == True:
        return "Taken"
    elif takenEmail == False and validEmail == True:
        return True
    else:
        return False
    
def usernameIsValid(Username):
    """"Validates the username, no longer than 15chars, no shorter than 6chars and no spaces or special characters."""
    validUsername = False
    if len(Username) <= 15 and len(Username) >= 6:
        if any(i.isspace() for i in Username):
            validUsername = False
        else:
            validUsername = True
    else:
        validUsername = False

    takenUsername = False
    getAllRowsAccounts = db.getAllRows(cursor, "tbl_Accounts")
    for row in getAllRowsAccounts:
        if Username == row[1]:
            takenUsername = True

    if takenUsername == True and validUsername == True:
        return "Taken"
    elif takenUsername == False and validUsername == True:
        return "Valid"
    else:
        return "Invalid"

def passwordIsValid(Password, ConfirmPassword):
    """Validates the password, no shorter than 8 chars no longer than 18 chars must have 1 number and 1 upper case letter."""
    validPassword = False
    passwordsMatch = False
    if len(Password) >= 8 and len(Password) <= 18:
        if any(i.isdigit() for i in Password) and any(i.isupper() for i in Password):
            validPassword = True
        else:
            validPassword = False
    else:
        validPassword = False

    if Password == ConfirmPassword:
        passwordsMatch = True
    else:
        passwordsMatch = False

    if validPassword == True and passwordsMatch == True:
        return "Valid"
    if validPassword == False:
        return "Invalid"
    if validPassword == True and passwordsMatch == False:
        return "MatchError"
    
def lengthCheck(Entry, maxLength, minLength):
    """"Checks the length of the entry"""
    if len(Entry) <= maxLength and len(Entry) >= minLength:
        return "Valid"
    else:
        return "Invalid"
    
def timeCheck(time):
    # First lets ensure the string is not empty
    if time == "":
        return False
                
    # Now lets check if the time has a coloon in the middle
    if ":" not in time:
        return False
                
    # Now lets check if the time is in integers
    timeParts = time.split(":")
    try:
        hours = int(timeParts[0])
        minutes = int(timeParts[1])
    except ValueError:
        return False
                
    # Now lets check if the hours and minutes are within the correct range
    if hours < 0 or hours > 23:
        return False
    if minutes < 0 or minutes > 59:
        return False
                
    return True

def duplicateCheck(Entry, Table, Column):
    """Checks if the entry is already in the table."""
    getAllRows = db.getAllRows(cursor, Table)
    for row in getAllRows:
        if Entry == row[Column]:
            return "Taken"
    return "Valid"

def emailCheck(emailGiven):
    """Checks if the email format is valid."""
    emailParts = emailGiven.split("@")
    
    if len(emailParts) != 2:
        return "Formatting Error"
    
    userPart = emailParts[0]
    domainPart = emailParts[1]
    
    if len(userPart) == 0 or len(domainPart) == 0:
        return "Formatting Error"
    
    if userPart[0] == "." or userPart[len(userPart)-1] == ".":
        return "Formatting Error"
    
    if domainPart[0] == "." or domainPart[len(domainPart)-1] == ".":
        return "Formatting Error"
    
    validType = [".", "_"]
    for char in userPart:
        if not char.isalnum() and char not in validType:
            return "Formatting Error"
    
    for char in domainPart:
        if not char.isalnum() and char != ".":
            return "Formatting Error"
    
    if domainPart.count(".") < 1:
        return False
    
    takenEmail = False
    
    return True

def presenceCheck(Entry):
    """Checks if the entry is empty."""
    if Entry == "":
        return "Invalid"
    else:
        return "Valid"
