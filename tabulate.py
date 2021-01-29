def tabulate(rows, headers):
    '''
    Custom tabulate function that returns a formatted table.
    '''
    
    # Casts every element to string
    rows = [[str(j) for j in i] for i in rows]
    
    # Combines the headers with the rows to create an acceptable format for the following commands.
    list = [headers] + rows

    # Finds the maximum length for each column in table.
    max_lengths_per_col = [max(len(word) for word in [row[col] for row in list]) for col in range(len(list[0]))]

    stringbuilder = ''

    # Appends the column headers.
    for i in range (len(max_lengths_per_col)):
        stringbuilder += list[0][i] + " " * (max_lengths_per_col[i]-len(list[0][i])+4)


    stringbuilder += '\n'

    # Appends the divider between the column headers and the records.
    for i in range (len(max_lengths_per_col)):
        stringbuilder += "-" * (max_lengths_per_col[i]+2) + "  "

    stringbuilder += '\n'

    # Appends the records.
    for i in range (1,len(list)): 
        for j in range (len(max_lengths_per_col)):
            stringbuilder += list[i][j] + " " * (max_lengths_per_col[j]-len(list[i][j])+4)
        
        stringbuilder += '\n'
        
    return stringbuilder

    
