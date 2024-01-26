import sqlite3 as sql

# Create a function that makes a tbl_Accounts table
def createtbl_Accounts(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Accounts(
        UserID INTEGER PRIMARY KEY,
        Username VARCHAR(30),
        Password VARCHAR(30),
        Role VARCHAR(20)
        );'''
    cursor.execute(sql)

# Create a function that makes a tbl_Administrators table
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

# Create a function that makes a tbl_Participants table
def createtbl_Participants(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Participants(
        ParticipantID INTEGER PRIMARY KEY,
        ParticipantDOB DATE,
        ParticipantEmail VARCHAR(20),
        IsTeamLeader BOOLEAN,
        UserID INTEGER,
        FOREIGN KEY (UserID) REFERENCES tbl_Accounts(UserID)
        );'''
    cursor.execute(sql)

# Create a function that makes a tbl_Teams table
def createtbl_Teams(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Teams(
        TeamID INTEGER PRIMARY KEY,
        TeamName VARCHAR(20),
        TeamCaptain VARCHAR(20),
        TeamMember2 VARCHAR(20),
        TeamMember3 VARCHAR(20),
        TeamCoach VARCHAR(20),
        TournamentID INTEGER
        );'''
    cursor.execute(sql)

# Create a function that makes a tbl_Tournaments table
def createtbl_Tournaments(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Tournaments(
        TournamentID INTEGER PRIMARY KEY,
        TournamentName VARCHAR(20),
        TournamentDate DATE,
        TournamentTime TIME,
        TournamentDescription VARCHAR(100)
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
    print(data)
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
    sql = f"INSERT INTO tbl_Teams(TeamName, TeamCaptain, TeamMember2, TeamMember3, TeamCoach, TournamentID) VALUES(?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

def insertToTournamentsTable(connection, cursor: sql.Cursor, data: list):
    sql = f"INSERT INTO tbl_Tournaments(TournamentName, TournamentDate, TournamentTime, TournamentDescription) VALUES(?, ?, ?, ?)"
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

# Create a function that gets the UserID from the tbl_Accounts table
def getUserID(cursor: sql.Cursor, username: str):
    sql = f"SELECT UserID FROM tbl_Accounts WHERE Username = '{username}'"
    cursor.execute(sql)
    return cursor.fetchone()

connection = sql.connect("database.db")
cursor = connection.cursor()