import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from PIL import ImageTk, Image
import db, validate as vd, email_recovery as email, functions as fn, sqlite3 as sql
from tkcalendar import DateEntry
from time import strftime, sleep
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
MAIN_FONT = ("Arial", 12)
MAIN_FONT_BOLD = ("Arial bold", 12)
MEDIUM_FONT = ("Arial", 15)
MEDIUM_FONT_BOLD = ("Arial bold", 15)
LARGE_FONT = ("Arial", 18)
LARGE_FONT_BOLD = ("Arial bold", 18)
VERY_LARGE_FONT = ("Arial bold", 25)
UNDERLINED_FONT = ("Arial underline", 8)

# Create the database and tables and connect to the database
connection = sql.connect("dbase.db")
cursor = connection.cursor()
db.createTables(cursor)
db.createConstUser(connection, cursor)
db.createConstAdmin(connection, cursor)

global isAdmin
isAdmin = False

global loggedinAs
loggedinAs = "EXAMPLEUSER"

class SamsTournamentsApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Sam's Tournaments")

        tk.Tk.geometry(self, "1920x1080")
        tk.Tk.minsize(self, 300, 175)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1) 
        container.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Toolbutton", background="#E3E2DF", font=LARGE_FONT_BOLD)
        style.configure("Treeview", background = "#E3E2DF", foreground = "black", rowheight = 25, fieldbackground = "#E3E2DF")

        style.map("Treeview", background=[('selected', 'green')])

        self.frames = {}

        # Create instances of LoginPage and SignupPage
        for i in (LoginPage, SignupPage, ForgotPasswordPage, DashboardPage, ScoringCalculatorPage, 
                  FAQandRulesPage, CreateAnAdminPage, CreateATournamentPage, RegisterToTournamentPage, 
                  UnregisterFromTournamentPage, UpcomingTournamentsDetailsPage, EditTournamentsPage,
                  RecoveryTokenPage, ResetPasswordPage, PreviousTournamentsPage, AdvancedDetailsPage,
                  PartSettingsPage, AdminSettingsPage, ShowTournamentTeamsPage, LeaderboardPage):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the LoginPage by default
        self.show_frame(LoginPage)

    def show_frame(self, cont):
        # Raise the specified frame to the top
        frame = self.frames[cont]
        frame.tkraise()

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):

        def ContinueAsGuestButton():
            """Change to the dashboard page and display the buttons that are available to participants."""
            global loggedinAs
            loggedinAs = "EXAMPLEUSER"
            controller.show_frame(DashboardPage)

        def userOrAdmin(Username):
            """Check if the user is an admin or a participant."""
            global isAdmin
            allRows = db.getAllRows(cursor, "tbl_Accounts")
            for row in allRows:
                if Username == row[1]:
                    if row[3] == "Admin":
                        isAdmin = True
                    else:
                        isAdmin = False
            
            # We want to change to the dashboard page and then run the displayAdminButtons function in the DashboardPage class
            controller.show_frame(DashboardPage)

        def Login(Username, Password):
            # Checking if the user has entered a valid length username and password
            if vd.presenceCheck(Username) == "Invalid":
                messagebox.showerror("Error", "Please enter a username.")
                UsernameEntry.focus()
            elif vd.presenceCheck(Password) == "Invalid":
                messagebox.showerror("Error", "Please enter a password.")
                UsernameEntry.focus()
            else:
                # Check if the username and password entered are valid
                allRows = db.getAllRows(cursor, "tbl_Accounts")
                validUsername = False
                validPassword = False
                for row in allRows:
                    if Username == row[1]:
                        validUsername = True
                        if Password == row[2]:
                            validPassword = True
                
                if validUsername == False:
                    messagebox.showerror("Error", "The username you entered is invalid.")
                    UsernameEntry.focus()
                elif validPassword == False:
                    messagebox.showerror("Error", "The password you entered is invalid.")
                    PasswordEntry.focus()
                else:
                    messagebox.showinfo("Login", "You have logged in successfully.")
                    global loggedinAs
                    loggedinAs = Username
                    userOrAdmin(Username)

            if IsChecked.get() == 1:
                with open("Text Files/RememberMe.txt", "w") as file:
                    file.write(Username + " " + Password)
            else:
                with open("Text Files/RememberMe.txt", "w") as file:
                    file.write("")

        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg="#E3E2DF")

        # Create StringVars for User Entry
        Username = tk.StringVar()
        Password = tk.StringVar()
        IsChecked = tk.IntVar()

        Username.set("ConstUser")
        Password.set("Password1")

        # Check if there are any details in the Remember Me File, if not set the variables equal to them
        with open("Text Files/RememberMe.txt", "r") as file:
            for line in file:
                if line != "":
                    Username.set(line.split()[0])
                    Password.set(line.split()[1])

        # Create a frame 
        WholeFrame = tk.Frame(self, bg="#5D011E")
        WholeFrame.pack(fill="both", expand=True)

        # Create a frame for the left side of the window and right side of the window
        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        LeftFrame.pack(side="left", fill="both", expand=True)
        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)

        # Start creating fields for entry of information
        MainLabel = tk.Label(LeftFrame, text="Sam's Tournaments", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabel.pack(pady=20)

        SpaceLabel = tk.Label(LeftFrame, text="", bg = "#E3E2DF", font=MAIN_FONT)
        SpaceLabel.pack(pady=60)

        UsernameLabel = tk.Label(LeftFrame, text="Username", bg = "#E3E2DF", font=LARGE_FONT)
        UsernameLabel.pack(padx=10)
        UsernameEntry = tk.Entry(LeftFrame, width=40, textvariable = Username)
        UsernameEntry.pack(padx=10, pady=10)


        PasswordLabel = tk.Label(LeftFrame, text="Password", bg = "#E3E2DF", font=LARGE_FONT)
        PasswordLabel.pack(padx=10, pady=10)
        PasswordEntry = tk.Entry(LeftFrame, width=40, textvariable = Password, show="*")   
        PasswordEntry.pack(padx=10, pady=10)

        ShowPassword = tk.Checkbutton(LeftFrame, text="Show Password", bg = "#E3E2DF", command=lambda: fn.show_and_hide(PasswordEntry, "None"))
        ShowPassword.pack()

        RememberMeButton = tk.Checkbutton(LeftFrame, text="Remember Me", bg = "#E3E2DF", variable = IsChecked)
        RememberMeButton.pack()

        LoginButton = tk.Button(LeftFrame, text="Log In", bg = "#5D011E",  fg = "white", width=20, height=2,
                                command=lambda: Login(Username.get(), Password.get()))
        LoginButton.pack(pady=20)

        # Start adding buttons to the right side 
        SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
        SpaceLabel.pack(pady=20)
        ParticipantViewButton = tk.Button(RightFrame, text="Continue as Guest", bg = "#E3E2DF", width=45, height=4, font = MAIN_FONT,
                                          command = lambda: ContinueAsGuestButton())
        ParticipantViewButton.pack(pady=35)
        ForgotMyPasswordButton = tk.Button(RightFrame, text="Forgot my password", bg = "#9A1750", fg = "white", width=45, height=4, font = MAIN_FONT,
                                           command=lambda: fn.frameSwitchGeometry(controller, ForgotPasswordPage, "375x200"))
        ForgotMyPasswordButton.pack(pady=35)
        GoToSignUpButton = tk.Button(RightFrame, text="Sign Up", bg = "#E3AFBC", font = MAIN_FONT, width=45, height=4,
                                     command=lambda: controller.show_frame(SignupPage))
        GoToSignUpButton.pack(pady=35)

class SignupPage(tk.Frame):

    def __init__(self, parent, controller):

        def DetailsValidation():
            """Check if the details entered are valid."""

            def SignupConfirmation():
                """Insert the details into the database."""
                db.insertToAccountsTable(connection, cursor, [Username.get(), Password.get(), "User"])
                UserIDForeignKey = db.getUserID(cursor, Username.get())
                db.insertToParticipantsTable(connection, cursor, [GameName.get(), Email.get(), GenderVar.get(), UserIDForeignKey[0]])
                messagebox.showinfo("Signup", "You have signed up successfully!")
                EmailEntry.delete(0, "end")
                UsernameEntry.delete(0, "end")
                GameNameEntry.delete(0, "end")
                GenderVar.set("Please Select")
                PasswordEntry.delete(0, "end")
                PasswordConfirmEntry.delete(0, "end")
            
            validEmail = False
            if vd.emailCheck(Email.get()) == "Valid":
                validEmail = True
            elif vd.emailCheck(Email.get()) == "Taken":
                messagebox.showerror("Error", "The email you entered is already associated with an account.")
                EmailEntry.focus()
            elif vd.emailCheck(Email.get()) == "Formatting Error":
                messagebox.showerror("Error", "The email you entered has an invalid format.")
                EmailEntry.focus()
            
            validUsername = False
            if vd.usernameIsValid(Username.get()) == "Valid":
                validUsername = True
            elif vd.usernameIsValid(Username.get()) == "Taken":
                messagebox.showerror("Error", "The username you entered is already taken.")
                UsernameEntry.focus()
            else:
                messagebox.showerror("Error", "The username you entered is invalid.")
                UsernameEntry.focus()
            
            validPassword = False
            if vd.passwordIsValid(Password.get(), PasswordConfirm.get()) == "Valid":
                validPassword = True
            elif vd.passwordIsValid(Password.get(), PasswordConfirm.get()) == "MatchError":
                messagebox.showerror("Error", "The passwords you entered do not match.")
                PasswordConfirmEntry.focus()
            else:
                messagebox.showerror("Error", "The password you entered is invalid.")
                PasswordEntry.focus()
            
            IsOver16Checked = False
            if IsOver16.get() == 1:
                IsOver16Checked = True
            else:
                messagebox.showerror("Error", "You must be over the age of 16 to sign up.")
            
            if validEmail == True and validUsername == True and validPassword == True and IsOver16Checked == True:
                SignupConfirmation()

        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        # Create StringVars for User Entry
        Email = tk.StringVar()
        Username = tk.StringVar()
        GameName = tk.StringVar()
        Password = tk.StringVar()
        PasswordConfirm = tk.StringVar()

        # Create a frame
        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        # Create a frame for the left side of the window and right side of the window
        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        LeftFrame.pack(side="left", fill="both", expand=True)
        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)

        # Start creating fields for entry of information
        MainLabel = tk.Label(LeftFrame, text="Sam's Tournaments", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabel.pack(pady=20)

        EmailLabel = tk.Label(LeftFrame, text = "Email", bg="#E3E2DF", font=LARGE_FONT)
        EmailLabel.pack(padx=10)
        EmailEntry = tk.Entry(LeftFrame, width=40, textvariable = Email)
        EmailEntry.pack(padx=10, pady=20)

        UsernameLabel = tk.Label(LeftFrame, text="Username", bg = "#E3E2DF", font=LARGE_FONT)
        UsernameLabel.pack(padx=10)
        UsernameEntry = tk.Entry(LeftFrame, width=40, textvariable = Username)
        UsernameEntry.pack(padx=10, pady=20)

        GameNameLabel = tk.Label(LeftFrame, text="Game Name", bg = "#E3E2DF", font=LARGE_FONT)
        GameNameLabel.pack(padx=10)
        GameNameEntry = tk.Entry(LeftFrame, width=40, textvariable = GameName)
        GameNameEntry.pack(padx=10, pady=20)

        # Create values to be used in the drop down menu
        Gender = ["Male", "Female"]
        GenderVar = tk.StringVar()
        GenderVar.set("Please Select")

        GenderLabel = tk.Label(LeftFrame, text="Gender", bg = "#E3E2DF", font=LARGE_FONT)
        GenderLabel.pack(padx=10)
        GenderEntry = tk.OptionMenu(LeftFrame, GenderVar, *Gender)
        GenderEntry.pack(padx=10, pady=20)
        GenderEntry.config(width=20, height=1, font = MAIN_FONT)

        PasswordLabel = tk.Label(LeftFrame, text="Password", bg = "#E3E2DF", font=LARGE_FONT)
        PasswordLabel.pack(padx=10)
        PasswordEntry = tk.Entry(LeftFrame, width=40, textvariable = Password, show = "*")
        PasswordEntry.pack(padx=10, pady=20)

        PasswordConfirmLabel = tk.Label(LeftFrame, text="Confirm Password", bg = "#E3E2DF", font=LARGE_FONT)
        PasswordConfirmLabel.pack(padx=10)
        PasswordConfirmEntry = tk.Entry(LeftFrame, width=40, textvariable = PasswordConfirm, show = "*")
        PasswordConfirmEntry.pack(padx=10, pady=20)

        # Lets add two checkboxes, one to show password and another to confirm the user is over the age of 16
        ShowPassword = tk.Checkbutton(LeftFrame, text="Show Password", bg = "#E3E2DF", command=lambda: fn.show_and_hide(PasswordEntry, PasswordConfirmEntry))
        ShowPassword.pack()

        IsOver16 = tk.IntVar()

        AgeConfirmation = tk.Checkbutton(LeftFrame, text="I confirm I am over the age of 16", background="#E3E2DF", variable = IsOver16)
        AgeConfirmation.pack(pady=5)

        # Button to create the account
        SignUpButton = tk.Button(LeftFrame, text="Sign Up", bg = "#5D011E",  fg = "white", width=15, height=2,
                    command=lambda: DetailsValidation())
        SignUpButton.pack(pady=10)

        # Start adding buttons to the right side
        SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
        SpaceLabel.pack(pady=20)

        ContinueAsGuestButton = tk.Button(RightFrame, text="Continue as Guest", bg = "#E3E2DF", width=45, height=4, font = MAIN_FONT,
                                          command = lambda: controller.show_frame(DashboardPage))
        ContinueAsGuestButton.pack(pady=20)
        GoToLoginButton = tk.Button(RightFrame, text="Login", bg="#E3AFBC", font = MAIN_FONT, width=45, height=4, command=lambda: controller.show_frame(LoginPage))
        GoToLoginButton.pack(pady=20)

        # Right Side Labels
        ValidUserLabel = tk.Label(RightFrame, text="A Valid username must contain:\n- At least 6 characters\n- No symbols or spaces", fg = "white", bg="#5D011E", font=LARGE_FONT)
        ValidUserLabel.pack(pady=20)
        ValidPassLabel = tk.Label(RightFrame, text="A Valid password must contain:\n- At least 8 characters\n- At least one capital letter\n- At least one number", fg="white", bg="#5D011E", font=LARGE_FONT)
        ValidPassLabel.pack(pady=20)

class ForgotPasswordPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        RecoveryEmail = tk.StringVar()

        Label1 = tk.Label(self, text="Please enter the email of the \n account you are trying to recover", bg="#E3E2DF", font=MAIN_FONT)
        Label1.pack(pady=5)
        RecoveryEmailEntry = tk.Entry(self, width=40, textvariable=RecoveryEmail)
        RecoveryEmailEntry.pack(pady=5)

        SendRecoveryEmailButton = tk.Button(self, text="Send", bg="#E3E2DF", width=8, height=1, command = lambda: email.checkEmail(RecoveryEmail.get(), RecoveryEmailEntry, controller, RecoveryTokenPage))
        SendRecoveryEmailButton.pack(pady=5)

        BackButton = tk.Button(self, text="Back", bg="#E3E2DF", width=8, height=1, command=lambda: fn.frameSwitchGeometry(controller, LoginPage, "1920x1080"))
        BackButton.pack(pady=5)

class RecoveryTokenPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        inputAuthToken = tk.StringVar()
        EnterAuthCodeLabel = tk.Label(WholeFrame, text="Please enter the 6 digit code sent to your email", bg="#E3E2DF", font=MAIN_FONT)
        EnterAuthCodeLabel.pack(pady=5)
        AuthCodeEntry = tk.Entry(WholeFrame, width=40, textvariable=inputAuthToken)
        AuthCodeEntry.pack(pady=5)

        ConfirmButton = tk.Button(WholeFrame, text="Confirm", bg="#E3E2DF", width=8, height=1, command=lambda: email.checkToken(inputAuthToken.get(), AuthCodeEntry, controller, ResetPasswordPage))
        ConfirmButton.pack(pady=5)

        BackButton = tk.Button(WholeFrame, text="Back", bg="#E3E2DF", width=8, height=1, command=lambda: controller.show_frame(ForgotPasswordPage))
        BackButton.pack(pady=5)

class ResetPasswordPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        NewPass = tk.StringVar()
        ConfirmPass = tk.StringVar()

        NewPassEntryLabel = tk.Label(WholeFrame, text="Enter your new password", bg="#E3E2DF", font=MAIN_FONT)
        NewPassEntryLabel.pack(pady=5)
        NewPassEntry = tk.Entry(WholeFrame, width=40, textvariable=NewPass, show="*")
        NewPassEntry.pack(pady=5)

        ConfirmPassEntryLabel = tk.Label(WholeFrame, text="Confirm your new password", bg="#E3E2DF", font=MAIN_FONT)
        ConfirmPassEntryLabel.pack(pady=5)
        ConfirmPassEntry = tk.Entry(WholeFrame, width=40, textvariable=ConfirmPass, show="*")
        ConfirmPassEntry.pack(pady=5)

        ResetButton = tk.Button(WholeFrame, text="Reset", bg="#E3E2DF", width=8, height=1, command=lambda: email.isPartOrAdmin(NewPassEntry.get(), ConfirmPassEntry.get(), controller, LoginPage))
        ResetButton.pack(pady=5)

class DashboardPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        def choosePage():
            if isAdmin == True:
                fn.frameSwitchGeometry(controller, AdminSettingsPage, "600x500")
            else:
                fn.frameSwitchGeometry(controller, PartSettingsPage, "600x500")

        def RefreshLoggedInAs():
            displayLoggedInAs.config(text="Logged in as: {0}".format(loggedinAs))
            displayLoggedInAs.after(500, RefreshLoggedInAs)

        def GoToCreateTournamentPage():
            if isAdmin == True:
                messagebox.showinfo("Welcome", "Welcome!")
                controller.show_frame(CreateATournamentPage)
            else:
                messagebox.showerror("Error", "You do not have the required permissions to access this page.")

        def GoToCreateAdminPage():
            if isAdmin == True:
                controller.show_frame(CreateAnAdminPage)
            else:
                messagebox.showerror("Error", "You do not have the required permissions to access this page.")

        def GoToRegisterToTournamentPage():
            if loggedinAs != "EXAMPLEUSER":
                controller.show_frame(RegisterToTournamentPage)
            else:
                messagebox.showerror("Error", "You must be logged in to access this page.")

        def GoToUnregisterFromTournamentPage():
            if loggedinAs != "EXAMPLEUSER":
                controller.show_frame(UnregisterFromTournamentPage)
            else:
                messagebox.showerror("Error", "You must be logged in to access this page.")

        def time():
            string = strftime('%H:%M:%S %p')
            ClockLabel.config(text = "TIME: " + string)
            ClockLabel.after(1000, time)
    
        # Create a frame
        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        # Create a frame for the left side of the window and right side of the window
        LeftFrame = tk.Frame(WholeFrame, bg="#5D011E")
        LeftFrame.pack(side="left", fill="both", expand=True)
        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)
        MiddleFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        MiddleFrame.pack(side="right", fill="both", expand=True)

        # Start adding buttons to the left side
        ScoringCalculatorButton = tk.Button(LeftFrame, text="Scoring Calculator", bg="#E3E2DF", width=45, height=4, font = MAIN_FONT, 
                                            command=lambda: controller.show_frame(ScoringCalculatorPage))
        ScoringCalculatorButton.pack(pady=35)

        RegisterToTournamentButton = tk.Button(LeftFrame, text="Register to a Tournament", bg="#E3AFBC", width=45, height=4, font = MAIN_FONT,
                                            command = lambda: GoToRegisterToTournamentPage())
        RegisterToTournamentButton.pack(pady=35)

        FAQandRulesButton = tk.Button(LeftFrame, text="FAQ & Rules", bg="#9A1750", fg = "white", width=45, height=4, font = MAIN_FONT,
                                      command = lambda: controller.show_frame(FAQandRulesPage))
        FAQandRulesButton.pack(pady=35)

        CreateATournamentButton = tk.Button(LeftFrame, text="Tournament Editor (ADMIN ONLY)", bg="#5D011E", fg = "white", width=45, height=4, font = MAIN_FONT,
                                            command = lambda: GoToCreateTournamentPage())
        CreateATournamentButton.pack(pady=35)

        # Add a clock label to the very bottom of the window on the left
        ClockLabel = tk.Label(LeftFrame, font=MAIN_FONT_BOLD, bg="#5D011E", fg="white")
        ClockLabel.pack(side="bottom", pady=20)
        time()

        # Start adding buttons to the right side
        UpcomingTournamentsButton = tk.Button(RightFrame, text="Upcoming Tournaments", bg="#E3E2DF", width=45, height=4, font = MAIN_FONT,
                                              command=lambda: controller.show_frame(UpcomingTournamentsDetailsPage))
        UpcomingTournamentsButton.pack(pady=35)

        UnregisterFromTournamentButton = tk.Button(RightFrame, text="Unregister From Tournaments", bg="#E3AFBC", width=45, height=4, font = MAIN_FONT,
                                        command = lambda: GoToUnregisterFromTournamentPage())
        UnregisterFromTournamentButton.pack(pady=35)

        PreviousTournamentsButton = tk.Button(RightFrame, text="Previous Tournaments", bg="#9A1750", fg = "white", width=45, height=4, font = MAIN_FONT,
                                              command = lambda: controller.show_frame(PreviousTournamentsPage))
        PreviousTournamentsButton.pack(pady=35)

        CreateAnAdminButton = tk.Button(RightFrame, text="Create an Admin (ADMIN ONLY)", bg="#5D011E", fg = "white", width=45, height=4, font = MAIN_FONT,
                                        command = lambda: GoToCreateAdminPage())
        CreateAnAdminButton.pack(pady=35)

        # Add a system version label to the very bottom of the window on the right
        SystemVersionLabel = tk.Label(RightFrame, text="SYSTEM VERSION: 1.3", font=MAIN_FONT_BOLD, bg="#5D011E", fg="white")
        SystemVersionLabel.pack(side="bottom", pady=20)

        # Add a label to the middle frame
        MainLabelTop = tk.Label(MiddleFrame, text="Sam's", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabelTop.pack(pady=60)

        logo = ImageTk.PhotoImage(Image.open("Images and Icons/Main_Logo.png"))
        LogoLabel = tk.Label(MiddleFrame, image=logo, bg="#E3E2DF")
        LogoLabel.image = logo
        LogoLabel.pack()

        MainLabelBottom = tk.Label(MiddleFrame, text="Tournaments", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabelBottom.pack(pady=50)
        
        settingsicon = tk.PhotoImage(file="Images and Icons/Settings_Icon.png")
        settingsicon.image = settingsicon
        SettingsButton = ttk.Button(MiddleFrame, image=settingsicon, style="Toolbutton", takefocus=False,
                       command=lambda: choosePage())
        SettingsButton.image = settingsicon
        SettingsButton.place(relx=0.75, rely=0.97, anchor="center")

        leaveicon = tk.PhotoImage(file="Images and Icons/Leave_Icon.png")
        leaveicon.image = leaveicon
        BackButton = ttk.Button(MiddleFrame, text="Logout", image=leaveicon, compound="left", style="Toolbutton", takefocus=False,
                               command=lambda: controller.show_frame(LoginPage))
        BackButton.image = leaveicon
        BackButton.pack(pady=20)

        # Add a logged in as label to the very bottom of the window in the middle, this will show the username of the person logged in, should be updated when the user logs in
        displayLoggedInAs = tk.Label(MiddleFrame, text="Logged in as: {0}".format(loggedinAs), font=MAIN_FONT_BOLD, bg="#E3E2DF")
        displayLoggedInAs.pack(side="bottom", pady=20)

        RefreshLoggedInAs()

class PartSettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        def changeEmail(DisplayEmailEntry, loggedinAs, email):
            """Change the email of the user in the database."""
            UserID = db.getUserID(cursor, loggedinAs)
            UserID = UserID[0]
            if vd.emailCheck(email) == "Valid":
                db.updateEmail(connection, cursor, [email, UserID])
                messagebox.showinfo("Email Change", "Your email has been changed successfully.")
                DisplayEmailEntry.delete(0, "end")
                DisplayEmailEntry.config(state="disabled")
            else:
                messagebox.showerror("Error", "The email you entered is invalid.")
                DisplayEmailEntry.focus()

        def changeGameName(DisplayGameNameEntry, loggedinAs, gameName):
            """Change the game name of the user in the database."""
            UserID = db.getUserID(cursor, loggedinAs)
            UserID = UserID[0]
            if vd.lengthCheck(gameName, 20, 1) == "Valid":
                db.updateGameName(connection, cursor, [gameName, UserID])
                messagebox.showinfo("Game Name Change", "Your game name has been changed successfully.")
                DisplayGameNameEntry.delete(0, "end")
                DisplayGameNameEntry.config(state="disabled")
            else:
                messagebox.showerror("Error", "The game name you entered is invalid.")
                DisplayGameNameEntry.focus()

        def changeUsername(DisplayUsernameEntry, username):
            """Change the username of the user in the database."""
            global loggedinAs
            UserID = db.getUserID(cursor, loggedinAs)
            UserID = UserID[0]
            if vd.usernameIsValid(username) == "Valid":
                db.updateUsername(connection, cursor, [username, UserID])
                loggedinAs = username
                messagebox.showinfo("Username Change", "Your username has been changed successfully.")
                DisplayUsernameEntry.delete(0, "end")
                DisplayUsernameEntry.config(state="disabled")
            else:
                messagebox.showerror("Error", "The username you entered is invalid.")
                DisplayUsernameEntry.focus()

        def changePassword(DisplayPasswordEntry, loggedinAs, password):
            """Change the password of the user in the database."""
            UserID = db.getUserID(cursor, loggedinAs)
            UserID = UserID[0]
            if vd.passwordIsValid(password, password) == "Valid":
                db.updatePassword(connection, cursor, [password, UserID])
                messagebox.showinfo("Password Change", "Your password has been changed successfully.")
                DisplayPasswordEntry.delete(0, "end")
                DisplayPasswordEntry.config(state="disabled")
            else:
                messagebox.showerror("Error", "The password you entered is invalid.")
                DisplayPasswordEntry.focus()

        def searchUser():
            """Search for user in the database and find their details"""
            global loggedinAs
            UserID = db.getUserID(cursor, loggedinAs)
            UserID = UserID[0]

            allRowsPart = db.getAllRows(cursor, "tbl_Participants")
            for row in allRowsPart:
                if row[4] == UserID:
                    DisplayGameName.set(row[1])
                    DisplayEmail.set(row[2])

            allRowsMain = db.getAllRows(cursor, "tbl_Accounts")
            for row in allRowsMain:
                if row[1] == loggedinAs:
                    DisplayUsername.set(row[1])
                    DisplayPassword.set(row[2])

            DisplayEmailEntry.config(state="normal")
            DisplayGameNameEntry.config(state="normal")
            DisplayUsernameEntry.config(state="normal")
            DisplayPasswordEntry.config(state="normal")

        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        DisplayUsername = tk.StringVar()
        DisplayGameName = tk.StringVar()
        DisplayEmail = tk.StringVar()
        DisplayPassword = tk.StringVar()

        DisplayGameNameLabel = tk.Label(WholeFrame, text="Display Game Name", bg="#E3E2DF", font=MAIN_FONT)
        DisplayGameNameLabel.place(relx=0.5, rely=0.05, anchor="center")
        DisplayGameNameEntry = tk.Entry(WholeFrame, width=40, textvariable=DisplayGameName, state="disabled")
        DisplayGameNameEntry.place(relx=0.5, rely=0.095, anchor="center") 

        DisplayUsernameLabel = tk.Label(WholeFrame, text="Display Username", bg="#E3E2DF", font=MAIN_FONT)
        DisplayUsernameLabel.place(relx=0.5, rely=0.17, anchor="center")
        DisplayUsernameEntry = tk.Entry(WholeFrame, width=40, textvariable=DisplayUsername, state="disabled")
        DisplayUsernameEntry.place(relx=0.5, rely=0.22, anchor="center")

        DisplayEmailLabel = tk.Label(WholeFrame, text="Display Email", bg="#E3E2DF", font=MAIN_FONT)
        DisplayEmailLabel.place(relx=0.5, rely=0.295, anchor="center")
        DisplayEmailEntry = tk.Entry(WholeFrame, width=40, textvariable=DisplayEmail, state="disabled")
        DisplayEmailEntry.place(relx=0.5, rely=0.345, anchor="center")

        DisplayPasswordLabel = tk.Label(WholeFrame, text="Display Password", bg="#E3E2DF", font=MAIN_FONT)
        DisplayPasswordLabel.place(relx=0.5, rely=0.42, anchor="center")
        DisplayPasswordEntry = tk.Entry(WholeFrame, width=40, textvariable=DisplayPassword, show="*", state="disabled")
        DisplayPasswordEntry.place(relx=0.5, rely=0.47, anchor="center")

        searchButton = tk.Button(WholeFrame, text="Search", bg="#5D011E", width=10, height=2, fg="white", 
                                 command=lambda: searchUser())
        searchButton.place(relx=0.5, rely=0.6, anchor="center")
        backButton = tk.Button(WholeFrame, text="Back", bg="#5D011E", width=10, height=2, fg="white",
                               command=lambda: fn.frameSwitchGeometry(controller, DashboardPage, "1920x1080"))
        backButton.place(relx=0.5, rely=0.7, anchor="center")

        # Construct edit buttons for each field, they will be positioned to the right of the entry fields
        editGameNameButton = tk.Button(WholeFrame, text="Save", bg="#5D011E", width=5, height=1, fg="white",
                                       command=lambda: changeGameName(DisplayGameNameEntry, loggedinAs, DisplayGameNameEntry.get()))
        editGameNameButton.place(relx=0.75, rely=0.095, anchor="center")

        editUsernameButton = tk.Button(WholeFrame, text="Save", bg="#5D011E", width=5, height=1, fg="white",
                                       command=lambda: changeUsername(DisplayUsernameEntry, DisplayUsernameEntry.get()))
        editUsernameButton.place(relx=0.75, rely=0.22, anchor="center")

        editEmailButton = tk.Button(WholeFrame, text="Save", bg="#5D011E", width=5, height=1, fg="white",
                                    command=lambda: changeEmail(DisplayEmailEntry, loggedinAs, DisplayEmailEntry.get()))
        editEmailButton.place(relx=0.75, rely=0.345, anchor="center")

        editPassButton = tk.Button(WholeFrame, text="Save", bg="#5D011E", width=5, height=1, fg="white",
                                    command=lambda: changePassword(DisplayPasswordEntry, loggedinAs, DisplayPasswordEntry.get()))
        editPassButton.place(relx=0.75, rely=0.47, anchor="center")

class AdminSettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        def changeEmail(DisplayEmailEntry, loggedinAs, email):
            """Change the email of the user in the database."""
            UserID = db.getUserID(cursor, loggedinAs)
            UserID = UserID[0]
            if vd.emailCheck(email) == "Valid":
                db.updateEmail(cursor, [email, UserID])
                messagebox.showinfo("Email Change", "Your email has been changed successfully.")
                DisplayEmailEntry.delete(0, "end")
                DisplayEmailEntry.config(state="disabled")
            else:
                messagebox.showerror("Error", "The email you entered is invalid.")
                DisplayEmailEntry.focus()

        def changeUsernameAdmin(DisplayUsernameEntry, username):
            """Change the username of the user in the database."""
            global loggedinAs
            UserID = db.getUserID(cursor, loggedinAs)
            UserID = UserID[0]
            if vd.usernameIsValid(username) == "Valid":
                db.updateUsername(cursor, [username, UserID])
                loggedinAs = username
                messagebox.showinfo("Username Change", "Your username has been changed successfully.")
                DisplayUsernameEntry.delete(0, "end")
                DisplayUsernameEntry.config(state="disabled")
            else:
                messagebox.showerror("Error", "The username you entered is not suitable.")
                DisplayUsernameEntry.focus()

        def changePassword(DisplayPasswordEntry, loggedinAs, password):
            """Change the password of the user in the database."""
            UserID = db.getUserID(cursor, loggedinAs)
            UserID = UserID[0]
            if vd.passwordIsValid(password, password) == "Valid":
                db.updatePassword(cursor, [password, UserID])
                messagebox.showinfo("Password Change", "Your password has been changed successfully.")
                DisplayPasswordEntry.delete(0, "end")
                DisplayPasswordEntry.config(state="disabled")
            else:
                messagebox.showerror("Error", "The password you entered is invalid.")
                DisplayPasswordEntry.focus()

        def changeDiscName(DisplayDiscNameEntry, loggedinAs, discName):
            """Change the discord name of the user in the database."""
            UserID = db.getUserID(cursor, loggedinAs)
            UserID = UserID[0]
            if vd.lengthCheck(discName, 20, 1) == "Valid":
                db.updateDiscordName(cursor, [discName, UserID])
                messagebox.showinfo("Discord Name Change", "Your discord name has been changed successfully.")
                DisplayDiscNameEntry.delete(0, "end")
                DisplayDiscNameEntry.config(state="disabled")
            else:
                messagebox.showerror("Error", "The discord name you entered is invalid.")
                DisplayDiscNameEntry.focus()

        def searchUser():
            """Search for user in the database and find their details"""
            UserID = db.getUserID(cursor, loggedinAs)
            UserID = UserID[0]

            allRowsPart = db.getAllRows(cursor, "tbl_Administrators")
            for row in allRowsPart:
                if row[6] == UserID:
                    DisplayDiscName.set(row[1])
                    DisplayEmail.set(row[5])

            allRowsMain = db.getAllRows(cursor, "tbl_Accounts")
            for row in allRowsMain:
                if row[1] == loggedinAs:
                    DisplayUsername.set(row[1])
                    DisplayPassword.set(row[2])

            DisplayEmailEntry.config(state="normal")
            DisplayDiscNameEntry.config(state="normal")
            DisplayUsernameEntry.config(state="normal")
            DisplayPasswordEntry.config(state="normal")

        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        DisplayDiscName = tk.StringVar()
        DisplayUsername = tk.StringVar()
        DisplayPassword = tk.StringVar()
        DisplayEmail = tk.StringVar()

        DisplayDiscNameLabel = tk.Label(WholeFrame, text="Display Discord Name", bg="#E3E2DF", font=MAIN_FONT)
        DisplayDiscNameLabel.place(relx=0.5, rely=0.05, anchor="center")
        DisplayDiscNameEntry = tk.Entry(WholeFrame, width=40, textvariable=DisplayDiscName, state="disabled")
        DisplayDiscNameEntry.place(relx=0.5, rely=0.095, anchor="center")

        DisplayUsernameLabel = tk.Label(WholeFrame, text="Display Username", bg="#E3E2DF", font=MAIN_FONT)
        DisplayUsernameLabel.place(relx=0.5, rely=0.17, anchor="center")
        DisplayUsernameEntry = tk.Entry(WholeFrame, width=40, textvariable=DisplayUsername, state="disabled")
        DisplayUsernameEntry.place(relx=0.5, rely=0.22, anchor="center")

        DisplayEmailLabel = tk.Label(WholeFrame, text="Display Email", bg="#E3E2DF", font=MAIN_FONT)
        DisplayEmailLabel.place(relx=0.5, rely=0.295, anchor="center")
        DisplayEmailEntry = tk.Entry(WholeFrame, width=40, textvariable=DisplayEmail, state="disabled")
        DisplayEmailEntry.place(relx=0.5, rely=0.345, anchor="center")

        DisplayPasswordLabel = tk.Label(WholeFrame, text="Display Password", bg="#E3E2DF", font=MAIN_FONT)
        DisplayPasswordLabel.place(relx=0.5, rely=0.42, anchor="center")
        DisplayPasswordEntry = tk.Entry(WholeFrame, width=40, textvariable=DisplayPassword, show="*", state="disabled")
        DisplayPasswordEntry.place(relx=0.5, rely=0.47, anchor="center")

        searchButton = tk.Button(WholeFrame, text="Search", bg="#5D011E", width=10, height=2, fg="white",
                                command=lambda: searchUser())
        searchButton.place(relx=0.5, rely=0.6, anchor="center")

        backButton = tk.Button(WholeFrame, text="Back", bg="#5D011E", width=10, height=2, fg="white",
                              command=lambda: fn.frameSwitchGeometry(controller, DashboardPage, "1920x1080"))
        backButton.place(relx=0.5, rely=0.7, anchor="center")

        # Construct edit buttons for each field, they will be positioned to the right of the entry fields
        editDiscNameButton = tk.Button(WholeFrame, text="Save", bg="#5D011E", width=5, height=1, fg="white",
                                      command=lambda: changeDiscName(DisplayDiscNameEntry, loggedinAs, DisplayDiscNameEntry.get()))
        editDiscNameButton.place(relx=0.75, rely=0.095, anchor="center")

        editUsernameButton = tk.Button(WholeFrame, text="Save", bg="#5D011E", width=5, height=1, fg="white",
                                     command=lambda: changeUsernameAdmin(DisplayUsernameEntry, loggedinAs, DisplayUsernameEntry.get()))
        editUsernameButton.place(relx=0.75, rely=0.22, anchor="center")

        editEmailButton = tk.Button(WholeFrame, text="Save", bg="#5D011E", width=5, height=1, fg="white",
                                  command=lambda: changeEmail(DisplayEmailEntry, loggedinAs, DisplayEmailEntry.get()))
        editEmailButton.place(relx=0.75, rely=0.345, anchor="center")

        editPasswordButton = tk.Button(WholeFrame, text="Save", bg="#5D011E", width=5, height=1, fg="white",
                                     command=lambda: changePassword(DisplayPasswordEntry, loggedinAs, DisplayPasswordEntry.get()))
        editPasswordButton.place(relx=0.75, rely=0.47, anchor="center")

class RegisterToTournamentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")
            
        def RegisterToTournament(TournamentName, TeamName, TeamMember2, TeamMember3, TeamCoach):
            """Register a team to a tournament."""

            def WriteTeamToDatabase():
                """Write the team to the database."""
                # First we need to find the TournamentID of the selected tournament
                allRows = db.getAllRows(cursor, "tbl_Tournaments")
                for row in allRows:
                    if row[1] == TournamentName:
                        TournamentID = row[0]
                
                UserID = db.getUserID(cursor, loggedinAs)
                UserID = UserID[0]

                # First we need to check if the tournament is full if it is, place the team on the waiting list
                if db.checkIfTournamentFull(cursor, TournamentID) == True:
                    TeamCaptain = db.getParticipantGameName(cursor, UserID)
                    TeamCaptain = TeamCaptain[0]
                    db.insertToWaitingList(connection, cursor, [TeamName, TeamCaptain, TeamMember2, TeamMember3, TeamCoach, "Waiting", TournamentID])
                    messagebox.showinfo("Success", "Your team has been successfully placed on the waiting list.")
                    SelectedTournament.set("Please Select")
                    TeamNameEntry.delete(0, "end")
                    TeamMember2Entry.delete(0, "end")
                    TeamMember3Entry.delete(0, "end")
                    TeamCoachEntry.delete(0, "end")
                    return

                # Now we need to write the team to the database

                try:
                    TeamCaptain = db.getParticipantGameName(cursor, UserID)
                    TeamCaptain = TeamCaptain[0]
                    db.insertToTeamsTable(connection, cursor, [TeamName, TeamCaptain, TeamMember2, TeamMember3, TeamCoach, "Participating", TournamentID])
                    messagebox.showinfo("Success", "Your team has been successfully registered to the tournament!")
                    SelectedTournament.set("Please Select")
                    TeamNameEntry.delete(0, "end")
                    TeamMember2Entry.delete(0, "end")
                    TeamMember3Entry.delete(0, "end")
                    TeamCoachEntry.delete(0, "end")
                except TypeError: # If the user is an admin they should not be able to register
                    messagebox.showerror("Error", "You must be a participant to register to a tournament.")
                    controller.show_frame(DashboardPage)
        
            # Validate the details entered by the user
        
            if TournamentName == "Please Select":
                messagebox.showerror("Error", "Please select a tournament.")
            elif TeamName == "" or len(TeamName) > 20:
                messagebox.showerror("Error", "Please enter a valid team name.")
                TeamNameEntry.focus()
            elif TeamMember2 == "" or len(TeamMember2) > 20:
                messagebox.showerror("Error", "Please enter a valid team member 2.")
                TeamMember2Entry.focus()
            elif TeamMember3 == "" or len(TeamMember3) > 20:
                messagebox.showerror("Error", "Please enter a valid team member 3.")
                TeamMember3Entry.focus()
            elif len(TeamCoach) > 20:
                messagebox.showerror("Error", "Team Coach name is too long, please shorten it.")
                TeamCoachEntry.focus()
            else:
                WriteTeamToDatabase()
        
        # Create a main frame
        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        # Create a frame for the left side of the window and right side of the window
        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        LeftFrame.pack(side="left", fill="both", expand=True)
        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)

        MainLabel = tk.Label(LeftFrame, text="Register To Tournament", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabel.pack(pady=20)

        TournamentNameLabel = tk.Label(LeftFrame, text="Select the Tournament you'd like to register to", bg = "#E3E2DF", font=LARGE_FONT)
        TournamentNameLabel.pack(pady=20)

        # Lets find all the tournaments stored in the database
        CurrentTournaments = []
        allTournaments = db.getAllRows(cursor, "tbl_Tournaments")
        for row in allTournaments:
            CurrentTournaments.append(row[1])

        # Now let's create a variable to store the selected tournament
        SelectedTournament = tk.StringVar()
        SelectedTournament.set("Please Select")

        # Let's create an option menu to choose from tournaments in the database.
        if len(CurrentTournaments) == 0:
            TournamentsAvailable = tk.OptionMenu(LeftFrame, SelectedTournament, "No Tournaments Available")
            TournamentsAvailable.config(width=20, height=1, font = MAIN_FONT)
            TournamentsAvailable.pack(pady=20)
        else:
            TournamentsAvailable = tk.OptionMenu(LeftFrame, SelectedTournament, *CurrentTournaments)
            TournamentsAvailable.config(width=20, height=1, font = MAIN_FONT)
            TournamentsAvailable.pack(pady=20)

        RefreshTournamentsLabel = tk.Label(LeftFrame, text="Tournaments will refresh every 3 seconds", bg="#E3E2DF", font=MAIN_FONT)
        RefreshTournamentsLabel.pack(pady=20)

        # Now let's start creating fields of entry.
        TeamName = tk.StringVar()
        TeamMember2 = tk.StringVar()
        TeamMember3 = tk.StringVar()
        TeamCoach = tk.StringVar()

        TeamNameLabel = tk.Label(LeftFrame, text="Team Name", bg = "#E3E2DF")
        TeamNameLabel.pack()
        TeamNameEntry = tk.Entry(LeftFrame, width=30, textvariable=TeamName)
        TeamNameEntry.pack(pady=5)

        TeamMember2Label = tk.Label(LeftFrame, text="Team Member 2", bg = "#E3E2DF")
        TeamMember2Label.pack()
        TeamMember2Entry = tk.Entry(LeftFrame, width=30, textvariable=TeamMember2)
        TeamMember2Entry.pack(pady=5)

        TeamMember3Label = tk.Label(LeftFrame, text="Team Member 3", bg = "#E3E2DF")
        TeamMember3Label.pack()
        TeamMember3Entry = tk.Entry(LeftFrame, width=30, textvariable=TeamMember3)
        TeamMember3Entry.pack(pady=5)

        TeamCoachLabel = tk.Label(LeftFrame, text="Team Coach (Optional)", bg = "#E3E2DF")
        TeamCoachLabel.pack()
        TeamCoachEntry = tk.Entry(LeftFrame, width=30, textvariable=TeamCoach)
        TeamCoachEntry.pack(pady=5)

        SpaceLabel = tk.Label(LeftFrame, text="", bg = "#E3E2DF")
        SpaceLabel.pack()

        RegisterButton = tk.Button(LeftFrame, text="Register", bg="#5D011E", fg = "white", width=20, height=2, font = MAIN_FONT,
                                        command = lambda: RegisterToTournament(SelectedTournament.get(), TeamName.get(), TeamMember2.get(), TeamMember3.get(), TeamCoach.get()))
        RegisterButton.pack(pady=5)
        
        fn.makeBackButton(LeftFrame, DashboardPage, controller)

        # Add guidance to right hand panel
        RegisterToTournamentExplanation = tk.Label(RightFrame, text="Register To Tournament Explanation", bg = "#5D011E", font=VERY_LARGE_FONT, fg = "white")
        RegisterToTournamentExplanation.pack(pady=20)

        TeamNameExplanation = tk.Label(RightFrame, text="Team Name: The name of your team\n max 20 chars", bg = "#5D011E", font=LARGE_FONT, fg = "white")
        TeamNameExplanation.pack(pady=10)

        TeamCaptainExplanation = tk.Label(RightFrame, text="Team Captain: Taken from your account details on sign up.", bg = "#5D011E", font=LARGE_FONT, fg = "white")
        TeamCaptainExplanation.pack(pady=10)

        TeamMember2Explanation = tk.Label(RightFrame, text="Team Member 2: The in game name of the second team member\n max 20 chars", bg = "#5D011E", font=LARGE_FONT, fg = "white")
        TeamMember2Explanation.pack(pady=10)

        TeamMember3Explanation = tk.Label(RightFrame, text="Team Member 3: The in game name of the third team member\n max 20 chars", bg = "#5D011E", font=LARGE_FONT, fg = "white")
        TeamMember3Explanation.pack(pady=10)

        TeamCoachExplanation = tk.Label(RightFrame, text="Team Coach: The in game name of the team coach\n (If you have no coach leave empty) max 20 chars", bg = "#5D011E", font=LARGE_FONT, fg = "white")
        TeamCoachExplanation.pack(pady=10)

        fn.newCheckPastFuture(self, "future", TournamentsAvailable, SelectedTournament)

class ScoringCalculatorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        TeamPlacement = tk.StringVar()
        TeamKills = tk.StringVar()

        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF") 
        LeftFrame.pack(side="left", fill="both", expand=True)
        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)
        
        MainLabel = tk.Label(LeftFrame, text="Scoring Calculator", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabel.pack(pady=20)

        TeamPlacementLabel = tk.Label(LeftFrame, text="Team Placement", bg = "#E3E2DF", font=LARGE_FONT)
        TeamPlacementLabel.pack(pady=20)
        TeamPlacementEntry = tk.Entry(LeftFrame, width=30, textvariable=TeamPlacement)
        TeamPlacementEntry.pack(pady=20)
        fn.CreateToolTip(TeamPlacementEntry, "Enter the placement your team got in the game. (1-20)")

        TeamKillsLabel = tk.Label(LeftFrame, text="Team Kills", bg = "#E3E2DF", font=LARGE_FONT)
        TeamKillsLabel.pack(pady=20)
        TeamKillsEntry = tk.Entry(LeftFrame, width=30, textvariable=TeamKills)
        TeamKillsEntry.pack(pady=20)
        fn.CreateToolTip(TeamKillsEntry, "Enter the number of kills your team got in the game.")

        CalculateTotalScore = tk.Button(LeftFrame, text="Calculate!", bg="#5D011E", width=20, height=2, fg = "white", font = MAIN_FONT, 
                                        command = lambda: fn.calculateScore(TeamPlacement.get(), TeamKills.get(), TeamPlacementEntry, TeamKillsEntry))
        CalculateTotalScore.pack(pady=5)

        fn.makeBackButton(LeftFrame, DashboardPage, controller)

        # Start adding an explanation for the points scoring on the right hand side
        ScoringCalculatorExplanation = tk.Label(RightFrame, text="Scoring Calculator Explanation", bg = "#5D011E", font=VERY_LARGE_FONT, fg = "white")
        ScoringCalculatorExplanation.pack(pady=20)

        ScoringCalculatorQ1 = tk.Label(RightFrame, text="How does the scoring work?", bg = "#5D011E", font=LARGE_FONT, fg = "white")
        ScoringCalculatorQ1.pack(pady=20)

        ScoringCalculatorExplanationPlacement = tk.Label(RightFrame, text="1st = 12 points \n 2nd = 9 points \n 3rd = 7 points \n 4th = 5 points \n 5th = 4 points \n 6th - 10th = 2 points \n 11th - 15th = 1 point \n 16th - 20th = 0 points", bg = "#5D011E", font=LARGE_FONT, fg = "white")
        ScoringCalculatorExplanationPlacement.pack()
        ScoringCalculatorExplanationKills = tk.Label(RightFrame, text="1 kill = 1 point", bg = "#5D011E", font=LARGE_FONT, fg = "white")
        ScoringCalculatorExplanationKills.pack()

        SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
        SpaceLabel.pack(pady=20)

        ScoringCalculatorQ2 = tk.Label(RightFrame, text="How do I use the calculator?", bg = "#5D011E", font=LARGE_FONT, fg = "white")
        ScoringCalculatorQ2.pack(pady=20)
        ScoringCalculatorExplanationUse = tk.Label(RightFrame, text="Enter your team placement and number of kills \n and click calculate to see your total score.", bg = "#5D011E", font=LARGE_FONT, fg = "white")
        ScoringCalculatorExplanationUse.pack()

class FAQandRulesPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")
        
        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        LeftFrame.pack(side="left", fill="both", expand=True)

        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)
        
        RulesLabel = tk.Label(LeftFrame, text="Rules", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        RulesLabel.pack(pady=20)

        FAQLabel = tk.Label(RightFrame, text="FAQ", bg = "#5D011E", font=VERY_LARGE_FONT, fg = "white")
        FAQLabel.pack(pady=20)

        RulesWarning = tk.Label(LeftFrame, text="By violating any of the following rules the \n person or team responsible will be disqualified from \n the tournament and banned from future tournaments.", bg = "#E3E2DF", font=LARGE_FONT)
        Rules1 = tk.Label(LeftFrame, text="1. No teaming, communication or co-operation with other teams", bg = "#E3E2DF", font=MEDIUM_FONT)
        Rules2 = tk.Label(LeftFrame, text="2. No stream sniping", bg = "#E3E2DF", font=MEDIUM_FONT)
        Rules3 = tk.Label(LeftFrame, text="3. No hacking or cheating", bg = "#E3E2DF", font=MEDIUM_FONT)
        Rules4 = tk.Label(LeftFrame, text="4. No offensive language or behaviour", bg = "#E3E2DF", font=MEDIUM_FONT)
        Rules5 = tk.Label(LeftFrame, text="5. Do not disobey admins", bg = "#E3E2DF", font=MEDIUM_FONT)
        Rules6 = tk.Label(LeftFrame, text="6. No teaming with banned players", bg = "#E3E2DF", font=MEDIUM_FONT)
        Rules7 = tk.Label(LeftFrame, text="7. No stream-sniping in Scrims or Tournaments \n - if this rule is broken you will be permanently banned", bg = "#E3E2DF", font=MEDIUM_FONT)
        Rules8 = tk.Label(LeftFrame, text="8. Leaving tournaments any time after the 1st game \n has started is undesired. If a player or the team \n needs to leave mid-scrim, let the Scrim Admin \n or Scrim Helper of your lobby know ASAP. Failure to \n do so will incur warnings.", bg = "#E3E2DF", font=MEDIUM_FONT)
        RulesWarning.pack(pady=5)
        Rules1.pack(pady=5)
        Rules2.pack(pady=5)
        Rules3.pack(pady=5)
        Rules4.pack(pady=5)
        Rules5.pack(pady=5)
        Rules6.pack(pady=5)
        Rules7.pack(pady=5)
        Rules8.pack(pady=5)

        FAQ1 = tk.Label(RightFrame, text="I am falsely banned, how do I appeal?", bg = "#5D011E", font=LARGE_FONT_BOLD, fg = "white")
        FAQ1Answer = tk.Label(RightFrame, text="Please contact an admin on Discord \n regarding applications. We will also publicise \n whenever we are seeking more staff.", bg = "#5D011E", font=MEDIUM_FONT, fg = "white")
        FAQ2 = tk.Label(RightFrame, text="How do I join a tournament?", bg = "#5D011E", font=LARGE_FONT_BOLD, fg = "white")
        FAQ2Answer = tk.Label(RightFrame, text="Go to the dashboard and click on \n the tournament you wish to join.", bg = "#5D011E", font=MEDIUM_FONT, fg = "white")
        FAQ3 = tk.Label(RightFrame, text="How do I apply to become an admin?", bg = "#5D011E", font=LARGE_FONT_BOLD, fg = "white")
        FAQ3Answer = tk.Label(RightFrame, text="Applications are closed as of now. When they open \n information will be available on our discord", bg = "#5D011E", font=MEDIUM_FONT, fg = "white")
        FAQ1.pack(pady=5)
        FAQ1Answer.pack(pady=5)
        SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
        SpaceLabel.pack(pady=5)
        FAQ2.pack(pady=5)
        FAQ2Answer.pack(pady=5)
        SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
        SpaceLabel.pack(pady=5)
        FAQ3.pack(pady=5)
        FAQ3Answer.pack(pady=5)

        Summary = tk.Label(RightFrame, text="If you have any further questions \n please contact an admin on Discord.", bg = "#5D011E", font=MEDIUM_FONT_BOLD, fg = "white")
        Summary.pack(pady=20)

        backIcon = tk.PhotoImage(file="Images and Icons/Leave_Icon.png")
        BackButton = ttk.Button(LeftFrame, image = backIcon, compound="left", style="Toolbutton", takefocus=False,
                                command=lambda: controller.show_frame(DashboardPage))
        BackButton.image = backIcon
        BackButton.place(relx=0.05, rely=0.03, anchor="center")

class CreateAnAdminPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        def CreateAdmin(AdminDiscNameStore, AdminFirstNameStore, AdminSurnameStore, AdminDOBStore, AdminEmailStore, AdminUsernameStore, AdminPasswordStore, AdminPasswordConfirmStore):
            """Create an admin account."""
    
            def SignupConfirmation():
                """Confirmation of the admin being created."""
                db.insertToAccountsTable(connection, cursor, [AdminUsernameStore, AdminPasswordStore, "Admin"])
                UserIDForeignKey = db.getUserID(cursor, AdminUsernameStore)
                db.insertToAdministratorsTable(connection, cursor, [AdminDiscNameStore, AdminFirstNameStore, AdminSurnameStore, AdminDOBStore, AdminEmailStore, UserIDForeignKey[0]])
                messagebox.showinfo("Admin", "You have created an admin successfully!")
                AdminDiscNameEntry.delete(0, "end")
                AdminFirstNameEntry.delete(0, "end")
                AdminSurnameEntry.delete(0, "end")
                AdminDOBCalendar.set_date("01-01-2008")
                AdminEmailEntry.delete(0, "end")
                AdminUsernameEntry.delete(0, "end")
                AdminPasswordEntry.delete(0, "end")
                AdminPasswordConfirmEntry.delete(0, "end")
        
            # Validate the details entered by the user
            validDiscName = False
            if vd.lengthCheck(AdminDiscNameStore, 20, 4) == False:
                messagebox.showerror("Error", "Discord Name must be between 4-20 chars.")
                AdminDiscNameEntry.focus()
            else:
                validDiscName = True
            
            validFirstName = False
            if vd.lengthCheck(AdminFirstNameStore, 20, 1) == False:
                messagebox.showerror("Error", "First Name must be between 1-20 chars.")
                AdminFirstNameEntry.focus()
            else:
                validFirstName = True
            
            validSurname = False
            if vd.lengthCheck(AdminSurnameStore, 20, 1) == False:
                messagebox.showerror("Error", "Surname must be between 1-20 chars.")
                AdminSurnameEntry.focus()
            else:
                validSurname = True
            
            validEmail = False
            if vd.emailCheck(AdminEmailStore) == "Valid":
                validEmail = True
            elif vd.emailCheck(AdminEmailStore) == "Taken":
                messagebox.showerror("Error", "Email is already in use.")
                AdminEmailEntry.focus()
            else:
                messagebox.showerror("Error", "Please enter a valid email.")
                AdminEmailEntry.focus()
                
            validUsername = False
            if vd.lengthCheck(AdminUsernameStore, 20, 4) == False:
                messagebox.showerror("Error", "Username must be between 4-20 chars.")
                AdminUsernameEntry.focus()
            else:
                validUsername = True
            
            validPassword = False
            if vd.lengthCheck(AdminPasswordStore, 20, 4) == False:
                messagebox.showerror("Error", "Password must be between 4-20 chars.")
                AdminPasswordEntry.focus()
            else:
                validPassword = True

            if validDiscName and validFirstName and validSurname and validEmail and validUsername and validPassword:
                SignupConfirmation()
            
        AdminDiscName = tk.StringVar()
        AdminFirstName = tk.StringVar()
        AdminSurname = tk.StringVar()
        AdminEmail = tk.StringVar()
        AdminUsername = tk.StringVar()
        AdminPassword = tk.StringVar()
        AdminPasswordConfirm = tk.StringVar()

        # Lets create a main frame
        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        # Create a frame for the left side of the window and right side of the window
        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        LeftFrame.pack(side="left", fill="both", expand=True)
        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)

        MainLabel = tk.Label(LeftFrame, text="Create an Admin", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabel.pack(pady=20)

        AdminDiscNameLabel = tk.Label(LeftFrame, text="Discord Name", bg = "#E3E2DF", font=MAIN_FONT)
        AdminDiscNameLabel.pack(padx=10)
        AdminDiscNameEntry = tk.Entry(LeftFrame, width=40, textvariable=AdminDiscName)
        AdminDiscNameEntry.pack(padx=10, pady=10)

        AdminFirstNameLabel = tk.Label(LeftFrame, text="First Name", bg = "#E3E2DF", font=MAIN_FONT)
        AdminFirstNameLabel.pack(padx=10)
        AdminFirstNameEntry = tk.Entry(LeftFrame, width=40, textvariable=AdminFirstName)
        AdminFirstNameEntry.pack(padx=10, pady=10)

        AdminSurnameLabel = tk.Label(LeftFrame, text="Surname", bg = "#E3E2DF", font=MAIN_FONT)
        AdminSurnameLabel.pack(padx=10)
        AdminSurnameEntry = tk.Entry(LeftFrame, width=40, textvariable=AdminSurname)
        AdminSurnameEntry.pack(padx=10, pady=10)

        AdminDOBLabel = tk.Label(LeftFrame, text="Date of Birth", bg = "#E3E2DF", font=MAIN_FONT)
        AdminDOBLabel.pack(padx=10)
        AdminDOBCalendar = DateEntry(LeftFrame, selectmode="day", year=2008, month=1, day=1, date_pattern="dd-mm-yyyy")
        AdminDOBCalendar.pack(padx=10, pady=10)
        fn.CreateToolTip(AdminDOBCalendar, "Select your date of birth, use the calendar provided to select the date")

        AdminEmailLabel = tk.Label(LeftFrame, text="Email", bg = "#E3E2DF", font=MAIN_FONT)
        AdminEmailLabel.pack(padx=10)
        AdminEmailEntry = tk.Entry(LeftFrame, width=40, textvariable=AdminEmail)
        AdminEmailEntry.pack(padx=10, pady=10)
        fn.CreateToolTip(AdminEmailEntry, "Enter your email address, e.g samstournaments@gmail.com")

        AdminUsernameLabel = tk.Label(LeftFrame, text="Username", bg = "#E3E2DF", font=MAIN_FONT)
        AdminUsernameLabel.pack(padx=10)
        AdminUsernameEntry = tk.Entry(LeftFrame, width=40, textvariable=AdminUsername)
        AdminUsernameEntry.pack(padx=10, pady=10)

        AdminPasswordLabel = tk.Label(LeftFrame, text="Password", bg = "#E3E2DF", font=MAIN_FONT)
        AdminPasswordLabel.pack(padx=10)
        AdminPasswordEntry = tk.Entry(LeftFrame, width=40, textvariable=AdminPassword, show="*")
        AdminPasswordEntry.pack(padx=10, pady=10)

        AdminPasswordConfirmLabel = tk.Label(LeftFrame, text="Confirm Password", bg = "#E3E2DF", font=MAIN_FONT)
        AdminPasswordConfirmLabel.pack(padx=10)
        AdminPasswordConfirmEntry = tk.Entry(LeftFrame, width=40, textvariable=AdminPasswordConfirm, show="*")
        AdminPasswordConfirmEntry.pack(padx=10, pady=10)
        fn.CreateToolTip(AdminPasswordConfirmEntry, "Confirm your password, must match the password entered above")

        ShowPassword = tk.Checkbutton(LeftFrame, text="Show Password", bg = "#E3E2DF", font=MAIN_FONT, command=fn.show_and_hide(AdminPasswordEntry, AdminPasswordConfirmEntry))
        ShowPassword.pack(pady=10)

        CreateAdminButton = tk.Button(LeftFrame, text="Create Admin", bg="#5D011E", fg = "white", width=20, height=2,
                                      command = lambda: CreateAdmin(AdminDiscName.get(), AdminFirstName.get(), AdminSurname.get(), AdminDOBCalendar.get(), AdminEmail.get(), AdminUsername.get(), AdminPassword.get(), AdminPasswordConfirm.get()))
        CreateAdminButton.pack(pady=5)
        
        fn.makeBackButton(LeftFrame, DashboardPage, controller)

        # Start explaining the rules for creating an admin on the right hand side
        SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
        SpaceLabel.pack(pady=30)
        AdminDiscNameExplanation = tk.Label(RightFrame, text="Discord Name: 20 Characters Max", bg = "#5D011E", fg = "white", font=LARGE_FONT)
        AdminDiscNameExplanation.pack(pady=20)  
        AdminFirstNameExplanation = tk.Label(RightFrame, text="First Name: 20 Characters Max", bg = "#5D011E", fg = "white", font=LARGE_FONT)
        AdminFirstNameExplanation.pack(pady=20)
        AdminSurnameExplanation = tk.Label(RightFrame, text="Surname: 20 Characters Max", bg = "#5D011E", fg = "white", font=LARGE_FONT)
        AdminSurnameExplanation.pack(pady=20)
        AdminDOBExplanation = tk.Label(RightFrame, text="Choose a date, set to 01/01/2008 by default", bg = "#5D011E", fg = "white", font=LARGE_FONT)
        AdminDOBExplanation.pack(pady=20)
        AdminEmailExplanation = tk.Label(RightFrame, text="Email: 50 Characters Max, @. format required", bg = "#5D011E", fg = "white", font=LARGE_FONT)
        AdminEmailExplanation.pack(pady=20)
        AdminUsernameExplanation = tk.Label(RightFrame, text="Username: 15 Characters Max", bg = "#5D011E", fg = "white", font=LARGE_FONT)
        AdminUsernameExplanation.pack(pady=20)
        AdminPasswordExplanation = tk.Label(RightFrame, text="Password: 18 Characters Max, 8 Characters Min, \n Must contain 1 capital letter and 1 number", bg = "#5D011E", fg = "white", font=LARGE_FONT)
        AdminPasswordExplanation.pack(pady=20)
        AdminPasswordConfirmExplanation = tk.Label(RightFrame, text="Confirm Password: Must match password", bg = "#5D011E", fg = "white", font=LARGE_FONT)
        AdminPasswordConfirmExplanation.pack(pady=20)

class CreateATournamentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        def CreateTournament(TournamentName, TournamentDate, TournamentTime, TournamentDescription, MaxTeams, NumGames):
            """Validate the details entered by the user"""
                
            def WriteToDatabase():
                """Write the details to the database"""
                db.insertToTournamentsTable(connection, cursor, [TournamentName, TournamentDate, TournamentTime, TournamentDescription, MaxTeams, NumGames])
                messagebox.showinfo("Tournament", "You have created a tournament successfully!")
                TournamentNameEntry.delete(0, "end")
                TournamentDateCalendar.set_date("01-01-2024")
                TournamentTimeEntry.delete(0, "end")
                TournamentDescriptionEntry.delete("1.0", tk.END)
                NumGamesVar.set(NumGamesList[0])
                MaxTeamsVar.set(MaxTeamsList[0])
            
            validName = False
            if vd.lengthCheck(TournamentName, 20, 1) == "Invalid":
                messagebox.showerror("Error", "Please enter a valid Tournament name.")
                TournamentNameEntry.focus()
            else:
                validName = True
            validTime = False
            if vd.timeCheck(TournamentTime) == False:
                messagebox.showerror("Error", "Please enter a valid time. Format: HH:MM")
                TournamentTimeEntry.focus()
            else:
                validTime = True

            # We also want to ensure that there are no tournaments with the same name
            tournamentNameTaken = False
            if vd.duplicateCheck(TournamentName, "tbl_Tournaments", 1) == "Taken":
                messagebox.showerror("Error", "Tournament name is already taken.")
                TournamentNameEntry.focus()
            else:
                tournamentNameTaken = True

            # Lets check if the Tournament Description is valid, it must be less than 100 characters and not empty
            descValid = False
            if vd.lengthCheck(TournamentDescription, 100, 1) == False:
                messagebox.showerror("Error", "Please enter a valid Tournament description.")
                TournamentDescriptionEntry.focus()
            else:
                descValid = True
            
            if validTime and validName and tournamentNameTaken and descValid:
                WriteToDatabase()

        TournamentName = tk.StringVar()
        TournamentTime = tk.StringVar()

        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)
        
        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        LeftFrame.pack(side="left", fill="both", expand=True)
        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)

        MainLabel = tk.Label(LeftFrame, text="Create Tournaments", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabel.pack(pady=20)

        editicon = tk.PhotoImage(file="Images and Icons/updatedicon.png")
        EditButton = ttk.Button(LeftFrame, image=editicon, style="Toolbutton", takefocus=False,
                               command=lambda: controller.show_frame(EditTournamentsPage))
        EditButton.image = editicon
        EditButton.place(relx=0.72, rely=0.04, anchor="center")

        TournamentNameLabel = tk.Label(LeftFrame, text="Tournament Name", bg = "#E3E2DF", font=MAIN_FONT)
        TournamentNameLabel.pack(padx=10)
        TournamentNameEntry = tk.Entry(LeftFrame, width=30, textvariable=TournamentName)
        TournamentNameEntry.pack(padx=10, pady=5)

        TournamentDateLabel = tk.Label(LeftFrame, text="Tournament Date", bg = "#E3E2DF", font=MAIN_FONT)
        TournamentDateLabel.pack(padx=10)
        TournamentDateCalendar = DateEntry(LeftFrame, selectmode="day", year=2024, month=1, day=1, date_pattern="dd-mm-yyyy")
        TournamentDateCalendar.pack(padx=10, pady=5)
        fn.CreateToolTip(TournamentDateCalendar, "Select the date of the tournament, use the calendar provided to select the date")

        TournamentTimeLabel = tk.Label(LeftFrame, text="Tournament Time", bg = "#E3E2DF", font=MAIN_FONT)
        TournamentTimeLabel.pack(padx=10)
        TournamentTimeEntry = tk.Entry(LeftFrame, width=30, textvariable=TournamentTime)
        TournamentTimeEntry.pack(padx=10, pady=10)
        fn.CreateToolTip(TournamentTimeEntry, "Enter the time of the tournament, format: HH:MM")

        TournamentDescriptionLabel = tk.Label(LeftFrame, text="Tournament Description", bg = "#E3E2DF", font=MAIN_FONT)
        TournamentDescriptionLabel.pack(padx=10)
        TournamentDescriptionEntry = scrolledtext.ScrolledText(LeftFrame, wrap=tk.WORD, width=40, height=5)
        TournamentDescriptionEntry.pack(padx=10, pady=10)

        MaxTeamsLabel = tk.Label(LeftFrame, text="Max Teams", bg = "#E3E2DF", font=MAIN_FONT)
        MaxTeamsLabel.pack(padx=10)

        MaxTeamsList = ["20", "40", "80"]
        MaxTeamsVar = tk.StringVar()
        MaxTeamsVar.set(MaxTeamsList[0])
        MaxTeamsDrop = tk.OptionMenu(LeftFrame, MaxTeamsVar, *MaxTeamsList)
        MaxTeamsDrop.pack(pady=10)

        NumGamesLabel = tk.Label(LeftFrame, text="Number of Games", bg = "#E3E2DF", font=MAIN_FONT)
        NumGamesLabel.pack(padx=10)
        NumGamesList = ["4", "6", "8"]
        NumGamesVar = tk.StringVar()
        NumGamesVar.set(NumGamesList[0])
        NumGamesDrop = tk.OptionMenu(LeftFrame, NumGamesVar, *NumGamesList)
        NumGamesDrop.pack(pady=10)

        CreateTournamentButton = tk.Button(LeftFrame, text="Create Tournament", bg="#5D011E", fg = "white", width=20, height=2, 
                                           command = lambda: CreateTournament(TournamentName.get(), TournamentDateCalendar.get(), TournamentTime.get(), TournamentDescriptionEntry.get("1.0", tk.END), MaxTeamsVar.get(), NumGamesVar.get()))
        CreateTournamentButton.pack(pady=5)

        fn.makeBackButton(LeftFrame, DashboardPage, controller)

        # Start adding an explanation for the points scoring on the right hand side
        SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
        SpaceLabel.pack(pady=30)
        TournamentNameExplanation = tk.Label(RightFrame, text="Tournament Name: 20 Characters Max\n TOURNAMENT NAMES MUST BE UNIQUE", bg = "#5D011E", fg = "white", font=LARGE_FONT)
        TournamentNameExplanation.pack(pady=20)
        TournamentDateExplanation = tk.Label(RightFrame, text="Choose an appropriate Tournament Date\nSet at 01/01/2024 by default", bg = "#5D011E", fg = "white", font=LARGE_FONT)
        TournamentDateExplanation.pack(pady=20)
        TournamentTimeExplanation = tk.Label(RightFrame, text="Tournament Time: HH:MM", bg = "#5D011E", fg = "white", font=LARGE_FONT)
        TournamentTimeExplanation.pack(pady=20)
        TournamentDescriptionExplanation = tk.Label(RightFrame, text="Tournament Description: 100 Characters Max", fg = "white", bg = "#5D011E", font=LARGE_FONT)
        TournamentDescriptionExplanation.pack(pady=20)
        MaxTeamsExplanation = tk.Label(RightFrame, text="Max Teams: 20, 40, 80 max", bg = "#5D011E", fg = "white", font=LARGE_FONT)
        MaxTeamsExplanation.pack(pady=20)
        NumGamesExplanation = tk.Label(RightFrame, text="Number of Games: 4, 6, 8", bg = "#5D011E", fg = "white", font=LARGE_FONT)
        NumGamesExplanation.pack(pady=20)

        AdditionalInfo = tk.Label(RightFrame, text="The Max Teams and Number of Games may be\n subject to change in the future but for now\n these are the only available formats", bg = "#5D011E", fg = "white", font=LARGE_FONT)
        AdditionalInfo.pack(pady=20)

class EditTournamentsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        def LoadDetails(tournament):
            # First lets check if the user has selected a tournament
            if tournament == "Please Select":
                messagebox.showerror("Error", "Please select a tournament.")
                return
            
            # Now lets find the details of the tournament
            tournamentDetails = db.getAllRows(cursor, "tbl_Tournaments")
            for row in tournamentDetails:
                if row[1] == tournament:
                    tournamentName = row[1]
                    tournamentDate = row[2]
                    tournamentTime = row[3]
                    tournamentDescription = row[4]
                    break
            
            # Now lets load the details into the entry boxes
            TournamentName.set(tournamentName)
            TournamentDateCalendar.set_date(tournamentDate)
            TournamentTime.set(tournamentTime)
            TournamentDescriptionEntry.delete("1.0", tk.END)
            TournamentDescriptionEntry.insert(tk.INSERT, tournamentDescription)
        
        def CommitChanges(ChosenTournament):
            # First lets check if the user has selected a tournament
            if SelectedTournament == "Please Select":
                messagebox.showerror("Error", "Please select a tournament.")
                return
            
            # Lets find the tournament ID
            allTournamentDetails = db.getAllRows(cursor, "tbl_Tournaments")
            for row in allTournamentDetails:
                if row[1] == ChosenTournament:
                    tournamentID = row[0]
                    break
            
            # Now lets get the details entered by the user
            tournamentName = TournamentName.get()
            tournamentDate = TournamentDateCalendar.get()
            tournamentTime = TournamentTime.get()
            tournamentDescription = TournamentDescriptionEntry.get("1.0", tk.END)
            maxTeams = MaxTeams.get()
            numGames = NumGames.get()

            db.updateTournamentDetails(connection, cursor, [tournamentName, tournamentDate, tournamentTime, tournamentDescription, maxTeams, numGames, tournamentID])
            messagebox.showinfo("Tournament", "Tournament details updated successfully!")

            SelectedTournament.set("Please Select")
            TournamentName.set("")
            TournamentDateCalendar.set_date("01-01-2024")
            TournamentTime.set("")
            TournamentDescriptionEntry.delete("1.0", tk.END)

        def DeleteTournament(tournament):
            if tournament == "Please Select":
                messagebox.showerror("Error", "Please select a tournament.")
                return

            allTournamentDetails = db.getAllRows(cursor, "tbl_Tournaments")
            for row in allTournamentDetails:
                if row[1] == tournament:
                    tournamentID = row[0]
                    break

            confirm = messagebox.askyesno("Delete Tournament", "Are you sure you want to delete tournament: " + tournament + "?")
            if confirm:
                db.deleteTournament(connection, cursor, tournamentID)
                db.delAllTeamsFromTournament(connection, cursor, tournamentID)
                messagebox.showinfo("Tournament", "Tournament deleted successfully!")
                SelectedTournament.set("Please Select")

        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        LeftFrame.pack(side="left", fill="both", expand=True)

        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)

        MainLabel = tk.Label(LeftFrame, text="Edit Tournaments", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabel.pack(pady=10)
        
        # Lets find all the tournaments stored in the database
        CurrentTournaments = []
        allTournaments = db.getAllRows(cursor, "tbl_Tournaments")
        for row in allTournaments:
            CurrentTournaments.append(row[1])
        
        # Now let's create a variable to store the selected tournament
        SelectedTournament = tk.StringVar()
        SelectedTournament.set("Please Select")

        ChooseATournamentLabel = tk.Label(LeftFrame, text="Choose a Tournament", bg = "#E3E2DF", font=LARGE_FONT)
        ChooseATournamentLabel.pack(pady=5)

        # Let's create an option menu to choose from tournaments in the database.
        if len(CurrentTournaments) == 0:
            TournamentsAvailable = tk.OptionMenu(LeftFrame, SelectedTournament, "No Tournaments Available")
            TournamentsAvailable.config(width=20, height=1, font = MAIN_FONT)
            TournamentsAvailable.pack(pady=10)
        else:
            TournamentsAvailable = tk.OptionMenu(LeftFrame, SelectedTournament, *CurrentTournaments)
            TournamentsAvailable.config(width=20, height=1, font = MAIN_FONT)
            TournamentsAvailable.pack(pady=10)

        LoadDetailsButton = tk.Button(LeftFrame, text="Load Details", bg="#5D011E", fg="white", width=20, height=2,
                                      command = lambda: LoadDetails(SelectedTournament.get()))
        LoadDetailsButton.pack(pady=10)

        TournamentName = tk.StringVar()
        TournamentTime = tk.StringVar()

        TournamentNameLabel = tk.Label(LeftFrame, text="Tournament Name", bg = "#E3E2DF", font=MAIN_FONT)
        TournamentNameLabel.pack()
        TournamentNameEntry = tk.Entry(LeftFrame, width=30, textvariable=TournamentName)
        TournamentNameEntry.pack(pady=10)

        TournamentDateLabel = tk.Label(LeftFrame, text="Tournament Date", bg = "#E3E2DF", font=MAIN_FONT)
        TournamentDateLabel.pack(padx=10)
        TournamentDateCalendar = DateEntry(LeftFrame, selectmode="day", year=2024, month=1, day=1, date_pattern="dd-mm-yyyy")
        TournamentDateCalendar.pack(padx=10, pady=5)
        fn.CreateToolTip(TournamentDateCalendar, "Select the date of the tournament, use the calendar provided to select the date")

        TournamentTimeLabel = tk.Label(LeftFrame, text="Tournament Time", bg = "#E3E2DF", font=MAIN_FONT)
        TournamentTimeLabel.pack()
        TournamentTimeEntry = tk.Entry(LeftFrame, width=30, textvariable=TournamentTime)
        TournamentTimeEntry.pack(pady=10)

        TournamentDescriptionLabel = tk.Label(LeftFrame, text="Tournament Description", bg = "#E3E2DF", font=MAIN_FONT)
        TournamentDescriptionLabel.pack(padx=10)
        TournamentDescriptionEntry = scrolledtext.ScrolledText(LeftFrame, wrap=tk.WORD, width=40, height=5)
        TournamentDescriptionEntry.pack(padx=10)

        MaxTeamsList = ["20", "40", "80"]
        MaxTeams = tk.StringVar()
        MaxTeams.set(MaxTeamsList[0])
        MaxTeamsLabel = tk.Label(LeftFrame, text="Max Teams", bg = "#E3E2DF", font=MAIN_FONT)
        MaxTeamsLabel.pack(pady=5)
        MaxTeamsDrop = tk.OptionMenu(LeftFrame, MaxTeams, *MaxTeamsList)
        MaxTeamsDrop.pack()

        NumGamesLabel = tk.Label(LeftFrame, text="Number of Games", bg = "#E3E2DF", font=MAIN_FONT)
        NumGamesLabel.pack(padx=10, pady=5)
        NumGamesList = ["4", "6", "8"]
        NumGames = tk.StringVar()
        NumGames.set(NumGamesList[0])
        NumGamesDrop = tk.OptionMenu(LeftFrame, NumGames, *NumGamesList)
        NumGamesDrop.pack(pady=5)

        CommitChangesButton = tk.Button(LeftFrame, text="Commit Changes", fg="white", bg="#5D011E", width=20, height=2,
                                        command=lambda: CommitChanges(SelectedTournament.get()))
        CommitChangesButton.pack(padx=10, pady=5)

        fn.makeBackButton(LeftFrame, DashboardPage, controller)

        # Now lets use the right hand panel to create a delete tournament section
        DeleteTournamentLabel = tk.Label(RightFrame, text="Delete Tournament", bg = "#5D011E", font=VERY_LARGE_FONT, fg = "white")
        DeleteTournamentLabel.pack(pady=10)

        ExplanationLabel = tk.Label(RightFrame, text="Please select a tournament from the dropdown\n menu on the left to delete a tournament.", bg = "#5D011E", font=LARGE_FONT, fg = "white")
        ExplanationLabel.pack(pady=10)

        DeleteTournamentButton = tk.Button(RightFrame, text="Delete Tournament", bg="#E3E2DF", fg="black", width=20, height=2, font=MAIN_FONT,
                                           command = lambda: DeleteTournament(SelectedTournament.get()))
        DeleteTournamentButton.pack(pady=5)

        fn.newCheckPastFuture(self, "all", TournamentsAvailable, SelectedTournament)

class UnregisterFromTournamentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")
        
        def FromWaitingList(TournamentName):
            # First lets getthe number of teams registered to the tournament with a status of "Waiting"
            allTeams = db.getAllRows(cursor, "tbl_Teams")
            for row in allTeams:
                if TournamentName == db.getTournamentName(cursor, row[7])[0]:
                    if row[6] == "Waiting":
                        TeamID = row[0]
                        TeamName = db.getTeamName(cursor, TeamID)
                        TeamName = TeamName[0]
                        break
            
            # If there are no teams on the waiting list, we can return
            if TeamID == None:
                return
            
            # Lets add the team to the tournament
            db.updateTeamStatus(connection, cursor, ["Participating", TeamID])
            TeamCaptainName = db.getTeamCaptainfromTeamID(cursor, TeamID)
            TeamCaptainName = TeamCaptainName[0]
            TeamCaptainUserID = db.getUserIDfromTeamCaptain(cursor, TeamCaptainName)
            TeamCaptainUserID = TeamCaptainUserID[0]
            TeamCaptainEmail = db.getEmailfromUserID(cursor, TeamCaptainUserID)
            TeamCaptainEmail = TeamCaptainEmail[0]
            email.sendParticipatingEmail(TeamName, TournamentName, TeamCaptainEmail)

        def UnregisterFromTournament(TournamentName):
            # First lets check if the user has selected a tournament
            if TournamentName == "Please Select":
                messagebox.showerror("Error", "Please select a tournament.")
                return
            
            UserID = db.getUserID(cursor, loggedinAs) 
            UserID = UserID[0]
            
            allTeams = db.getAllRows(cursor, "tbl_Teams")
            GameName = db.getParticipantGameName(cursor, UserID)
            try:
                GameName = GameName[0]
                for row in allTeams:
                    if GameName in row[2]: 
                        if TournamentName == db.getTournamentName(cursor, row[7])[0]:
                            TeamID = row[0]
                            break
            except TypeError:
                messagebox.showerror("Error", "Admins should not register/unregister from their admin accounts.")
                return

            TeamName = db.getTeamName(cursor, TeamID)
            TeamName = TeamName[0]

            # Confirm whether the user wants to unregister their team from the tournament
            confirm = messagebox.askyesno("Unregister", "Are you sure you want to unregister your team: " + TeamName + " from the tournament: " + TournamentName + "?")
            if confirm:
                db.deleteTeam(connection, cursor, TeamID)
                messagebox.showinfo("Unregister", "You have unregistered your team from the tournament successfully!")
                SelectedTournament.set("Please Select")
                FindRegisteredTo()
                FromWaitingList(TournamentName)

        def FindRegisteredTo():
            # First we need to find the UserID of the current user
            UserID = db.getUserID(cursor, loggedinAs)
            
            # Turn the UserID into an integer
            UserID = UserID[0]

            # Now we need to get their game name
            GameName = db.getParticipantGameName(cursor, UserID)
            GameName = GameName[0]
            RegisteredToTournamentsUpdated = []
            allTeams = db.getAllRows(cursor, "tbl_Teams")
            for row in allTeams:
                # Check if the users game name is equal to the game name in the row
                if GameName == row[2]:
                    TournamentName = db.getTournamentName(cursor, row[7])
                    RegisteredToTournamentsUpdated.append(TournamentName[0])

            menu = ChooseATournament["menu"]
            menu.delete(0, "end")

            if len(RegisteredToTournamentsUpdated) == 0:
                menu.add_command(label="No Tournaments Available")
            else:
                for tournament in RegisteredToTournamentsUpdated:
                    menu.add_command(label=tournament, command=lambda value=tournament: SelectedTournament.set(value))

        # Create a main frame
        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        # Create a frame for the left side of the window and right side of the window
        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        LeftFrame.pack(side="left", fill="both", expand=True)

        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)

        ChooseATournamentLabel = tk.Label(LeftFrame, text="Choose a Tournament", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        ChooseATournamentLabel.pack(pady=20)

        RegisteredToTournaments = []
        SelectedTournament = tk.StringVar()
        SelectedTournament.set("Please Select")

        if len(RegisteredToTournaments) == 0:
            ChooseATournament = tk.OptionMenu(LeftFrame, SelectedTournament, "No Tournaments Available")
            ChooseATournament.config(width=20, height=1, font = MAIN_FONT)
            ChooseATournament.pack(pady=10)
        else:
            ChooseATournament = tk.OptionMenu(LeftFrame, SelectedTournament, *RegisteredToTournaments)
            ChooseATournament.config(width=20, height=1, font = MAIN_FONT)
            ChooseATournament.pack(pady=10)

        SearchForRegisteredTournaments = tk.Button(LeftFrame, text="Search", bg="#5D011E", fg="white", width=20, height=2, font=MAIN_FONT,
                                                    command = FindRegisteredTo)
        SearchForRegisteredTournaments.pack(pady=5)

        UnregisterButton = tk.Button(LeftFrame, text="Unregister", bg="#5D011E", fg="white", width=20, height=2, font=MAIN_FONT,
                                     command=lambda: UnregisterFromTournament(SelectedTournament.get()))
        UnregisterButton.pack(pady=5)

        fn.makeBackButton(LeftFrame, DashboardPage, controller)

class UpcomingTournamentsDetailsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")
            
        def SelectedTournamentDetails(TournamentName):
            if TournamentName == "Please Select":
                messagebox.showerror("Error", "Please select a tournament.")
                return

            # Let's start by finding the tournament ID of the selected tournament
            allTournaments = db.getAllRows(cursor, "tbl_Tournaments")
            for row in allTournaments:
                if row[1] == TournamentName:
                    TournamentID = row[0]

            # Now let's find the tournament details
            for row in allTournaments:
                if row[0] == TournamentID:
                    TournamentDate = row[2]
                    TournamentTime = row[3]
                    TournamentDescription = row[4]
                    MaxTeams = row[5]
                    NumGames = row[6]

                    # Let's now get rid of all current information on the right side frame
                    for widget in RightFrame.winfo_children():
                        widget.destroy()
            
            # Let's display the details on the right side frame now
            TournamentDetailsLabel = tk.Label(RightFrame, text="Tournament Details:", bg = "#5D011E", fg = "white", font=VERY_LARGE_FONT)
            TournamentDetailsLabel.pack(pady=30)            
            
            TournamentNameLabel = tk.Label(RightFrame, text="Tournament Name", bg = "#5D011E", fg = "white", font=LARGE_FONT_BOLD)
            TournamentNameLabel.pack(pady=5)
            TournamentNameDetailsLabel = tk.Label(RightFrame, text=TournamentName, bg = "#5D011E", fg = "white", font=LARGE_FONT)
            TournamentNameDetailsLabel.pack(pady=5)

            TournamentDateLabel = tk.Label(RightFrame, text="Tournament Date", bg = "#5D011E", fg = "white", font=LARGE_FONT_BOLD)
            TournamentDateLabel.pack(pady=5)
            TournamentDateDetailsLabel = tk.Label(RightFrame, text=TournamentDate, bg = "#5D011E", fg = "white", font=LARGE_FONT)
            TournamentDateDetailsLabel.pack(pady=10)

            TournamentTimeLabel = tk.Label(RightFrame, text="Tournament Time", bg = "#5D011E", fg = "white", font=LARGE_FONT_BOLD)
            TournamentTimeLabel.pack(pady=5)
            TournamentTimeDetailsLabel = tk.Label(RightFrame, text=TournamentTime, bg = "#5D011E", fg = "white", font=LARGE_FONT)
            TournamentTimeDetailsLabel.pack(pady=10)

            # In order to keep frame size appropriate we will need to split the description into a new line for every 8 words
            TournamentDescriptionLabel = tk.Label(RightFrame, text="Tournament Description", bg = "#5D011E", fg = "white", font=LARGE_FONT_BOLD)
            TournamentDescriptionLabel.pack(pady=5)
            TournamentDescription = TournamentDescription.split()
            if len(TournamentDescription) > 8:
                TournamentDescription = " ".join(TournamentDescription[:8]) + "\n" + " ".join(TournamentDescription[8:])
            
            TournamentDescriptionDetailsLabel = tk.Label(RightFrame, text=TournamentDescription, bg = "#5D011E", fg = "white", font=LARGE_FONT) 
            TournamentDescriptionDetailsLabel.pack(pady=10)
            
            MaxTeamsLabel = tk.Label(RightFrame, text="Max Teams", bg = "#5D011E", fg = "white", font=LARGE_FONT_BOLD)
            MaxTeamsLabel.pack(pady=5)
            MaxTeamsString = str(MaxTeams)
            MaxTeamsDetailsLabel = tk.Label(RightFrame, text=MaxTeamsString, bg = "#5D011E", fg = "white", font=LARGE_FONT)
            MaxTeamsDetailsLabel.pack(pady=10)

            NumGamesLabel = tk.Label(RightFrame, text="Number of Games", bg = "#5D011E", fg = "white", font=LARGE_FONT_BOLD)
            NumGamesLabel.pack(pady=5)
            NumGamesString = str(NumGames)
            NumGamesDetailsLabel = tk.Label(RightFrame, text=NumGamesString, bg = "#5D011E", fg = "white", font=LARGE_FONT)
            NumGamesDetailsLabel.pack(pady=10)
            
        # Create a whole frame
        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        # Create a frame for the left side of the window and right side of the window
        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        LeftFrame.pack(side="left", fill="both", expand=True)
        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)

        # Create a label for the tournament name and a dropdown menu to select the tournament
        TournamentNameLabel = tk.Label(LeftFrame, text="Upcoming Tournaments", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        TournamentNameLabel.pack(pady=30)

        # Lets find all the tournaments stored in the database
        CurrentTournaments = []
        allTournaments = db.getAllRows(cursor, "tbl_Tournaments")
        for row in allTournaments:
            CurrentTournaments.append(row[1])
        
        # Now let's create a variable to store the selected tournament
        SelectedTournament = tk.StringVar()
        SelectedTournament.set("Please Select")

        ChooseATournamentLabel = tk.Label(LeftFrame, text="Choose a Tournament", bg = "#E3E2DF", font=LARGE_FONT)
        ChooseATournamentLabel.pack(pady=5)

        # Let's create an option menu to choose from tournaments in the database.
        if len(CurrentTournaments) == 0:
            TournamentsAvailable = tk.OptionMenu(LeftFrame, SelectedTournament, "No Tournaments Available")
            TournamentsAvailable.config(width=20, height=1, font = MAIN_FONT)
            TournamentsAvailable.pack(pady=20)
        else:
            TournamentsAvailable = tk.OptionMenu(LeftFrame, SelectedTournament, *CurrentTournaments)
            TournamentsAvailable.config(width=20, height=1, font = MAIN_FONT)
            TournamentsAvailable.pack(pady=10)

        RefreshLabel = tk.Label(LeftFrame, text="Tournament List Refreshes itself every 3 seconds", bg = "#E3E2DF", font=MAIN_FONT)
        RefreshLabel.pack(pady=5)

        SeeTournamentDetailsButton = tk.Button(LeftFrame, text="See Details", bg="#5D011E", fg = "white", width=20, height=2, font = MAIN_FONT,
                                               command=lambda: SelectedTournamentDetails(SelectedTournament.get()))
        SeeTournamentDetailsButton.pack(pady=20)

        SeeRegisteredTeamsButton = tk.Button(LeftFrame, text="Show Teams", bg="#5D011E", fg = "white", width=20, height=2, font = MAIN_FONT,
                                             command=lambda: controller.show_frame(ShowTournamentTeamsPage))
        SeeRegisteredTeamsButton.pack(pady=5)

        fn.makeBackButton(LeftFrame, DashboardPage, controller)

        TournamentDetailsLabel = tk.Label(RightFrame, text="Tournament Details", bg = "#5D011E", fg = "white", font=VERY_LARGE_FONT)
        TournamentDetailsLabel.pack(pady=30)

        # Refresh the Tournaments list every 3 seconds
        fn.newCheckPastFuture(self, "future", TournamentsAvailable, SelectedTournament)

class ShowTournamentTeamsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")
        
        def ShowTeams(TournamentName):

            def clearSearch():
                tree.selection_remove(tree.selection())
                searchesFoundLabel.config(text="Searches Found: 0")

            def search(query):
                selections = []
                for child in tree.get_children():
                    for item in tree.item(child)["values"]:
                        if type(item) == str:
                            item = item.lower()
                            if query.lower() in item:
                                selections.append(child)
                                break
                
                # If there are multiple selections, we need to iterate through them
                if len(selections) > 1:
                    searchesFound = len(selections)
                    searchesFoundLabel.config(text="Searches Found: " + str(searchesFound))
                    for selection in selections:
                        tree.selection_add(selection)
                        
                elif len(selections) == 1:
                    tree.selection_set(selections)
                    searchesFoundLabel.config(text="Searches Found: 1")
                
                else:
                    messagebox.showerror("Error", "No item found with that name.")
                    tree.selection_remove(tree.selection())
                    searchesFoundLabel.config(text="Searches Found: 0")
                
            if TournamentName == "Please Select":
                messagebox.showerror("Error", "Please select a tournament.")
                return
            
            # Lets clear everything from the right frame
            for widget in RightFrame.winfo_children():
                widget.destroy()

            SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
            SpaceLabel.pack(pady=10)

            searchLabel = tk.Label(RightFrame, text="Search", fg="white", bg = "#5D011E", font=LARGE_FONT_BOLD)
            searchLabel.pack(pady=5)
            searchEntry = tk.Entry(RightFrame, width=40)
            searchEntry.pack(pady=5)

            searchesFound = 0
            searchesFoundLabel = tk.Label(RightFrame, text="Searches Found: " + str(searchesFound), fg="white", bg = "#5D011E", font=LARGE_FONT)
            searchesFoundLabel.pack(pady=5)

            searchBtn = tk.Button(RightFrame, text="Search", bg="#5D011E", fg = "white", width=20, height=2, font = MAIN_FONT,
                                command=lambda: search(searchEntry.get()))
            searchBtn.pack(pady=5)

            clearSearchBtn = tk.Button(RightFrame, text="Clear Search", bg="#5D011E", fg = "white", width=20, height=2, font = MAIN_FONT,
                                        command=lambda: clearSearch())
            clearSearchBtn.pack(pady=5)

            # Now lets create a treeview to display the teams in the tournament and their players
            SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
            SpaceLabel.pack(pady=50)
            tree = ttk.Treeview(RightFrame, show="headings")
            tree["columns"] = ("Team Name", "Team Captain", "Player 2", "Player 3", "Status")
            tree.heading("Team Name", text="Team Name")
            tree.heading("Team Captain", text="Team Captain")
            tree.heading("Player 2", text="Player 2")
            tree.heading("Player 3", text="Player 3")
            tree.heading("Status", text="Status")
            tree.pack()

            tournamentID = db.getTournamentID(cursor, TournamentName)
            tournamentID = tournamentID[0]

            allTeams = db.getAllRows(cursor, "tbl_Teams")
            teamList = []
            for row in allTeams:
                if row[7] == tournamentID:
                    teamList.append(row[1])
                    teamList.append(row[2])
                    teamList.append(row[3])
                    teamList.append(row[4])
                    teamList.append(row[6])
            
            for i in range(0, len(teamList), 5):
                tree.insert(parent="", index=0, values=(teamList[i], teamList[i+1], teamList[i+2], teamList[i+3], teamList[i+4]))
            
        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        LeftFrame.pack(side="left", fill="both", expand=True)

        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)

        MainLabel = tk.Label(LeftFrame, text="Show Tournament Teams", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabel.pack(pady=20)

        CurrentTournaments = []
        allTournaments = db.getAllRows(cursor, "tbl_Tournaments")
        for row in allTournaments:
            CurrentTournaments.append(row[1])

        SelectedTournament = tk.StringVar()
        SelectedTournament.set("Please Select")

        ChooseATournamentLabel = tk.Label(LeftFrame, text="Choose a Tournament", bg = "#E3E2DF", font=LARGE_FONT)
        ChooseATournamentLabel.pack(pady=5)

        if len(CurrentTournaments) == 0:
            ChooseATournamentDrop = tk.OptionMenu(LeftFrame, SelectedTournament, "No Tournaments Available")
            ChooseATournamentDrop.config(width=20, height=1, font = MAIN_FONT)
            ChooseATournamentDrop.pack(pady=10)
        else:
            ChooseATournamentDrop = tk.OptionMenu(LeftFrame, SelectedTournament, *CurrentTournaments)
            ChooseATournamentDrop.config(width=20, height=1, font = MAIN_FONT)
            ChooseATournamentDrop.pack(pady=10)
        
        ShowTeamsButton = tk.Button(LeftFrame, text="Show Teams", bg="#5D011E", fg = "white", width=20, height=2, font = MAIN_FONT,
                                    command=lambda: ShowTeams(SelectedTournament.get()))
        ShowTeamsButton.pack()

        fn.makeBackButton(LeftFrame, UpcomingTournamentsDetailsPage, controller)

class PreviousTournamentsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        def DisplayTournamentDetails(TournamentName):
            if TournamentName == "Please Select":
                messagebox.showerror("Error", "Please select a tournament.")
                return

            allTournaments = db.getAllRows(cursor, "tbl_Tournaments")
            for row in allTournaments:
                if row[1] == TournamentName:
                    TournamentID = row[0]

            for row in allTournaments:
                if row[0] == TournamentID:
                    TournamentDate = row[2]
                    TournamentTime = row[3]
                    TournamentDescription = row[4]
                    MaxTeams = row[5]
                    NumGames = row[6]

                    for widget in RightFrame.winfo_children():
                        widget.destroy()

            TournamentDetailsLabel = tk.Label(RightFrame, text="Tournament Details:", bg = "#5D011E", fg = "white", font=VERY_LARGE_FONT)
            TournamentDetailsLabel.pack(pady=30)            
            
            TournamentNameLabel = tk.Label(RightFrame, text="Tournament Name", bg = "#5D011E", fg = "white", font=LARGE_FONT_BOLD)
            TournamentNameLabel.pack(pady=5)
            TournamentNameDetailsLabel = tk.Label(RightFrame, text=TournamentName, bg = "#5D011E", fg = "white", font=LARGE_FONT)
            TournamentNameDetailsLabel.pack(pady=5)

            TournamentDateLabel = tk.Label(RightFrame, text="Tournament Date", bg = "#5D011E", fg = "white", font=LARGE_FONT_BOLD)
            TournamentDateLabel.pack(pady=5)
            TournamentDateDetailsLabel = tk.Label(RightFrame, text=TournamentDate, bg = "#5D011E", fg = "white", font=LARGE_FONT)
            TournamentDateDetailsLabel.pack(pady=10)

            TournamentTimeLabel = tk.Label(RightFrame, text="Tournament Time", bg = "#5D011E", fg = "white", font=LARGE_FONT_BOLD)
            TournamentTimeLabel.pack(pady=5)
            TournamentTimeDetailsLabel = tk.Label(RightFrame, text=TournamentTime, bg = "#5D011E", fg = "white", font=LARGE_FONT)
            TournamentTimeDetailsLabel.pack(pady=10)

            TournamentDescriptionLabel = tk.Label(RightFrame, text="Tournament Description", bg = "#5D011E", fg = "white", font=LARGE_FONT_BOLD)
            TournamentDescriptionLabel.pack(pady=5)
            TournamentDescription = TournamentDescription.split()
            if len(TournamentDescription) > 8:
                TournamentDescription = " ".join(TournamentDescription[:8]) + "\n" + " ".join(TournamentDescription[8:])
            
            TournamentDescriptionDetailsLabel = tk.Label(RightFrame, text=TournamentDescription, bg = "#5D011E", fg = "white", font=LARGE_FONT) 
            TournamentDescriptionDetailsLabel.pack(pady=10)

            MaxTeamsLabel = tk.Label(RightFrame, text="Max Teams", bg = "#5D011E", fg = "white", font=LARGE_FONT_BOLD)
            MaxTeamsLabel.pack(pady=5)
            MaxTeamsString = str(MaxTeams)
            MaxTeamsDetailsLabel = tk.Label(RightFrame, text=MaxTeamsString, bg = "#5D011E", fg = "white", font=LARGE_FONT)
            MaxTeamsDetailsLabel.pack(pady=10)

            NumGamesLabel = tk.Label(RightFrame, text="Number of Games", bg = "#5D011E", fg = "white", font=LARGE_FONT_BOLD)
            NumGamesLabel.pack(pady=5)
            NumGamesString = str(NumGames)
            NumGamesDetailsLabel = tk.Label(RightFrame, text=NumGamesString, bg = "#5D011E", fg = "white", font=LARGE_FONT)
            NumGamesDetailsLabel.pack(pady=10)

        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        LeftFrame.pack(side="left", fill="both", expand=True)

        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)

        MainLabel = tk.Label(LeftFrame, text="Previous Tournaments", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabel.pack(pady=20)

        PreviousTournaments = []
        SelectedTournament = tk.StringVar()
        SelectedTournament.set("Please Select")

        ChooseATournamentLabel = tk.Label(LeftFrame, text="Choose a Tournament", bg = "#E3E2DF", font=LARGE_FONT)
        ChooseATournamentLabel.pack(pady=5)
        
        if len(PreviousTournaments) == 0:
            ChooseATournamentDrop = tk.OptionMenu(LeftFrame, SelectedTournament, "No Tournaments Available")
            ChooseATournamentDrop.config(width=20, height=1, font = MAIN_FONT)
            ChooseATournamentDrop.pack(pady=10)
        else:
            ChooseATournamentDrop = tk.OptionMenu(LeftFrame, SelectedTournament, *PreviousTournaments)
            ChooseATournamentDrop.config(width=20, height=1, font = MAIN_FONT)
            ChooseATournamentDrop.pack(pady=10)

        LoadDetailsButton = tk.Button(LeftFrame, text="Load Details", bg="#5D011E", fg="white", width=20, height=2, font=MAIN_FONT,
                                      command=lambda: DisplayTournamentDetails(SelectedTournament.get()))
        LoadDetailsButton.pack(pady=5)

        AdvancedDetailsButton = tk.Button(LeftFrame, text="Advanced Details", bg="#5D011E", fg="white", width=20, height=2, font=MAIN_FONT,
                                          command=lambda: controller.show_frame(AdvancedDetailsPage))
        AdvancedDetailsButton.pack(pady=5)
        
        fn.makeBackButton(LeftFrame, DashboardPage, controller)
        fn.newCheckPastFuture(self, "past", ChooseATournamentDrop, SelectedTournament)

class AdvancedDetailsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        def ShowTeams(TournamentName):

            def clearSearch():
                tree.selection_remove(tree.selection())
                searchesFoundLabel.config(text="Searches Found: 0")

            def search(query):
                selections = []
                for child in tree.get_children():
                    for item in tree.item(child)["values"]:
                        item = str(item)
                        item = item.lower()
                        if query.lower() in item:
                            selections.append(child)
                            break
                        
                
                # If there are multiple selections, we need to iterate through them
                if len(selections) > 1:
                    searchesFound = len(selections)
                    searchesFoundLabel.config(text="Searches Found: " + str(searchesFound))
                    for selection in selections:
                        tree.selection_add(selection)
                        
                elif len(selections) == 1:
                    tree.selection_set(selections)
                    searchesFoundLabel.config(text="Searches Found: 1")
                
                else:
                    messagebox.showerror("Error", "No item found with that name.")
                    tree.selection_remove(tree.selection())
                    searchesFoundLabel.config(text="Searches Found: 0")
                
            if TournamentName == "Please Select":
                messagebox.showerror("Error", "Please select a tournament.")
                return
            
            # Lets clear everything from the right frame
            for widget in RightFrame.winfo_children():
                widget.destroy()

            SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
            SpaceLabel.pack(pady=10)

            searchLabel = tk.Label(RightFrame, text="Search", fg="white", bg = "#5D011E", font=LARGE_FONT_BOLD)
            searchLabel.pack(pady=5)
            searchEntry = tk.Entry(RightFrame, width=40)
            searchEntry.pack(pady=5)

            searchesFound = 0
            searchesFoundLabel = tk.Label(RightFrame, text="Searches Found: " + str(searchesFound), fg="white", bg = "#5D011E", font=LARGE_FONT)
            searchesFoundLabel.pack(pady=5)

            searchBtn = tk.Button(RightFrame, text="Search", bg="#5D011E", fg = "white", width=20, height=2, font = MAIN_FONT,
                                command=lambda: search(searchEntry.get()))
            searchBtn.pack(pady=5)

            clearSearchBtn = tk.Button(RightFrame, text="Clear Search", bg="#5D011E", fg = "white", width=20, height=2, font = MAIN_FONT,
                                        command=lambda: clearSearch())
            clearSearchBtn.pack(pady=5)

            readFile = pd.read_excel("Stats Files/StatsFile.xlsx")

            # Now lets create a treeview to display the teams in the tournament and their players
            SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
            SpaceLabel.pack(pady=50)
            tree = ttk.Treeview(RightFrame, show="headings")
            tree["columns"] = ("PlayerName", "TeamName", "DamageDone", "Placement", "Kills")
            tree.heading("PlayerName", text="PlayerName")
            tree.heading("TeamName", text="TeamName")
            tree.heading("DamageDone", text="DamageDone")
            tree.heading("Placement", text="Placement")
            tree.heading("Kills", text="Kills")
            tree.pack()

            for index, row in readFile.iterrows():
                tree.insert("", "end", values=(row["PlayerName"], row["TeamName"], row["DamageDone"], row["Placement"], row["Kills"]))

            leaderBoardBtn = tk.Button(RightFrame, text="Leaderboard", bg="#5D011E", fg = "white", width=20, height=2, font = MAIN_FONT,
                                        command=lambda: controller.show_frame(LeaderboardPage))
            leaderBoardBtn.pack(pady=15)
            
        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        LeftFrame.pack(side="left", fill="both", expand=True)

        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)

        MainLabel = tk.Label(LeftFrame, text="Show Tournament Teams", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabel.pack(pady=20)

        CurrentTournaments = []
        allTournaments = db.getAllRows(cursor, "tbl_Tournaments")
        for row in allTournaments:
            CurrentTournaments.append(row[1])

        SelectedTournament = tk.StringVar()
        SelectedTournament.set("Please Select")

        ChooseATournamentLabel = tk.Label(LeftFrame, text="Choose a Tournament", bg = "#E3E2DF", font=LARGE_FONT)
        ChooseATournamentLabel.pack(pady=5)

        ChooseATournamentDrop = tk.OptionMenu(LeftFrame, SelectedTournament, "Test Tournament")
        ChooseATournamentDrop.config(width=20, height=1, font = MAIN_FONT)
        ChooseATournamentDrop.pack(pady=10)
        
        ShowTeamsButton = tk.Button(LeftFrame, text="Show Teams", bg="#5D011E", fg = "white", width=20, height=2, font = MAIN_FONT,
                                    command=lambda: ShowTeams(SelectedTournament.get()))
        ShowTeamsButton.pack()

        fn.makeBackButton(LeftFrame, UpcomingTournamentsDetailsPage, controller)

class LeaderboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        def DisplayLeaderboard():

            def createGraph():
                fig, ax = plt.subplots()
                for index, row in readFile.iterrows():
                    teamName = row["TeamName"]
                    placement = row["Placement"]
                    kills = findTeamKills(teamName)
                    placement = int(placement)
                    kills = int(kills)
                    score = fn.calculateScoreSolo(placement, kills)
                    if teamName in teamsInTree:
                        ax.bar(teamName, score, label=teamName)
                    
                ax.set_xlabel("Teams (In Order of Placement)")
                ax.set_ylabel("Scores")
                ax.set_title("Team Scores")

                fig.set_size_inches(18.5, 10.5)
                plt.show()

            def findTeamKills(teamName):
                teamKills = 0
                for index, row in readFile.iterrows():
                    if row["TeamName"] == teamName:
                        teamKills += row["Kills"]
                return teamKills
            
            # Lets clear everything from the right frame
            for widget in RightFrame.winfo_children():
                widget.destroy()

            # Now lets create a treeview to display the teams in the tournament and their players
            SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
            SpaceLabel.pack(pady=50)
            tree = ttk.Treeview(RightFrame, show="headings")
            tree["columns"] = ("TeamName", "Placement", "Kills", "Score")
            tree.heading("TeamName", text="TeamName")
            tree.heading("Placement", text="Placement")
            tree.heading("Kills", text="Kills")
            tree.heading("Score", text="Score")
            tree.pack(pady=40)

            readFile = pd.read_excel("Stats Files/StatsFile.xlsx")

            # We now want to sort the data by placement, the team with the lowest placement will be at the top
            readFile = readFile.sort_values(by="Placement")
            
            teamsInTree = []
            for index, row in readFile.iterrows():
                teamName = row["TeamName"]
                placement = row["Placement"]
                kills = findTeamKills(teamName)
                placement = int(placement)
                kills = int(kills)
                score = fn.calculateScoreSolo(placement, kills)

                if teamName not in teamsInTree:
                    tree.insert("", "end", values=(teamName, placement, kills, score))
                    teamsInTree.append(teamName)
            
            graphButton = tk.Button(RightFrame, text="Graph", bg="#5D011E", fg = "white", width=20, height=2, font = MAIN_FONT,
                                    command=lambda: createGraph())
            graphButton.pack(pady=15)
                    
        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        LeftFrame.pack(side="left", fill="both", expand=True)

        RightFrame = tk.Frame(WholeFrame, bg="#5D011E")
        RightFrame.pack(side="right", fill="both", expand=True)

        MainLabel = tk.Label(LeftFrame, text="Leaderboard", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabel.pack(pady=20)

        DisplayLeaderboardButton = tk.Button(LeftFrame, text="Display Leaderboard", bg="#5D011E", fg = "white", width=20, height=2, font = MAIN_FONT,
                                            command=lambda: DisplayLeaderboard())
        DisplayLeaderboardButton.pack(pady=5)

        fn.makeBackButton(LeftFrame, DashboardPage, controller)

# Create an instance of the SamsTournamentsApp class and start the application
app = SamsTournamentsApp()
app.mainloop()