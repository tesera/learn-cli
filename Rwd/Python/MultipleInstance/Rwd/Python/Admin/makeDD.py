from fileUtilities import newFilePath, newFilePath_v2

def data_dictionary(filepath, filename):
    dict_path = newFilePath(filepath, filename)
    '''
    Author:  Ian Moss
    Last Modified Jan 23, 2006 (source file: READv1)
    Converted to following dictionary format:
    {('VariableName','TableName'):'Type'}
    where type is an integer, string or float
    Updated: August 27, 2012 (Mishtu Banerjee, Ian Moss)
    Copyright Ian Moss
    '''
    #print dict_path
    temp_file =open (dict_path,'r')
    outfile = {}
    i=0
    variables = {'VARIABLES':{}}
    data ={'DATA':{}}
    for line in temp_file:
        #This part of the program strips off linefeed symbol, '\n' that
        #is inserted by ACCESS or Python at the end of line(s)
        #when it reads files.
        x=line.split(',')
        end_j = len(x)
        j=end_j-1
        #x[j].rstrip()
        #print x[j]
        #break
        dummy = x[j]
        end_l = len(dummy)
        x[j] = ''
        l=0
        for l in range(0,end_l-1,1):
            x[j] = x[j]+dummy[l]
        #End of routine for stripping away of linefeed symbol at end
        #of line.
        if i == 0:
            j = 0
            for j in range(0,end_j):
                if x[j] == 'Variable':
                    var_col = j
                else:
                    if x[j] == 'Table':
                        table_col = j
                    else:
                        if x[j] == 'Type':
                            type_col = j
        if not i==0:
            #Old method below
            #key = (str(x[var_col]), str(x[table_col]))
            #newline = {key:str(x[type_col])}
            #outfile.update(newline)
            #New method
            table_name = str(x[table_col])
            var_name = str(x[var_col])
            var_type = str(x[type_col])
            if not outfile.has_key(table_name):
                outfile.update({table_name:{}})
            if not outfile[table_name].has_key(var_name):
                outfile[table_name].update({var_name:var_type})
            
        i=i+1
    temp_file.close()
    return outfile

