#William Stearns
#4-20-25
#Module 8.2
#This program connects to a MySQL database,displays information, and makes changes to the database.

""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode

import dotenv # to use .env file
from dotenv import dotenv_values


def show_films(cursor, title):
    
    cursor.execute("SELECT `f`.`film_name` AS `FilmTitle`,`f`.`film_director` AS `Director`,`g`.`genre_name` AS `Genre`,`s`.`studio_name` AS `Studio`FROM((`film` `f`JOIN `genre` `g` ON ((`f`.`genre_id` = `g`.`genre_id`)))JOIN `studio` `s` ON ((`f`.`studio_id` = `s`.`studio_id`)))")
    films = cursor.fetchall()
    print(f"-- {title} --")
    for film in films:
        print(f"Film Name: {film[0]}\nDirector: {film[1]}\nGenre Name: {film[2]}\nStudio Name: {film[3]}\n")

                 


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
    cursor = db.cursor()
    show_films(db.cursor(), "DISPLAYING FILMS")
    cursor.execute("INSERT INTO film VALUES ('4', 'Superstar', '1999', '82', 'Bruce McCulloch', '4', '4');")
    show_films(db.cursor(), "DISPLAYING FILMS AFTER INSERT")
    cursor.execute("UPDATE film SET genre_id = '1' WHERE film_name = 'Alien';")
    show_films(db.cursor(), "DISPLAYING FILMS AFTER UPDATE - Changed Alien to Horror")
    cursor.execute("DELETE FROM film WHERE film_name = 'Gladiator';")
    show_films(db.cursor(), "DISPLAYING FILMS AFTER DELETE")
    db.close()

if __name__ == "__main__":
    main()


