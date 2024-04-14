import sqlite3 as sql

def createtbl_Accounts(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Accounts(
        UserID INTEGER PRIMARY KEY,
        Username VARCHAR(30),
        Password VARCHAR(30),
        Role VARCHAR(20)
        );'''
    cursor.execute(sql)

def createtbl_Administrators(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Administrators(
        AdminID INTEGER PRIMARY KEY,
        AdminDiscName VARCHAR(30),
        AdminFirstName VARCHAR(20),
        AdminSurname VARCHAR(20),
        AdminDOB VARCHAR(20),
        AdminEmail VARCHAR(50),
        UserID INTEGER,
        FOREIGN KEY (UserID) REFERENCES tbl_Accounts(UserID)
        );'''
    cursor.execute(sql)

def createtbl_Participants(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Participants(
        ParticipantID INTEGER PRIMARY KEY,
        ParticipantGameName VARCHAR(20) NOT NULL,
        ParticipantEmail VARCHAR(50),
        ParticipantGender VARCHAR(10),
        UserID INTEGER,
        FOREIGN KEY (UserID) REFERENCES tbl_Accounts(UserID)
        );'''
    cursor.execute(sql)

def createtbl_Teams(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Teams(
        TeamID INTEGER PRIMARY KEY,
        TeamName VARCHAR(20),
        TeamCaptainName VARCHAR(20) NOT NULL,
        TeamMember2 VARCHAR(20) NOT NULL,
        TeamMember3 VARCHAR(20) NOT NULL,
        TeamCoach VARCHAR(20),
        Status VARCHAR(15),
        TournamentID INTEGER,
        FOREIGN KEY (TeamCaptainName) REFERENCES tbl_Participants(ParticipantID),
        FOREIGN KEY (TournamentID) REFERENCES tbl_Tournaments(TournamentID)
        );'''
    cursor.execute(sql)

def createtbl_Tournaments(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Tournaments(
        TournamentID INTEGER PRIMARY KEY,
        TournamentName VARCHAR(20),
        TournamentDate DATE,
        TournamentTime TIME,
        TournamentDescription VARCHAR(100),
        MaxTeams INTEGER NOT NULL,
        NumGames INTEGER NOT NULL
        );'''
    cursor.execute(sql)

def createTables(cursor: sql.Cursor):
    """Create all tables."""
    createtbl_Accounts(cursor)
    createtbl_Administrators(cursor)
    createtbl_Participants(cursor)
    createtbl_Teams(cursor)
    createtbl_Tournaments(cursor)

def insertToAccountsTable(connection, cursor: sql.Cursor, data: list):
    """Insert data into the tbl_Accounts table."""
    sql = f"INSERT INTO tbl_Accounts(Username, Password, Role) VALUES(?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

def insertToAdministratorsTable(connection, cursor: sql.Cursor, data: list):
    """Insert data into the tbl_Administrators table."""
    sql = f"INSERT INTO tbl_Administrators(AdminDiscName, AdminFirstName, AdminSurname, AdminDOB, AdminEmail, UserID) VALUES(?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

def insertToParticipantsTable(connection, cursor: sql.Cursor, data: list):
    """Insert data into the tbl_Participants table."""
    sql = f"INSERT INTO tbl_Participants(ParticipantGameName, ParticipantEmail, ParticipantGender, UserID) VALUES(?, ?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

def insertToTeamsTable(connection, cursor: sql.Cursor, data: list):
    """Insert data into the tbl_Teams table."""
    sql = f"INSERT INTO tbl_Teams(TeamName, TeamCaptainName, TeamMember2, TeamMember3, TeamCoach, Status, TournamentID) VALUES(?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

def insertToTournamentsTable(connection, cursor: sql.Cursor, data: list):
    """Insert data into the tbl_Tournaments table."""
    sql = f"INSERT INTO tbl_Tournaments(TournamentName, TournamentDate, TournamentTime, TournamentDescription, MaxTeams, NumGames) VALUES(?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

def getAllRows(cursor: sql.Cursor, table: str):
    """Get all rows from a table."""
    sql = f"SELECT * FROM {table}"
    cursor.execute(sql)
    return cursor.fetchall()

def getSpecificRows(cursor: sql.Cursor, table, condition):
    """Get specific rows from a table based on a condition."""
    sql = f"SELECT * FROM {table} WHERE {condition}"
    cursor.execute(sql)
    return cursor.fetchone()

def getUserID(cursor: sql.Cursor, username: str):
    """Get the UserID of a user."""
    sql = f"SELECT UserID FROM tbl_Accounts WHERE Username = '{username}'"
    cursor.execute(sql)
    return cursor.fetchone()

def updateTournamentDetails(connection, cursor: sql.Cursor, data: list):
    """Update a row in the tbl_Tournaments table."""
    sql = f"UPDATE tbl_Tournaments SET TournamentName = ?, TournamentDate = ?, TournamentTime = ?, TournamentDescription = ? WHERE TournamentID = ?"
    cursor.execute(sql, data)
    connection.commit()

def updateUserPassword(connection, cursor: sql.Cursor, data: list):
    """Update the password of a user."""
    sql = f"UPDATE tbl_Accounts SET Password = ? WHERE UserID = ?"
    cursor.execute(sql, data)
    connection.commit()

def getAdminUserIDfromEmail(cursor: sql.Cursor, email: str):
    """Get the UserID of an admin from their email."""
    sql = f"SELECT UserID FROM tbl_Administrators WHERE AdminEmail = '{email}'"
    cursor.execute(sql)
    return cursor.fetchone()

def getUserIDfromEmail(cursor: sql.Cursor, email: str):
    """Get the UserID of a user from their email."""
    sql = f"SELECT UserID FROM tbl_Participants WHERE ParticipantEmail = '{email}'"
    cursor.execute(sql)
    return cursor.fetchone()

def deleteTournament(connection, cursor: sql.Cursor, TournamentID: int):
    """Delete a tournament."""
    sql = f"DELETE FROM tbl_Teams WHERE TournamentID = {TournamentID}"
    cursor.execute(sql)
    connection.commit()

def getAllTournamentNames(cursor: sql.Cursor):
    """Get all tournament names."""
    sql = "SELECT TournamentName FROM tbl_Tournaments"
    cursor.execute(sql)
    return cursor.fetchall()

def getTournamentName(cursor: sql.Cursor, TournamentID: int):
    """Get the name of a tournament."""
    sql = f"SELECT TournamentName FROM tbl_Tournaments WHERE TournamentID = {TournamentID}"
    cursor.execute(sql)
    return cursor.fetchone()

def deleteTeam(connection, cursor: sql.Cursor, TeamID: int):
    """Delete a team."""
    sql = f"DELETE FROM tbl_Teams WHERE TeamID = {TeamID}"
    cursor.execute(sql)
    connection.commit()

def getTeamName(cursor: sql.Cursor, TeamID: int):
    """Get the name of a team."""
    sql = f"SELECT TeamName FROM tbl_Teams WHERE TeamID = {TeamID}"
    cursor.execute(sql)
    return cursor.fetchone()

def getParticipantGameName(cursor: sql.Cursor, UserID: int):
    """Get the game name of a participant."""
    sql = f"SELECT ParticipantGameName FROM tbl_Participants WHERE UserID = {UserID}"
    cursor.execute(sql)
    return cursor.fetchone()

def createConstUser(connection, cursor: sql.Cursor):
    """Check if the user already exists, if not create a constant user."""
    sql = "SELECT * FROM tbl_Accounts WHERE Username = 'ConstUser' AND Password = 'Password1'"
    cursor.execute(sql)
    if cursor.fetchone() == None:
        insertToAccountsTable(connection, cursor, ["ConstUser", "Password1", "User"])
        UserID = getUserID(cursor, "ConstUser")
        UserID = UserID[0]
        insertToParticipantsTable(connection, cursor, ["ConstUserGameName", "woodyhenderson@hotmail.com", "Male", UserID])

def createConstAdmin(connection, cursor: sql.Cursor):
    """Check if the admin already exists, if not create a constant admin."""
    sql = "SELECT * FROM tbl_Accounts WHERE Username = 'ConstAdmin' AND Password = 'Password1'"
    cursor.execute(sql)
    if cursor.fetchone() == None:
        insertToAccountsTable(connection, cursor, ["ConstAdmin", "Password1", "Admin"])
        AdminID = getUserID(cursor, "ConstAdmin")
        AdminID = AdminID[0]
        insertToAdministratorsTable(connection, cursor, ["Admin", "Admin", "Admin", "01/01/2000", "samstournaments@gmail.com", AdminID])

def updateEmail(connection, cursor: sql.Cursor, data: list):
    sql = f"UPDATE tbl_Participants SET ParticipantEmail = ? WHERE UserID = ?"
    cursor.execute(sql, data)
    connection.commit()

def updateGameName(connection, cursor: sql.Cursor, data: list):
    sql = f"UPDATE tbl_Participants SET ParticipantGameName = ? WHERE UserID = ?"
    cursor.execute(sql, data)
    connection.commit()

def updatePassword(connection, cursor: sql.Cursor, data: list):
    sql = f"UPDATE tbl_Accounts SET Password = ? WHERE UserID = ?"
    cursor.execute(sql, data)
    connection.commit()

def getEmailfromUsername(cursor: sql.Cursor, username: str):
    sql = f"SELECT ParticipantEmail FROM tbl_Participants WHERE ParticipantGameName = '{username}'"
    cursor.execute(sql)
    return cursor.fetchone()

def updateDiscordName(connection, cursor: sql.Cursor, data: list):
    sql = f"UPDATE tbl_Administrators SET AdminDiscName = ? WHERE UserID = ?"
    cursor.execute(sql, data)
    connection.commit()

def updateUsername(connection, cursor: sql.Cursor, data: list):
    sql = f"UPDATE tbl_Accounts SET Username = ? WHERE UserID = ?"
    cursor.execute(sql, data)
    connection.commit()

def checkIfTournamentFull(cursor: sql.Cursor, TournamentID: int):
    sql = f"SELECT COUNT(TeamID) FROM tbl_Teams WHERE TournamentID = {TournamentID}"
    # If the number of teams in the tournament is equal to the max number of teams, return True
    cursor.execute(sql)
    if cursor.fetchone()[0] == getSpecificRows(cursor, "tbl_Tournaments", f"TournamentID = {TournamentID}")[5]:
        return True
    else:
        return False

def insertToWaitingList(connection, cursor: sql.Cursor, data: list):
    """Insert a team into the tbl_Teams table, with a status of 'Waiting'."""
    sql = f"INSERT INTO tbl_Teams(TeamName, TeamCaptainName, TeamMember2, TeamMember3, TeamCoach, Status, TournamentID) VALUES(?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

def updateTeamStatus(connection, cursor: sql.Cursor, data: list):
    """Update the status of a team."""
    sql = f"UPDATE tbl_Teams SET Status = ? WHERE TeamID = ?"
    cursor.execute(sql, data)
    connection.commit()

def getTeamCaptainfromTeamID(cursor: sql.Cursor, TeamID: int):
    """Get the team captain name from a team ID."""
    sql = f"SELECT TeamCaptainName FROM tbl_Teams WHERE TeamID = {TeamID}"
    cursor.execute(sql)
    return cursor.fetchone()

def getUserIDfromTeamCaptain(cursor: sql.Cursor, TeamCaptainName: str):
    """Get the UserID of a team captain."""
    sql = f"SELECT UserID FROM tbl_Participants WHERE ParticipantGameName = '{TeamCaptainName}'"
    cursor.execute(sql)
    return cursor.fetchone()

def getEmailfromUserID(cursor: sql.Cursor, UserID: int):
    """Get the email of a user from their UserID."""
    sql = f"SELECT ParticipantEmail FROM tbl_Participants WHERE UserID = {UserID}"
    cursor.execute(sql)
    return cursor.fetchone()

connection = sql.connect("dbase.db")
cursor = connection.cursor()