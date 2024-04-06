import sqlite3 as sql

# Create a function that makes a tbl_Accounts table
def createtbl_Accounts(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Accounts(
        UserID INTEGER PRIMARY KEY,
        Username VARCHAR(30) NOT NULL,
        Password VARCHAR(30) NOT NULL,
        Role VARCHAR(20) NOT NULL
        );'''
    cursor.execute(sql)

# Create a function that makes a tbl_Administrators table
def createtbl_Administrators(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Administrators(
        AdminID INTEGER PRIMARY KEY,
        AdminDiscName VARCHAR(30) NOT NULL,
        AdminFirstName VARCHAR(20) NOT NULL,
        AdminSurname VARCHAR(20) NOT NULL,
        AdminDOB VARCHAR(20) NOT NULL,
        AdminEmail VARCHAR(50) NOT NULL,
        UserID INTEGER NOT NULL,
        FOREIGN KEY (UserID) REFERENCES tbl_Accounts(UserID)
        );'''
    cursor.execute(sql)

# Create a function that makes a tbl_Participants table
def createtbl_Participants(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Participants(
        ParticipantID INTEGER PRIMARY KEY,
        ParticipantDOB DATE NOT NULL,
        ParticipantEmail VARCHAR(20) NOT NULL,
        UserID INTEGER NOT NULL,
        FOREIGN KEY (UserID) REFERENCES tbl_Accounts(UserID)
        );'''
    cursor.execute(sql)

# Create a function that makes a tbl_Teams table
def createtbl_Teams(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Teams(
        TeamID INTEGER PRIMARY KEY,
        TeamName VARCHAR(20) NOT NULL,
        TeamCaptainID INTEGER NOT NULL,
        TeamMember2Name VARCHAR(20) NOT NULL,
        TeamMember3Name VARCHAR(20) NOT NULL,
        TournamentID INTEGER NOT NULL,
        FOREIGN KEY (TeamCaptainID) REFERENCES tbl_Participants(ParticipantID),
        FOREIGN KEY (TournamentID) REFERENCES tbl_Tournaments(TournamentID)
        );'''
    cursor.execute(sql)

# Create a function that makes a tbl_Tournaments table
def createtbl_Tournaments(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Tournaments(
        TournamentID INTEGER PRIMARY KEY,
        TournamentName VARCHAR(20) NOT NULL,
        TournamentDate DATE NOT NULL,
        TournamentTime TIME NOT NULL,
        TournamentDescription VARCHAR(100) NOT NULL,
        MaxTeams INTEGER NOT NULL,
        NumGames INTEGER NOT NULL
        );'''
    cursor.execute(sql)

# Create a function that makes all the tables
def createTables(cursor: sql.Cursor):
    createtbl_Accounts(cursor)
    createtbl_Administrators(cursor)
    createtbl_Participants(cursor)
    createtbl_Teams(cursor)
    createtbl_Tournaments(cursor)

# Create a function that inserts data into the tbl_Accounts table
def insertToAccountsTable(connection, cursor: sql.Cursor, data: list):
    sql = f"INSERT INTO tbl_Accounts(Username, Password, Role) VALUES(?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

# Create a function that inserts data into the tbl_Administrators table
def insertToAdministratorsTable(connection, cursor: sql.Cursor, data: list):
    sql = f"INSERT INTO tbl_Administrators(AdminDiscName, AdminFirstName, AdminSurname, AdminDOB, AdminEmail, UserID) VALUES(?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

# Create a function that inserts data into the tbl_Participants table
def insertToParticipantsTable(connection, cursor: sql.Cursor, data: list):
    sql = f"INSERT INTO tbl_Participants(ParticipantDOB, ParticipantEmail, IsTeamLeader, UserID, TeamID) VALUES(?, ?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

# Create a function that inserts data into the tbl_Teams table
def insertToTeamsTable(connection, cursor: sql.Cursor, data: list):
    sql = f"INSERT INTO tbl_Teams(TeamName, TeamCaptainID, TeamMember2Name, TeamMember3Name, TournamentID) VALUES(?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

def insertToTournamentsTable(connection, cursor: sql.Cursor, data: list):
    sql = f"INSERT INTO tbl_Tournaments(TournamentName, TournamentDate, TournamentTime, TournamentDescription, MaxTeams, NumGames) VALUES(?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

# Create a function that gets all the rows from a table
def getAllRows(cursor: sql.Cursor, table: str):
    sql = f"SELECT * FROM {table}"
    cursor.execute(sql)
    return cursor.fetchall()

# Create a function that gets specific rows from a table based on a condition
def getSpecificRows(cursor: sql.Cursor, table, condition):
    sql = f"SELECT * FROM {table} WHERE {condition}"
    cursor.execute(sql)
    return cursor.fetchone()

# Create a function that gets the UserID of a user based on their username
def getUserID(cursor: sql.Cursor, username: str):
    sql = f"SELECT UserID FROM tbl_Accounts WHERE Username = '{username}'"
    cursor.execute(sql)
    return cursor.fetchone()

# Create a function that allows the deletion of a specific row from the tournaments table
def deleteTournament(connection, cursor: sql.Cursor, tournamentID: int):
    sql = f"DELETE FROM tbl_Tournaments WHERE TournamentID = {tournamentID}"
    cursor.execute(sql)
    connection.commit()

# Create a function for getting all the names of the tournaments
def getAllTournamentNames(cursor: sql.Cursor):
    sql = "SELECT TournamentName FROM tbl_Tournaments"
    cursor.execute(sql)
    return cursor.fetchall()

# Create a function for updating the details of a tournament
def updateTournamentDetails(connection, cursor: sql.Cursor, data: list):
    sql = f"UPDATE tbl_Tournaments SET TournamentName = ?, TournamentDate = ?, TournamentTime = ?, TournamentDescription = ?, MaxTeams = ?, NumGames = ? WHERE TournamentID = ?"
    cursor.execute(sql, data)
    connection.commit()

connection = sql.connect("database.db")
cursor = connection.cursor()