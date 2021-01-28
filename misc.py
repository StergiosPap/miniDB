import operator

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
    

