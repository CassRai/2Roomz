import sqlite3
import random
import os
conn = sqlite3.connect("C:/Users/Cassie/Documents/A-Levels/CS/Component 2/Game.db")
playa_current_point = 0

c = conn.cursor()
#creates the 2 tables 1 for the usernames and passwords and one for the league table
#establishes the username as the primary key - so there will be no repeats
c.execute("""CREATE TABLE IF NOT EXISTS userpass (
            user text NOT NULL PRIMARY KEY,
            pass text,
            high_score integer,
            current_score integer
            )""")
c.execute("""CREATE TABLE IF NOT EXISTS leaguetable (
             user text NOT NULL PRIMARY KEY,
             high_score integer
            )""")
c.execute("""CREATE TABLE IF NOT EXISTS question (
             questionType text,
             questionp1 text,
             questionp2 text,
             answer text
            )""")

class Player():
   #allows us to easily create players and update scores
   def __init__(self,usern,passw):
      self.usern = usern
      self.passw = passw
      self.current  = 0
      self.high = 0
      c.execute("INSERT or IGNORE INTO userpass VALUES(?,?,?,?)", (self.usern,self.passw,self.high,self.current,))
      #if you try to create a player with a name already in the DB the db will ignore this request
      #good so the program wont crash
      conn.commit()
   
   def update_current(self,current):
      self.current = current
      c.execute("UPDATE userpass SET current_score=? WHERE user=?", (self.current,self.usern,))
      conn.commit()
      #updates the 2 columns in the db based on input
   def update_high(self,high):
      self.high = high
      c.execute("UPDATE userpass SET high_score=? WHERE user=?", (self.high,self.usern,))
      conn.commit()

def log_in():
    flag  = "a"
    global playa
    #log-in function if the username isnt there - wont allow you to log-in
    while flag == "a":
        print("Welcome Back to The 2 Roomz!")  
        un = input("Enter username ")
        pw = input("Enter password ") 
        if un != "" and pw != "":
           c.execute("SELECT * FROM userpass WHERE user=? AND pass=?",(un,pw,))
           conn.commit()
           exist = c.fetchone()
           if exist == None:
            return False
           else:
            playa = Player(exist[0],exist[1])
            return True
        else:
            flag = "a"
      
def sign_up():
    #sign-up function if the username exists will direct to the log-in function based on input or go back to 
    #the new account process
    print("")
    global playa
    print("")
    print("Welcome to The 2 Roomz -  Lets get you started")
    un = input("Enter a username ")
    pw = input("Enter a password ")
    c.execute("SELECT user FROM userpass WHERE user=?",(un,))
    conn.commit()
    exist = c.fetchone()
    if exist == None:
     playa = Player(un,pw)
     print("Account Succesfully Created")
     return True
    else:
     print("Username taken - try a new one ")
     print("")
     print("Or")
     alt = input("Are you {}".format(un))
     altLow = alt.lower()
     if altLow == "yes":
        print("Please Sign-in")
        return False
     else:
        print("Back to Account Creation")
        return False

def askQuestion(qType,a,b):
#there are only 2 types of question - 1 for each room - to streamline the process - Question Template
   if qType == "movie":
      print("")
      Guess = input("{} was played by {} " .format(a,b))
      return Guess
   elif qType == "tv":
      print("")
      Guess = input("{} ran for {} seasons ".format(a,b))
      return Guess
   else:
      print("Error: Invalid Question Type")

def room_1():
   #the first room category = Movies
   global playa_current_point
   print("Leo: Welcome to Room 1- Movies, have a key!")
   print("Leo: I'm Leonardo Dicaprio - I'm pretty famous, Titanic and all")
   print("Leo: I'll say 4 statements and you have to say if they are TRUE or FALSE")
   print("Leo: Let's start")
   c.execute("SELECT * FROM question WHERE questionType=?",("Movie",))
   movie_Qs = c.fetchall()
   #fetches all the movie questions from the question table
   Guess = askQuestion("movie",movie_Qs[0][1],movie_Qs[0][2])
   #inputs the names/charaters from the quesiton table into the question template 
   if Guess == movie_Qs[0][3]:
      #guess is returned from the question template - if the guess = the answer from the db
      print("Correct")
      playa_current_point += 1
   else:
      print("Incorrect")

   Guess = askQuestion("movie",movie_Qs[1][1],movie_Qs[1][2])
   if Guess == movie_Qs[1][3]:
      print("Correct")
      playa_current_point += 1
   else:
      print("Incorrect")

   Guess = askQuestion("movie",movie_Qs[2][1],movie_Qs[2][2])
   if Guess == movie_Qs[2][3]:
      print("Correct")
      playa_current_point += 1
   else:
      print("Incorrect")

   Guess = askQuestion("movie",movie_Qs[3][1],movie_Qs[3][2])
   if Guess == movie_Qs[3][3]:
      print("Correct")
      playa_current_point += 1
   else:
      print("Incorrect")
   
