from database import Database
import re

def execSQL(query):
    query = query.rstrip(';') #Removes any semicolons from the end of the query, as they are not needed.
    
    if (re.match("(?i)^[\s]*CREATE DATABASE .+", query)): ### CREATE DATABASE ###
        name = re.search('(?i)CREATE DATABASE (.+)', query).group(1)
        
        global db 
        db = Database(name, load=False)
    
    else:
        print ("## ERROR -> Invalid SQL statement")
