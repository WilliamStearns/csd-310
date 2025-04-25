#William Stearns
#4-20-25
#Module 7.2
#This program connects to a MySQL database and displays information about movies, studios, genres, and directors.

""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode

import dotenv # to use .env file
from dotenv import dotenv_values

def display_studios(db):
    print("\n-- DISPLAYING Studio RECORDS --")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM studio;")
    studios = cursor.fetchall()
    for s in studios:
        print(f"Studio: {s[0]}\nStudio Name: {s[1]}\n")

def display_genres(db):
    print("\n-- DISPLAYING Genre RECORDS --")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM genre;")
    genres = cursor.fetchall()
    for g in genres:
        print(f"Genre ID: {g[0]}\nGenre Name: {g[1]}\n")
        
def display_short(db):
    print("\n-- DISPLAYING Short Film RECORDS --")
    cursor = db.cursor()
    cursor.execute("SELECT film_name, film_runtime FROM film " \
    "where film_runtime <= 120;")
    shorts = cursor.fetchall()
    for s in shorts:
        print(f"Film Name: {s[0]}\nRuntime: {s[1]}\n") 
        
def display_directors(db):
    print("\n-- DISPLAYING Director RECORDS in Order --")
    cursor = db.cursor()
    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director;")
    directors = cursor.fetchall()
    for d in directors:
        print(f"Film : {d[0]}\nDirector: {d[1]}\n")                       

#using our .env file
secrets = dotenv_values(".env")
def main():
    """ database config object """
    config = {
        "user": secrets["USER"],
        "password": secrets["PASSWORD"],
        "host": secrets["HOST"],
        "database": secrets["DATABASE"],
        "raise_on_warnings": True #not in .env file
    }

    try:
        """ try/catch block for handling potential MySQL database errors """ 

        db = mysql.connector.connect(**config) # connect to the movies database 
        
        # output the connection status 
        print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

        input("\n\n  Press any key to continue...")

    except mysql.connector.Error as err:
        """ on error code """

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password are invalid")

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("  The specified database does not exist")

        else:
            print(err)
    
    display_studios(db)
    display_genres(db)
    display_short(db)
    display_directors(db)
    db.close()

if __name__ == "__main__":
    main()


