import smtplib, ssl
from email.message import EmailMessage
import random
import string
import db
import sqlite3 as sql
from tkinter import messagebox
import functions as fn

connection = sql.connect("dbase.db")
cursor = connection.cursor()

def checkEmail(receiver_email, RecoveryEmailEntry, controller, page):
    """Check if the email entered is associated with an account."""
    # Check if the email is in either the administrator or participant table
    allAdminRows = db.getAllRows(cursor, "tbl_Administrators")
    allParticipantRows = db.getAllRows(cursor, "tbl_Participants")

    global emailEntered
    emailEntered = receiver_email

    emailFound = False
    for row in allAdminRows:
        if receiver_email == row[5]:
            emailFound = True
    
    for row in allParticipantRows:
        if receiver_email == row[2]:
            emailFound = True
    
    if emailFound == False:
        messagebox.showerror("Error", "The email you entered is not associated with any account.")
        RecoveryEmailEntry.focus()
    else:
        sendEmail(receiver_email, RecoveryEmailEntry, controller, page)

def sendEmail(receiver_email, RecoveryEmailEntry, controller, page):

    """Send an email to the user with a recovery token."""
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "samstournaments@gmail.com"
    password = "dzui zaka oxqj juvm"
    global generate_auth_token
    generate_auth_token = "".join(random.choices(string.ascii_letters + string.digits, k=6))

    subject = "Sams Tournaments: Password Recovery"
    body = """
    Your password recovery token is: {0}
    """.format(generate_auth_token)

    em = EmailMessage()
    em["From"] = sender_email
    em["To"] = receiver_email
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, em.as_string())
            messagebox.showinfo("Success", "An email has been sent to you with a recovery token.")
            RecoveryEmailEntry.delete(0, "end")
            controller.show_frame(page)
    except:
        messagebox.showerror("Error", "Email could not be sent, ensure you have entered a valid email address.")
        RecoveryEmailEntry.focus()

def sendParticipatingEmail(TeamName, TournamentName, receiver_email):
    """Send an email telling the team captain their team is now participating."""
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "samstournaments@gmail.com"
    password = "dzui zaka oxqj juvm"

    subject = "Sams Tournaments: Team Participation"
    body = """
    Your team, {0}, is now participating in the tournament, {1}.
    """.format(TeamName, TournamentName)

    em = EmailMessage()
    em["From"] = sender_email
    em["To"] = receiver_email
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, em.as_string())
    except:
        messagebox.showerror("Error", "Email could not be sent, ensure you have entered a valid email address.")

def checkToken(token, RecoveryTokenEntry, controller, page):
    """Check if the token entered matches the generated token."""
    if token == generate_auth_token:
        messagebox.showinfo("Success", "Token is correct.")
        RecoveryTokenEntry.delete(0, "end")
        controller.show_frame(page)
    else:
        messagebox.showerror("Error", "Token is incorrect.")
        RecoveryTokenEntry.delete(0, "end")
        RecoveryTokenEntry.focus()

def ResetAdminPassword(NewPass, ConfirmPass, receiver_email, controller, LoginPage):
    if NewPass == ConfirmPass:
        UserID = db.getAdminUserIDfromEmail(cursor, receiver_email)
        db.updateUserPassword(connection, cursor, [NewPass, UserID[0]])
        messagebox.showinfo("Success", "Your password has been successfully reset.")
        fn.frameSwitchGeometry(controller, LoginPage, "1920x1080")
    else:
        messagebox.showerror("Error", "The passwords you entered do not match. Please try again.")

def ResetParticipantPassword(NewPass, ConfirmPass, receiver_email, controller, LoginPage):
    if NewPass == ConfirmPass:
        UserID = db.getUserIDfromEmail(cursor, receiver_email)
        db.updateUserPassword(connection, cursor, [NewPass, UserID[0]])
        messagebox.showinfo("Success", "Your password has been successfully reset.")
        fn.frameSwitchGeometry(controller, LoginPage, "1920x1080")
    else:
        messagebox.showerror("Error", "The passwords you entered do not match. Please try again.")

def isPartOrAdmin(NewPass, ConfirmPass, controller, LoginPage):
    global emailEntered
    allAdminRows = db.getAllRows(cursor, "tbl_Administrators")
    allParticipantRows = db.getAllRows(cursor, "tbl_Participants")

    for row in allAdminRows:
        if emailEntered == row[5]:
            ResetAdminPassword(NewPass, ConfirmPass, emailEntered, controller, LoginPage)
    
    for row in allParticipantRows:
        if emailEntered == row[2]:
            ResetParticipantPassword(NewPass, ConfirmPass, emailEntered, controller, LoginPage)