def dataDictionaryType_2(filepath = '', filename = ''):
    '''
    Author:  Ian Moss

    Input
    The file path indicates where the data dictionary can be found
    The filename indicates the name of the text (.txt) file where the comma delimmmited dictionary can be found,
        excluding the extension, for example 'DATDICT'. 
          
    This is a new dictionary type to allow for relabelling of input variables
    and to identify different kinds of variables.  Column names are provided
    in the first line and and can be provided in any order, but by convention they
    are used in the following order (the names must be used as column headings
    separated by a comma) after having been processued using this function:

    TVID        - This is a unique ID refering to each row in the data dictionary
                    This must be an integer (see below)
    TABLENAME   - This generaly refers to a comma delimmted text file containg data without the '.txt. extension
    VARNAME     - This is the list of variables found in the files
    NEWVARNAME  - This is the new name to be assigned to the input variable
                    (they may be the same as the original variable names) 
    VARTYPE     - This is defined as integer, float or string ... or any other Python variable type
    VARKIND     - This is nominal, ordinal or continuous (at the moment this is for reference purposes only)
    VARDEFAULT  - This is the default value for blank entries in a data table, i.e. ''
                - If the default is left blank then a '' will be used as the default for string types
                    a 0(zero) will be used as the default for integer types, and
                    a 0.0 (i.e. float(0)) will be used as the default for float types
                    Note that if VARTYPE is 'numeric' and VARDEFAULT' is left blank then the default will be a float, 0.0
    SELECT      - This is optional and for reference purposes only.  All of the data in the data file with a corresponding
                    variable name will be loaded into the Python module.
                    Use a 1 to indicate if a variable is to be included, otherwise 0. 
    DESCRIPTION - This is a description for reference purposes only

    The data dictionary itself must be a comma delimmeted file ... and as a result there must be no
    commas used under the 'Description' in the last column.
    No commas can be used anwhere in the data, other than to separate columns of variables 

    This function returns two dictionaries as follows:

    originalNameDict = {tableName:{varName:{'TVID':tvid, 'NEWVARNAME': 'newVarName','VARTYPE': varType,'VARKIND':varKind, 'VARDEFAULT':varDefault, 'DESCRIPTION':description}
    newNameDict = {tableName:{newVarName:{'TVID':tvid,'VARNAME': 'varName','VARTYPE': varType,'VARKIND':varKind, 'VARDEFAULT':varDefault, 'DESCRIPTION':description}

    Note if the newVarname is left blank then the original varName will be used to represent the newVarname.

    Note that the following variable types are permissible (all in lower case):

    boolean     - This will be type() cast as an integer in Python and must be coded as 1 or 0.
                    The rule above for declaring integer types apply. 
    character   - This will be type() cast as a string.
    classint    - This is a clas described as an integer(e.g; 1,2,,3 ... n classes undera single varName) generally to be used
                    when the classes do not qualify as being ordinal.
                    These will be type() cast as integers.
                    Generaly there will be more than 2 classes; 2 classes are better represented as boolean or dummy varTypes
                    Classes may also be described as nominal and therefore type() cast as string
    continuous  - This will be type() cast as a float, may or may not include decimal points, but must not include characters.
    count       - This is type() cast as an integer.
                    It should be reserved for actual counts of certain kinds or classes of objects 
    dummy       - This is type() cast as an integer (same as boolean) and must be coded as 1 or 0.
    float       - This may or may not include a decimal place but must not include characters.
    integer     - No decimal may be recorded next to a number declared as being integer anywhere in the data table;
                    If there is a decimal point included Python will not convert it from a string to an integer.
                    If characters are included Python will NOT convert it from a string to an integer.
    nominal     - This will be a type() cast as a string.
    ordinal     - This will be type() cast as an integer in Python.
                    The rule above for declaring integer types apply.
                    These kind of variables reflect a distinct order or rank and can be treated as continuous variables.
    proportion  - This is float type() between 0 and 1
    string      - This may be in any format since all values are initially imported in this format.

    The 'numeric' type (not a type used in Python but referred to elsewhere) was rejected due to ambiguity between a float and an integer
   
    This is a refactoring of code developed previously under ForesTree Dynamics Ltd 
    Copyright Ian Moss
    '''
    if filepath == '':
        print 'No filepath indicated for data dictionary'
    if filename == '':
        print 'No filename indicated for data data dictionary'
    #Initialize dictionary filepath
    dict_path = newFilePath(filepath, filename)
    #Open dictionary
    temp_file = open (dict_path,'r')
    #Define original data dictionary (with original table and variable names as keys) and
    #Define new data dictionary (with original table names and new variable names as keys) 
    originalNameDict = {}
    newNameDict = {}
    #Set line index to 0
    i = 0 
    for line in temp_file:
        #This part of the program strips off linefeed symbol, '\n' that
        #is inserted by ACCESS or Python at the end of line(s)
        #when it reads files.
        x=line.split(',')
        end_j = len(x)
        j=end_j-1
        #x[j].rstrip()
        #print x[j]
        #break
        dummy = x[j]
        end_l = len(dummy)
        x[j] = ''
        l=0
        for l in range(0,end_l-1,1):
            x[j] = x[j]+dummy[l]
        #End of routine for stripping away of linefeed symbol at end
        #of line.
        if i == 0:
            #Get column numbers associated with variable names
            for j in range(0,end_j):
                if x[j] == 'TVID':
                    tvidCol = j
                else:
                    if x[j] == 'TABLENAME':
                        tableCol = j
                    else:
                        if x[j] == 'VARNAME':
                            varCol = j
                        else:
                            if x[j] == 'NEWVARNAME':
                                newVarCol = j
                            else:
                                if x[j] == 'VARTYPE':
                                    varTypeCol = j
                                else:
                                    if x[j] == 'VARDEFAULT':
                                        varDefaultCol = j
                                    else:
                                        if x[j] == 'SELECT':
                                            selectCol = j
                                        else:
                                            if x[j] == 'DESCRIPTION':
                                                descriptionCol = j
        if not i==0:
            #assign variable values from appropriate column numbers  
            tvid = int(x[tvidCol])
            tableName = str(x[tableCol])
            varName = str(x[varCol])
            newVarName = str(x[newVarCol])
            #if newVarName is left blank then replace with varName
            if newVarName == '':
                newVarName = varName
            varType = str(x[varTypeCol])
            #varDefault
            try:
                int(x[varDefaultCol])
            except:
                try:
                    float(x[varDefaultCol])
                except:
                    varDefault = str(x[varDefaultCol])
                else:
                    varDefault = float(x[varDefaultCol])       
            else:
                varDefault = int(x[varDefaultCol])
            #select
            try:
                int(x[selectCol])
            except:
                select = str(x[selectCol])
            else:
                select = int(x[selectCol])

                          
            description = str(x[descriptionCol])
            #Start process of assigning appropriate types() to varDefault values
            #If variable type is not a string, character or nominal type() the change the type
            #Must either be related to a float or integer type
            if not varType == 'string' or not varType == 'character' or not varType == 'nominal':
                #If varType is integer, boolean or ordinal
                if varType == 'integer' or varType == 'boolean' or varType == 'dummy' or varType == 'ordinal' \
                   or varType == 'classint' or varType == 'count':
                    if varDefault == '':
                        varDefault = 0
                    else:
                        try:
                            int(varDefault)
                        except:
                            print 'Default value', varDefault, 'TABLENAME', tableName, 'VARNAME', varName, \
                                  'in DATA DICTIONARY TVID', tvid, 'cannot be converted to an integer'
                        else:
                            varDefault = int(varDefault)
                            
                #if varType is float or coninuous
                if  varType == 'float' or varType == 'continuous' or varType == 'proportion':
                    if varDefault == '':
                        varDefault = float(0)
                    else:
                        try:
                            float(varDefault)
                        except:
                            print 'Default value', varDefault, 'TABLENAME', tableName, 'VARNAME', varName, \
                                  'in DATA DICTIONARY TVID', tvid, 'cannot be converted to a float'
                        else:
                            varDefault = float(varDefault)
                        
                        
            #If the tableName has not been added as the primary key to the originalNameDict
            #Then by definition it has not yet been assigned to the newNameDict
            #Update these two dictionaries with the table names
            if not originalNameDict.has_key(tableName):
                originalNameDict.update({tableName:{}})
                newNameDict.update({tableName:{}})
            #If the variable name, varName has not yet been assigned as a key subdivision of tableName
            #Then    
            if not originalNameDict[tableName].has_key(varName):
                originalNameDict[tableName].update({varName:{'TVID':tvid,'NEWVARNAME':newVarName,'VARTYPE':varType, 'VARDEFAULT':varDefault, \
                                                             'SELECT':select,'DESCRIPTION':description}})
            else:
                #tableName in originalNameDict has duplicate variable names 
                print 'TABLE', tableName, 'has a duplicate VARNAME', varName, 'in data dictionary type 2'
                
            #Update the newVarName as a key in the newNameDict 
            #If newVarName is blank then replace blank with varName
            if newVarName == '':
                newVarName = varName    
            if not newNameDict[tableName].has_key(newVarName):
                newNameDict[tableName].update({newVarName:{'TVID':tvid,'VARNAME':varName, 'NEWVARNAME':varName,'VARTYPE':varType, \
                                                           'VARDEFAULT':varDefault,'SELECT':select,'DESCRIPTION':description}})
            else:
                #TableName in newNameDict has duplicate variable names
                print 'TABLE', tableName, 'has a duplicate NEWVARNAME', newVarName, 'TVID', tvid, 'in data dictionary type 2'
        i=i+1
    temp_file.close()
    return originalNameDict, newNameDict
     
