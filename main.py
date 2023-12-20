import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

MAIN_FONT = ("Arial", 12)
VERY_LARGE_FONT = ("Arial bold", 18)
UNDERLINED_FONT = ("Arial underline", 8)

class SamsTournamentsApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Sam's Tournaments")
        tk.Tk.iconbitmap(self, default="MainLogo.ico")

        tk.Tk.geometry(self, "800x550")
        tk.Tk.minsize(self, 300, 175)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1) 
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Create instances of LoginPage and SignupPage
        for i in (LoginPage, SignupPage, ForgotPasswordPage, DashboardPage, ScoringCalculatorPage):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the LoginPage by default
        self.show_frame(LoginPage)

    def show_frame(self, cont):
        # Raise the specified frame to the top
        frame = self.frames[cont]
        frame.tkraise()

def LoginConfirmation():
    messagebox.showinfo("Login", "You have logged in successfully!")

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg="#E3E2DF")

        # Create StringVars for User Entry

        Username = tk.StringVar()
        Password = tk.StringVar()

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
        SpaceLabel.pack(pady=30)

        UsernameLabel = tk.Label(LeftFrame, text="Username", bg = "#E3E2DF", font=MAIN_FONT)
        UsernameLabel.pack(padx=10)
        UsernameEntry = tk.Entry(LeftFrame, width=30, textvariable = Username)
        UsernameEntry.pack(padx=10, pady=10)

        PasswordLabel = tk.Label(LeftFrame, text="Password", bg = "#E3E2DF", font=MAIN_FONT)
        PasswordLabel.pack(padx=10, pady=10)
        PasswordEntry = tk.Entry(LeftFrame, width=30, textvariable = Password)   
        PasswordEntry.pack(padx=10, pady=10)

        # Button to switch to the SignupPage
        LoginButton = tk.Button(LeftFrame, text="Log In", bg = "#5D011E",  fg = "white", width=15, height=2,
                                command=lambda: LoginConfirmation())
        LoginButton.pack(pady=10)

        # Start adding buttons to the right side 

        SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
        SpaceLabel.pack(pady=20)
        ContinueAsGuestButton = tk.Button(RightFrame, text="Continue as Guest", bg = "#E3E2DF", width=20, height=2, font = MAIN_FONT,
                                          command = lambda: controller.show_frame(DashboardPage))
        ContinueAsGuestButton.pack(pady=20)
        ForgotMyPasswordButton = tk.Button(RightFrame, text="Forgot my password", bg = "#9A1750", fg = "white", width=20, height=2, font = MAIN_FONT,
                                           command=lambda: self.ButtonCallBack(controller, ForgotPasswordPage))
        ForgotMyPasswordButton.pack(pady=20)
        GoToSignUpButton = tk.Button(RightFrame, text="Sign Up", bg = "#E3AFBC", font = MAIN_FONT, width=20, height=2,
                                     command=lambda: controller.show_frame(SignupPage))
        GoToSignUpButton.pack(pady=20)

    # Creating an intermediary function to do two things at once on one button press

    def ButtonCallBack(self, parent, ForgotPasswordPage):
        parent.show_frame(ForgotPasswordPage)
        parent.geometry("300x175")

