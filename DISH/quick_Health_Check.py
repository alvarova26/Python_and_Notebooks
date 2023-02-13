###############################################################################################################################################
########################################     IMPORTS     ######################################################################################
###############################################################################################################################################
import pandas as pd
import numpy as np
import requests
from datetime import datetime

###############################################################################################################################################
########################################     DEFINE FUNCITIONS     ############################################################################
###############################################################################################################################################
def open_file(my_file_path, flag='csv'):
    '''
    Function:   
        + Opens a csv or excel file and converts it into a pandas dataframe with all fields read as string (except NaN)
    Input:
        + my_file_path  => Path of the file
    Output:
        + my_file_as_df => Pandas dataframe
    '''

    # Variable control
    assert isinstance(my_file_path, str), 'The path to the file must be as string'
    assert len(my_file_path) > 0, 'Path is empty'
    assert isinstance(flag, str), 'Flag must be a string (csv, xls or txt in this version of the function)'
    assert (flag == 'csv') or (flag == 'xls') or (flag == 'txt'), 'Flag must be csv, xls or txt in this version of the function'

    # Code
    if flag == 'csv':
        try:
            #with open(my_file_path) as my_file: # Opening this way it is not necessary to close the file to release resources
            my_file_as_df = pd.read_csv(my_file_path, dtype=str)
            return my_file_as_df
        except:
            print('Something went wrong @open_file => flag == csv')
    elif flag == 'xls':
        try:
            #with open(my_file_path) as my_file: # Opening this way it is not necessary to close the file to release resources
            my_file_as_df = pd.read_excel(my_file_path)
            return my_file_as_df   
        except:
            print('Something went wrong @open_file => flag == xls')
    elif flag == 'txt':
        try:
            with open(my_file_path,'r') as my_file: # Opening this way it is not necessary to close the file to release resources
                my_file_as_txt = my_file.readlines()
                print("file loaded")
            return my_file_as_txt
        except:
            print('Something went wrong @open_file => flag == txt')
    else:
        print('Flag must be csv, xls or txt in this version of the function')
        return -1


###############################################################################################################################################
########################################     LOAD SOURCE FILES     ############################################################################
###############################################################################################################################################
#path_to_vm_url = '/tmp/vm_url.txt'
#path_to_vm_url = 'vm_url.txt'
path_to_vm_url = 'vm_url_csv.csv'

###############################################################################################################################################
########################################     DATA MANIPULATION     ############################################################################
###############################################################################################################################################
#### vm_url File
#vm_url_txt = open_file(path_to_vm_url, flag='txt')
vm_url_df = open_file(path_to_vm_url, flag='csv')

for i in range(len(vm_url_df)):
    try:
        res = requests.get(vm_url_df.vm_url[i], timeout=3)
        print(res.status_code)
        print(res)
    except requests.exceptions.RequestException as e:
        print("connection_error")


