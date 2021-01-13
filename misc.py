import operator
import re

def get_op(op, a, b):
    '''
    Get op as a function of a and b by using a symbol
    '''
    ops = {'>': operator.gt,
                '<': operator.lt,
                '>=': operator.ge,
                '<=': operator.le,
                '==': operator.eq}

    try:
        return ops[op](a,b)
    except TypeError:  # if a or b is None (deleted record), python3 raises typerror
        return False

def split_condition(condition):
    condition = condition.replace(' ','') # remove all whitespaces
    ops = {'>=': operator.ge,
           '<=': operator.le,
           '==': operator.eq,
           '>': operator.gt,
           '<': operator.lt}

    for op_key in ops.keys():
        splt=condition.split(op_key)
        if len(splt)>1:
            return splt[0], op_key, splt[1]

            
def convert_to_type(string):
    '''
    Converts a string to the data type it represents.    
    Supported types: string, integer, float, boolean
    '''

    string = string.lower() #SQL keywords are case insensitive
    
    type_samples = {'str': '',
           'string': '',
           'varchar': '',
           'text': '',
           'int': 0,
           'integer': 0,
           'float': 0.0,
           'bool': True,
           'boolean': True}
           
    return (type(type_samples[string]))
    

def parameter_config(string, word1, word2):
    '''
    Returns an array that contains all words between word1 and word2 in the given string.
    This will help us pass these parameters to functions like select, delete, etc...

    ex:
    Command: parameter_config("SELECT ID,dept_name FROM instructor WHERE salary>8000", 'SELECT', 'FROM')
    Meaning: Find the requested table columns in this query.
    Returns: ['ID', 'dept_name'] 
    
    'word2' can also be a list of words. Sometimes we can't be sure about the next keyword.
    This way, it builds a custom regex pattern (using create_pattern) and returns the words between word1 and ANY word in word2.
    
    ex:
    Command: parameter_config("SELECT ID,dept_name FROM instructor WHERE salary>8000 ORDER BY name LIMIT 3", 'FROM', ['INNER JOIN','WHERE','ORDER BY','LIMIT'])
    Meaning: Find the requested table in this query. It is always after FROM and before 'INNER JOIN', 'WHERE', 'ORDER BY' or 'LIMIT'.
    Returns: ['instructor'] 
    

    Notes:
    -word1 and word2 are NOT case sensitive as they always are SQL keywords.    
    -word2 being empty means "Find all words after word1".    
    -Any extra spaces and tabs between words are ignored.    
    -Unlike in a reqular SQL compiler, column names can be separated by spaces.
        ex: SELECT ID dept_name FROM ...
        An SQL compiler returns only the 'ID' column. However, this function recognizes both 'ID' and 'dept_name'.    
    -If word2 is a list, the order of the keywords matters. The regex gives priority to the first detected keyword in the list's order.
        ex: SELECT * FROM instructor WHERE salary>8000 ORDER BY name
        Using "parameter_config(query, 'FROM', ['WHERE', 'ORDER BY'])" will return ['instructor'] (the result we want).
        Using "parameter_config(query, 'FROM', ['ORDER BY', 'WHERE'])" will return ['instructor', 'WHERE', 'salary>8000'].
        Obviously this will cause problems when we handle the parameters. 
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
   
        array = re.split("\s|\,", array) #seperate by ',' or by space
        array = list(filter(None, array)) #remove any empty strings
        
        return (array)
    else: #requested substring does not exist
        return (None)

        
        
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
    