class SignupPage(tk.Frame):

    def __init__(self, parent, controller):

        def show_and_hide():
            if PasswordEntry["show"] == "*":
                PasswordEntry["show"] = ""
            else:
                PasswordEntry["show"] = "*"
            
            if PasswordConfirmEntry["show"] == "*":
                PasswordConfirmEntry["show"] = ""
            else:
                PasswordConfirmEntry["show"] = "*"

        def DetailsValidation():

            validEmail = False
            validUsername = False
            validPassword = False
            validPasswordConfirm = False
            over16 = False
            genderGiven = False

            def SignupConfirmation():
                with open("UserDetails.txt", "a") as f:
                    f.write("\n" + Email.get() + " " + Username.get() + " " + GenderVar.get() + " " + Password.get() + " " + PasswordConfirm.get())
                    messagebox.showinfo("Sign Up", "You have signed up successfully!")

                EmailEntry.delete(0, "end")
                UsernameEntry.delete(0, "end")
                GenderVar.set("Please Select")
                PasswordEntry.delete(0, "end")
                PasswordConfirmEntry.delete(0, "end")
        
            # Start by checking if the email is valid (it must contain an @ symbol and a .) and cannot contain spaces
            if "@" in Email.get() and "." in Email.get():
                validEmail = True

                if any(i.isspace() for i in Email.get()):
                    validEmail = False
                else:
                    validEmail = True
            else:
                validEmail = False

            # Now we need to check if the username is valid (it must be at least 6 characters long and no longer than 15 characters) it also cannot include symbols or spaces
            if len(Username.get()) >= 6 and len(Username.get()) <= 15:
                validUsername = True

                if any(i.isalpha() for i in Username.get()):
                    validUsername = True

                    if any(i.isspace() for i in Username.get()):
                        validUsername = False
                    else:
                        validUsername = True
                else:
                    validUsername = False
            else:
                validUsername = False

            # Now we need to check if the password is valid (must be 8 characters and contain one capital letter and one number and no longer than 18 characters) it also cannot contain spaces
            if len(Password.get()) >= 8 and len(Password.get()) <= 18:
                validPassword = True
                
                if any(i.isdigit() for i in Password.get()):
                    validPassword = True

                    if any(i.isupper() for i in Password.get()):
                        validPassword = True

                        if any(i.isspace() for i in Password.get()):
                            validPassword = False
                        else: 
                            validPassword = True
                    else:
                        validPassword = False
                else:
                    validPassword = False    
            else:
                validPassword = False
            
            # Now we need to check if the password confirmation is valid (must be the same as the password)
            if Password.get() == PasswordConfirm.get():
                validPasswordConfirm = True
            else:
                validPasswordConfirm = False

            if validEmail == False:
                messagebox.showerror("Error", "Please enter a valid email address.")
            elif validUsername == False:
                messagebox.showerror("Error", "Please enter a valid username.")
            elif validPassword == False:
                messagebox.showerror("Error", "Please enter a valid password.")
            elif validPasswordConfirm == False:
                messagebox.showerror("Error", "Please make sure your passwords match.")

            # Now we need to check if the user has selected a gender

            if GenderVar.get() == "Please Select":
                messagebox.showerror("Error", "Please select a Gender.")
                genderGiven = False
            else:
                genderGiven = True

            # Now we need to check if the user has checked the over 16 box

            if IsOver16.get() == 1:
                over16 = True
            else:
                over16 = False
                messagebox.showerror("Error", "Please confirm you are over the age of 16.")

            if validEmail == True and validUsername == True and genderGiven == True and validPassword == True and validPasswordConfirm == True and over16 == True:
                SignupConfirmation()

        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        # Create StringVars for User Entry

        Email = tk.StringVar()
        Username = tk.StringVar()
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

        EmailLabel = tk.Label(LeftFrame, text = "Email", bg="#E3E2DF", font=MAIN_FONT)
        EmailLabel.pack(padx=10)
        EmailEntry = tk.Entry(LeftFrame, width=30, textvariable = Email)
        EmailEntry.pack(padx=10, pady=10)

        UsernameLabel = tk.Label(LeftFrame, text="Username", bg = "#E3E2DF", font=MAIN_FONT)
        UsernameLabel.pack(padx=10)
        UsernameEntry = tk.Entry(LeftFrame, width=30, textvariable = Username)
        UsernameEntry.pack(padx=10, pady=10)

        # Create values to be used in the drop down menu

        Gender = ["Male", "Female"]
        GenderVar = tk.StringVar()
        GenderVar.set("Please Select")

        GenderLabel = tk.Label(LeftFrame, text="Gender", bg = "#E3E2DF", font=MAIN_FONT)
        GenderLabel.pack(padx=10)
        GenderEntry = tk.OptionMenu(LeftFrame, GenderVar, *Gender)
        GenderEntry.pack(padx=10, pady=10)

        PasswordLabel = tk.Label(LeftFrame, text="Password", bg = "#E3E2DF", font=MAIN_FONT)
        PasswordLabel.pack(padx=10)
        PasswordEntry = tk.Entry(LeftFrame, width=30, textvariable = Password, show = "*")
        PasswordEntry.pack(padx=10, pady=10)

        PasswordConfirmLabel = tk.Label(LeftFrame, text="Confirm Password", bg = "#E3E2DF", font=MAIN_FONT)
        PasswordConfirmLabel.pack(padx=10)
        PasswordConfirmEntry = tk.Entry(LeftFrame, width=30, textvariable = PasswordConfirm, show = "*")
        PasswordConfirmEntry.pack(padx=10, pady=10)

        # Lets add two checkboxes, one to show password and another to confirm the user is over the age of 16

        ShowPassword = tk.Checkbutton(LeftFrame, text="Show Password", bg = "#E3E2DF", command=lambda: show_and_hide())
        ShowPassword.pack()

        IsOver16 = tk.IntVar()

        AgeConfirmation = tk.Checkbutton(LeftFrame, text="I confirm I am over the age of 16", background="#E3E2DF", variable = IsOver16)
        AgeConfirmation.pack(pady=5)

        # Button to switch to the LoginPage
        SignUpButton = tk.Button(LeftFrame, text="Sign Up", bg = "#5D011E",  fg = "white", width=15, height=2,
                    command=lambda: DetailsValidation())
        SignUpButton.pack(pady=10)

        # Start adding buttons to the right side
        SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
        SpaceLabel.pack(pady=20)

        ContinueAsGuestButton = tk.Button(RightFrame, text="Continue as Guest", bg = "#E3E2DF", width=20, height=2, font = MAIN_FONT,
                                          command = lambda: controller.show_frame(DashboardPage))
        ContinueAsGuestButton.pack(pady=20)
        GoToLoginButton = tk.Button(RightFrame, text="Login", bg="#E3AFBC", font = MAIN_FONT, width=20, height=2, command=lambda: controller.show_frame(LoginPage))
        GoToLoginButton.pack(pady=20)