def room_2():
   #the second room category = Tv Shows
   global playa_current_point
   print("Kerry: Welcome to Room 2 - TV Shows, looks like you have a key")
   print("Kerry: I'm Kerry Washington aka THE Olivia Pope")
   print("Kerry: I'll say 4 statements and you have to say if they are TRUE or FALSE")
   print("Kerry: Let's start")
   c.execute("SELECT * FROM question WHERE questionType=?",("TV",))
   TVShow_Qs = c.fetchall()
   Guess = askQuestion("tv",TVShow_Qs[0][1],TVShow_Qs[0][2])
   if Guess == TVShow_Qs[0][3]:
      print("Correct")
      playa_current_point += 1
   else:
      print("Incorrect")

   Guess = askQuestion("tv",TVShow_Qs[1][1],TVShow_Qs[1][2])
   if Guess == TVShow_Qs[1][3]:
      print("Correct")
      playa_current_point += 1
   else:
      print("Incorrect")

   Guess = askQuestion("tv",TVShow_Qs[2][1],TVShow_Qs[2][2])
   if Guess == TVShow_Qs[2][3]:
      print("Correct")
      playa_current_point += 1
   else:
      print("Incorrect")

   Guess = askQuestion("tv",TVShow_Qs[3][1],TVShow_Qs[3][2])
   if Guess == TVShow_Qs[3][3]:
      print("Correct")
      playa_current_point += 1
   else:
      print("Incorrect")
   
   print(playa_current_point)

def league_updates():
   #alsp creates the user in the leaguetable and then just goes to the leaderboard
   # a procedure to update the high scores into both the leaguetable and the userpass table
   c.execute("SELECT high_score FROM userpass WHERE user=?",(playa.usern,))
   user_high = c.fetchone()
   c.execute("INSERT or IGNORE INTO leaguetable VALUES(?,?)",(playa.usern,user_high[0],))
   conn.commit()
   playa.update_current(playa_current_point)
   if user_high[0] < playa_current_point:
      playa.update_high(playa_current_point)
      conn.commit
      c.execute("UPDATE leaguetable SET high_score=? WHERE user=?",(playa_current_point,playa.usern,))
      conn.commit()
      leaderboard()

def leaderboard():
   #the winner section - prints top 5 winners from the league_table
   c.execute("SELECT * FROM leaguetable ORDER BY high_score DESC")
   winners = c.fetchmany(5)
   conn.commit()
   print("Leaderboard - Top 5 Winners")
   print("")
   for i in range(len(winners)):
      for j in range(len(winners[i])):
         print(winners[i][j])


def main():
   #the main part of the code consists of the menu and all of the procedures coming together
   print("𝕋ℍ𝔼 𝟚 ℝ𝕆𝕆𝕄ℤ 𝔾𝔸𝕄𝔼")
   print("AJ: Hi Im AJ your host and welcome to the 2 Roomz!")
   print("AJ: This is a TRUE or FALSE game")
   while True:
    user_c = input("""1. Log-in > \n2. Sign-Up > \n3. Exit > \nEnter: """)
    if user_c.isdigit() == True:
        user_c = int(user_c)
        if user_c == 1:
            auth = log_in()
            if auth == True:
               room_1()
               if playa_current_point >= 3:
                  print("Leo: Congrats - here's the key to Room 2")
                  print("Inventory: Room 1 Key, Room 2 Key")
                  room_2()
                  break
               else:
                  print("You didnt score high enough to get to Room 2 - Back to main menu")
                  league_updates()
                  conn.commit()
            else:
               print("Couldn't verify try again or Sign-up")
        elif user_c == 2:
            auth = sign_up()
            if auth == True:
               room_1()
               if playa_current_point >= 3:
                  print("Leo: Congrats - here's the key to Room 2")
                  print("Inventory: Room 1 Key, Room 2 Key")
                  room_2()
                  break
               else:
                  print("You didnt score high enough to get to Room 2 - Back to main menu")
                  league_updates()
                  conn.commit()
            else:
               print("Couldn't verify try again or Log-in")
        elif user_c == 3:
            break
   league_updates()

main()
