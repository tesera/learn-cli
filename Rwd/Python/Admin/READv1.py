'''
'''
from types import *
from operator import concat

import PRINTv1
import time

readErrorFilePath = r'E:\Python25\Admin\Error\ReadError.txt'
PRINTv1.deleteFileIfItExists(readErrorFilePath)

def writeToReadErrorFile(textLine):
    time.sleep(0.1)
    readErrorFile = open(readErrorFilePath,'a')
    print >> readErrorFile, textLine
    readErrorFile.close()
    return
  
PRINTv1.deleteFileIfItExists(readErrorFilePath)

def new_file_path(filepath, filename):
    FileKind = '.txt'
    newFilename = concat(filename, FileKind)
    newFilePath = concat(filepath, newFilename)
    return newFilePath

def read_entire_file_text_line_as_string(filepath, table_name):
    file_path = new_file_path(filepath, table_name)
    temp_file =open (file_path,'r')
    out_file=[]
    i=0
    for line in temp_file:
        #print i
        x = line.rstrip()
        out_file.append(x)
        return out_file

def read_single_line_as_string(newLine):
    #print i
    x = newLine.rstrip()
    return x

 
def data_dictionary(filepath, filename):
    dict_path = new_file_path(filepath, filename)
    '''
    Last Modified Jan 23, 2006
    Converted to following dictionary format:
    {('VariableName','TableName'):'Type'}
    where type is an integer, string or float
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
            key = (str(x[var_col]), str(x[table_col]))
            newline = {key:str(x[type_col])}
            outfile.update(newline)
        i=i+1
    temp_file.close()
    return outfile

def rebuild_data_dictionary_with_new_file_names(currentDatdic,dictHeader,currentDictTableName,newFilename):
    '''
    This routine builds a new dictionary from the current dictionary by essentialy replacing
    the current filenames with new file names - all other things remain the same. This allows users to use a
    single dictionary to access mutiple files.
    User's must supply a dictHeader with the variable names to be used in both dictionaries.
    '''
    newDict = {}
    for varName in dictHeader:
        newKeyName = (varName, newFilename)
        varValue = currentDatdic[(varName, currentDictTableName)]
        #print currentDictTableName, newKeyName, varValue
        newDict.update({newKeyName:varValue})
    return newDict


def get_dataDictionary_version_2_information(filepath, filename):
    '''
    Version 2 dictionary supplies the file header information in the
    dictionary and not in the data file. As a result the column numbers
    for each variable are identified.  This function then creates the
    standard datdic file, referred to below as the outfile, and another
    file that is used to create the header, referred to as the
    headerConstructionFile.  Both these files are returned to the main
    program in a tuple format, in the same order as just introduced.

    The get_header_for_version_2_dictionary_filetype(filetype, datheader) function can then
    be used to produce the header, which can then be appended to the datafile
    after it is first openned.

    The new header is then used with:
    read_csv_text_file_data_dict_version2(filepath,data_dict,table_name, header)
    to open the file.

    Created April, 2008.

    Other Notes - File Format - August 2009
    'Variable' is the variable name
    'Table' is the table in which the file data is to be found, without the file extension
    'Type' is the variable type - either integer, string or float
    'FileType' is the file extension, e.g. 'txt' without the dot, '.'
    'Column' is the order in which the variables occur (not the column number where the variable starts)
    'Description' is an open area where text may be entered; avoid using commas, ','


    
    '''
    dict_path = filepath + filename
    temp_file =open (dict_path,'r')
    outfile = {}
    headerConstructionFile = {}
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
                        else:
                            if x[j] == 'FileType':
                                file_type_col = j
                            else:
                                if x[j] == 'Column':
                                    column_col = j
                                else:
                                    if x[j] == 'Description':
                                        description_col = j
        if not i==0:
            #Create dictionary as per original type dictionaries.
            key = (str(x[var_col]), str(x[table_col]))
            newline = {key:str(x[type_col])}
            outfile.update(newline)
            #Create headerConstructionFile
            if not headerConstructionFile.has_key(x[file_type_col]):
                headerConstructionFile.update({x[file_type_col]:{}})
            if not headerConstructionFile[x[file_type_col]].has_key(x[column_col]):
                headerConstructionFile[x[file_type_col]].update({x[column_col]:{}})
            headerConstructionFile[x[file_type_col]][x[column_col]] = \
                    {'Variable':x[var_col],'Table':x[table_col]}            
        i=i+1
    temp_file.close()
    return (outfile, headerConstructionFile)

def get_header_for_version_2_dictionary_filetype(filetype, datheader):
    newHeader = []
    i = 0
    columnNos = datheader[filetype].keys()
    newColList = []
    #Convert coumn numbers to integers from strings
    for col in columnNos:
        newCol = int(col)
        newColList.append(newCol)
    #Sort the column numbers
    newColList.sort()
    #Convert sorted column numbers back to strings
    columnNos = []
    for col in newColList:
        newCol = str(col)
        columnNos.append(newCol)
    #Obtain variable names in the propper order
    for col in columnNos:
        varName = datheader[filetype][col]['Variable']
        newHeader.append(varName)
    return newHeader

def variable_types(x, var_name, data_dict, table_name):
    '''
    Last modified Jan 23, 2006 to match with changes in dictionary
    format.
    '''
    i=0
    end_i = len(data_dict)
    var_type = ''
    key = (var_name, table_name)
    if data_dict.has_key(key)==True:
        var_type = data_dict[key]
    else:
        print key, 'has no var_type'
        var_type = 'float'
#    if var_name == 'UNIT_IDENTITY_NUMBER':
#        print 'Yes_var_name'
#        if table_name == 'dat_LINKS':
#            print 'Yes_table'
#        if data_dict[i][0] == var_name:
#            print 'Yes_dict_var_name'
#        if data_dict[i][1] == table_name:
#            print 'Yes_dict_table_name'
#    print var_name, table_name, var_type
    return var_type

def read_csv_text_file(filepath,data_dict,table_name):
    '''
    Last modified Jan 23, 2006 to match with changes in dictionary
    format.
    '''

    # This module will read files created using PRINT_MODULE.print_csv().
    #
    file_path = new_file_path(filepath, table_name)
    temp_file =open (file_path,'r')
    out_file=[]
    i=0
    for line in temp_file:
        #print i
        out_file.append([])
        x = line.rstrip()
        x = x.split(',')
        #print 'Y', x
        end_j = len(x)
        j=0
        if i == 0:
            for j in range(0,end_j,1):
                x[j]=str(x[j]).lstrip()               
        else:
            for j in range(0,end_j,1):
                #if table_name == 'MEAS':
                    #print i,j, out_file[0][j], table_name
                vartype = variable_types(x[j], out_file[0][j], data_dict, table_name)
                if vartype == 'string':
                    x[j] = str(x[j])
                else:
                    try:
                        float(x[j])
                    except:
                        textLine = '1. Table Name Is %s' % table_name
                        writeToReadErrorFile(textLine)
                        textLine =  '1. Variable in column number %i can not be converted to a number' % (j+1)
                        writeToReadErrorFile(textLine)
                        textLine =  '1. Line number:' + str(i) + 'Variable:' + str(x[j])
                        writeToReadErrorFile(textLine)
                    if vartype == 'integer':
                        if x[j] == '':
                            textLine = '1a. Replacing variable with an integer value of -1'
                            writeToReadErrorFile(textLine)
                            x[j] = -1
                        else:
                            x[j] = int(float(x[j]))
                    if vartype == 'float':
                        if x[j] == '':
                            textLine = '1b. Replacing variable with a float value of 0.0'
                            writeToReadErrorFile(textLine)
                            x[j] = float(0)
                        else:
                            try:
                                float(x[j])
                            except:
                                print 'Read error row, column, value', i, j, x[j], line[0]
                            else:
                                x[j] = float(x[j])
        if not x == [ ]:
            #print x
            out_file[i]= x
        i=i+1
    print 'Check ReadError File in Admin Directory'
    return out_file

def read_csv_text_file_data_dict_version2(filepath,data_dict,table_name, header, delimitKind):
    '''
    This version deals with different kinds of delimmeted FILES.

    
    '''
    temp_file =open (filepath,'r')
    out_file = []
    out_file.append(header)
    i=1
    for line in temp_file:
#       print i
        out_file.append([])
        x = line.rstrip()
        if delimitKind == 'comma':
            x = x.split(',')
        else:
            if delimitKind == 'space':
                x = x.split()
        end_j = len(x)
        j=0
        for j in range(0,end_j,1):
            #print i,j, out_file[0][j], table_name
            vartype = variable_types(x[j], out_file[0][j], data_dict, table_name)
            if vartype == 'string':
                x[j] = str(x[j])
            else:
                try:
                    float(x[j])
                except:
                    print 'Variable number %i can not be converted to a number' % (j+1)
                    print  'Table name:', table_name, 'Line number:', i, 'Variable:', x[j]
                if vartype == 'integer':
                    x[j] = int(float(x[j]))
                if vartype == 'float':
                    if x[j] == '':
                        x[j] = float(0)
                    else:
                        x[j] = float(x[j])
        if not x == [ ]:
            #print x
            out_file[i]= x
        i=i+1
    return out_file


def read_csv_text_line_data_dict_version2(textline,data_dict,table_name, header, delimitKind):
    '''
    This version deals with different kinds of delimmeted TEXT LINES.
    
    '''
    out_file = []
    out_file.append(header)
    out_file.append([])
    x = textline.rstrip()
    if delimitKind == 'comma':
        x = x.split(',')
    else:
        if delimitKind == 'space':
            x = x.split()
    end_j = len(x)
    j=0
    for j in range(0,end_j,1):
        #print j, out_file[0][j], table_name
        vartype = variable_types(x[j], out_file[0][j], data_dict, table_name)
        if vartype == 'string':
            x[j] = str(x[j])
        else:
            try:
                float(x[j])
            except:
                print 'Variable number %i can not be converted to a number' % (j+1)
                print  'Table name:', table_name, 'Variable', j, 'Variable Value:', x[j]
            if vartype == 'integer':
                x[j] = int(float(x[j]))
            if vartype == 'float':
                if x[j] == '':
                    x[j] = float(0)
                else:
                    x[j] = float(x[j])
    if not x == [ ]:
        #print x
        out_file[1] = x
    return out_file


def convert_to_single_variable_key_dictionary(file_name,key_varname):
    '''
    This routine handles only single variable dictionaries.
    The non-key variables are recorded as a list, rather than
    as a dictionary where the variable names precede the variable
    expression.
    '''
    end_i = len(file_name)
    large_dict={}
    for i in range(0, end_i,1):
        end_j = len(file_name[i])
        new_list=[]
        for j in range(0,end_j,1):
            if file_name[0][j]== key_varname:
                key=file_name[i][j]
            else:
                new_list.append(file_name[i][j])
        small_dict = {key:new_list}
        large_dict.update(small_dict)
    return large_dict

def convert_to_compound_variable_key_dictionary(file_name,key_varnames):
    '''
    This routine enters the keys into a tuple format and then records
    the non-key variables in a list, rather than a dictionary contained
    a list where the variable names (the dictionary keys) precede the
    variable expression.
    '''
    end_i = len(file_name)
    large_dict={}
    for i in range(0, end_i,1):
        end_j = len(file_name[i])
        end_k = len(key_varnames)
        new_list=[]
        key_list=[]
        #print file_name[i]
        for j in range(0,end_j,1):
            flag = 'False'
            for k in range(0,end_k):
                if file_name[0][j]== key_varnames[k]:
                    key_list.append(file_name[i][j])
                    #print key_varnames[k], file_name[i][j]
                    flag = 'True'
            if flag == 'False':
                new_list.append(file_name[i][j])
                #print 'data',file_name[0][j], file_name[i][j]
        key_tuple = tuple(key_list)
        small_dict = {key_tuple:new_list}
        #print small_dict
        large_dict.update(small_dict)
    return large_dict

def convert_to_total_compound_variable_key_dictionary(file_name,key_varnames):
    '''
    This routine ensures that all non-key variables are entered in a
    dictionary format within a list where the first entry, the dictionary key,
    is the variable name, and the second entry, is the variable eexpression.
    '''

    end_i = len(file_name)
    large_dict={}
    for i in range(0, end_i,1):
        end_j = len(file_name[i])
        end_k = len(key_varnames)
        new_dict={}
        key_list=[]
        #print file_name[i]
        for j in range(0,end_j,1):
            flag = 'False'
            for k in range(0,end_k):
                if file_name[0][j]== key_varnames[k]:
                    ##Add the variable expression to the key list
                    key_list.append(file_name[i][j])
                    #print key_varnames[k], file_name[i][j]
                    flag = 'True'
            if flag == 'False':
                ##Add the dictionary {variable name:variable expression}
                ##to the variable list.
                new_dict.update({file_name[0][j]:file_name[i][j]})
                #print 'data',file_name[0][j], file_name[i][j]
        if len(key_list)>1:
            key_tuple = tuple(key_list)
        else:
            key_tuple = key_list[0]
        small_dict = {key_tuple:new_dict}
        #print small_dict
        large_dict.update(small_dict)
    return large_dict

def convert_new_line_to_dictionary(var_names,var_expr,data_dict,table_name):
    '''
    This subroutine assumes that the variable names have already been
    established in a list and a corresponding line of variable expressions
    has been established, but the variables have not been converted into their
    proper format in accordance with the data dictionary.  It returns dictionary
    items: {var_name:var_expr, ...}
    '''
    new_dict={}
    i=0
    for item in var_expr:
        var_type = variable_types(item, var_names[i], data_dict, table_name)
        if var_type == 'string':
            var_expr[i] = str(var_expr[i])
        else:
            if item == '':
                textLine = '2. module: convert_new_line_to_dictionary'
                writeToReadErrorFile(textLine)
                textLine = '2. Table name is:' + table_name
                writeToReadErrorFile(textLine)
                textLine = '2. Variable name is:' + var_names[i]
                writeToReadErrorFile(textLine)
                textLine = '2. Variable value set equal to 0'
                writeToReadErrorFile(textLine)
                var_expr[i] = '0'
            #print var_expr[i]
            if var_type == 'integer': var_expr[i] = int(float(var_expr[i]))
            if var_type == 'float': var_expr[i] = float(var_expr[i])
        new_dict.update({var_names[i]:var_expr[i]})
        i=i+1
    return new_dict

def get_unique_key_list(file_name,column_no):
    
    new_list = []
    i=0
    for item in file_name:
        if not i==0:
            if i==1:
                new_list.append(item[column_no])
            else:
                flag = 'false'
                for new_item in new_list:
                    if item[column_no]==new_item:
                        flag = 'true'
                        break
                if flag == 'false':
                    new_list.append(item[column_no])
        i=i+1
    return new_list

def given_key_find_and_read_csv_access_text_line(filepath,data_dict, table_name,key_values,key_names):
    '''
    This subroutine searches a file to find a record matching
    with a single variable key and converts that line into a
    list and returns that list in row 1, along with all of the
    variable names in row 0.
    '''
    # This module will read files created using PRINT_MODULE.print_csv().
    #
    file_path = new_file_path(filepath, table_name)
    temp_file =open (file_path,'r')
    out_file = [[],[]]
    i=0
    for line in temp_file:
#       print i
        x = line.rstrip()
        x = x.split(',')
        #print 'Y', x
        end_j = len(x)
        j=0
        if i == 0:
            for j in range(0,end_j,1):
                x[j]=str(x[j]).lstrip()
                if x[j] == key_name:
                    k=j
            out_file[0]=x
        else:
            vartype = variable_types(x[k], out_file[0][k], data_dict, table_name)
            if vartype == 'string':
                x[j] = str(x[j])
            else:
                if vartype == 'integer': x[k] = int(float(x[k]))
                if vartype == 'float': x[k] = float(x[k])
            if key_value == x[k]:
                for j in range(0,end_j,1):
                    vartype = variable_types(x[j], out_file[0][j], data_dict, table_name)
                    if vartype == 'string':
                        x[j] = str(x[j])
                    else:
                        if vartype == 'integer': x[j] = int(float(x[j]))
                        if vartype == 'float': x[j] = float(x[j])
                        out_file[1]=x
                        break
        i=i+1
    return out_file

def read_csv_text_line(var_labels,tline,data_dict, table_name):
    '''
    This module takes a line of unseparated text, splits it up according to
    comma delimitted breaks, removes end of line control characters, establishes
    variable types as recorded in dictionary, reads variables in appropriate format
    (string, float or integer) and returns a list with the first item (row 0) being the
    variable labels and the second item (row 1) being the variable values.
    '''
    # This module will read files created using PRINT_MODULE.print_csv().
    #
    
    out_file=[var_labels,[]] 
    #print out_file
    i=0
    k=0
    m=0
    #   print i
    x = tline.rstrip()
    x = x.split(',')
    #print x
    end_j = len(x)               
    for j in range(0,end_j,1):
        #print j, x[j], out_file[0][j]
        vartype = variable_types(x[j], out_file[0][j], data_dict, table_name)
        if vartype == 'string':
            x[j] = str(x[j])
        else:
            if vartype == 'integer':
                if x[j] == '':
                    x[j] = int(0)
                else:
                    x[j] = int(float(x[j]))
            if vartype == 'float':
                if x[j] == '':
                    x[j] = float(0)
                else:
                    x[j] = float(x[j])
    if not x == [ ]:
        out_file[1]= x
    return out_file
    
def read_csv_header_line_string_variables(text_line):
    '''
    This module takes the first line in a file with the variable names and
    converts it to a list of string variables.
    '''
    var_labels = text_line.rstrip()
    var_labels = var_labels.split(',')
    end_j = len(var_labels)
    for j in range(0,end_j,1):
        var_labels[j]=str(var_labels[j]).lstrip()               
    return var_labels

def read_csv_header_line_string_variables_from_file(filepath, filename):
    '''
    This module opens the file, takes the first line in a file
    with the variable names and converts it to a list of string variables.
    '''
    file_path = new_file_path(filepath, filename)
    temp_file = open(file_path,'r')
    for line in temp_file:
        text_line = line
        break
    temp_file.close()
    var_labels = text_line.rstrip()
    var_labels = var_labels.split(',')
    end_j = len(var_labels)
    for j in range(0,end_j,1):
        var_labels[j]=str(var_labels[j]).lstrip()               
    return var_labels

def read_csv_line_string_variables(header,text_line):
    '''
    This module takes the first line in a file with the variable names and
    converts it to a list of string variables.
    '''
    out_file=[header,[]]
    var_values = text_line.rstrip()
    var_values = var_values.split(',')
    end_j = len(var_values)
    for j in range(0,end_j,1):
        var_values[j]=str(var_values[j]).lstrip()
    out_file[1] = var_values
    return out_file

def convert_header_plus_variables_to_dictionary(new_list):
    new_dict = {}
    i=0
    for item in new_list[0]:
        new_dict.update({item:new_list[1][i]})
        i=i+1
    return new_dict

def get_unique_compound_key_list(file_name,key_varnames):
    key_list = []
    var_column = []
    end_key = len(key_varnames)
    i=0
    for item in file_name:
        if i==0:
            j=0
            for var_name1 in item:
                for var_name2 in key_varnames:
                    if var_name1 == var_name2:
                        var_column.append(j)
                j=j+1
        else:
            j=0
            temp_key =[]
            for var_value in item:
                for column in var_column:
                    if column == j:
                        temp_key.append(var_value)
                j=j+1
            if i==1:
                key_list.append(temp_key)
                #print temp_key
            else:
                flag = 'false'
                for old_key in key_list:
                    j=0
                    key_count = 0
                    for var_value in temp_key:
                        if temp_key[j]== old_key[j]:
                            key_count = key_count + 1
                        j=j+1
                    if key_count == end_key:
                        flag = 'true'
                if flag == 'false':
                    key_list.append(temp_key)
                    #print temp_key
        i=i+1
    return key_list

def get_compound_key_single_variable_list(KeyList,KeyVarnames,FileName,VarName):
    '''
    This subroutine uses a list of keys (KeyList as a list) and their respective labels(KeyVarnames as a list)
    in a given file (FileName)that is in a list format, and a single variable identified
    by its name (VarName as a string). It constructs a dictionary with the KeyList as keys
    (including the actual KeyVarnames which are added to the dictionary for decoding
    purposes)and the values associated with VarName in an associated list.
    '''
    new_dict = {}
    end_i = len(FileName[0])
    VarColumn = -1
    KeyColumn=[]
    for i in range(0,end_i):
        ##Get column number for list variable
        if VarName == FileName[0][i]:
            VarColumn = i
        ##Get column numbers for key names in order
        ##of occurrence in the file
        for item in KeyVarnames:
            if item == FileName[0][i]:
                KeyColumn.append(i)
    #print 'VarColumn', VarColumn, VarName
    #print 'KeyColumn', KeyColumn, KeyVarnames
    ##For items in KeyList - convert to tuple
    ##and initialize dictionary
    for item in KeyList:
        key = tuple(item)
        new_dict.update({key:[]})
    ##Add the actual KeyVarnames as another key in the dictionary    
    key = tuple(KeyVarnames)
    new_dict.update({key:[]})
    ##Get record length of file
    end_i = len(FileName)
    for i in range(0,end_i):
        ##identify key for each record
        key = []
        for j in KeyColumn:
            key.append(FileName[i][j])
        key = tuple(key)
        ##get new variable associated with key
        new_var = FileName[i][VarColumn]
        ##add new variable to dictionary given key
        new_dict[key].append(new_var)
    return new_dict 

def get_single_key_multpile_item_dictionary(KeyVarnames,FileName):
    '''
    Last Modified Jan 23, 2006
    This is a simpler version of the function:
    convert_to_total_compound_variable_key_dictionary(file_name,key_varnames)
    '
    A key list is provided identifying the field(s) in the primary key 
    (KeyList) along with a file in list format; the first line (line[0])
    providing the field names.  All fields are
    added to the dictionary associated with the key in the
    following format: {FieldName:FieldValue}.  The final dictionary format
    is as follows: {PrimaryKey1:{FieldNames:FieldValues,...},...}
    Oct 27, 2005
    '''
    NewDict={}
    header = FileName[0]
    i=0
    for line in FileName:
        if not i==0:
            NewKey = []
            j=0
            for Key in KeyVarnames:
                for item in header:
                    if item == Key:
                        NewKey.append(line[j])
                        j=j+1
            if j == 1:
                NewKey = NewKey[0]
            else:
                NewKey = tuple(NewKey)
            NewDict.update({NewKey:{}})
            j=0
            for item in header:
                NewDict[NewKey].update({item:line[j]})
                j=j+1
        i=i+1
    return NewDict

def get_dict_of_variable_values_for_key_item_in_file(filepath,table_name,data_dict,keyNames,keyValues,varNames):
    '''
    This routine opens a file identified at a certain file_path, identifies the header, identifies the column numbers
    associated with each of the keyNames and sets up a keyName:column number dictionary, identifies the column numbers
    associated with each of the varNames and sets up a varName:column number dictionary, runs through each line until
    it finds a match with the keyValues, and then gets the varValues associated with the varNames and puts them into
    a varDict, that is then returned to the main subroutine.
    '''
    file_path = new_file_path(filepath, tablename)
    new_file = open(file_path,'r')
    varColumns = []
    keyColumns = []
    varValuesDict = {}
    keyDict={}
    varDict={}
    targetDict = {}
    end_i = len(keyNames)
    ##Identify the keyValues associated with the keyNames; place in the targetDict
    for i in range(0,end_i,1):
        targetDict.update({keyNames[i]:keyValues[i]})
    i=0
    ##For each line in the new_file, look for the varValues associated with the varNames in the
    ##record where the keyValues are found.  Put the varNames and varValues in the varDict before
    ##returning it to the main subroutine.
    for line in new_file:
        if i==0:
            header = read_csv_header_line_string_variables(line)
            i=i+1
            for keys in keyNames:
                j=0
                for items in header:
                    if items == keys:
                        keyColumns.append(j)
                    j=j+1

            end_j = len(keyNames)
            for j in range(0,end_j,1):
                keyDict.update({keyNames[j]:keyColumns[j]})
                #print 'keyDict', keyDict
            for var in varNames:
                j=0
                for items in header:
                    if items == var:
                        varColumns.append(j)
                    j=j+1
            end_j = len(varNames)
            for j in range(0,end_j,1):
                varDict.update({varNames[j]:varColumns[j]})
                #print 'varDict', varDict
        else:
            new_line = read_csv_text_line(header,line,data_dict,table_name)
            flag = 'true'
            for keys in keyDict:
                #print keys, targetDict[keys],keyDict[keys],new_line[1][keyDict[keys]]
                if not targetDict[keys]==new_line[1][keyDict[keys]]:
                    flag = 'false'
                    break
            if flag == 'true':
                for var in varNames:
                    newVarValue = {var:new_line[1][varDict[var]]}
                    varValuesDict.update(newVarValue)
                break
    if varValuesDict == {}:
        print 'READ_BB_FILES'
        print 'get_dict_of_variable_values_for_key_item_in_file'
        print 'Returning empty dictionary'
    return varValuesDict
            
def get_two_level_key_multpile_item_dictionary(KeyVarnames1,KeyVarnames2,FileName):
    '''
    This is a simpler version of the function:
    convert_to_total_compound_variable_key_dictionary(file_name,key_varnames)
    '
    A key list is provided identifying the field(s) in the primary key 
    (KeyList) along with a file in list format; the first line (line[0])
    providing the field names.  The fields not in the primary key are
    added to the dictionary associated with the primary field in the
    following format: {FieldName:FieldValue}.  The final dictionary format
    is as follows: {PrimaryKey1:{FieldNames:FieldValues,...},...}
    Oct 27, 2005
    '''
    NewDict={}
    NewKeyCol1=[]
    NewKeyCol2=[]
    header = FileName[0]
    for var in KeyVarnames1:
        i=0
        for item in header:
            if var == item:
                NewKeyCol1.append(i)
            i=i+1
    for var in KeyVarnames2:
        i=0
        for item in header:
            if var == item:
                NewKeyCol2.append(i)
            i=i+1
    end_i = len(FileName)
    for i in range(1,end_i,1):
        NewKey1 = []
        NewKey2 = []
        for col in NewKeyCol1:
            NewKey1.append(FileName[i][col])
        for col in NewKeyCol2:
            NewKey2.append(FileName[i][col])
        NewKey1 = tuple(NewKey1)
        NewKey2 = tuple(NewKey2)
        if NewDict.has_key(NewKey1)== False:
            NewDict.update({NewKey1:{NewKey2:{}}})
        if NewDict[NewKey1].has_key(NewKey2)==False:
            NewDict[NewKey1].update({NewKey2:{}})
        j=0
        newLine = {}
        for item in FileName[i]:
            NewDict[NewKey1][NewKey2].update({header[j]:item})
            j=j+1
    return NewDict

def nested_key_multiple_item_dictionary(KeyVarnames,FileName):
    '''
    Created Jan 23, 2006
    Updated June 23, 2006
    
    This produces a dictionary as follows:
    
    A list of KeyVarnames is provided as follows:
    [KeyVar1, KeyVar2, KeyVar3, KeyVar4]
    ... up to 7 levels with each key being on a separate level.

    These are used to transform the dataset from a list format
    to a dictionary format as follows:

    {KeyVar1:{KeyVar2:{KeyVar3:{Var1:Value,Var2:Value...}}}}

    The items specified as keys are not repeated in the variable list.
    '''
    NewDict={}
    header = FileName[0]
    headerLength = len(header)
    #print header
    i=0
    for line in FileName:
        lineLength = len(line)
        if not i==0 and not line ==[]:
            j=0
            NKList=[]
            if not KeyVarnames == []:
                for Key in KeyVarnames:
                    k=0
                    for item in header:
                        if item == Key:
                            if j == 0:
                                if NewDict.has_key(line[k])==False:
                                    NewDict.update({line[k]:{}})
                                NKList.append(line[k])
                                j=j+1
                                break
                            else:
                                if j == 1:
                                    if NewDict[NKList[0]].has_key(line[k])==False:
                                        NewDict[NKList[0]].update({line[k]:{}})
                                    NKList.append(line[k])
                                    j=j+1
                                    break
                                else:
                                    if j == 2:
                                        if NewDict[NKList[0]][NKList[1]].has_key(line[k])==False:
                                            NewDict[NKList[0]][NKList[1]].update({line[k]:{}})
                                        NKList.append(line[k])
                                        j=j+1
                                        break
                                    else:
                                        if j == 3:
                                            if NewDict[NKList[0]][NKList[1]][NKList[2]].has_key(line[k])==False:
                                                NewDict[NKList[0]][NKList[1]][NKList[2]].update({line[k]:{}})
                                            NKList.append(line[k])
                                            j=j+1
                                            break
                                        else:
                                            if j == 4:
                                                if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]].has_key(line[k])==False:
                                                    NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]].update({line[k]:{}})
                                                NKList.append(line[k])
                                                j=j+1
                                                break
                                            else:
                                                if j == 5:
                                                    if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]].has_key(line[k])==False:
                                                        NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]].update({line[k]:{}})
                                                    NKList.append(line[k])
                                                    j=j+1
                                                    break
                                                else:
                                                    if j == 6:
                                                        if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]].has_key(line[k])==False:
                                                            NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]].update({line[k]:{}})
                                                        NKList.append(line[k])
                                                        j=j+1
                                                        break

                                                    
                        k=k+1
            k=0
            for item in header:
                flag = 'True'
                if not lineLength == headerLength:
                    flag = 'False'
                    print 'lineLangth:', lineLength, 'headerLength:',headerLength
                    print 'Header item not found in line while constructing dictionary'
                    print 'Item k', k, 'in header'
                    print header
                    print 'line:'
                    print line
                    print 'Line 965 in READv1'
                for key in KeyVarnames:
                    if key == item:
                        flag = 'False'
                        break
                if flag == 'True':
                    if j == 0:
                        NewDict.update({item:line[k]})
                    else:
                        if j == 1:
                            NewDict[NKList[0]].update({item:line[k]})
                        else:
                            if j == 2:
                                #print NKList[0], NKList[1], item, line[k]
                                NewDict[NKList[0]][NKList[1]].update({item:line[k]})
                            else:
                                if j == 3:
                                    NewDict[NKList[0]][NKList[1]][NKList[2]].update({item:line[k]})
                                else:
                                    if j == 4:
                                        NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]].update({item:line[k]})
                                    else:
                                        if j == 5:
                                            NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]].update({item:line[k]})
                                        else:
                                            if j == 6:
                                                NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]].update({item:line[k]})
                                            else:
                                                if j == 7:
                                                    NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]][NKList[6]].update({item:line[k]})
                k=k+1
        i=i+1
    return NewDict

def nested_key_multiple_list_dictionary(KeyVarnames,FileName):
    '''
    Created Jan 23, 2006
    Updated July 23, 2006
    
    This produces a dictionary as follows:
    
    A list of KeyVarnames is provided as follows:
    [KeyVar1, KeyVar2, KeyVar3, KeyVar4, KeyVar5, KeyVar6, KeyVar7]
    ... up to 4 levels with each key being on a separate level.

    These are used to transform the dataset from a list format
    to a dictionary format as follows (version 2 ends with a list,
    i.e. instead of {Var1,Value, ...} it is {Var1:[Value1,Value2...],
    Var2:[Value1,Value2,...],...}

    {KeyVar1:{KeyVar2:{KeyVar3:{Var1:[Values],Var2:[Values],...}}}}

    The items specified as keys are not repeated in the variable list.

    Update: March 15, 2007:
    Ian S Moss
    
    Note that this function previously included the word "multpile" instead
    of "multiple".

    

    '''
    NewDict={}
    header = FileName[0]
    i=0
    for line in FileName:
        if not i==0:
            j=0
            NKList=[]
            if not KeyVarnames == []:
                for Key in KeyVarnames:
                    k=0
                    for item in header:
                        if item == Key:
                            if j == 0:
                                if NewDict.has_key(line[k])==False:
                                    NewDict.update({line[k]:{}})
                                NKList.append(line[k])
                                j=j+1
                                break
                            else:
                                if j == 1:
                                    if NewDict[NKList[0]].has_key(line[k])==False:
                                        NewDict[NKList[0]].update({line[k]:{}})
                                    NKList.append(line[k])
                                    j=j+1
                                    break
                                else:
                                    if j == 2:
                                        if NewDict[NKList[0]][NKList[1]].has_key(line[k])==False:
                                            NewDict[NKList[0]][NKList[1]].update({line[k]:{}})
                                        NKList.append(line[k])
                                        j=j+1
                                        break
                                    else:
                                        if j == 3:
                                            if NewDict[NKList[0]][NKList[1]][NKList[2]].has_key(line[k])==False:
                                                NewDict[NKList[0]][NKList[1]][NKList[2]].update({line[k]:{}})
                                            NKList.append(line[k])
                                            j=j+1
                                            break
                                        else:
                                            if j == 4:
                                                if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]].has_key(line[k])==False:
                                                    NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]].update({line[k]:{}})
                                                NKList.append(line[k])
                                                j=j+1
                                                break
                                            else:
                                                if j == 5:
                                                    if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]].has_key(line[k])==False:
                                                        NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]].update({line[k]:{}})
                                                    NKList.append(line[k])
                                                    j=j+1
                                                    break
                                                else:
                                                    if j == 6:
                                                        if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]].has_key(line[k])==False:
                                                            NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]].update({line[k]:{}})
                                                        NKList.append(line[k])
                                                        j=j+1
                                                        break
                                                    

                                                
                        k=k+1
            k=0
            for item in header:
                flag = 'True'
                for key in KeyVarnames:
                    if key == item:
                        flag = 'False'
                        break
                if flag == 'True':
                    if j == 0:
                        if NewDict.has_key(item) == False:
                            NewDict.update({item:[]})
                        #print item, k
                        NewDict[item].append(line[k])
                    else:
                        if j == 1:
                            if NewDict[NKList[0]].has_key(item) == False:
                                NewDict[NKList[0]].update({item:[]})
                            NewDict[NKList[0]][item].append(line[k])
                        else:
                            if j == 2:
                                if NewDict[NKList[0]][NKList[1]].has_key(item) == False:
                                    NewDict[NKList[0]][NKList[1]].update({item:[]})
                                NewDict[NKList[0]][NKList[1]][item].append(line[k])
                            else:
                                if j == 3:
                                    if NewDict[NKList[0]][NKList[1]][NKList[2]].has_key(item) == False:
                                        NewDict[NKList[0]][NKList[1]][NKList[2]].update({item:[]})
                                    NewDict[NKList[0]][NKList[1]][NKList[2]][item].append(line[k])
                                else:
                                    if j == 4:
                                        if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]].has_key(item) == False:
                                            NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]].update({item:[]})
                                        NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][item].append(line[k])
                                    else:
                                        if j == 5:
                                            if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]].has_key(item) == False:
                                                NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]].update({item:[]})
                                            NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][item].append(line[k])
                                        else:
                                            if j == 6:
                                                if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]].has_key(item) == False:
                                                    NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]].update({item:[]})
                                                NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]][item].append(line[k])
                                            else:
                                                if j == 7:
                                                    if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]][NKList[6]].has_key(item) == False:
                                                        NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]][NKList[6]].update({item:[]})
                                                    NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]][NKList[6]][item].append(line[k])
                                            
                k=k+1
        i=i+1
    return NewDict
                    
def update_newTable_keys(keyList,newTable):
    '''
    This function checks for keys in the keyList to see if
    they are in the newTable dictionary.  If not the newTable is updated.
    The keyList provides the variables in the proper order
    according to a multi-level dictionary
    '''
    end_i = len(keyList)
    for i in range(0,end_i,1):
        if i == 0:
            key0 = keyList[0]
            if not newTable.has_key(key0):
                newTable.update({key0:{}})
        else:
            if i == 1:
                key1 = keyList[1]
                if not newTable[key0].has_key(key1):
                    newTable[key0].update({key1:{}})
            else:
                if i == 2:
                    key2 = keyList[2]
                    if not newTable[key0][key1].has_key(key2):
                        newTable[key0][key1].update({key2:{}})
                else:
                    if i == 3:
                        key3 = keyList[3]
                        if not newTable[key0][key1][key2].has_key(key3):
                            newTable[key0][key1][key2].update({key3:{}})
                    else:
                        if i == 4:
                            key4 = keyList[4]
                            if not newTable[key0][key1][key2][key3].has_key(key4):
                                newTable[key0][key1][key2][key3].update({key4:{}})
                        else:
                            if i == 5:
                                key5 = keyList[5]
                                if not newTable[key0][key1][key2][key3][key4].has_key(key5):
                                    newTable[key0][key1][key2][key3][key4].update({key5:{}})
                            else:
                                if i == 6:
                                    key6 = keyList[6]
                                    if not newTable[key0][key1][key2][key3][key4][key5].has_key(key6):
                                        newTable[key0][key1][key2][key3][key4][key5].update({key6:{}})
                            
    return newTable


def create_list_of_initial_values_for_corresponding_list_of_variable_names(varNameList, initialValue):
    '''
    This function produces a list of values that are all equal to the initialValue
    for each of the corresponding variable names in the varNameList
    '''
    initialValueList = []
    for varName in varNameList:
        initialValueList.append(initialValue)
    return initialValueList


def update_line_dictionary_and_assign_the_initial_value_to_each_item(varNameList, initialValueList, lineDict, instruction):
    '''
    This function produces a dictionary of values that are all equal to the initialValue
    for each of the corresponding variable names in the varNameList
    Potential instructions:
        INITIALIZE
        OVERWRITE
        REPLACE
        ADD
        SUBTRACT
        MULTIPLY
        DIVIDE
        SQUARE_THEN_ADD

    
    '''
    #If variable names are not in line dicttionary then they will be entered and set to 0
    end_i = len(varNameList)
    for i in range(0,end_i,1):
        varName = varNameList[i]
        initialValue = initialValueList[i]
        if not lineDict.has_key(varName):
            #By default this action completes an INITIALIZE instruction
            lineDict.update({varName:initialValue})
        else:
            if instruction == 'OVERWRITE' or instruction == 'REPLACE':
                lineDict[varName] = initialValue
            if instruction == 'ADD':
                lineDict[varName] = lineDict[varName] + initialValue
            if instruction == 'SUBTRACT':
                lineDict[varName] = lineDict[varName] - initialValue
            if instruction == 'MULTIPLY':
                lineDict[varName] = lineDict[varName] * initialValue
            if instruction == 'DIVIDE':
                lineDict[varName] = lineDict[varName] / initialValue
            if instruction == 'SQUARE_AND_ADD':
                lineDict[varName] = lineDict[varName] + initialValue**2
    return lineDict


def update_new_keys_in_multiple_item_dictionary_and_initialize_new_variables_and_values(oldDict,keyVarValueList,newVarNameList,newVarValueList, instruction):
    '''
    This routine

        1. Updates oldDict keys using variables in keyVarValueList listed in order hierarchy in the dictionary using the following function:
            update_newTable_keys(keyList,newTable); if the keys are already there it will not overwrite them
            
        2. Checks to see if the variable names listed in newVarNameList are in the old dictionary in association with the identified keyVarValues
            using the following function: initialize_new_multiple_item_dictionary_default_variable_names(newDictLine, newVarNameList);
            if the variable names are already there it will not overwrite them
            
        3. Updates the values associated with the variable names in the newVarNameList according to the instructions listed in the following function:
            update_new_variable_values_multiple_item_dictionary(oldDict, newVarNameList, instruction);
            the variable values in newVarValueList are used to update the variables in newVarNameList given the keyVarValues in keyVarValueList
        
    
    '''
    oldDict = update_newTable_keys(keyVarValueList,oldDict)
    end_i =len(keyVarValueList)
    nKeys = end_i
    if nKeys == 0:
        oldDict = update_new_variable_values_multiple_item_dictionary(oldDict, newVarNameList, newVarValueList, instruction)
    else:
        key0 = keyVarValueList[0]
        if nKeys == 1:
            oldDict[key0] = update_new_variable_values_multiple_item_dictionary(oldDict[key0], newVarNameList, newVarValueList, instruction)
        else:
            key1 = keyVarValueList[1]
            if nKeys == 2:
                oldDict[key0][key1] = update_new_variable_values_multiple_item_dictionary(oldDict[key0][key1], newVarNameList, newVarValueList, instruction)
            else:
                key2 = keyVarValueList[2]
                if nKeys == 3:
                    oldDict[key0][key1][key2] = update_new_variable_values_multiple_item_dictionary(oldDict[key0][key1][key2], newVarNameList, newVarValueList, instruction)
                else:
                    key3 = keyVarValueList[3]
                    if nKeys == 4:
                        oldDict[key0][key1][key2][key3] = update_new_variable_values_multiple_item_dictionary(oldDict[key0][key1][key2][key3], newVarNameList, newVarValueList, instruction)
                    else:
                        key4 = keyVarValueList[4]
                        if nKeys == 5:
                            oldDict[key0][key1][key2][key3][key4] = update_new_variable_values_multiple_item_dictionary(oldDict[key0][key1][key2][key3][key4], newVarNameList, newVarValueList, instruction)
                        else:
                            key5 = keyVarValueList[5]
                            if nKeys == 6:
                                oldDict[key0][key1][key2][key3][key4][key5] = update_new_variable_values_multiple_item_dictionary(oldDict[key0][key1][key2][key3][key4][key5], newVarNameList, newVarValueList, instruction)
                            else:
                                key6 = keyVarValueList[6]
                                if nKeys == 7:
                                    oldDict[key0][key1][key2][key3][key4][key5][key6] = update_new_variable_values_multiple_item_dictionary(oldDict[key0][key1][key2][key3][key4][key5][key6], newVarNameList, newVarValueList, instruction)       
        
    return oldDict



def initialize_new_multiple_item_dictionary_default_variable_names(newDictLine, newVarNameList):
    '''
    This routine checks a zero level (single line) dictionary to see if it includes the variable names.
    If not the variable is added to the 1 line dictionary.  This ensures that existing
    dictionary variables will not be overwritten.

    This routine is called from:

    update_new_keys_in_multiple_item_dictionary_and_initialize_new_variables_and_values

    October 14, 2010   
    '''
    for varName in newVarNameList:
        if not newDictLine.has_key(varName):
            #Note a zero is assigned but it could be any value
            newDictLine.update({varName:0})
    return varName


def update_new_keys_in_multiple_item_dictionary_and_initialize_new_line_dictionary_variables_and_values(oldDict,keyVarValueList,newVarNameList, initialValueList, instruction):
    '''
    This routine

        1. Updates oldDict keys using variables in keyVarValueList listed in order hierarchy in the dictionary using the following function:
            update_newTable_keys(keyList,newTable); if the keys are already there it will not overwrite them
            
        2. Updates a 1 line dictionary using:
            uupdate_new_variable_values_multiple_item_dictionary(newVarNameList, initialValueList, oldLineDict, instruction)
            
        3. Replaces the line dictionary
        
    
    '''
    oldDict = update_newTable_keys(keyVarValueList,oldDict)
    end_i =len(keyVarValueList)
    nKeys = end_i
    if nKeys == 0:
        oldLineDict = oldDict
        newVarValueDict = update_line_dictionary_and_assign_the_initial_value_to_each_item(newVarNameList, initialValueList, oldLineDict, instruction)
        oldDict = newVarValueDict
    else:
        key0 = keyVarValueList[0]
        if nKeys == 1:
            oldLineDict = oldDict[key0]
            newVarValueDict = update_line_dictionary_and_assign_the_initial_value_to_each_item(newVarNameList, initialValueList, oldLineDict, instruction)
            oldDict[key0] = newVarValueDict
        else:
            key1 = keyVarValueList[1]
            if nKeys == 2:
                oldLineDict = oldDict[key0][key1]
                newVarValueDict = update_line_dictionary_and_assign_the_initial_value_to_each_item(newVarNameList, initialValueList, oldLineDict, instruction)
                oldDict[key0][key1] = newVarValueDict
            else:
                key2 = keyVarValueList[2]
                if nKeys == 3:
                    oldLineDict = oldDict[key0][key1][key2]
                    newVarValueDict = update_line_dictionary_and_assign_the_initial_value_to_each_item(newVarNameList, initialValueList, oldLineDict, instruction)
                    oldDict[key0][key1][key2] = newVarValueDict
                else:
                    key3 = keyVarValueList[3]
                    if nKeys == 4:
                        oldLineDict = oldDict[key0][key1][key2][key3]
                        newVarValueDict = update_line_dictionary_and_assign_the_initial_value_to_each_item(newVarNameList, initialValueList, oldLineDict, instruction)
                        oldDict[key0][key1][key2][key3] = newVarValueDict
                    else:
                        key4 = keyVarValueList[4]
                        if nKeys == 5:
                            oldLineDict = oldDict[key0][key1][key2][key3][key4]
                            newVarValueDict = update_line_dictionary_and_assign_the_initial_value_to_each_item(newVarNameList, initialValueList, oldLineDict, instruction)
                            oldDict[key0][key1][key2][key3][key4] = newVarValueDict
                        else:
                            key5 = keyVarValueList[5]
                            if nKeys == 6:
                                oldLineDict = oldDict[key0][key1][key2][key3][key4][key5]
                                newVarValueDict = update_line_dictionary_and_assign_the_initial_value_to_each_item(newVarNameList, initialValueList, oldLineDict, instruction)
                                oldDict[key0][key1][key2][key3][key4][key5] = newVarValueDict
                            else:
                                key6 = keyVarValueList[6]
                                if nKeys == 7:
                                    oldLineDict = oldDict[key0][key1][key2][key3][key4][key5][key6]
                                    newVarValueDict = update_line_dictionary_and_assign_the_initial_value_to_each_item(newVarNameList, initialValueList, oldLineDict, instruction)
                                    oldDict[key0][key1][key2][key3][key4][key5][key6] = newVarValueDict
        
    return oldDict                                                                                                     
    



def get_list_of_key_variables(VarNames,VarDict):
    '''
    This extracts specific variables listed in VarNames
    from 0-level dictionary, and returns them as a list
    in the order listed in VarNames.
    March 29, 2006
    '''
    newList = []
    for var in VarNames:
        if not VarDict.has_key(var):
            print 'missing varName', var, 'in READv1.get_list_of_key_variables'
        else:
            if type(VarDict[var])==ListType:
                newVar = VarDict[var][0]
            else:
                newVar = VarDict[var]
            newList.append(newVar)
    return newList



def add_new_list_line_item_to_grand_list(myList, grandList):
    '''
    This takes a list item and makes a new list and then adds
    the new list to the grand list so that the resultant
    file structure is [[header][x1,x2,x3,..][...][...]] where the outside
    parenthesis denote the grand list and the inside ones denote
    the list that is to be added.  This routine is necessary because
    list items of a given initial name remain attached to that name in Python
    even when assigned another name (alias in this case).
    '''
    newItem = []
    for item in myList:
        newItem.append(item)
    grandList.append(newItem)
    return grandList
    
        
def check_for_varNames_in_dictionary(varNameList, dictionaryName):
    '''
    This checks for variable names at certain level in a dictionary.
    '''
    for varName in varNameList:
        if not dictionaryName.has_key(varName):
            dictionaryName.update({varName:0.0})
    return dictionaryName

def del_line_control_character_from_end_of_line(textline):
    newTextLine = ''
    listText = list(textline)
    end_i = len(listText)-1
    for i in range(0,end_i):
        newTextLine = newTextLine + listText[i]
    return newTextLine

def get_dataDictionary_version_3_information(filepath, filename):
    '''
    Version 3 dictionary supplies the file header information in the
    dictionary and not in the data file, and also it supplies the start
    column for each variable in the table. As a result the column numbers
    for each variable are identified.  This function then creates a non
    standard datdic file, dictTypeThree

    Created August 2009.

    File Format - August 2009
    'Variable' is the variable name
    'Table' is the table in which the file data is to be found, without the file extension
    'Type' is the variable type - either integer, string or float
    'ColumnNo is the order in which the variables occur
    'Column' is the first column in which the variable may be entered ('the last column can be figured out)
    'Description' is an open area where text may be entered; avoid using commas, ','

    Table is the first key
    ColumnNo is the second key
    
    '''
    dict_path = filepath + filename
    temp_file =open (dict_path,'r')
    outfile = {}
    headerConstructionFile = {}
    dictTypeThree = {}
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
                        else:
                            if x[j] == 'ColumnNo':
                                columnNo_col = j
                            else:
                                if x[j] == 'Description':
                                    description_col = j
                                else:
                                    if x[j] == 'Column':
                                        start_read_col = j
                                        
        if not i==0:
            #Create dictionaryTypeThree
            #key1 is table name, key 2 is column number (i.e. ordewr in which variables occur
            key1 = str(x[table_col])
            key2 = int(x[columnNo_col])          
            newline = {'Variable':x[var_col],'Type':x[type_col],'Column':int(x[start_read_col]),'Description':x[description_col]}
            if not dictTypeThree.has_key(key1):
                dictTypeThree.update({key1:{}})
            if not dictTypeThree[key1].has_key(key2):
                dictTypeThree[key1].update({key2:newline})
        i = i + 1
    return dictTypeThree

def get_dictionary_version_3_header_and_column_numbers(dictionaryTypeThree,tableName):
    startColumnList = []
    newHeader = []
    if not dictionaryTypeThree.has_key(tableName):
        print 'dictionaryTypeThree does not have the following table name: ', tableName
    columnOrder = dictionaryTypeThree[tableName].keys()
    columnOrder.sort()
    for col in columnOrder:
        newHeader.append(dictionaryTypeThree[tableName][col]['Variable'])
        startColumnList.append(dictionaryTypeThree[tableName][col]['Column'])                       
    return [newHeader, startColumnList]

def rebuild_data_dictionary_version_3_with_new_file_names(currentDatdic,currentDictTableName,newTableName):
    '''
    This routine builds a new dictionary from the current dictionary version 3 by essentialy replacing
    the current filenames with new file names - all other things remain the same. This allows users to use a
    single dictionary to access mutiple files.
    User's must supply a dictHeader with the variable names to be used in both dictionaries.
    '''
    newDict = {newTableName:{}}
    for colNo in currentDatdic[currentDictTableName]:
        varValue = currentDatdic[currentDictTableName][colNo]
        #print currentDictTableName, newKeyName, varValue
        newDict[newTableName].update({colNo:varValue})
    return newDict

def read_line_using_version_3_dictionary(readLine, dataDictVersionThree, tableName, tableHeader, varStartColumn):
    '''
    This routine takes a formatted statement and (A) breaks into a list, and (B) converts the list items to
    their proper format. It does it 1 line at a time. The line to be converted is a text string ending
    with control charachters '\n' in the last column.  The associated data dictionary is formatted according
    to data dictionary version 3.  The table name is the name of the table from which the data format
    (string, float or integer) must be interpreted.  The table header has been compiled from dataDict
    VersionThree and must be re-entered.  The varStartColumn indicates the first column in which a variable
    charachter or number may be entered (as a string) in the order that the variables have occurred. This
    has already been extracted from the dataDictionaryVersionThree.

    The input tables for this program were constructed in LigLifelinePlotTreeData_Aug_2009.xlsm
    These tables are data dictionary version 3:  PROGTLDICT.txt
    
    '''
    end_i = len(readLine)
    end_col = len(varStartColumn)
    colCount = 1
    varValue = ''
    varValueList = []
    newVarValueList = []
    nextCol = varStartColumn[colCount]
    #range end_i-1 to eleminate '\n' control charachter at end of line
    for i in range(0,end_i-1,1):
        varValue = varValue + readLine[i]
        #print i, colCount, nextCol, varValue
        if i == nextCol:
            varValueList.append(varValue)
            varValue = ''
            if colCount < end_col - 1:
                colCount = colCount + 1
                nextCol = varStartColumn[colCount]
            else:
                colCount = 999
    varValueList.append(varValue)
    end_i = len(varValueList)
    for i in range(0,end_i,1):
        varType = dataDictVersionThree[tableName][i+1]['Type']
        if varType == 'float':
            newVarValue = float(varValueList[i])
        else:
            if varType == 'integer':
                #print i
                newVarValue = int(float(varValueList[i]))
            else:
                newVarValue = varValueList[i].strip()
        newVarValueList.append(newVarValue)
        #print newVarValueList
            
    #print varValueList
    #print newVarValueList
    return [tableHeader,newVarValueList]

def update_dictionary_with_newLineDictionary_in_same_format(wholeDict,lineDict, nKeys):
    if nKeys <= 0:
        for varName in lineDict:
            newValue = lineDict[varName]
            wholeDict.update({varName:varValue})
    else:
        if nKeys <= 1:
            Key1 = lineDict.keys()
            Key1 = Key1[0]
            if not wholeDict.has_key(Key1):
                wholeDict.update({Key1:{}})
                for varName in lineDict[Key1]:
                    varValue = lineDict[Key1][varName]
                    wholeDict[Key1].update({varName:varValue})
        else:
            if nKeys <= 2:
                Key1 = lineDict.keys()
                Key1 = Key1[0]
                if not wholeDict.has_key(Key1):
                    wholeDict.update({Key1:{}})
                Key2 = lineDict[Key1].keys()
                Key2 = Key2[0]
                if not wholeDict[Key1].has_key(Key2):
                    wholeDict[Key1].update({Key2:{}})
                    for varName in lineDict[Key1][Key2]:
                        varValue = lineDict[Key1][Key2][varName]
                        wholeDict[Key1][Key2].update({varName:varValue})
            else:
                if nKeys <= 3:
                    Key1 = lineDict.keys()
                    Key1 = Key1[0]
                    if not wholeDict.has_key(Key1):
                        wholeDict.update({Key1:{}})
                    Key2 = lineDict[Key1].keys()
                    Key2 = Key2[0]
                    if not wholeDict[Key1].has_key(Key2):
                        wholeDict[Key1].update({Key2:{}})
                    Key3 = lineDict[Key1][Key2].keys()
                    Key3 = Key3[0]
                    if not wholeDict[Key1][Key2].has_key(Key3):
                        wholeDict[Key1][Key2].update({Key3:{}})
                        for varName in lineDict[Key1][Key2][Key3]:
                            varValue = lineDict[Key1][Key2][Key3][varName]
                            wholeDict[Key1][Key2][Key3].update({varName:varValue})
                else:
                    if nKeys <= 4:
                        Key1 = lineDict.keys()
                        Key1 = Key1[0]
                        if not wholeDict.has_key(Key1):
                            wholeDict.update({Key1:{}})
                        Key2 = lineDict[Key1].keys()
                        Key2 = Key2[0]
                        if not wholeDict[Key1].has_key(Key2):
                            wholeDict[Key1].update({Key2:{}})
                        Key3 = lineDict[Key1][Key2].keys()
                        Key3 = Key3[0]
                        if not wholeDict[Key1][Key2].has_key(Key3):
                            wholeDict[Key1][Key2].update({Key3:{}})
                        Key4 = lineDict[Key1][Key2][Key3].keys()
                        Key4 = Key4[0]
                        if not wholeDict[Key1][Key2][Key3].has_key(Key4):
                            wholeDict[Key1][Key2][Key3].update({Key4:{}})
                            for varName in lineDict[Key1][Key2][Key3][Key4]:
                                varValue = lineDict[Key1][Key2][Key3][Key4][varName]
                                wholeDict[Key1][Key2][Key3][Key4].update({varName:varValue})
                    else:
                        if nKeys <= 5:
                            Key1 = lineDict.keys()
                            Key1 = Key1[0]
                            if not wholeDict.has_key(Key1):
                                wholeDict.update({Key1:{}})
                            Key2 = lineDict[Key1].keys()
                            Key2 = Key2[0]
                            if not wholeDict[Key1].has_key(Key2):
                                wholeDict[Key1].update({Key2:{}})
                            Key3 = lineDict[Key1][Key2].keys()
                            Key3 = Key3[0]
                            if not wholeDict[Key1][Key2].has_key(Key3):
                                wholeDict[Key1][Key2].update({Key3:{}})
                            Key4 = lineDict[Key1][Key2][Key3].keys()
                            Key4 = Key4[0]
                            if not wholeDict[Key1][Key2][Key3].has_key(Key4):
                                wholeDict[Key1][Key2][Key3].update({Key4:{}})
                            Key5 = lineDict[Key1][Key2][Key3][Key4].keys()
                            Key5 = Key5[0]
                            if not wholeDict[Key1][Key2][Key3][Key4].has_key(Key5):
                                wholeDict[Key1][Key2][Key3][Key4].update({Key5:{}})
                                for varName in lineDict[Key1][Key2][Key3][Key4][Key5]:
                                    varValue = lineDict[Key1][Key2][Key3][Key4][Key5][varName]
                                    wholeDict[Key1][Key2][Key3][Key4][Key5].update({varName:varValue})
                        else:
                            if nKeys <= 6:
                                Key1 = lineDict.keys()
                                Key1 = Key1[0]
                                if not wholeDict.has_key(Key1):
                                    wholeDict.update({Key1:{}})
                                Key2 = lineDict[Key1].keys()
                                Key2 = Key2[0]
                                if not wholeDict[Key1].has_key(Key2):
                                    wholeDict[Key1].update({Key2:{}})
                                Key3 = lineDict[Key1][Key2].keys()
                                Key3 = Key3[0]
                                if not wholeDict[Key1][Key2].has_key(Key3):
                                    wholeDict[Key1][Key2].update({Key3:{}})
                                Key4 = lineDict[Key1][Key2][Key3].keys()
                                Key4 = Key4[0]
                                if not wholeDict[Key1][Key2][Key3].has_key(Key4):
                                    wholeDict[Key1][Key2][Key3].update({Key4:{}})
                                Key5 = lineDict[Key1][Key2][Key3][Key4].keys()
                                Key5 = Key5[0]
                                if not wholeDict[Key1][Key2][Key3][Key4].has_key(Key5):
                                    wholeDict[Key1][Key2][Key3][Key4].update({Key5:{}})
                                Key6 = lineDict[Key1][Key2][Key3][Key4][Key5].keys()
                                Key6 = Key6[0]
                                if not wholeDict[Key1][Key2][Key3][Key4][Key5].has_key(Key6):
                                    wholeDict[Key1][Key2][Key3][Key4][Key5].update({Key6:{}})
                                    for varName in lineDict[Key1][Key2][Key3][Key4][Key5][Key6]:
                                        varValue = lineDict[Key1][Key2][Key3][Key4][Key5][Key6][varName]
                                        wholeDict[Key1][Key2][Key3][Key4][Key5][Key6].update({varName:varValue})
                            else:
                                if nKeys <= 7:
                                    Key1 = lineDict.keys()
                                    Key1 = Key1[0]
                                    if not wholeDict.has_key(Key1):
                                        wholeDict.update({Key1:{}})
                                    Key2 = lineDict[Key1].keys()
                                    Key2 = Key2[0]
                                    if not wholeDict[Key1].has_key(Key2):
                                        wholeDict[Key1].update({Key2:{}})
                                    Key3 = lineDict[Key1][Key2].keys()
                                    Key3 = Key3[0]
                                    if not wholeDict[Key1][Key2].has_key(Key3):
                                        wholeDict[Key1][Key2].update({Key3:{}})
                                    Key4 = lineDict[Key1][Key2][Key3].keys()
                                    Key4 = Key4[0]
                                    if not wholeDict[Key1][Key2][Key3].has_key(Key4):
                                        wholeDict[Key1][Key2][Key3].update({Key4:{}})
                                    Key5 = lineDict[Key1][Key2][Key3][Key4].keys()
                                    Key5 = Key5[0]
                                    if not wholeDict[Key1][Key2][Key3][Key4].has_key(Key5):
                                        wholeDict[Key1][Key2][Key3][Key4].update({Key5:{}})
                                    Key6 = lineDict[Key1][Key2][Key3][Key4][Key5].keys()
                                    Key6 = Key6[0]
                                    if not wholeDict[Key1][Key2][Key3][Key4][Key5].has_key(Key6):
                                        wholeDict[Key1][Key2][Key3][Key4][Key5].update({Key6:{}})
                                    Key7 = lineDict[Key1][Key2][Key3][Key4][Key5][Key6].keys()
                                    Key7 = Key7[0]
                                    if not wholeDict[Key1][Key2][Key3][Key4][Key5][Key6].has_key(Key7):
                                        wholeDict[Key1][Key2][Key3][Key4][Key5][Key6].update({Key7:{}})
                                        for varName in lineDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7]:
                                            varValue = lineDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7][varName]
                                            wholeDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7].update({varName:varValue})
                            
    return wholeDict



def get_varmap(filepath, KeyVarname):
    '''
    This produces varmap with PROGVAR keys, these being the standard keys
    used in the ensueing programs
    
    Note that PRINTv1 has a function to convert a varmapDict
    into standard dictionary format.
    '''
    table_name = 'VARMAP'
    file_path = new_file_path(filepath, table_name)
    temp_file =open (file_path,'r')
    outFile = [[]]
    outList = []
    i = 0
    for line in temp_file:
        #print i
        x = line.rstrip()
        x = x.split(',')
        #print 'Y', x
        j=0
        #print end_j
        if len(x) == 6:
            for j in range(0,6,1):
                if j == 0:
                    outFile.append([])
                x[j]=str(x[j]).lstrip()
                outFile[i].append(x[j])
            i = i + 1
    j = 0
    k = 0
    #Delete [] from list
    
    #Find the column in which the ORDER is established
    for item in outFile[0]:
        if item == 'ORDER':
            orderColumn = j
        if item == 'DEFAULT':
            defaultColumn = j
        if item == 'TYPE':
            typeColumn = j
        j = j + 1
    #print j
    #Change the ORDER from text to integer
    i = 0
    for line in outFile:
        #print i,j
        #print line
        if not i == 0:
            if len(outFile[i])==6:
                a = int(outFile[i][orderColumn])
                outFile[i][orderColumn] = a
                vartype = outFile[i][typeColumn]
                if vartype == 'integer':
                    a = int(outFile[i][defaultColumn])
                    outFile[i][defaultColumn] = a
                if vartype == 'float':
                    a = float(outFile[i][defaultColumn])
                    outFile[i][defaultColumn] = a
        i = i + 1
    KeyVarnames = [KeyVarname]
    outDict = nested_key_multiple_item_dictionary(KeyVarnames,outFile)
    return outDict

def get_varmap_v2(filepath, KeyVarname, table_name):
    '''
    This produces varmap with PROGVAR keys, these being the standard keys
    used in the ensueing programs

    Only 1 KeyVarname can be identified and it must not be provided in a
    list format, i.e. do not use []
    
    Note that PRINTv1 has a function to convert a varmapDict
    into standard dictionary format.

    The general format for reading dictionaries is as follows:

    myvar_data_dict = READv1.get_varmap_v2(filepath, 'MYVAR' ,'VARMAP_CUMDIST')
    progvar_data_dict = READv1.get_varmap_v2(filepath, 'PROGVAR' ,'VARMAP_CUMDIST')
    order_data_dict = READv1.get_varmap_v2(filepath, 'PROGVAR' ,'VARMAP_CUMDIST')

    Associated files use the following READv1 function:

    read_csv_text_file_as_string_conversion(filepath,varmapDict,table_name)

    This was modified Feb 17, 2010

    
    '''
    file_path = new_file_path(filepath, table_name)
    temp_file =open (file_path,'r')
    outFile = []
    outList = []
    i = 0
    for line in temp_file:
        #print i
        x = line.rstrip()
        x = x.split(',')
        #print 'Y', x
        j=0
        #print end_j
        x_len = len(x)
        for j in range(0,x_len,1):
            if x_len > 0:
                if j == 0:
                    outFile.append([])
                x[j]=str(x[j]).lstrip()
                outFile[i].append(x[j])
        i = i + 1
    j = 0
    k = 0
    #Find the column in which the ORDER is established
    for item in outFile[0]:
        if item == 'ORDER':
            orderColumn = j
        if item == 'DEFAULT':
            defaultColumn = j
        if item == 'TYPE':
            typeColumn = j
        j = j + 1
    #print j
    #Change the ORDER from text to integer
    end_i = len(outFile)
    for i in range(0,end_i,1):
        if not i == 0:
            a = int(outFile[i][orderColumn])
            outFile[i][orderColumn] = a
            vartype = outFile[i][typeColumn]
            if vartype == 'integer':
                a = int(outFile[i][defaultColumn])
                outFile[i][defaultColumn] = a
            if vartype == 'float':
                a = float(outFile[i][defaultColumn])
                outFile[i][defaultColumn] = a
        i = i + 1
    KeyVarnames = [KeyVarname]
    outDict = nested_key_multiple_item_dictionary(KeyVarnames,outFile)
    return outDict


def get_new_varmap_header(varmapDictX):
    '''
    This creates a header file for the new program
    Note that PROGVAR must include any new variables
    that are to be added in the process and the ORDER
    in which they occur.  The varmapDict keys must
    represent the order in which the variable names are to occur.
    '''
    varmapHeader = []
    newHeaderDict = {}
    varmapKeys = varmapDictX.keys()
    varmapKeys.sort()
    for order in varmapKeys:
        newKey = varmapDictX[order]['PROGVAR']
        varmapHeader.append(newKey)
    return varmapHeader

def read_csv_text_file_as_string_conversion(filepath,varmapDict,table_name):
    '''
    This read file was developed for use with ExtractTheaderData.py
    as a general format for looking up variable names associated with a
    particular set, and then storing them in a list format for later
    conversion to a dictionary.  Before conversion.

    The varmapDict must have MYVAR as the key variable name

    '''

    # This module will read files created using PRINT_MODULE.print_csv().
    #
    file_path = new_file_path(filepath, table_name)
    temp_file =open (file_path,'r')
    out_file=[]
    initial_header = []
    new_header = []
    i=0
    for line in temp_file:
        #print i
        x = line.rstrip()
        x = x.split(',')
        #print 'Y', x
        end_j = len(x)
        j=0
        new_line = []
        if i == 0:
            for j in range(0,end_j,1):
                x[j]=str(x[j]).lstrip()
                initial_header.append(x[j])
                if varmapDict.has_key(x[j]):
                    newVarname = varmapDict[x[j]]['PROGVAR']
                    new_header.append(newVarname)
            if not new_header == []:
                out_file.append([])
                out_file[i] = new_header    
        else:
            for j in range(0,end_j,1):
                #print i,j, out_file[0][j], table_name
                varname = initial_header[j]
                if varmapDict.has_key(varname):
                    vartype = varmapDict[varname]['TYPE']
                    if vartype == 'string':
                        x[j] = str(x[j])
                    else:
                        try:
                            float(x[j])
                        except:
                            textLine = '1. Table Name Is %s' % table_name
                            writeToReadErrorFile(textLine)
                            textLine =  '1. Variable in column number %i can not be converted to a number' % (j+1)
                            writeToReadErrorFile(textLine)
                            textLine =  '1. Line number:' + str(i) + 'Variable:' + str(x[j])
                            writeToReadErrorFile(textLine)
                        if vartype == 'integer':
                            if x[j] == '':
                                textLine = '1a. Replacing variable with an integer value of -1'
                                writeToReadErrorFile(textLine)
                                x[j] = -1
                            else:
                                x[j] = int(float(x[j]))
                        if vartype == 'float':
                            if x[j] == '':
                                textLine = '1b. Replacing variable with a float value of 0.0'
                                writeToReadErrorFile(textLine)
                                x[j] = float(0)
                            else:         
                                x[j] = float(x[j])
                    new_line.append(x[j])    
            if not new_line == []:
                end_j = len(new_line)
                out_file.append([])
                for j in range(0,end_j,1):
                            a = new_line[j]
                            out_file[i].append(a)
        i=i+1
    print 'Check ReadError File in Admin Directory'
    return out_file

def read_csv_text_file_as_string_conversion_with_default_values(filepath,varmapDict,table_name):
    '''
    This read file was developed for use with ExtractTheaderData.py
    as a general format for looking up variable names associated with a
    particular set, and then storing them in a list format for later
    conversion to a dictionary.  Before conversion.

    The varmapDict must have MYVAR as the key variable name

    Default values are used instead of blanks!

    '''

    # This module will read files created using PRINT_MODULE.print_csv().
    #
    file_path = new_file_path(filepath, table_name)
    temp_file =open (file_path,'r')
    out_file=[]
    initial_header = []
    new_header = []
    i=0
    for line in temp_file:
        #print i
        x = line.rstrip()
        x = x.split(',')
        #print 'Y', x
        end_j = len(x)
        j=0
        new_line = []
        if i == 0:
            for j in range(0,end_j,1):
                x[j]=str(x[j]).lstrip()
                initial_header.append(x[j])
                if varmapDict.has_key(x[j]):
                    newVarname = varmapDict[x[j]]['PROGVAR']
                    new_header.append(newVarname)
                else:
                    print 'varmapDict key:', x[j], 'has no PROGVAR'
            if not new_header == []:
                out_file.append([])
                out_file[i] = new_header    
        else:
            for j in range(0,end_j,1):
                #print i,j, out_file[0][j], table_name
                varname = initial_header[j]
                if varmapDict.has_key(varname):
                    vartype = varmapDict[varname]['TYPE']
                    x[j] = x[j].strip()
                    if vartype == 'string':
                        if x[j] == '':
                            newVar = varmapDict[varname]['DEFAULT']
                            #print varname, newVar, varmapDict[varname]['DEFAULT']
                        else:
                            newVar = str(x[j])
                    else:
                        #try:
                        #    float(x[j])
                        #except:
                        #    textLine = '1. Table Name Is %s' % table_name
                        #    writeToReadErrorFile(textLine)
                        #    textLine =  '1. Variable in column number %i can not be converted to a number' % (j+1)
                        #    writeToReadErrorFile(textLine)
                        #    textLine =  '1. Line number:' + str(i) + 'Variable:' + str(x[j])
                        #    writeToReadErrorFile(textLine)
                        if vartype == 'integer':
                            if x[j] == '':
                                #textLine = '1a. Replacing variable with an integer value of -1'
                                #writeToReadErrorFile(textLine)
                                newVar = int(float(varmapDict[varname]['DEFAULT']))
                            else:
                                newVar = int(float(x[j]))
                        if vartype == 'float':
                            #print x[j]
                            if x[j] == '':
                                #textLine = '1b. Replacing variable with a float value of 0.0'
                                #writeToReadErrorFile(textLine)
                                newVar = float(varmapDict[varname]['DEFAULT'])
                            else:
                                #if x[j] == '#DIV/0!': print varname, j, x[j]
                                newVar = float(x[j])
                    new_line.append(newVar)    
            if not new_line == []:
                end_j = len(new_line)
                out_file.append([])
                for j in range(0,end_j,1):
                            a = new_line[j]
                            out_file[i].append(a)
        i=i+1
    print 'Check ReadError File in Admin Directory'
    return out_file



def read_csv_text_file_and_convert_to_multiple_item_dictionary(filepath,data_dict,table_name, KeyVarnames):
    '''
    Last modified Jan 23, 2006 to match with changes in dictionary
    format.
    '''

    # This module will read files created using PRINT_MODULE.print_csv().
    #
    file_path = new_file_path(filepath, table_name)
    temp_file =open (file_path,'r')
    newFile = temp_file.readlines()
    temp_file.close()
    out_file = []
    newDict = {}
    printi = 20000
    printCount = 1000000
    i=0
    end_k = len(newFile)
    print table_name, 'has', end_k, 'records'
    for k in range(0,end_k,1):
        line = newFile[0]
        #print i
        out_file.append([])
        x = line.rstrip()
        x = x.split(',')
        #print 'Y', x
        end_j = len(x)
        j=0
        if i == 0:
            for j in range(0,end_j,1):
                x[j]=str(x[j]).lstrip()        
            header = x
        else:
            for j in range(0,end_j,1):
                #print i,j, out_file[0][j], table_name
                vartype = variable_types(x[j], out_file[0][j], data_dict, table_name)
                if vartype == 'string':
                    x[j] = str(x[j])
                else:
                    try:
                        float(x[j])
                    except:
                        textLine = '1. Table Name Is %s' % table_name
                        writeToReadErrorFile(textLine)
                        textLine =  '1. Variable in column number %i can not be converted to a number' % (j+1)
                        writeToReadErrorFile(textLine)
                        textLine =  '1. Line number:' + str(i) + 'Variable:' + str(x[j])
                        writeToReadErrorFile(textLine)
                    if vartype == 'integer':
                        if x[j] == '':
                            textLine = '1a. Replacing variable with an integer value of -1'
                            writeToReadErrorFile(textLine)
                            x[j] = -1
                        else:
                            x[j] = int(float(x[j]))
                    if vartype == 'float':
                        if x[j] == '':
                            textLine = '1b. Replacing variable with a float value of 0.0'
                            writeToReadErrorFile(textLine)
                            x[j] = float(0)
                        else:         
                            x[j] = float(x[j])
        if not x == [] and not x == [ ]:
            out_file[i] = x
        if i == 20000:
            if printi == printCount:
                print printCount
                printCount = printCount + 1000000
            printi = printi + 20000
            newDict = additive_nested_key_multiple_item_dictionary(newDict,KeyVarnames,out_file)
            out_file = []
            out_file.append(header)
            i = 0
        i=i+1
        del newFile[0]
    if len(out_file) > 1:
        newDict = additive_nested_key_multiple_item_dictionary(newDict,KeyVarnames,out_file)
    print 'Check ReadError File in Admin Directory'
    return [header, newDict]

def additive_nested_key_multiple_item_dictionary(NewDict,KeyVarnames,FileName):
    '''
    Created Jan 23, 2006
    Updated June 23, 2006
    
    This produces a dictionary as follows:
    
    A list of KeyVarnames is provided as follows:
    [KeyVar1, KeyVar2, KeyVar3, KeyVar4]
    ... up to 7 levels with each key being on a separate level.

    These are used to transform the dataset from a list format
    to a dictionary format as follows:

    {KeyVar1:{KeyVar2:{KeyVar3:{Var1:Value,Var2:Value...}}}}

    The items specified as keys are not repeated in the variable list.
    '''
    header = FileName[0]
    headerLength = len(header)
    #print header
    i=0
    for line in FileName:
        lineLength = len(line)
        if not i==0 and not line ==[]:
            j=0
            NKList=[]
            if not KeyVarnames == []:
                for Key in KeyVarnames:
                    k=0
                    for item in header:
                        if item == Key:
                            if j == 0:
                                if NewDict.has_key(line[k])==False:
                                    NewDict.update({line[k]:{}})
                                NKList.append(line[k])
                                j=j+1
                                break
                            else:
                                if j == 1:
                                    if NewDict[NKList[0]].has_key(line[k])==False:
                                        NewDict[NKList[0]].update({line[k]:{}})
                                    NKList.append(line[k])
                                    j=j+1
                                    break
                                else:
                                    if j == 2:
                                        if NewDict[NKList[0]][NKList[1]].has_key(line[k])==False:
                                            NewDict[NKList[0]][NKList[1]].update({line[k]:{}})
                                        NKList.append(line[k])
                                        j=j+1
                                        break
                                    else:
                                        if j == 3:
                                            if NewDict[NKList[0]][NKList[1]][NKList[2]].has_key(line[k])==False:
                                                NewDict[NKList[0]][NKList[1]][NKList[2]].update({line[k]:{}})
                                            NKList.append(line[k])
                                            j=j+1
                                            break
                                        else:
                                            if j == 4:
                                                if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]].has_key(line[k])==False:
                                                    NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]].update({line[k]:{}})
                                                NKList.append(line[k])
                                                j=j+1
                                                break
                                            else:
                                                if j == 5:
                                                    if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]].has_key(line[k])==False:
                                                        NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]].update({line[k]:{}})
                                                    NKList.append(line[k])
                                                    j=j+1
                                                    break
                                                else:
                                                    if j == 6:
                                                        if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]].has_key(line[k])==False:
                                                            NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]].update({line[k]:{}})
                                                        NKList.append(line[k])
                                                        j=j+1
                                                        break

                                                    
                        k=k+1
            k=0
            #print NewDict.keys()
            for item in header:
                flag = 'True'
                if not lineLength == headerLength:
                    flag = 'False'
                    print 'Header item not found in line while constructing dictionary'
                    print 'Item k', k, 'in header'
                    print header
                    print 'line:'
                    print line
                    print 'Line 965 in READv1'
                for key in KeyVarnames:
                    if key == item:
                        flag = 'False'
                        break
                if flag == 'True':
                    if j == 0:
                        NewDict.update({item:line[k]})
                    else:
                        if j == 1:
                            NewDict[NKList[0]].update({item:line[k]})
                        else:
                            if j == 2:
                                #print NKList[0], NKList[1], item, line[k]
                                NewDict[NKList[0]][NKList[1]].update({item:line[k]})
                            else:
                                if j == 3:
                                    NewDict[NKList[0]][NKList[1]][NKList[2]].update({item:line[k]})
                                else:
                                    if j == 4:
                                        NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]].update({item:line[k]})
                                    else:
                                        if j == 5:
                                            NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]].update({item:line[k]})
                                        else:
                                            if j == 6:
                                                NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]].update({item:line[k]})
                                            else:
                                                if j == 7:
                                                    NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]][NKList[6]].update({item:line[k]})
                k=k+1
        i=i+1
    return NewDict

def update_dictionary_with_newDictionary_in_same_format(masterDict,tempDict, keyVarnames):
    '''
    Created December 14, 2010
    A temporary dictionary with the same key variable name structure as the master dictionary
    is added to the master dictionary
    '''
    nKeys = len(keyVarnames)
    if nKeys <= 0:
        for varName in tempDict:
            newValue = tempDict[varName]
            if not masterDict[Key1].has_key(varName):
                masterDict.update({varName:varValue})
    else:
        if nKeys >= 1:
            for Key1 in tempDict:
                if not masterDict.has_key(Key1):
                    masterDict.update({Key1:{}})
                if nKeys == 1:
                    for varName in tempDict[Key1]:
                        varValue = tempDict[Key1][varName]
                        if not masterDict[Key1].has_key(varName):
                            masterDict[Key1].update({varName:varValue})
                else:
                    if nKeys >= 2:
                        for Key2 in tempDict[Key1]:
                            if not masterDict[Key1].has_key(Key2):
                                masterDict[Key1].update({Key2:{}})
                            if nKeys == 2:
                                for varName in tempDict[Key1][Key2]:
                                    varValue = tempDict[Key1][Key2][varName]
                                    if not masterDict[Key1][Key2].has_key(varName):
                                        masterDict[Key1][Key2].update({varName:varValue})
                            else:
                                if nKeys >= 3:
                                    for Key3 in tempDict[Key1][Key2]:
                                        if not masterDict[Key1][Key2].has_key(Key3):
                                            masterDict[Key1][Key2].update({Key3:{}})
                                        if nKeys == 3:
                                            for varName in tempDict[Key1][Key2][Key3]:
                                                varValue = tempDict[Key1][Key2][Key3][varName]
                                                if not masterDict[Key1][Key2][Key3].has_key(varName):
                                                    masterDict[Key1][Key2][Key3].update({varName:varValue})
                                        else:
                                            if nKeys >= 4:
                                                for Key4 in tempDict[Key1][Key2][Key3]:
                                                    if not masterDict[Key1][Key2][Key3].has_key(Key4):
                                                        masterDict[Key1][Key2][Key3].update({Key4:{}})
                                                    if nKeys == 4:
                                                        for varName in tempDict[Key1][Key2][Key3][Key4]:
                                                            varValue = tempDict[Key1][Key2][Key3][Key4][varName]
                                                            if not masterDict[Key1][Key2][Key3][Key4].has_key(varName):
                                                                masterDict[Key1][Key2][Key3][Key4].update({varName:varValue})
                                                    else:
                                                        if nKeys >= 5:
                                                            for Key5 in tempDict[Key1][Key2][Key3][Key4]:
                                                                if not masterDict[Key1][Key2][Key3][Key4].has_key(Key5):
                                                                    masterDict[Key1][Key2][Key3][Key4].update({Key5:{}})
                                                                if nKeys == 5:
                                                                    for varName in tempDict[Key1][Key2][Key3][Key4][Key5]:
                                                                        varValue = tempDict[Key1][Key2][Key3][Key4][Key5][varName]
                                                                        if not masterDict[Key1][Key2][Key3][Key4][Key5].has_key(varName):
                                                                            masterDict[Key1][Key2][Key3][Key4][Key5].update({varName:varValue})
                                                                else:
                                                                    if nKeys >= 6:
                                                                        for Key6 in tempDict[Key1][Key2][Key3][Key4][Key5]:
                                                                            if not masterDict[Key1][Key2][Key3][Key4][Key5].has_key(Key6):
                                                                                masterDict[Key1][Key2][Key3][Key4][Key5].update({Key6:{}})
                                                                            if nKeys == 6:
                                                                                for varName in tempDict[Key1][Key2][Key3][Key4][Key5][Key6]:
                                                                                    varValue = tempDict[Key1][Key2][Key3][Key4][Key5][Key6][varName]
                                                                                    if not masterDict[Key1][Key2][Key3][Key4][Key5][Key6].has_key(varName):
                                                                                        masterDict[Key1][Key2][Key3][Key4][Key5][Key6].update({varName:varValue})
                                                                            else:
                                                                                if nKeys >= 7:
                                                                                    for Key7 in tempDict[Key1][Key2][Key3][Key4][Key5][Key6]:
                                                                                        if not masterDict[Key1][Key2][Key3][Key4][Key5][Key6].has_key(Key7):
                                                                                            masterDict[Key1][Key2][Key3][Key4][Key5][Key6].update({Key7:{}})
                                                                                        if nKeys == 7:
                                                                                            for varName in tempDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7]:
                                                                                                varValue = tempDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7][varName]
                                                                                                if not masterDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7].has_key(varName):
                                                                                                    masterDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7].update({varName:varValue})                            
    return masterDict