class ForgotPasswordPage(tk.Frame):

    def __init__(self, parent, controller):

        def SendRecoveryEmail():
            messagebox.showinfo("Recovery Email", "An email has been sent to the address provided.")
            RecoveryEmailEntry.delete(0, "end")

        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        RecoveryEmail = tk.StringVar()

        Label1 = tk.Label(self, text="Please enter the email of the \n account you are trying to recover", bg="#E3E2DF", font=MAIN_FONT)
        Label1.pack(pady=5)
        RecoveryEmailEntry = tk.Entry(self, width=40, textvariable=RecoveryEmail)
        RecoveryEmailEntry.pack(pady=5)

        SendRecoveryEmailButton = tk.Button(self, text="Save", bg="#E3E2DF", width=8, height=1, command = SendRecoveryEmail)
        SendRecoveryEmailButton.pack(pady=5)

        BackButton = tk.Button(self, text="Back", bg="#E3E2DF", width=8, height=1, command=lambda: self.ButtonCallBack(controller, LoginPage))
        BackButton.pack(pady=5)
        
    def ButtonCallBack(self, parent, LoginPage):
        parent.show_frame(LoginPage)
        parent.geometry("800x450")

class DashboardPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        def ButtonCallBack():
            controller.show_frame(ScoringCalculatorPage)
            controller.geometry("400x300")

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

        SpaceLabel = tk.Label(LeftFrame, text="", bg = "#5D011E", font=MAIN_FONT)
        SpaceLabel.pack(pady=20)

        ScoringCalculatorButton = tk.Button(LeftFrame, text="Scoring Calculator", bg="#E3E2DF", width=20, height=2, font = MAIN_FONT, command=lambda: ButtonCallBack())
        ScoringCalculatorButton.pack(pady=20)

        CreateATournamentButton = tk.Button(LeftFrame, text="Create a Tournament", bg="#E3AFBC", width=20, height=2, font = MAIN_FONT)
        CreateATournamentButton.pack(pady=20)

        FAQandRulesButton = tk.Button(LeftFrame, text="FAQ & Rules", bg="#9A1750", fg = "white", width=20, height=2, font = MAIN_FONT)
        FAQandRulesButton.pack(pady=20)

        BackButton = tk.Button(LeftFrame, text="Logout", bg="#E3E2DF", width=20, height=2, font = MAIN_FONT, command=lambda: controller.show_frame(LoginPage))
        BackButton.pack(pady=20)

        # Start adding buttons to the right side

        SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
        SpaceLabel.pack(pady=20)

        UpcomingTournamentsButton = tk.Button(RightFrame, text="Upcoming Tournaments", bg="#E3E2DF", width=20, height=2, font = MAIN_FONT)
        UpcomingTournamentsButton.pack(pady=20)

        CreateAnAdminButton = tk.Button(RightFrame, text="Create an Admin", bg="#E3AFBC", width=20, height=2, font = MAIN_FONT)
        CreateAnAdminButton.pack(pady=20)

        PreviousTournamentsButton = tk.Button(RightFrame, text="Previous Tournaments", bg="#9A1750", fg = "white", width=20, height=2, font = MAIN_FONT)
        PreviousTournamentsButton.pack(pady=20)

        # Add a label to the middle frame

        MainLabelTop = tk.Label(MiddleFrame, text="Sam's", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabelTop.pack(pady=20)

        logo = ImageTk.PhotoImage(Image.open("Main_Logo.png"))
        LogoLabel = tk.Label(MiddleFrame, image=logo, bg="#E3E2DF")
        LogoLabel.image = logo
        LogoLabel.pack()

        MainLabelBottom = tk.Label(MiddleFrame, text="Tournaments", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabelBottom.pack()

class ScoringCalculatorPage(tk.Frame):

    def ButtonCallBack(self, parent, DashboardPage):
        parent.show_frame(DashboardPage)
        parent.geometry("800x450")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        def CalculateScore():
            # Start by defining what placements give what scores
            OverallScore = 0
            validPlacement = False
            validKills = False

            try:
                placement = int(TeamPlacement.get())
                if placement == 1:
                    OverallScore += 12
                    validPlacement = True
                elif placement == 2:
                    OverallScore += 9
                    validPlacement = True
                elif placement == 3:
                    OverallScore += 7
                    validPlacement = True
                elif placement == 4:
                    OverallScore += 5
                    validPlacement = True
                elif placement == 5:
                    OverallScore += 4
                    validPlacement = True
                elif placement >= 6 and placement <= 10:
                    OverallScore += 2
                    validPlacement = True
                elif placement >= 11 and placement <= 15:
                    OverallScore += 1
                    validPlacement = True
                elif placement >= 16 and placement <= 20:
                    OverallScore += 0
                    validPlacement = True
                else:
                    messagebox.showerror("Error", "Please enter a valid team placement.")
                    validPlacement = False
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid team placement.")

            try:
                kills = int(TeamKills.get())
                if kills >= 0:
                    validKills = True
                else:
                    messagebox.showerror("Error", "Please enter a valid number of team kills.")
                    validKills = False
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of team kills.")

            if validPlacement and validKills:
                OverallScore += kills
                messagebox.showinfo("Score", "Your team scored " + str(OverallScore) + " points!")

            TeamPlacementEntry.delete(0, "end")
            TeamKillsEntry.delete(0, "end")

        # Create StringVars for User Entry

        TeamPlacement = tk.StringVar()
        TeamKills = tk.StringVar()

        MainLabel = tk.Label(self, text="Scoring Calculator", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabel.pack(pady=20)

        TeamPlacementLabel = tk.Label(self, text="Team Placement", bg = "#E3E2DF", font=MAIN_FONT)
        TeamPlacementLabel.pack(pady=10)
        TeamPlacementEntry = tk.Entry(self, width=10, textvariable=TeamPlacement)
        TeamPlacementEntry.pack()

        TeamKillsLabel = tk.Label(self, text="Team Kills", bg = "#E3E2DF", font=MAIN_FONT)
        TeamKillsLabel.pack(pady=10)
        TeamKillsEntry = tk.Entry(self, width=10, textvariable=TeamKills)
        TeamKillsEntry.pack(pady=5)

        CalculateTotalScore = tk.Button(self, text="Save", bg="#E3E2DF", width=8, height=1, command = lambda: CalculateScore())
        CalculateTotalScore.pack(pady=5)

        BackButton = tk.Button(self, text="Back", bg="#E3E2DF", width=8, height=1, command=lambda: self.ButtonCallBack(controller, DashboardPage))
        BackButton.pack(pady=5)

# Create an instance of the SamsTournamentsApp class and start the application
app = SamsTournamentsApp()
app.mainloop()