import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

MAIN_FONT = ("Arial", 12)
MAIN_FONT_BOLD = ("Arial bold", 12)
LARGE_FONT = ("Arial", 18)
VERY_LARGE_FONT = ("Arial bold", 25)
UNDERLINED_FONT = ("Arial underline", 8)

class SamsTournamentsApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Sam's Tournaments")
        tk.Tk.iconbitmap(self, default="MainLogo.ico")

        tk.Tk.geometry(self, "1920x1080")
        tk.Tk.minsize(self, 300, 175)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1) 
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Create instances of LoginPage and SignupPage
        for i in (LoginPage, SignupPage, ForgotPasswordPage, DashboardPage, ScoringCalculatorPage, FAQandRulesPage, CreateAnAdminPage):
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

        def show_and_hide():
            if PasswordEntry["show"] == "*":
                PasswordEntry["show"] = ""
            else:
                PasswordEntry["show"] = "*"

        def Login(Username, Password):
        # Checking if the user has entered a username and password
            if Username == "" or Password == "":
                messagebox.showerror("Error", "Please enter a username and password.")
            else:
                # Check if the user has entered the correct username and password
                with open("UserDetails.txt", "r") as file:
                    for line in file:
                        if Username in line:
                            if Password in line:
                                # Now check if the Remember Me button is ticked
                                if IsChecked.get() == 1:
                                    with open("RememberMe.txt", "w") as file2:
                                        file2.write(Username + " " + Password)
                                else:
                                    with open("RememberMe.txt", "w") as file2:
                                        file2.write("")
                                        UsernameEntry.delete(0, "end")
                                        PasswordEntry.delete(0, "end")

                                messagebox.showinfo("Login", "You have logged in successfully!")
                                controller.show_frame(DashboardPage)
                                controller.geometry("800x450")
                                break
                            else:
                                messagebox.showerror("Error", "Incorrect password.")
                                break
                    else:
                        messagebox.showerror("Error", "Incorrect username.")

        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg="#E3E2DF")

        # Create StringVars for User Entry

        Username = tk.StringVar()
        Password = tk.StringVar()
        IsChecked = tk.IntVar()

        # Check if there are any details in the Remember Me File, if not set the variables equal to them

        with open("RememberMe.txt", "r") as file:
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

        ShowPassword = tk.Checkbutton(LeftFrame, text="Show Password", bg = "#E3E2DF", command=lambda: show_and_hide())
        ShowPassword.pack()

        RememberMeButton = tk.Checkbutton(LeftFrame, text="Remember Me", bg = "#E3E2DF", variable = IsChecked)
        RememberMeButton.pack()

        LoginButton = tk.Button(LeftFrame, text="Log In", bg = "#5D011E",  fg = "white", width=20, height=2,
                                command=lambda: Login(Username.get(), Password.get()))
        LoginButton.pack(pady=20)

        # Start adding buttons to the right side 

        SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
        SpaceLabel.pack(pady=20)
        ContinueAsGuestButton = tk.Button(RightFrame, text="Continue as Guest", bg = "#E3E2DF", width=45, height=4, font = MAIN_FONT,
                                          command = lambda: controller.show_frame(DashboardPage))
        ContinueAsGuestButton.pack(pady=35)
        ForgotMyPasswordButton = tk.Button(RightFrame, text="Forgot my password", bg = "#9A1750", fg = "white", width=45, height=4, font = MAIN_FONT,
                                           command=lambda: self.ButtonCallBack(controller, ForgotPasswordPage))
        ForgotMyPasswordButton.pack(pady=35)
        GoToSignUpButton = tk.Button(RightFrame, text="Sign Up", bg = "#E3AFBC", font = MAIN_FONT, width=45, height=4,
                                     command=lambda: controller.show_frame(SignupPage))
        GoToSignUpButton.pack(pady=35)

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

        def ScoringButtonCallBack():
            controller.show_frame(ScoringCalculatorPage)
            controller.geometry("400x300")
        
        def AdminButtonCallBack():
            controller.show_frame(CreateAnAdminPage)
            controller.geometry("400x400")

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

        ScoringCalculatorButton = tk.Button(LeftFrame, text="Scoring Calculator", bg="#E3E2DF", width=45, height=4, font = MAIN_FONT, 
                                            command=lambda: ScoringButtonCallBack())
        ScoringCalculatorButton.pack(pady=35)

        CreateATournamentButton = tk.Button(LeftFrame, text="Create a Tournament", bg="#E3AFBC", width=45, height=4, font = MAIN_FONT)
        CreateATournamentButton.pack(pady=35)

        FAQandRulesButton = tk.Button(LeftFrame, text="FAQ & Rules", bg="#9A1750", fg = "white", width=45, height=4, font = MAIN_FONT,
                                      command = lambda: controller.show_frame(FAQandRulesPage))
        FAQandRulesButton.pack(pady=35)

        # Start adding buttons to the right side

        SpaceLabel = tk.Label(RightFrame, text="", bg = "#5D011E", font=MAIN_FONT)
        SpaceLabel.pack(pady=20)

        UpcomingTournamentsButton = tk.Button(RightFrame, text="Upcoming Tournaments", bg="#E3E2DF", width=45, height=4, font = MAIN_FONT)
        UpcomingTournamentsButton.pack(pady=35)

        CreateAnAdminButton = tk.Button(RightFrame, text="Create an Admin", bg="#E3AFBC", width=45, height=4, font = MAIN_FONT,
                                        command = lambda: AdminButtonCallBack())
        CreateAnAdminButton.pack(pady=35)

        PreviousTournamentsButton = tk.Button(RightFrame, text="Previous Tournaments", bg="#9A1750", fg = "white", width=45, height=4, font = MAIN_FONT)
        PreviousTournamentsButton.pack(pady=35)

        # Add a label to the middle frame

        MainLabelTop = tk.Label(MiddleFrame, text="Sam's", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabelTop.pack(pady=50)

        logo = ImageTk.PhotoImage(Image.open("Main_Logo.png"))
        LogoLabel = tk.Label(MiddleFrame, image=logo, bg="#E3E2DF")
        LogoLabel.image = logo
        LogoLabel.pack()

        MainLabelBottom = tk.Label(MiddleFrame, text="Tournaments", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabelBottom.pack(pady=50)

        BackButton = tk.Button(MiddleFrame, text="Logout", bg="#E3E2DF", width=20, height=2, font = MAIN_FONT, command=lambda: controller.show_frame(LoginPage))
        BackButton.pack(pady=20)

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

class FAQandRulesPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        def ButtonCallBack():
            controller.show_frame(DashboardPage)
            controller.geometry("800x450")
        
        # Create a main frame
        WholeFrame = tk.Frame(self, bg="#E3E2DF")
        WholeFrame.pack(fill="both", expand=True)

        #Create a frame for the left side of the window and right side of the window
        LeftFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        LeftFrame.pack(side="left", fill="both", expand=True)

        RightFrame = tk.Frame(WholeFrame, bg="#E3E2DF")
        RightFrame.pack(side="right", fill="both", expand=True)

        RulesLabel = tk.Label(LeftFrame, text="Rules", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        RulesLabel.pack(pady=20)

        FAQLabel = tk.Label(RightFrame, text="FAQ", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        FAQLabel.pack(pady=20)

        RulesWarning = tk.Label(LeftFrame, text="By violating any of the following rules the \n person or team responsible will be disqualified from \n the tournament and banned from future tournaments.", bg = "#E3E2DF", font=MAIN_FONT)
        Rules1 = tk.Label(LeftFrame, text="1. No teaming, communication or co-operation with other teams", bg = "#E3E2DF", font=MAIN_FONT)
        Rules2 = tk.Label(LeftFrame, text="2. No stream sniping", bg = "#E3E2DF", font=MAIN_FONT)
        Rules3 = tk.Label(LeftFrame, text="3. No hacking or cheating", bg = "#E3E2DF", font=MAIN_FONT)
        Rules4 = tk.Label(LeftFrame, text="4. No offensive language or behaviour", bg = "#E3E2DF", font=MAIN_FONT)
        Rules5 = tk.Label(LeftFrame, text="5. Do not disobey admins", bg = "#E3E2DF", font=MAIN_FONT)
        Rules6 = tk.Label(LeftFrame, text="6. No teaming with banned players", bg = "#E3E2DF", font=MAIN_FONT)
        RulesWarning.pack(pady=5)
        Rules1.pack(pady=5)
        Rules2.pack(pady=5)
        Rules3.pack(pady=5)
        Rules4.pack(pady=5)
        Rules5.pack(pady=5)
        Rules6.pack(pady=5)

        FAQ1 = tk.Label(RightFrame, text="I am falsely banned, how do I appeal?", bg = "#E3E2DF", font=MAIN_FONT_BOLD)
        FAQ1Answer = tk.Label(RightFrame, text="Please contact an admin on Discord.", bg = "#E3E2DF", font=MAIN_FONT)
        FAQ2 = tk.Label(RightFrame, text="How do I join a tournament?", bg = "#E3E2DF", font=MAIN_FONT_BOLD)
        FAQ2Answer = tk.Label(RightFrame, text="Go to the dashboard and click on \n the tournament you wish to join.", bg = "#E3E2DF", font=MAIN_FONT)
        FAQ3 = tk.Label(RightFrame, text="How do I apply to become an admin?", bg = "#E3E2DF", font=MAIN_FONT_BOLD)
        FAQ3Answer = tk.Label(RightFrame, text="Applications are closed as of now. When they open \n information will be available on our discord", bg = "#E3E2DF", font=MAIN_FONT)
        FAQ1.pack(pady=5)
        FAQ1Answer.pack(pady=5)
        FAQ2.pack(pady=5)
        FAQ2Answer.pack(pady=5)
        FAQ3.pack(pady=5)
        FAQ3Answer.pack(pady=5)

        Summary = tk.Label(self, text="If you have any further questions please contact an admin on Discord.", bg = "#E3E2DF", font=MAIN_FONT)
        Summary.pack()

        BackButton = tk.Button(self, text="Back", bg="#E3E2DF", width=8, height=1, command=lambda: ButtonCallBack())
        BackButton.pack(pady=5)

class CreateAnAdminPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg="#E3E2DF")

        def BackToDashboard():
            controller.show_frame(DashboardPage)
            controller.geometry("800x450")

        def CreateAdmin(AdminEmail, AdminUsername, AdminPassword, AdminPasswordConfirm):

            def SignupConfirmation():
                with open("UserDetails.txt", "a") as f:
                    f.write("\n" + AdminEmail + " " + AdminUsername + " " + AdminPassword + " Admin")
                    messagebox.showinfo("Sign Up", "You have signed up successfully!")

                AdminEmailEntry.delete(0, "end")
                AdminUsernameEntry.delete(0, "end")
                AdminPasswordEntry.delete(0, "end")
                AdminPasswordConfirmEntry.delete(0, "end")
        
            validEmail = False
            validUsername = False
            validPassword = False
            validPasswordConfirm = False

            # Start by checking if the email is valid (it must contain an @ symbol and a .)
            if "@" in AdminEmail and "." in AdminEmail:
                validEmail = True
            else:
                validEmail = False

            # Now we need to check if the username is valid (it must be at least 6 characters long and no longer than 15 characters) it also cannot include symbols or spaces
            if len(AdminUsername) >= 6 and len(AdminUsername) <= 15:
                validUsername = True

                if any(i.isspace() for i in AdminUsername):
                    validUsername = False
                else:
                    validUsername = True
            else:
                validUsername = False

            # Now we need to check if the password is valid (must be 8 characters and contain one capital letter and one number and no longer than 18 characters) it also cannot contain spaces
            if len(AdminPassword) >= 8 and len(AdminPassword) <= 18:
                validPassword = True
                
                if any(i.isdigit() for i in AdminPassword):
                    validPassword = True

                    if any(i.isupper() for i in AdminPassword):
                        validPassword = True

                        if any(i.isspace() for i in AdminPassword):
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
            if AdminPassword == AdminPasswordConfirm:
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
            else:
                SignupConfirmation()
        
        AdminEmail = tk.StringVar()
        AdminUsername = tk.StringVar()
        AdminPassword = tk.StringVar()
        AdminPasswordConfirm = tk.StringVar()

        MainLabel = tk.Label(self, text="Create an Admin", bg = "#E3E2DF", font=VERY_LARGE_FONT)
        MainLabel.pack(pady=20)

        AdminEmailLabel = tk.Label(self, text="Email", bg = "#E3E2DF", font=MAIN_FONT)
        AdminEmailLabel.pack(padx=10)
        AdminEmailEntry = tk.Entry(self, width=30, textvariable=AdminEmail)
        AdminEmailEntry.pack(padx=10, pady=10)

        AdminUsernameLabel = tk.Label(self, text="Username", bg = "#E3E2DF", font=MAIN_FONT)
        AdminUsernameLabel.pack(padx=10)
        AdminUsernameEntry = tk.Entry(self, width=30, textvariable=AdminUsername)
        AdminUsernameEntry.pack(padx=10, pady=10)

        AdminPasswordLabel = tk.Label(self, text="Password", bg = "#E3E2DF", font=MAIN_FONT)
        AdminPasswordLabel.pack(padx=10)
        AdminPasswordEntry = tk.Entry(self, width=30, textvariable=AdminPassword, show="*")
        AdminPasswordEntry.pack(padx=10, pady=10)

        AdminPasswordConfirmLabel = tk.Label(self, text="Confirm Password", bg = "#E3E2DF", font=MAIN_FONT)
        AdminPasswordConfirmLabel.pack(padx=10)
        AdminPasswordConfirmEntry = tk.Entry(self, width=30, textvariable=AdminPasswordConfirm, show="*")
        AdminPasswordConfirmEntry.pack(padx=10, pady=10)

        CreateAdminButton = tk.Button(self, text="Create Admin", bg="#E3E2DF", width=10, height=1,
                                      command = lambda: CreateAdmin(AdminEmail.get(), AdminUsername.get(), AdminPassword.get(), AdminPasswordConfirm.get()))
        CreateAdminButton.pack(pady=5)
        BackButton = tk.Button(self, text="Back", bg="#E3E2DF", width=10, height=1, command=BackToDashboard)
        BackButton.pack(pady=5)
    

# Create an instance of the SamsTournamentsApp class and start the application
app = SamsTournamentsApp()
app.mainloop()