from misc import convert_to_type
import re

def first_element(list):
    '''
    Returns list[0] or None if list is empty (or is not a list).
    '''
    try:
        return list[0]
    except:
        return None
    

def create_pattern(word, list):
    '''
    Creates a regex pattern that translates to: "Find all words between 'word' and any word in 'list'".

    Note: This method always appends the 'end of string' character, in case there isn't any word from 'list' in the given string.
    '''

    pattern = r'(?i)'
    
    for i in range (len(list)):
        pattern += word + ' (.+) (' + list[i] + ')|'
        
    pattern += word + ' (.+)$' #append 'end of string' character

    return pattern


def parameter_config(string, word1, word2):
    '''
    Returns an array that contains all words between word1 and word2 in the given string. 
    'word2' can also be a list of words. Sometimes we can't be sure about the next keyword.
    This way, it builds a custom regex pattern (using create_pattern) and returns the words between word1 and ANY word in word2.
    '''

    if (isinstance(word2,list)): #if word2 is a list of words
        pattern = create_pattern(word1, word2)
    else:
        pattern = r'(?i)' + word1 + '(.+)' + word2
        
    array = re.search(pattern, string) #find the requested substring 

    if (array != None):
        for i in range(1,100): #find the first non-empty group (max 99 keywords, extreme case)
            if (array.group(i) != None):
                array = array.group(i)
                break
   
        array = re.split("\t|\s|\,", array) #seperate by ',' or by space
        array = list(filter(None, array)) #remove any empty strings
        
        return (array)
    else: #requested substring does not exist
        return (None)



'''
The following functions use 'parameter_config' in order to split the query into its parameters depending on the SQL command.
These parameters will be used in execSQL (in database.py) to execute the corresponding miniDB function.
'''

def parameters_select(query):
    columns = parameter_config(query, 'SELECT', 'FROM')
    table = parameter_config(query, 'FROM', ['INNER JOIN','WHERE','ORDER BY','LIMIT'])
    innerjoin_table = parameter_config(query, 'INNER JOIN', 'ON')
    innerjoin_condition = parameter_config(query, 'ON', ['WHERE','ORDER BY','LIMIT'])
    condition = parameter_config(query, 'WHERE', ['ORDER BY','LIMIT'])
    order_by = parameter_config(query, 'ORDER BY', ['ASC','DESC','LIMIT'])
    asc_order = (re.match(r'(?i).* ORDER BY .+ DESC', query)==None)
    limit = parameter_config(query, 'LIMIT', '')
    
    if (columns == ['*']): columns = '*'
    
    table = first_element(table)
    order_by = first_element(order_by)
    condition = first_element(condition)
    innerjoin_table = first_element(innerjoin_table)
    innerjoin_condition = first_element(innerjoin_condition)  
    
    try: #Converting limit to integer (if possible).
        limit = int(limit[0])
    except:
        limit = None
        
    return columns, table, innerjoin_table, innerjoin_condition, condition, order_by, asc_order, limit


def parameters_insert_select(query):
    save_as = parameter_config(query, 'INSERT INTO', 'SELECT')
    select_query = re.search('(?i)[\s]*(SELECT .+)', query).group(1) #Query without 'INSERT'. A normal 'SELECT' query.
    
    #Same steps as 'SELECT'
    columns = parameter_config(select_query, 'SELECT', 'FROM')
    table = parameter_config(select_query, 'FROM', ['INNER JOIN','WHERE','ORDER BY','LIMIT'])
    innerjoin_table = parameter_config(select_query, 'INNER JOIN', 'ON')
    innerjoin_condition = parameter_config(select_query, 'ON', ['WHERE','ORDER BY','LIMIT'])
    condition = parameter_config(select_query, 'WHERE', ['ORDER BY','LIMIT'])
    order_by = parameter_config(select_query, 'ORDER BY', ['ASC','DESC','LIMIT'])
    asc_order = (re.match(r'(?i).* ORDER BY .+ DESC', select_query)==None)
    limit = parameter_config(select_query, 'LIMIT', '')
    
    if (columns == ['*']): columns = '*'      
        
    table = first_element(table)
    save_as = first_element(save_as)
    order_by = first_element(order_by)
    condition = first_element(condition)
    innerjoin_table = first_element(innerjoin_table)
    innerjoin_condition = first_element(innerjoin_condition)
    
    try:
        limit = int(limit[0])
    except:
        limit = None

    return save_as, select_query, columns, table, innerjoin_table, innerjoin_condition, condition, order_by, asc_order, limit
        

def parameters_insert(query):
    table = parameter_config(query, 'INSERT INTO', 'VALUES')
    values = re.search('(?i)VALUES (.+)', query).group(1)
    
    #Converting string (values) to array.
    values = values.replace('\'','').replace('\"','').replace('[','').replace(']','').split(',')
    values = [item.strip() for item in values]
    
    table = first_element(table)
    
    return table, values

    
def parameters_update(query):
    '''
    Note: The current version of miniDB supports only 1 change per update. 
    We can easily fetch all requested updates with a for loop in 'changes'.
    However, if we change a value that also exist in our condition, 
    the other changes in the same statement might be affected.            
    For now, we will only use the first change in the query.
    '''
    
    table = parameter_config(query, 'UPDATE', 'SET')
    changes = parameter_config(query, 'SET', 'WHERE') 
    condition = parameter_config(query, 'WHERE', '') 

    column = changes[0].split('=')[0] #characters before '='
    value = changes[0].split('=')[1] #characters after '='
    
    table = first_element(table)
    condition = first_element(condition)
    
    return table, changes, condition, column, value

    
def parameters_delete(query):
    table = parameter_config(query, 'DELETE FROM', 'WHERE')
    condition = parameter_config(query, 'WHERE', '')
    
    table = first_element(table)
    condition = first_element(condition)

    return table, condition
    
    
def parameters_create_table(query):
    name = parameter_config(query, 'CREATE TABLE', '\(')    
    columns = parameter_config(query, '\(', '\)')
    '''
    According to the SQL syntax, columns should look like this:
    ['ID','str','Name','str','Age','int','Salary','int']
    So, in order to separate the column names and their types,
    we have to extract the even positioned elements (starting from 0).
    and the odd positioned elements respectively.            
    '''
    colnames = columns[0::2]
    coltypes = columns[1::2]

    coltypes = [convert_to_type(i) for i in coltypes] #Converting to a list of types.
    
    name = first_element(name)
    
    return name, colnames, coltypes


def parameters_drop_table(query):
    table = parameter_config(query, 'DROP TABLE', '')
    
    table = first_element(table)
    
    return table
    
    
def parameters_create_index(query):
    name = parameter_config(query, 'CREATE INDEX', 'ON')
    table = parameter_config(query, 'ON', '')
    
    name = first_element(name)
    table = first_element(table)
    
    return name, table
    
    
def parameters_drop_index(query):
    name = parameter_config(query, 'DROP INDEX', '')
    
    name = first_element(name)
    
    return name


def parameters_create_database(query):
    name = re.search('(?i)CREATE DATABASE (.+)', query).group(1)
    
    name = first_element(name)
    
    return name



