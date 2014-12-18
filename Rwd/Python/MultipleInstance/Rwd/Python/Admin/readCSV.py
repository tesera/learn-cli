from fileUtilities import newFilePath, newFilePath_v2

def read_csv_text_file(filepath,table_name):
    '''
    Last modified Jan 23, 2006 to match with changes in dictionary
    format.
    '''

    # This module will read files created using PRINT_MODULE.print_csv().
    #
    file_path = newFilePath(filepath, table_name)
    temp_file =open (file_path,'r')
    out_file=[]
    i=0
    for line in temp_file:
        #print i
        x = line.rstrip()
        x = x.split(',')
        out_file.append(x)
    temp_file.close()
    return out_file

def read_csv_text_file_v2(filepath,table_name, fileExtension):
    '''
    Last modified Jan 23, 2006 to match with changes in dictionary
    format.
    '''

    # This module will read files created using PRINT_MODULE.print_csv().
    #
    file_path = newFilePath_v2(filepath, table_name, fileExtension)
    temp_file =open (file_path,'r')
    out_file=[]
    i=0
    for line in temp_file:
        #print i
        x = line.rstrip()
        if not line == []:
            out_file.append([])
            line = line.replace('"','').strip()
            x = x.split(',')
            for item in x:
                y = item.replace('"','').strip()
                out_file[i].append(y)
            i = i + 1
    temp_file.close()
    return out_file
