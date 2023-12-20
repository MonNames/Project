CREATE TABLE tblParticipant (
    ParticipantID INT PRIMARY KEY,
    PartUsername VARCHAR(20),
    PartDOB DATE,
    PartSex VARCHAR(6),
    PartEmail VARCHAR(30),
    PartRegion VARCHAR(20),
    IsTeamCaptain BOOLEAN
);

CREATE TABLE tblAdministrators (
    AdministratorID INT PRIMARY KEY,
    AdminDiscName VARCHAR(30),
    AdminFirstName VARCHAR(20),
    AdminSurname VARCHAR(30),
    AdminDOB DATE,
    AdminSex VARCHAR(6),
    AdminEmail VARCHAR(30)
);

CREATE TABLE tblTournaments (
    TournamentID INT PRIMARY KEY,
    AdminID INT FOREIGN KEY (AdminID) REFERENCES tblAdministrators(AdministratorID)
    MaxTeams INT,
    TournFormat VARCHAR(100),
    TournName VARCHAR(100),
);

CREATE TABLE tblLinkGroup (
    GroupID INT PRIMARY KEY,
    TeamID INT FOREIGN KEY (TeamID) REFERENCES tblTeams(TeamID),
    ParticipantID INT FOREIGN KEY (ParticipantID) REFERENCES tblParticipant(ParticipantID)
);

CREATE TABLE tblTeams(
    TeamID INT PRIMARY KEY,
    TeamCaptainID INT FOREIGN KEY (TeamCaptainID) REFERENCES tblParticipant(ParticipantID),
    UserID INT FOREIGN KEY (UserID) REFERENCES tblParticipant(ParticipantID)
    TeamName VARCHAR(20),
);