def makeNewDataDictionaryFromDataStringFile(dataTableName = '', newDataStringList = [], oldDict = {}):
    '''
    This function identifies the type to be assigned to each variable based
    on the type in row 1 of a dataStringList following after the
    list of variable names in row 0.  It is then assumed that
    the types of all of the remaining data in a given column are consistent
    with those indicated in the second row.  The types are cast hierarchically
    starting with integer, and if that fails (the variable can not be converted
    to an integer), then a float, and if that fails, then the variable must be in a
    string format.  As a result if there is a variable that is entered in row 1 as '5'
    and the variable in the same column in the next row is '5.6', then an error
    will occur.  This can be avoided by recording '5.' or '5.0' in the first row. 
    '''
    end_i = len(newDataStringList)
    if end_i <= 1:
        print 'typeDataset.typeDatasetWithoutDataDictionary() error'
        print 'newDataStringList has only 1 row but requires 2 rows'
        print 'the first row must contain the variable names'
        print 'the second row and all other rows must contain variable vaulues'
        
    else:
        if oldDict.has_key(dataTableName) == True:
            print 'makeDD.makeNewDataDictionary error'
            print 'cannot update oldDict due to pre-existing dataTableName:', dataTableName
        else:
            oldDict.update({dataTableName:{}})
            #Get variable name list from row 0 in newDataStringList
            varNamesList = newDataStringList[0]
            if varNamesList == []:
                print 'makeDD.makeNewDataDictionary error'
                print 'there are no variable names in dataTableName:', dataTableName
            else:
                end_j = len(varNamesList)
                #Establish variable type based on type according to first row
                #Note that all variables must be of a consitent type - either integer (no decimal place), float or string  
                for j in range(0,end_j,1):
                    varName = varNamesList[j]
                    try:
                        newVarValue = int(newDataStringList[1][j])
                    except:
                        try:
                            newVarValue = float(newDataStringList[1][j])
                        except:
                            varType = 'string'
                        else:
                            varType = 'float'
                    else:
                        varType = 'integer'
                    if oldDict[dataTableName].has_key(varName) == False:
                        oldDict[dataTableName].update({varName:{'TVID':j,'VARNAME':varName,'NEWVARNAME':'','VARTYPE':varType, \
                                                            'VARDEFAULT':'','SELECT':1,'DESCRIPTION':''}})
                    else:
                        print 'makeDD.makeNewDataDictionary error'
                        print 'dataTableName:', dataTableName, 'has duplicate variable names:', varName
                        print 'unable to include both variables in dictionary'
            return oldDict
        
