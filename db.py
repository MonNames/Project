import sqlite3 as sql

# Create a function that makes a tbl_Accounts table
def createtbl_Accounts(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Accounts(
        UserID INTEGER PRIMARY KEY,
        Username VARCHAR(20) NOT NULL,
        Password VARCHAR(20) NOT NULL
        );'''
    cursor.execute(sql)

# Create a function that makes a tbl_Administrators table
def createtbl_Administrators(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Administrators(
        AdminID INTEGER PRIMARY KEY,
        AdminDiscName VARCHAR(20) NOT NULL,
        AdminFirstName VARCHAR(20) NOT NULL,
        AdminSurname VARCHAR(20) NOT NULL,
        AdminDOB DATE NOT NULL,
        AdminEmail VARCHAR(20) NOT NULL,
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
        IsTeamLeader BOOLEAN NOT NULL,
        UserID INTEGER NOT NULL,
        TeamID INTEGER NOT NULL,
        FOREIGN KEY (UserID) REFERENCES tbl_Accounts(UserID),
        FOREIGN KEY (TeamID) REFERENCES tbl_Teams(TeamID)
        );'''
    cursor.execute(sql)

# Create a function that makes a tbl_Teams table
def createtbl_Teams(cursor: sql.Cursor):
    sql = '''CREATE TABLE IF NOT EXISTS tbl_Teams(
        TeamID INTEGER PRIMARY KEY,
        TeamName VARCHAR(20) NOT NULL,
        TeamCaptainID INTEGER NOT NULL,
        TeamMemberID INTEGER NOT NULL,
        TournamentID INTEGER NOT NULL,
        FOREIGN KEY (TeamCaptainID) REFERENCES tbl_Participants(ParticipantID),
        FOREIGN KEY (TeamMemberID) REFERENCES tbl_Participants(ParticipantID),
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
        TournamentDescription VARCHAR(100) NOT NULL
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
    sql = f"INSERT INTO tbl_Accounts(UserID, Username, Password) VALUES(?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

# Create a function that inserts data into the tbl_Administrators table
def insertToAdministratorsTable(connection, cursor: sql.Cursor, data: list):
    sql = f"INSERT INTO tbl_Administrators( AdminDiscName, AdminFirstName, AdminSurname, AdminDOB, AdminEmail) VALUES(?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

# Create a function that inserts data into the tbl_Participants table
def insertToParticipantsTable(connection, cursor: sql.Cursor, data: list):
    sql = f"INSERT INTO tbl_Participants(ParticipantDOB, ParticipantEmail, IsTeamLeader, UserID, TeamID) VALUES(?, ?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

# Create a function that inserts data into the tbl_Teams table
def insertToTeamsTable(connection, cursor: sql.Cursor, data: list):
    sql = f"INSERT INTO tbl_Teams(TeamName, TeamCaptainID, TeamMemberID, TournamentID) VALUES(?, ?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

def insertToTournamentsTable(connection, cursor: sql.Cursor, data: list):
    sql = f"INSERT INTO tbl_Tournaments(TournamentName, TournamentDate, TournamentTime, TournamentDescription) VALUES(?, ?, ?, ?)"
    cursor.execute(sql, data)
    connection.commit()

conn = sql.connect("database.db")