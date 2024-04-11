import smtplib, ssl
from email.message import EmailMessage
import random
import string
import db
import sqlite3 as sql
from tkinter import messagebox

connection = sql.connect("database.db")
cursor = connection.cursor()

def checkEmail(receiver_email, RecoveryEmailEntry):
    """Check if the email entered is associated with an account."""
    # Check if the email is in either the administrator or participant table
    allAdminRows = db.getAllRows(cursor, "tbl_Administrators")
    allParticipantRows = db.getAllRows(cursor, "tbl_Participants")

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
        sendEmail(receiver_email, RecoveryEmailEntry)

def sendEmail(receiver_email, RecoveryEmailEntry):
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
    except:
        messagebox.showerror("Error", "Email could not be sent, ensure you have entered a valid email address.")
        RecoveryEmailEntry.focus()