def dataDictionaryType_21(filepath = '', filename = '', fileExtension = '.csv'):
    '''
    Author:  Ian Moss

    Input
    The file path indicates where the data dictionary can be found
    The filename indicates the name of the text (.txt) file where the comma delimmmited dictionary can be found,
        excluding the extension, for example 'DATDICT'. 
          
    This is a new dictionary type to allow for relabelling of input variables
    and to identify different kinds of variables.  Column names are provided
    in the first line and and can be provided in any order, but by convention they
    are used in the following order (the names must be used as column headings
    separated by a comma) after having been processued using this function:

    TVID        - This is a unique ID refering to each row in the data dictionary
                    This must be an integer (see below)
    TABLENAME   - This generaly refers to a comma delimmted text file containg data without the '.txt. extension
    VARNAME     - This is the list of variables found in the files
    NEWVARNAME  - This is the new name to be assigned to the input variable
                    (they may be the same as the original variable names) 
    VARTYPE     - This is defined as integer, float or string ... or any other Python variable type
    VARKIND     - This is nominal, ordinal or continuous (at the moment this is for reference purposes only)
    VARDEFAULT  - This is the default value for blank entries in a data table, i.e. ''
                - If the default is left blank then a '' will be used as the default for string types
                    a 0(zero) will be used as the default for integer types, and
                    a 0.0 (i.e. float(0)) will be used as the default for float types
                    Note that if VARTYPE is 'numeric' and VARDEFAULT' is left blank then the default will be a float, 0.0
    SELECT      - This is optional and for reference purposes only.  All of the data in the data file with a corresponding
                    variable name will be loaded into the Python module.
                    Use a 1 to indicate if a variable is to be included, otherwise 0. 
    DESCRIPTION - This is a description for reference purposes only

    The data dictionary itself must be a comma delimmeted file ... and as a result there must be no
    commas used under the 'Description' in the last column.
    No commas can be used anwhere in the data, other than to separate columns of variables 

    This function returns two dictionaries as follows:

    originalNameDict = {tableName:{varName:{'TVID':tvid, 'NEWVARNAME': 'newVarName','VARTYPE': varType,'VARKIND':varKind, 'VARDEFAULT':varDefault, 'DESCRIPTION':description}
    newNameDict = {tableName:{newVarName:{'TVID':tvid,'VARNAME': 'varName','VARTYPE': varType,'VARKIND':varKind, 'VARDEFAULT':varDefault, 'DESCRIPTION':description}

    Note if the newVarname is left blank then the original varName will be used to represent the newVarname.

    Note that the following variable types are permissible (all in lower case):

    boolean     - This will be type() cast as an integer in Python and must be coded as 1 or 0.
                    The rule above for declaring integer types apply. 
    character   - This will be type() cast as a string.
    classint    - This is a clas described as an integer(e.g; 1,2,,3 ... n classes undera single varName) generally to be used
                    when the classes do not qualify as being ordinal.
                    These will be type() cast as integers.
                    Generaly there will be more than 2 classes; 2 classes are better represented as boolean or dummy varTypes
                    Classes may also be described as nominal and therefore type() cast as string
    continuous  - This will be type() cast as a float, may or may not include decimal points, but must not include characters.
    count       - This is type() cast as an integer.
                    It should be reserved for actual counts of certain kinds or classes of objects 
    dummy       - This is type() cast as an integer (same as boolean) and must be coded as 1 or 0.
    float       - This may or may not include a decimal place but must not include characters.
    integer     - No decimal may be recorded next to a number declared as being integer anywhere in the data table;
                    If there is a decimal point included Python will not convert it from a string to an integer.
                    If characters are included Python will NOT convert it from a string to an integer.
    nominal     - This will be a type() cast as a string.
    ordinal     - This will be type() cast as an integer in Python.
                    The rule above for declaring integer types apply.
                    These kind of variables reflect a distinct order or rank and can be treated as continuous variables.
    proportion  - This is float type() between 0 and 1
    string      - This may be in any format since all values are initially imported in this format.

    The 'numeric' type (not a type used in Python but referred to elsewhere) was rejected due to ambiguity between a float and an integer
   
    This is a refactoring of code developed previously under ForesTree Dynamics Ltd 
    Copyright Ian Moss
    '''
    if filepath == '':
        print 'No filepath indicated for data dictionary'
    if filename == '':
        print 'No filename indicated for data data dictionary'
    #Initialize dictionary filepath
    dict_path = newFilePath_v2(filepath, filename, fileExtension)
    #Open dictionary
    temp_file = open (dict_path,'r')
    #Define original data dictionary (with original table and variable names as keys) and
    #Define new data dictionary (with original table names and new variable names as keys) 
    originalNameDict = {}
    newNameDict = {}
    #Set line index to 0
    i = 0 
    for line in temp_file:
        #This part of the program strips off linefeed symbol, '\n' that
        #is inserted by ACCESS or Python at the end of line(s)
        #when it reads files.
        x=line.split(',')
        end_j = len(x)
        j=end_j-1
        #x[j].rstrip()
        #print x[j]
        #break
        dummy = x[j]
        end_l = len(dummy)
        x[j] = ''
        l=0
        for l in range(0,end_l-1,1):
            x[j] = x[j]+dummy[l]
        #End of routine for stripping away of linefeed symbol at end
        #of line.
        if i == 0:
            #Get column numbers associated with variable names
            for j in range(0,end_j):
                if x[j] == 'TVID':
                    tvidCol = j
                else:
                    if x[j] == 'TABLENAME':
                        tableCol = j
                    else:
                        if x[j] == 'VARNAME':
                            varCol = j
                        else:
                            if x[j] == 'NEWVARNAME':
                                newVarCol = j
                            else:
                                if x[j] == 'VARTYPE':
                                    varTypeCol = j
                                else:
                                    if x[j] == 'VARDEFAULT':
                                        varDefaultCol = j
                                    else:
                                        if x[j] == 'SELECT':
                                            selectCol = j
                                        else:
                                            if x[j] == 'DESCRIPTION':
                                                descriptionCol = j
        if not i==0:
            #assign variable values from appropriate column numbers  
            tvid = int(x[tvidCol])
            tableName = str(x[tableCol])
            varName = str(x[varCol])
            newVarName = str(x[newVarCol])
            #if newVarName is left blank then replace with varName
            if newVarName == '':
                newVarName = varName
            varType = str(x[varTypeCol])
            #varDefault
            try:
                int(x[varDefaultCol])
            except:
                try:
                    float(x[varDefaultCol])
                except:
                    varDefault = str(x[varDefaultCol])
                else:
                    varDefault = float(x[varDefaultCol])       
            else:
                varDefault = int(x[varDefaultCol])
            #select
            try:
                int(x[selectCol])
            except:
                select = str(x[selectCol])
            else:
                select = int(x[selectCol])

                          
            description = str(x[descriptionCol])
            #Start process of assigning appropriate types() to varDefault values
            #If variable type is not a string, character or nominal type() the change the type
            #Must either be related to a float or integer type
            if not varType == 'string' or not varType == 'character' or not varType == 'nominal':
                #If varType is integer, boolean or ordinal
                if varType == 'integer' or varType == 'boolean' or varType == 'dummy' or varType == 'ordinal' \
                   or varType == 'classint' or varType == 'count':
                    if varDefault == '':
                        varDefault = 0
                    else:
                        try:
                            int(varDefault)
                        except:
                            print 'Default value', varDefault, 'TABLENAME', tableName, 'VARNAME', varName, \
                                  'in DATA DICTIONARY TVID', tvid, 'cannot be converted to an integer'
                        else:
                            varDefault = int(varDefault)
                            
                #if varType is float or coninuous
                if  varType == 'float' or varType == 'continuous' or varType == 'proportion':
                    if varDefault == '':
                        varDefault = float(0)
                    else:
                        try:
                            float(varDefault)
                        except:
                            print 'Default value', varDefault, 'TABLENAME', tableName, 'VARNAME', varName, \
                                  'in DATA DICTIONARY TVID', tvid, 'cannot be converted to a float'
                        else:
                            varDefault = float(varDefault)
                        
                        
            #If the tableName has not been added as the primary key to the originalNameDict
            #Then by definition it has not yet been assigned to the newNameDict
            #Update these two dictionaries with the table names
            if not originalNameDict.has_key(tableName):
                originalNameDict.update({tableName:{}})
                newNameDict.update({tableName:{}})
            #If the variable name, varName has not yet been assigned as a key subdivision of tableName
            #Then    
            if not originalNameDict[tableName].has_key(varName):
                originalNameDict[tableName].update({varName:{'TVID':tvid,'NEWVARNAME':newVarName,'VARTYPE':varType, 'VARDEFAULT':varDefault, \
                                                             'SELECT':select,'DESCRIPTION':description}})
            else:
                #tableName in originalNameDict has duplicate variable names 
                print 'TABLE', tableName, 'has a duplicate VARNAME', varName, 'in data dictionary type 2'
                
            #Update the newVarName as a key in the newNameDict 
            #If newVarName is blank then replace blank with varName
            if newVarName == '':
                newVarName = varName    
            if not newNameDict[tableName].has_key(newVarName):
                newNameDict[tableName].update({newVarName:{'TVID':tvid,'VARNAME':varName, 'NEWVARNAME':varName,'VARTYPE':varType, \
                                                           'VARDEFAULT':varDefault,'SELECT':select,'DESCRIPTION':description}})
            else:
                #TableName in newNameDict has duplicate variable names
                print 'TABLE', tableName, 'has a duplicate NEWVARNAME', newVarName, 'TVID', tvid, 'in data dictionary type 2'
        i=i+1
    temp_file.close()
    return originalNameDict, newNameDict
