from database import Database
from sql_helper import parameters_create_database
import re

def execSQL(query):
    '''
    SQL commands related to a database and not its tables.
    '''
    query = query.rstrip(';') #Removes any semicolons from the end of the query, as they are not needed.
    
    global db 
    
    if (re.match("(?i)^[\s]*CREATE DATABASE .+", query)): ### CREATE DATABASE ###
        name = parameters_create_database(query)

        db = Database(name, load=False)
        
    elif (re.match("(?i)^[\s]*LOAD DATABASE .+", query)): ### LOAD DATABASE ###
        name = parameters_create_database(query)
        
        db = Database(name, load=True)
    
    else:
        print ("## ERROR -> Invalid SQL statement")
