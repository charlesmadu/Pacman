from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3

connection = sqlite3.connect("/Users/charles/Documents/Python Projects/Pacman/database.db")
# CONNECT TO PLAYERS DATABASE

cursor = connection.cursor()
# CREATE CURSOR TO RUN SQL QUERIES

cursor.execute(
    'CREATE TABLE IF NOT EXISTS user(user_id integer PRIMARY KEY AUTOINCREMENT, username MESSAGE_TEXT NOT NULL, password MESSAGE_TEXT NOT NULL, highscore integer NOT NULL)')
# CREATE THE USER TABLE WITH THE VARIABLES IF IT DOES NOT ALREADY EXIST

connection.commit()
# CLOSE THE CONNECTION

cursor.close()


# CLOSE THE CURSOR


class Login:
    def __init__(self, screen):
        self.screen = screen
        self.register_screen = None
        self.register_username_text = None
        self.register_password_text = None
        self.screen.title("Pacman Login System")
        self.icon = PhotoImage(file="/images/pacman_image.png")
        self.logged_in = False
        self.username = None
        self.password = None
        register_image = Image.open("/images/register_background.jpg")
        register_resized_image = register_image.resize((400, 500), Image.ANTIALIAS)
        self.register_background_image = ImageTk.PhotoImage(register_resized_image)
        # REGISTER BACKGROUND

        self.image = Image.open("/images/log_in_screen.jpg")
        self.resize_image = self.image.resize((600, 400), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(self.resize_image)
        # MAIN SCREEN BACKGROUND

        self.screen.iconphoto(False, self.icon)
        self.screen.geometry("600x300")
        self.screen.resizable(False, False)
        # Screen Variables

        Label(self.screen, image=self.background_image).place(x=0, y=0, relwidth=1, relheight=1)
        # BACKGROUND

        login_frame = Frame(self.screen, bg="white")
        login_frame.place(x=10, y=60, height="200", width="240")
        # CREATE A WHITE SQUARE ON THE BACKGROUND

        Label(login_frame, text="Login Here", font=("Fixedsys", 20, "bold"), bg="white", fg="#008AC9").place(x=36, y=10)
        Label(login_frame, text="Player Login", font=("Terminal", 7), bg="white", fg="#008AC9").place(x=75, y=40)
        # TITLES AND HEADINGS

        Label(login_frame, text="Username", font=("Fixedsys", 11, "bold"), bg="white", fg="gray").place(x=78, y=70)
        self.username_text = Entry(login_frame, font=("Fixedsys", 11), bg="lightgray")
        self.username_text.place(x=45, y=90, height=20, width=150)
        # USERNAME LABEL AND ENTERING

        Label(login_frame, text="Password", font=("Fixedsys", 11, "bold"), bg="white", fg="gray").place(x=78, y=120)
        self.password_text = Entry(login_frame, font=("Fixedsys", 11), bg="lightgray")
        self.password_text.place(x=45, y=140, height=20, width=150)
        # PASSWORD LABEL AND ENTERING

        Button(login_frame, text="LOGIN", bg="white", fg="#008AC9", font=("Fixedsys", 15, "bold"),
               command=self.login).place(x=85, y=170)
        # LOGIN BUTTON

        Button(login_frame, text="New User?", bg="white", fg="gray", bd=0, font=("Fixedsys", 10),
               command=self.register).place(x=160, y=180)
        # REGISTER BUTTON

    def login(self):

        ##### login #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Checks if the user meets the requirements to be logged into the game against the game database
        ##########################

        # FUNCTION IF THE PLAYER CLICKS THE LOGIN BUTTON

        if self.username_text.get() == "" or self.password_text.get() == "":
            # IF THE PLAYER HAS NOT TYPED ANYTHING INTO EITHER THE USERNAME OR PASSWORD SECTION

            messagebox.showerror("Error", "All fields must be filled", parent=self.screen)
            # SEND AN ERROR TO THE USERS SCREEN

        else:
            # IF THE USER HAS ENTERED DATA INTO BOTH SECTIONS

            database = sqlite3.connect("database/players.db")
            # CONNECT TO PLAYERS DATABASE

            cursor_log = database.cursor()
            # CREATE CURSOR FOR LOGIN

            username_search = 'SELECT password FROM user WHERE username = ?'
            # SQL QUERY TO GET THE PLAYER PASSWORD

            cursor_log.execute(username_search, [(self.username_text.get())])
            # SEARCH FOR THE PLAYERS PASSWORD

            password = cursor_log.fetchall()
            # ASSIGN ALL THE VALUES THAT ARE RECEIVED TO PASSWORD VARIABLE

            if password:
                # IF THE PLAYERS USERNAME IS IN THE DATABASE

                if (password[0][0]) == self.password_text.get():
                    # IF THE PASSWORD IS THE SAME AS IN THE SYSTEM

                    self.username = self.username_text.get()
                    self.password = self.password_text.get()
                    self.logged_in = True
                    self.screen.destroy()
                    # LOG PLAYER IN AND CLOSE THE SCREEN

                else:
                    # INCORRECT PASSWORD

                    messagebox.showerror("Error", "Incorrect Password", parent=self.screen)
                    # SEND INCORRECT PASSWORD ERROR TO HE PLAYERS SCREEN

            else:
                # THE PLAYERS USERNAME CAN NOT BE FOUND

                messagebox.showerror("Error", "No User With That Username Could Be Found", parent=self.screen)
                # SEND AN ERROR TO THE PLAYERS SCREEN

            database.commit()
            # CLOSE THE DATABASE

            cursor_log.close()
            # CLOSE THE CURSOR

    def register_account(self):

        ##### register_account #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Registers a new user if their account meets requirements and saves their data to a database
        ##########################

        # FUNCTION CALLED ONCE THE PLAYER ATTEMPTS TO CREATE A NEW ACCOUNT

        if self.register_username_text.get() == "" or self.register_password_text.get() == "":
            # IF THE PLAYER HAS NOT TYPED ANYTHING IN EITHER THE USERNAME OR PASSWORD SECTION

            messagebox.showerror("Error", "All fields must be filled", parent=self.screen)
            # SEND AN ERROR TO THEIR SCREEN

        elif len(self.register_username_text.get()) < 3 or len(self.register_username_text.get()) > 15:
            # IF THEIR USERNAME IS LESS THAN 3 OR MORE THAN 15 CHARACTERS

            messagebox.showerror("Error", "Username must be between 3 and 15 characters long", parent=self.screen)
            # SEND AN ERROR TO THE USER

        elif len(self.register_password_text.get()) < 4:
            # IF THEIR PASSWORD IS LESS THAN 4 CHARACTERS

            messagebox.showerror("Error", "Password must be greater than 3 characters", parent=self.screen)
            # SEND AN ERROR TO THE USERS SCREEN

        else:
            # IF THE USERNAME AND PASSWORD MEET THE REQUIREMENTS

            database = sqlite3.connect("database/players.db")
            # OPEN THE DATABASE

            cursor_reg = database.cursor()
            # OPEN THE CURSOR

            username_search = 'SELECT username FROM user WHERE username = ?'
            # SQL QUERY TO SEARCH IF THE USERNAME IS ALREADY TAKEN

            cursor_reg.execute(username_search, [(self.register_username_text.get())])
            # EXECUTE SQL QUERY

            if cursor_reg.fetchall():
                # IF THE QUERY RETURNS ANY VALUE

                messagebox.showerror("Error", "That Username Has Already Been Taken")
                # SEND AN ERROR TO THE USER

            else:
                # OTHERWISE THE USERNAME IS NEW

                insert_data = 'INSERT INTO user(username, password, highscore) VALUES(?, ?, ?)'
                # SQL QUERY TO ENTER THE PLAYER DETAILS INTO THE DATABASE

                cursor_reg.execute(insert_data,
                                   [(self.register_username_text.get()), (self.register_password_text.get()), 0])
                # EXECUTE THE SQL QUERY

                messagebox.showinfo("Successful Event", "Account Created Successfully")
                # SEND AN INFO BOX TO THE USER TO SHOW THEIR ACCOUNT WAS CREATED SUCCESSFULLY

                self.register_screen.destroy()
                # CLOSE THE SCREEN

            database.commit()
            # CLOSE THE DATABASE

            cursor_reg.close()
            # CLOSE THE CURSOR

    def register(self):

        ##### register #######
        # Parameters : None
        # Return Type : None
        # Purpose :- A new register window and allows the user to enter the username and password they want for the account
        ##########################

        # FUNCTION CALLED WHEN THE PLAYER CLICKS THE NEW USER BUTTON

        self.register_screen = Toplevel(self.screen)
        self.register_screen.title("Register")
        self.register_screen.geometry("300x350")
        self.register_screen.iconphoto(False, self.icon)
        self.register_screen.resizable(False, False)
        # CREATING A NEW REGISTER WINDOW WITH THE SAME ICON AND NEW TITLE

        Label(self.register_screen, image=self.register_background_image).place(x=-5, y=0)
        # PUTS BACKGROUND ONTO SCREEN

        register_frame = Frame(self.register_screen, bg="white")
        register_frame.place(x=10, y=70, height="200", width="200")
        # CREATES A WHITE SQUARE ON THE SCREEN

        Label(register_frame, text="Register Below", font=("Fixedsys", 16, "bold"), bg="white", fg="#026FB3").place(
            x=28, y=10)
        Label(register_frame, text="User Registration", font=("Terminal", 10), bg="white", fg="#026FB3").place(x=53,
                                                                                                               y=30)
        # TITLES AND SUBTITLES

        Label(register_frame, text="New Username", font=("Fixedsys", 11, "bold"), bg="white", fg="gray").place(x=45,
                                                                                                               y=50)
        self.register_username_text = Entry(register_frame, font=("Fixedsys", 11), bg="lightgray")
        self.register_username_text.place(x=26, y=70, height=20, width=150)
        # USERNAME LABEL AND ENTERING

        Label(register_frame, text="New Password", font=("Fixedsys", 11, "bold"), bg="white", fg="gray").place(x=45,
                                                                                                               y=100)
        self.register_password_text = Entry(register_frame, font=("Fixedsys", 11), bg="lightgray")
        self.register_password_text.place(x=26, y=120, height=20, width=150)
        # PASSWORD LABEL AND ENTERING

        Button(register_frame, text="REGISTER", bg="white", fg="#008AC9", font=("Fixedsys", 15, "bold"),
               command=self.register_account).place(x=55, y=160)
        # REGISTER BUTTON
