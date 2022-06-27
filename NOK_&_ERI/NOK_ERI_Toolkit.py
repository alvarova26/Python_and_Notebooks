import pandas as pd
import numpy as np
import scipy.stats as st
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
import math
from bs4 import BeautifulSoup
from yahooquery import Ticker
import requests
from urllib.request import urlopen
import json
from datetime import datetime


###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
########################################     General/ Common Functions     ####################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

###############################################################################################################################################
def open_file(my_file_path):
    '''
    Function:   
        + Opens a file and converts it into a list of strings
    Input:
        + my_file_path                  => Path of the file
    Output:
        + my_file_as_list_of_strings    => List of the strings where each item is a line of the txt file
    '''
    
    # Variable control
    assert isinstance(my_file_path, str), 'The path to the file must be as string'
    assert len(my_file_path) > 0, 'Path is empty'

    # Code
    with open(my_file_path) as my_file:                     # Opening this way it is not necessary to close the file to release resources
        my_file_as_list_of_strings = my_file.readlines()    # Reads the entire file as a list, where each eleme is a string corresponding
                                                            # to a line 
    
    return my_file_as_list_of_strings

###############################################################################################################################################
def string_search_nok(file, start_idx, str):
    '''
    Function:   Searches a substring passed as argument, in the file (list of strings)
    Input:      File as list of strings, index for starting the search and the substring to look up for
    Output:     Index of the list of strings where the substring was found and position inside the string
    '''
    idx = start_idx                                             # Sets the startin index to a local variable
    pos =  file[idx].find(str)                                  # Looks for the string in the line. Returns the position if found, -1 if not 
    if file[idx].find('COMMAND EXECUTED') >= 0: pos = 999       # if COMMAND EXECUTED found, pos = 999 (code)

    while (pos < 0) and (idx < len(file)-1) and (not pos == 999):
        idx = idx + 1                                           # Increments the indext to read the next line
        pos =  file[idx].find(str)                              # Looks for the string in the line. Returns the position if found, -1 if not
        if file[idx].find('COMMAND EXECUTED') >=0: pos = 999    # if COMMAND EXECUTED found, pos = 999 (code)
   
    return idx, pos

###############################################################################################################################################
def string_search_eri(file, start_idx, str):
    '''
    Function:   Searches a substring passed as argument, in the file (list of strings)
    Input:      File as list of strings, index for starting the search and the substring to look up for
    Output:     Index of the list of strings where the substring was found and position inside the string
    '''
    idx = start_idx                                             # Sets the startin index to a local variable
    pos = file[idx].find(str)                                   # Looks for the string in the line. Returns the position if found, -1 if not 
    if (file[idx].find('END') >= 0): pos = 999                  # if 'END' found => 999 (code)
    if (file[idx].find('EXIT') >= 0): pos = 998                 # if 'EXIT' found => 998 (code)

    while (pos < 0) and (idx < len(file)-1) and (not pos == 999) and (not pos == 998):
        idx = idx + 1                                           # Increments the indext to read the next line
        pos = file[idx].find(str)                               # Looks for the string in the line. Returns the position if found, -1 if not
        if (file[idx].find('END') >= 0): pos = 999              # if 'END' found => 999 (code)
        if (file[idx].find('EXIT') >= 0): pos = 998             # if 'EXIT' found => 998 (code)
   
    return idx, pos

###############################################################################################################################################
def string_search_nok_n_max(file, start_idx, str, n_max_lines):
    '''
    Function:   Searches a substring passed as argument, in the file (list of strings)
    Input:      File as list of strings, index for starting the search, the substring to look up for and the maximum number of lines to search
    Output:     Index of the list of strings where the substring was found and position inside the string
    '''
    idx = start_idx                                             # Sets the starting index to a local variable
    n_max = n_max_lines                                         # Sets the maximum number of line to shearch the string
    pos =  file[idx].find(str)                                  # Looks for the string in the line. Returns the position if found, -1 if not 
    if file[idx].find('COMMAND EXECUTED') >= 0: pos = 999       # if COMMAND EXECUTED found, pos = 999 (code)

    while (pos < 0) and (idx < len(file)-1) and (not pos == 999) and (n_max > 0):
        idx = idx + 1                                           # Increments the indext to read the next line
        n_max = n_max - 1                                       # Decrements the number of lines remaining to search
        pos =  file[idx].find(str)                              # Looks for the string in the line. Returns the position if found, -1 if not
        if file[idx].find('COMMAND EXECUTED') >=0: pos = 999    # if COMMAND EXECUTED found, pos = 999 (code)
   
    return idx, pos

###############################################################################################################################################
def string_search_nok_n_lines(my_file, sub_str, start_idx, n_max_lines=None):
    '''
    Function:   
        + Trys to find a substring in a list of strings (a txt file converted to a list of strings)
    Arguments:      
        + my_file       => logfile as list of strings (each element of the list is a string equivalent to each line of the original txt file)
        + sub_str       => substring to look for in each element of the list (aka  line of the txt file)
        + start_idx     => index from where the search will start 
        + n_max_lines   => max number of lines to look for the substring (if not passed - aka = None - the search has no limit of lines)
    Output:     
        + idx           => current index of the list (after running the function, it could be different to the start_idx)
        + pos           => if pos < 0       => the substring was not found
                        => if pos >= 0      => position in the string where the substring was found
                        => if pos == 999    => code to identify that 'COMMAND EXECUTED' was found
    '''
    
    # Variable control
    assert len(my_file) > 0, 'File is empty'
    assert isinstance(my_file, list), 'Index must be list of strings'
    assert isinstance(start_idx, int), 'Index must be int'
    assert start_idx >= 0, 'Index must be grather than or equal to zero'
    assert isinstance(sub_str, str), 'Substring to look for must be string'
    if (not n_max_lines == None):
        assert isinstance(n_max_lines, int), 'Max number of lines must be int'
        assert n_max_lines >= 1, 'Max number of lines to look for the substring must be grather than or equal to one'
        assert n_max_lines <= (len(my_file)-start_idx), 'Max number of lines to look for the substring must less than the remaining lines in the file'

    # Code
    if (n_max_lines == None):
        idx = start_idx                                             # Sets the starting index to a local variable
        pos =  my_file[idx].find(sub_str)                           # Looks for the string in the line. Returns the position if found, -1 if not 
        if my_file[idx].find('COMMAND EXECUTED') >= 0: pos = 999    # if COMMAND EXECUTED found, pos = 999 (code)

        while (pos < 0) and (idx < len(my_file)-1) and (not pos == 999):
            idx = idx + 1                                           # Increments the indext to read the next line
            pos =  my_file[idx].find(sub_str)                       # Looks for the string in the line. Returns the position if found, -1 if not
            if my_file[idx].find('COMMAND EXECUTED') >=0: pos = 999 # if COMMAND EXECUTED found, pos = 999 (code)
    else:
        idx = start_idx                                             # Sets the starting index to a local variable
        n_max = n_max_lines                                         # Sets the maximum number of line to shearch the string
        pos =  my_file[idx].find(sub_str)                           # Looks for the string in the line. Returns the position if found, -1 if not 
        if my_file[idx].find('COMMAND EXECUTED') >= 0: pos = 999    # if COMMAND EXECUTED found, pos = 999 (code)

        while (pos < 0) and (idx < len(my_file)-1) and (not pos == 999) and (n_max > 0):
            idx = idx + 1                                           # Increments the indext to read the next line
            n_max = n_max - 1                                       # Decrements the number of lines remaining to search
            pos =  my_file[idx].find(sub_str)                       # Looks for the string in the line. Returns the position if found, -1 if not
            if my_file[idx].find('COMMAND EXECUTED') >=0: pos = 999 # if COMMAND EXECUTED found, pos = 999 (code)
    
    return idx, pos

###############################################################################################################################################
def string_search_eri_n_max(file, start_idx, str, n_max_lines):
    '''
    Function:   Searches a substring passed as argument, in the file (list of strings)
    Input:      File as list of strings, index for starting the search and the substring to look up for
    Output:     Index of the list of strings where the substring was found and position inside the string
    '''
    idx = start_idx                                             # Sets the startin index to a local variable
    n_max = n_max_lines                                         # Sets the maximum number of line to shearch the string
    pos = file[idx].find(str)                                   # Looks for the string in the line. Returns the position if found, -1 if not 
    if (file[idx].find('END') >= 0): pos = 999                  # if 'END' found => 999 (code)
    if (file[idx].find('EXIT') >= 0): pos = 998                 # if 'EXIT' found => 998 (code)

    while (pos < 0) and (idx < len(file)-1) and (not pos == 999) and (not pos == 998) and (n_max > 0):
        idx = idx + 1                                           # Increments the indext to read the next line
        n_max = n_max - 1                                       # Decrements the number of lines remaining to search
        pos = file[idx].find(str)                               # Looks for the string in the line. Returns the position if found, -1 if not
        if (file[idx].find('END') >= 0): pos = 999              # if 'END' found => 999 (code)
        if (file[idx].find('EXIT') >= 0): pos = 998             # if 'EXIT' found => 998 (code)
   
    return idx, pos

###############################################################################################################################################
def get_mss_pars(my_file, start_idx, my_cmd):
    '''
    Function:
        + Looks for the MSS's parameters
    Input:
        + my_file       => logfile as list of strings (each element of the list is a string equivalent to each line of the original txt file)
        + start_idx     => index from where the search will start 
        + my_cmd        => command as substring (code) to enter in differents block of code
    Output:
        + my_data       => list of strings with the MSS's parameters
        + idx           => current index of the list (after running the function, it could be different to the start_idx)
        + pos           => if pos < 0       => the substring was not found
                        => if pos >= 0      => position in the string where the substring was found
                        => if pos == 999    => code to identify that 'COMMAND EXECUTED' was found

    '''
    # Variable control
    assert len(my_file) > 0, 'File is empty'
    assert isinstance(my_file, list), 'Index must be list of strings'
    assert isinstance(start_idx, int), 'Index must be int'
    assert start_idx >= 0, 'Index must be grather than or equal to zero'
    assert isinstance(my_cmd, str), 'Command to look for must be string'

    ###################################################### Code

    # Init Variables
    mss_name = mss_date = mss_time = '0'
    my_data = [mss_name, mss_date, mss_time]                                # Initialize Data: list of strings containing data
    cmd = my_cmd                       

    if (cmd == 'ZEKO:LAC') or (cmd == 'ZELO;') or \
        (cmd == 'ZEPO;') or (cmd == 'ZE2I::RT=ALL;') or \
        (cmd == 'ZEPO:TYPE=SA;'):                                           # IF NOKIA                    
        idx = start_idx                                                     # Sets the startin index to a local variable
        #idx, pos = string_search_nok(my_file, idx, cmd)                    # Searchs for 'cmd' - string to allow reuse the code
        idx, pos = string_search_nok_n_lines(my_file=my_file,
                                            sub_str=cmd,
                                            start_idx=idx,
                                            n_max_lines=None)               # Searchs for 'cmd' substring
        if (pos >= 0) and (idx < len(my_file)-1) and (not pos == 999):      # if found and not EOF and not 'COMMAND EXECUTED'=>
            #idx, pos = string_search_nok(my_file, idx, 'MSSBA')            # Searchs for 'MSSBA'
            idx, pos = string_search_nok_n_lines(my_file=my_file,
                                                sub_str='MSSBA',
                                                start_idx=idx,
                                                n_max_lines=None)           # Searchs for 'cmd' substring
            if (pos >= 0) and (idx < len(my_file)-1) and (not pos == 999):  # if found and not EOF and not 'COMMAND EXECUTED'=>
                my_line = my_file[idx]                                      # Reads the line and extracts data
                mss_name = my_line[10:21:].strip()
                mss_date = my_line[35:47:].strip()
                mss_time = my_line[48:58:].strip()
                my_data = [mss_name, mss_date, mss_time]                    # Update Data: list of strings containing data

    if (cmd == 'eaw'):                                                      # IF ERICSSON
        idx = start_idx                                                     # Sets the startin index to a local variable
        idx, pos = string_search_eri(my_file, idx, cmd)                     # Searchs for 'cmd' - string to allow reuse the code
        if (pos >= 0) and (idx < len(my_file)-1) and (not pos == 999) and (not pos == 998):     # if found and not EOF and not 'COMMAND EXECUTED'=>
            idx, pos = string_search_eri(my_file, idx, 'MSSBA')             # Searchs for 'MSSBA'
            if (pos >= 0) and (idx < len(my_file)-1) and (not pos == 999) and (not pos == 998): # if found and not EOF and not 'COMMAND EXECUTED'=>
                my_line = my_file[idx]                                      # Reads the line and extracts data
                mss_name = my_line[21:30:].strip()
                mss_date = '0000-00-00'                                      # Mantain '0' as ther is no timestamp in Ericsson
                mss_time = '00:00:00'                                        # Mantain '0' as ther is no timestamp in Ericsson
                my_data = [mss_name, mss_date, mss_time]                     # Update Data: list of strings containing data

    return idx, pos, my_data


###############################################################################################################################################
########################################     ZELO Functions     ###############################################################################
###############################################################################################################################################

###############################################################################################################################################
def get_zelo_lac_pars(file, start_idx):
    '''
    Function:   Looks for the LAC parameters in the file passed as argument, starting at the specified index
    Input:      File as list of strings and index for starting the search 
    Output:     LAC parameters as strings and the current index
    '''
    
    #### INITIALIZE LOCAL VARIABLES
    LA_MCC = '0'
    LA_MNC = '0'
    LA_NO = '0'
    LA_NAME = '0'
    LA_AT = '0'
    LA_REPAG_INT = '0'
    LA_RNGP = '0'
    LA_MNC_AL = '0'
    LA_DSAV = '0'
    LA_TZ = '0'
    LA_HONLA = '0'
    Data = [LA_MCC, LA_MNC, LA_NO, LA_NAME, LA_AT, LA_REPAG_INT,
            LA_RNGP, LA_MNC_AL, LA_DSAV, LA_TZ, LA_HONLA]           # Initialize Data: list of strings

    idx = start_idx                                                 # Sets the startin index to a local variable
    idx, pos = string_search_nok(file, idx, 'LOCATION AREA')        # Searchs for 'LOCATION AREA'
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):     # if found and not EOF and not 'COMMAND EXECUTED'=>
        idx, pos = string_search_nok(file, idx, 'LA    NAME')       # Searchs for 'LA    NAME'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999): # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                     # Reads the line and extracts data
            LA_NAME = my_line[12:23:].strip()
            LA_NO = my_line[49:59:].strip()
            idx, pos = string_search_nok(file, idx, 'MOBILE COUNTRY CODE')
            if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):
                my_line = file[idx]
                LA_MCC = my_line[49:59:].strip()
            idx, pos = string_search_nok(file, idx, 'MOBILE NETWORK CODE')
            if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):
                my_line = file[idx]
                LA_MNC = my_line[49:59:].strip()
            idx, pos = string_search_nok(file, idx, 'REPAGING ATTEMPTS')
            if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):
                my_line = file[idx]
                LA_AT = my_line[49:59:].strip()
            idx, pos = string_search_nok(file, idx, 'REPAGING INTERVAL TIMER')
            if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):
                my_line = file[idx]
                LA_REPAG_INT = my_line[50:70:].strip()
            idx, pos = string_search_nok(file, idx, 'MSRN GROUP')
            if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):
                my_line = file[idx]
                LA_RNGP = my_line[49:59:].strip()
            idx, pos = string_search_nok(file, idx, 'ALLOWED MNC')
            if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):
                my_line = file[idx]
                LA_MNC_AL = my_line[49:59:].strip()
            idx, pos = string_search_nok(file, idx, 'DAYLIGHT SAVING')
            if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):
                my_line = file[idx]
                LA_DSAV = my_line[49:59:].strip()
            idx, pos = string_search_nok(file, idx, 'TIME ZONE')
            if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):
                my_line = file[idx]
                LA_TZ = my_line[49:59:].strip()
            idx, pos = string_search_nok(file, idx, 'HANDOVER NUMBER')
            if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):
                my_line = file[idx]
                LA_HONLA = my_line[49:59:].strip()
        Data = [LA_MCC, LA_MNC, LA_NO, LA_NAME, LA_AT, LA_REPAG_INT, LA_RNGP, LA_MNC_AL, LA_DSAV, LA_TZ, LA_HONLA]  # Prepare to return

    return idx, pos, Data


###############################################################################################################################################
########################################     ZEKO Functions     ###############################################################################
###############################################################################################################################################

###############################################################################################################################################
def get_zeko_lac_pars(file, start_idx):
    '''
    Function:   Looks for the Roaming's LAC parameters in the file passed as argument, starting at the specified index
    Input:      File as list of strings and index for starting the search 
    Output:     Roaming's LAC parameters as list of strings, the current index  and position of the text in the line
    '''
    
    #### INITIALIZE LOCAL VARIABLES
    LA_str = LA_Name = ZC0_Stat = ZC1_Stat = ZC2_Stat = ZC3_Stat = ZC4_Stat = ZC5_Stat = '0'
    Data = [LA_str, LA_Name, ZC0_Stat, ZC1_Stat, ZC2_Stat, ZC3_Stat, ZC4_Stat, ZC5_Stat]    # Initialize Data: list of strings

    idx = start_idx                                                                         # Sets the starting index to a local variable
    idx, pos = string_search_nok(file, idx, 'LOCATION AREA:')                                   # Searchs for 'LOCATION AREA'
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                             # if found and not EOF and not 'COMMAND EXECUTED'=>
        my_line = file[idx]                                                                 # Reads the line and extracts data
        LA_Name = my_line[15:25:].strip()
        LA_str = my_line[31:41:].strip()
        idx, pos = string_search_nok(file, idx, '----  ---------------')                        # Searchs for '----  ---------------'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            ZC0_Stat, ZC1_Stat, ZC2_Stat, ZC3_Stat, ZC4_Stat, ZC5_Stat = search_zc(file, idx)

    Data = [LA_str, LA_Name, ZC0_Stat, ZC1_Stat, ZC2_Stat, ZC3_Stat, ZC4_Stat, ZC5_Stat]    # Assign to return

    return idx + 1, pos, Data

###############################################################################################################################################
def search_zc(file, start_idx):
    '''
    Function:   Looks for the ZCs of a LAC found in previous funcion in the file passed as argument, starting at the specified index
    Input:      File as list of strings and index for starting the search 
    Output:     ZCs states of the LAC, the current index  and position of the text in the line
    '''
    ZC0_St = ZC1_St = ZC2_St = ZC3_St = ZC4_St = ZC5_St = '0'

    idx = start_idx                                                                         # Sets the starting index to a local variable
    idx_this_LAC = start_idx                                                                # Stores the index of this LAC
   
    idx, pos = string_search_nok_n_max(file, idx_this_LAC, '0000', 12)                      # Searchs for '0000' in the next 2 lines
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999): ZC0_St = '1'                # if found and not EOF and not 'COMMAND EXECUTED'=>

    idx, pos = string_search_nok_n_max(file, idx_this_LAC, '0001', 12)                      # Searchs for '0000' in the next 2 lines
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999): ZC1_St = '1'                # if found and not EOF and not 'COMMAND EXECUTED'=>

    idx, pos = string_search_nok_n_max(file, idx_this_LAC, '0002', 12)                      # Searchs for '0000' in the next 2 lines
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999): ZC2_St = '1'                # if found and not EOF and not 'COMMAND EXECUTED'=>

    idx, pos = string_search_nok_n_max(file, idx_this_LAC, '0003', 12)                      # Searchs for '0000' in the next 2 lines
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999): ZC3_St = '1'                # if found and not EOF and not 'COMMAND EXECUTED'=>

    idx, pos = string_search_nok_n_max(file, idx_this_LAC, '0004', 12)                      # Searchs for '0000' in the next 2 lines
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999): ZC4_St = '1'                # if found and not EOF and not 'COMMAND EXECUTED'=>

    idx, pos = string_search_nok_n_max(file, idx_this_LAC, '0005', 12)                      # Searchs for '0000' in the next 2 lines
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999): ZC5_St = '1'                # if found and not EOF and not 'COMMAND EXECUTED'=>

    return ZC0_St, ZC1_St, ZC2_St, ZC3_St, ZC4_St, ZC5_St


###############################################################################################################################################
########################################     MGLAP Functions     ##############################################################################
###############################################################################################################################################

###############################################################################################################################################
def get_mglap_lac_pars(file, start_idx):
    '''
    Function:   Looks for the Roaming's LAC parameters in the file passed as argument, starting at the specified index
    Input:      File as list of strings and index for starting the search 
    Output:     Roaming's LAC parameters as list of strings, the current index  and position of the text in the line
    '''
    
    #### INITIALIZE LOCAL VARIABLES
    LA_MCC = LA_MNC = LA_NO = LA_LAI = LA_PFC = LA_PRL = LA_POOL = '0'
    Data = [LA_MCC, LA_MNC, LA_NO, LA_LAI, LA_PFC, LA_PRL, LA_POOL]                         # Initialize Data: list of strings

    idx = start_idx                                                                         # Sets the starting index to a local variable
    idx, pos = string_search_eri(file, idx, '-')                                            # Searchs for '-'
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999) and (not pos == 998):        # if found and not EOF and not 'COMMAND EXECUTED'=>
        my_line = file[idx]                                                                 # Reads the line and extracts data
        LA_LAI = my_line[0:13:].strip()
        LA_PFC = my_line[13:18:].strip()
        LA_PRL = my_line[19:25:].strip()
        LA_POOL = my_line[26:32:].strip()
        LA_MCC, LA_MNC, LA_NO = my_line[0:13:].split('-', 2)
        LA_MCC = LA_MCC.strip()
        LA_MNC = LA_MNC.strip()
        LA_NO = LA_NO.strip()

    Data = [LA_MCC, LA_MNC, LA_NO, LA_LAI, LA_PFC, LA_PRL, LA_POOL]                         # Assign to return

    return idx, pos, Data


###############################################################################################################################################
########################################     MGNRP Functions     ##############################################################################
###############################################################################################################################################

###############################################################################################################################################
def get_mgnrp_lac_pars(file, start_idx):
    '''
    Function:   Looks for the Roaming's LAC parameters in the file passed as argument, starting at the specified index
    Input:      File as list of strings and index for starting the search 
    Output:     Roaming's LAC parameters as list of strings, the current index  and position of the text in the line
    '''
    
    #### INITIALIZE LOCAL VARIABLES
    LA_MCC = LA_MNC = LA_str = LA_Name = ZC0_Stat = ZC1_Stat = ZC2_Stat = ZC3_Stat = ZC4_Stat = ZC5_Stat = '0'
    Data = [LA_str, LA_Name, ZC0_Stat, ZC1_Stat, ZC2_Stat, ZC3_Stat, ZC4_Stat, ZC5_Stat]    # Initialize Data: list of strings

    idx = start_idx                                                                         # Sets the starting index to a local variable
    idx, pos = string_search_eri(file, idx, '-')                                            # Searchs for '-'
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999) and (not pos == 998):        # if found and not EOF and not 'COMMAND EXECUTED'=>
        my_line = file[idx]                                                                 # Reads the line and extracts data
        LA_Name = my_line[0:13:].strip()
        LA_MCC, LA_MNC, LA_str = my_line[0:13:].split('-', 2)

        ZC0_Stat = ZC4_Stat = '1'                                                           # Claro & CTBC opened
        if (my_line.find(' 1 ') < 0): ZC3_Stat = '1'                                        # TIM has R30k opened 
        if (my_line.find(' 2 ') < 0): ZC2_Stat = '1'                                        # OI has R30k opened 
        if (my_line.find(' 6 ') < 0): ZC1_Stat = '1'                                        # VIVO has R30k opened 

    Data = [LA_str, LA_Name, ZC0_Stat, ZC1_Stat, ZC2_Stat, ZC3_Stat, ZC4_Stat, ZC5_Stat]    # Assign to return

    return idx, pos, Data


###############################################################################################################################################
########################################     ZEPO 2G Functions     ############################################################################
###############################################################################################################################################

###############################################################################################################################################
def get_zepo_2g_cell_pars(my_file, start_idx):
    '''
    Function:   Looks for the CELL's parameters in the file passed as argument, starting at the specified index
    Input:      File as list of strings and index for starting the search 
    Output:     Cell's parameters as list of strings, the current index  and position of the text in the line
    '''
    
    #### INITIALIZE LOCAL VARIABLES
    CELL_NAME = CELL_NO = CELL_BSC_NAME = '0'
    CELL_BSC_NO = CELL_LAC_NAME = CELL_LAC_NO = '0'
    CELL_MCC = CELL_MNC = CELL_CI = '0'
    CELL_STAT = CELL_RZ = CELL_CDR = '0'

    Data = [CELL_NAME, CELL_NO, CELL_BSC_NAME, CELL_BSC_NO,
                CELL_LAC_NAME, CELL_MCC, CELL_MNC, CELL_LAC_NO,
                CELL_CI, CELL_STAT, CELL_RZ, CELL_CDR]                                          # Initialize Data: list of strings

    idx = start_idx                                                                             # Sets the starting index to a local variable
    idx, pos = string_search_nok(my_file, idx, 'BASE TRANSCEIVER STATION')                      # Searchs for 'BASE TRANSCEIVER STATION'
    if (pos >= 0) and (idx < len(my_file)-1) and (not pos == 999):                              # if found and not EOF and not 'COMMAND EXECUTED'=>
        idx, pos = string_search_nok(my_file, idx, 'BTS   NAME')                                # Searchs for 'BTS   NAME'
        if (pos >= 0) and (idx < len(my_file)-1) and (not pos == 999):                          # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = my_file[idx]                                                              # Reads the line and extracts data
            CELL_NAME = my_line[12:30:].strip()
            CELL_NO = my_line[50:60:].strip()

        idx, pos = string_search_nok(my_file, idx, 'BSC   NAME')                                # Searchs for 'BTS   NAME'
        if (pos >= 0) and (idx < len(my_file)-1) and (not pos == 999):                          # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = my_file[idx]                                                              # Reads the line and extracts data
            CELL_BSC_NAME = my_line[12:30:].strip()
            CELL_BSC_NO = my_line[50:60:].strip()

        idx, pos = string_search_nok(my_file, idx, 'LA    NAME')                                # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(my_file)-1) and (not pos == 999):                          # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = my_file[idx]                                                              # Reads the line and extracts data
            CELL_LAC_NAME = my_line[12:30:].strip()
            CELL_LAC_NO = my_line[50:60:].strip()

        idx, pos = string_search_nok(my_file, idx, 'MOBILE COUNTRY')                            # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(my_file)-1) and (not pos == 999):                          # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = my_file[idx]                                                              # Reads the line and extracts data
            CELL_MCC = my_line[50:60:].strip()

        idx, pos = string_search_nok(my_file, idx, 'MOBILE NETWORK')                            # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(my_file)-1) and (not pos == 999):                          # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = my_file[idx]                                                              # Reads the line and extracts data
            CELL_MNC = my_line[50:60:].strip()

        idx, pos = string_search_nok(my_file, idx, 'CELL IDENTITY')                             # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(my_file)-1) and (not pos == 999):                          # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = my_file[idx]                                                              # Reads the line and extracts data
            CELL_CI = my_line[50:60:].strip()

        idx, pos = string_search_nok(my_file, idx, 'BTS ADM')                                   # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(my_file)-1) and (not pos == 999):                          # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = my_file[idx]                                                              # Reads the line and extracts data
            CELL_STAT = my_line[50:60:].strip()

        idx, pos = string_search_nok(my_file, idx, 'ROUTING ZONE')                              # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(my_file)-1) and (not pos == 999):                          # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = my_file[idx]                                                              # Reads the line and extracts data
            CELL_RZ = my_line[50:60:].strip()

        idx, pos = string_search_nok(my_file, idx, 'CELL DEPENDENT')                            # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(my_file)-1) and (not pos == 999):                          # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = my_file[idx]                                                              # Reads the line and extracts data
            CELL_CDR = my_line[50:60:].strip()

    Data = [CELL_NAME, CELL_NO, CELL_BSC_NAME, CELL_BSC_NO,
                CELL_LAC_NAME, CELL_MCC, CELL_MNC, CELL_LAC_NO,
                CELL_CI, CELL_STAT, CELL_RZ, CELL_CDR]                                          # Assign to return

    return idx, pos, Data


###############################################################################################################################################
########################################     ZEPO 3G Functions     ############################################################################
###############################################################################################################################################

###############################################################################################################################################
def get_zepo_3g_sa_pars(file, start_idx):
    '''
    Function:   Looks for the CELL's parameters in the file passed as argument, starting at the specified index
    Input:      File as list of strings and index for starting the search 
    Output:     Cell's parameters as list of strings, the current index  and position of the text in the line
    '''
    
    #### INITIALIZE LOCAL VARIABLES
    S_A_NAME = S_A_NO = '0'
    S_A_LAC_NAME = S_A_LAC_NO = '0'
    S_A_MCC = S_A_MNC = S_A_CI = '0'
    S_A_STAT = S_A_RZ = S_A_CDR = '0'

    Data = [S_A_NAME, S_A_NO, S_A_LAC_NAME, S_A_LAC_NO, S_A_MCC, S_A_MNC,
                S_A_CI, S_A_STAT, S_A_RZ, S_A_CDR]                                          # Initialize Data: list of strings

    idx = start_idx                                                                         # Sets the starting index to a local variable
    idx, pos = string_search_nok(file, idx, 'SERVICE AREA DATA')                            # Searchs for 'xxxxxxxxxx'
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                             # if found and not EOF and not 'COMMAND EXECUTED'=>
        idx, pos = string_search_nok_n_max(file, idx, 'SA    NAME :', 5)                    # Searchs for 'xxxxxxxxxx' in next 'n' lines
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            S_A_NAME = my_line[12:30:].strip()
            S_A_NO = my_line[50:60:].strip()

        idx, pos = string_search_nok_n_max(file, idx, 'LA    NAME :', 5)                    # Searchs for 'xxxxxxxxxx' in next 'n' lines
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            S_A_LAC_NAME = my_line[12:30:].strip()
            S_A_LAC_NO = my_line[50:60:].strip()

        idx, pos = string_search_nok_n_max(file, idx, '(MCC)... :', 5)                      # Searchs for 'xxxxxxxxxx' in next 'n' lines
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            S_A_MCC = my_line[50:60:].strip()

        idx, pos = string_search_nok_n_max(file, idx, '(MNC)... :', 5)                      # Searchs for 'xxxxxxxxxx' in next 'n' lines
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            S_A_MNC = my_line[50:60:].strip()

        idx, pos = string_search_nok_n_max(file, idx, '(SAC)... :', 5)                      # Searchs for 'xxxxxxxxxx' in next 'n' lines
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            S_A_CI = my_line[50:60:].strip()

        idx, pos = string_search_nok_n_max(file, idx, 'ADMINISTRATIVE STATE', 5)            # Searchs for 'xxxxxxxxxx' in next 'n' lines
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            S_A_STAT = my_line[50:60:].strip()

        idx, pos = string_search_nok_n_max(file, idx, '(RZ).... :', 5)                      # Searchs for 'xxxxxxxxxx' in next 'n' lines
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            S_A_RZ = my_line[50:60:].strip()

        idx, pos = string_search_nok_n_max(file, idx, '(CDR)... :', 5)                      # Searchs for 'xxxxxxxxxx' in next 'n' lines
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            S_A_CDR = my_line[50:60:].strip()

    Data = [S_A_NAME, S_A_NO, S_A_LAC_NAME, S_A_LAC_NO, S_A_MCC, S_A_MNC,
                S_A_CI, S_A_STAT, S_A_RZ, S_A_CDR]                                      # Assign to return

    return idx, pos, Data

###############################################################################################################################################
########################################     ZE2I 2G Functions     ############################################################################
###############################################################################################################################################

###############################################################################################################################################
def get_ze2i_rnc_pars(file, start_idx):
    '''
    Function:   Looks for the RNC's parameters in the file passed as argument, starting at the specified index
    Input:      File as list of strings and index for starting the search 
    Output:     RNC's parameters as list of strings, the current index  and position of the text in the line
    '''
    
    #### INITIALIZE LOCAL VARIABLES
    R_NAME = R_MCC = R_MNC = R_ID = R_MUL_PLMN = R_STAT = R_OSTAT = '0'

    Data = [R_NAME, R_MCC, R_MNC, R_ID, R_MUL_PLMN, R_STAT, R_OSTAT]                        # Initialize Data: list of strings

    idx = start_idx                                                                         # Sets the starting index to a local variable
    idx, pos = string_search_nok(file, idx, 'RNC IDENTIFICATION:')                          # Searchs for 'RNC IDENTIFICATION:'
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                             # if found and not EOF and not 'COMMAND EXECUTED'=>
        idx, pos = string_search_nok(file, idx, 'RNCID ... :')                              # Searchs for 'RNCID '
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            R_ID = my_line[44:54:].strip()

        idx, pos = string_search_nok(file, idx, 'MCC ..... :')                              # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            R_MCC = my_line[44:54:].strip()

        idx, pos = string_search_nok(file, idx, 'MNC ..... :')                              # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            R_MNC = my_line[44:54:].strip()

        idx, pos = string_search_nok(file, idx, 'RNCNAME . :')                              # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            R_NAME = my_line[44:54:].strip()

        m_idx = idx
        m_pos = pos
        m_idx, m_pos = string_search_nok_n_max(file, m_idx, 'MULTIPLE PLMN', 5)
        if (m_pos >= 0) and (m_idx < len(file)-1) and (not m_pos == 999):                   # if found and not EOF and not 'COMMAND EXECUTED'=>
            R_MUL_PLMN = '1'

        idx, pos = string_search_nok(file, idx, 'STATE ... :')                              # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            R_STAT = my_line[44:54:].strip()

        idx, pos = string_search_nok(file, idx, 'OPSTATE . :')                              # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            R_OSTAT = my_line[44:54:].strip()

        Data = [R_NAME, R_MCC, R_MNC, R_ID, R_MUL_PLMN, R_STAT, R_OSTAT]                    # Assign to return

    return idx, pos, Data


###############################################################################################################################################
def get_ze2i_rnc_lac_pars(file, start_idx, flag):
    '''
    Function:   Looks for the RNC's LAC parameters in the file passed as argument, starting at the specified index
    Input:      File as list of strings and index for starting the search and a flag to limit the search
    Output:     RNC's LAC parameters as list of strings, the current index  and position of the text in the line
    '''
    
    #### INITIALIZE LOCAL VARIABLES
    R_LAC_MCC = R_LAC_MNC = R_LAC_NO = '0'

    Data = [R_LAC_MCC, R_LAC_MNC, R_LAC_NO]                                                 # Initialize Data: list of strings

    idx = start_idx                                                                         # Sets the starting index to a local variable
    if (flag == 0):
        idx, pos = string_search_nok(file, idx, 'LAC    MCC  MNC')
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            flag = 1
            idx, pos = string_search_nok_n_max(file, idx, '724', 5)                         # Looks for 'xxxxxxx' in the next 'n' lines
            if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                     # if found and not EOF and not 'COMMAND EXECUTED'=>
                my_line = file[idx]                                                         # Reads the line and extracts data
                R_LAC_NO = my_line[0:6:].strip()
                R_LAC_MCC = my_line[7:11:].strip()
                R_LAC_MNC = my_line[12:15:].strip()
    else:
        idx, pos = string_search_nok_n_max(file, idx, '724', 3)                             # Looks for 'xxxxxxx' in the next 'n' lines
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            R_LAC_NO = my_line[0:6:].strip()
            R_LAC_MCC = my_line[7:11:].strip()
            R_LAC_MNC = my_line[12:15:].strip()
        else:
            flag = 0

    Data = [R_LAC_MCC, R_LAC_MNC, R_LAC_NO]                                                 # Assign to return

    return idx + 1, pos, flag, Data

###############################################################################################################################################
########################################     MGMAP Functions     ##############################################################################
###############################################################################################################################################

###############################################################################################################################################
def get_mgmap_rnc_pars(file, start_idx):
    '''
    Function:   Looks for the RNC's parameters in the file passed as argument, starting at the specified index
    Input:      File as list of strings and index for starting the search 
    Output:     RNC's parameters as list of strings, the current index  and position of the text in the line
    '''
    
    #### INITIALIZE LOCAL VARIABLES
    R_NAME = '0'
    Data = [R_NAME]                                                                         # Initialize Data: list of strings

    idx = start_idx                                                                         # Sets the starting index to a local variable
    idx, pos = string_search_eri(file, idx, 'RNC     LAI')                                  # Searchs for 'xxxxxx'
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999) and (not pos == 998):        # if found and not EOF and not 'COMMAND EXECUTED'=>
        idx, pos = string_search_eri_n_max(file, idx + 1, 'RNC', 1)                         # Searchs for 'xxxxxx'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999) and (not pos == 998):    # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            R_NAME = my_line[0:8:].strip()
    Data = [R_NAME]                                                                         # Assign to return

    return idx, pos, Data

###############################################################################################################################################
def get_mgmap_rnc_lac_pars(file, start_idx):
    '''
    Function:   Looks for the RNC's LAC parameters in the file passed as argument, starting at the specified index
    Input:      File as list of strings and index for starting the search and a flag to limit the search
    Output:     RNC's LAC parameters as list of strings, the current index  and position of the text in the line
    '''
    
    #### INITIALIZE LOCAL VARIABLES
    RN_LAC_MCC = RN_LAC_MNC = RN_LAC_NO = '0'
    Data = [RN_LAC_MCC, RN_LAC_MNC, RN_LAC_NO]                                          # Initialize Data: list of strings

    idx = start_idx                                                                     # Sets the starting index to a local variable
    idx, pos = string_search_eri_n_max(file, idx, '-', 1)
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999) and (not pos == 998):    # if found and not EOF and not 'COMMAND EXECUTED'=>
        my_line = file[idx]                                                             # Reads the line and extracts data
        RN_LAC_MCC, RN_LAC_MNC, RN_LAC_NO = my_line[8:20:].split('-', 2)
        RN_LAC_MCC = RN_LAC_MCC.strip()
        RN_LAC_MNC = RN_LAC_MNC.strip()
        RN_LAC_NO = RN_LAC_NO.strip()

    Data = [RN_LAC_MCC, RN_LAC_MNC, RN_LAC_NO]                                           # Assign to return

    return idx , pos, Data


###############################################################################################################################################
########################################     MGCEP Functions     ##############################################################################
###############################################################################################################################################

###############################################################################################################################################
def get_mgcep_cell_pars(file, start_idx):
    '''
    Function:   Looks for the RNC's parameters in the file passed as argument, starting at the specified index
    Input:      File as list of strings and index for starting the search 
    Output:     RNC's parameters as list of strings, the current index  and position of the text in the line
    '''
    
    #### INITIALIZE LOCAL VARIABLES
    CELL_NAME = CELL_CGI = CELL_MCC = '0'
    CELL_MNC = CELL_LAC = CELL_CI = CELL_BSC = '0'
    CELL_CO = CELL_RO = CELL_NCS = CELL_EA = '0'


    Data = [CELL_NAME, CELL_CGI, CELL_MCC, CELL_MNC,
                CELL_LAC, CELL_CI, CELL_BSC,
                CELL_CO, CELL_RO, CELL_NCS, CELL_EA]                                        # Initialize Data: list of strings

    idx = start_idx                                                                         # Sets the starting index to a local variable
    idx, pos = string_search_eri(file, idx, '-')                                            # Searchs for 'xxxxxx'
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999) and (not pos == 998):        # if found and not EOF and not 'END' or 'EXIT' =>
        my_line = file[idx]                                                                 # Reads the line and extracts data
        CELL_NAME = my_line[0:8:].strip()
        CELL_CGI = my_line[9:27:].strip()
        CELL_MCC, CELL_MNC, CELL_LAC, CELL_CI = my_line[9:26:].split('-', 3)
        CELL_MCC = CELL_MCC.strip()
        CELL_MNC = CELL_MNC.strip()
        CELL_LAC = CELL_LAC.strip()
        CELL_CI = CELL_CI.strip()
        CELL_BSC = my_line[28:36:].strip()
        CELL_CO = my_line[37:41:].strip()
        CELL_RO = my_line[44:48:].strip()
        CELL_NCS = my_line[51:55:].strip()
        CELL_EA = my_line[56:60:].strip()

        if CELL_NAME[0] == '9':
            str_as_lst = list(CELL_NAME)
            str_as_lst[0] = 'A'
            CELL_NAME = 'B' + ''.join(str_as_lst)
        else:
            CELL_NAME = 'ERROR'
    
    Data = [CELL_NAME, CELL_CGI, CELL_MCC, CELL_MNC,
                CELL_LAC, CELL_CI, CELL_BSC,
                CELL_CO, CELL_RO, CELL_NCS, CELL_EA]                                        # Assign to return

    return idx, pos, Data


###############################################################################################################################################
########################################     MGAAP Functions     ##############################################################################
###############################################################################################################################################

###############################################################################################################################################
def get_mgaap_area_pars(file, start_idx):
    '''
    Function:   Looks for the RNC's parameters in the file passed as argument, starting at the specified index
    Input:      File as list of strings and index for starting the search 
    Output:     RNC's parameters as list of strings, the current index  and position of the text in the line
    '''
    
    #### INITIALIZE LOCAL VARIABLES
    SA_NAME = SA_CGI = SA_MCC = '0'
    SA_MNC = SA_LAC = SA_CI = '0'
    SA_RO = SA_CO = SA_EA = '0'

    Data = [SA_NAME, SA_CGI, SA_MCC, SA_MNC, SA_LAC, SA_CI,
                SA_RO, SA_CO, SA_EA]                                                        # Initialize Data: list of strings

    idx = start_idx                                                                         # Sets the starting index to a local variable
    idx, pos = string_search_eri(file, idx, 'SAI')                                            # Searchs for 'xxxxxx'
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999) and (not pos == 998):        # if found and not EOF and not 'END' or 'EXIT' =>
        my_line = file[idx]                                                                 # Reads the line and extracts data
        SA_NAME = my_line[0:8:].strip()
        SA_CGI = my_line[14:34:].strip()
        SA_MCC, SA_MNC, SA_LAC, SA_CI = my_line[14:34:].split('-', 3)
        SA_MCC = SA_MCC.strip()
        SA_MNC = SA_MNC.strip()
        SA_LAC = SA_LAC.strip()
        SA_CI = SA_CI.strip()
        SA_RO = my_line[36:40:].strip()
        SA_CO = my_line[41:45:].strip()
        SA_EA = my_line[46:50:].strip()

        if SA_NAME[0] == 'I':
            str_as_lst = list(SA_NAME)
            str_as_lst[0] = 'A'
            SA_NAME = 'UB' + ''.join(str_as_lst)
        elif SA_NAME[0] == 'F':
            SA_NAME = SA_NAME
        else:
            SA_NAME = 'ERROR'
    
    Data = [SA_NAME, SA_CGI, SA_MCC, SA_MNC, SA_LAC, SA_CI,
                SA_RO, SA_CO, SA_EA]                                                        # Assign to return

    return idx, pos, Data


###############################################################################################################################################
########################################     MAIN Functions     ###############################################################################
###############################################################################################################################################

###############################################################################################################################################
def get_2g_cell_nok(log_file_path):
    '''
    Function:   
        + Process a log_file with all the 2G cells of NOKIA's MSSs
    Arguments:      
        + log_file_path => path to the log_file
    Output:     
        + df_full       => DataFrame with full 2G cells of NOKIA's MSSs information
        + df_summ       => DataFrame with summarized 2G cells of NOKIA's MSSs information
    '''
    
    # Variable control
    assert isinstance(log_file_path, str),'Path to look for the file must be string'
    assert len(log_file_path) > 0, 'File is empty'

    ###################################################### Code

    # Init NOKIA Variables
    nok_cell_mss_name = '0'
    nok_cell_mss_date = '0'
    nok_cell_mss_time = '0'
    nok_cell_name = '0'
    nok_cell_no = '0'
    nok_cell_bsc_name = '0'
    nok_cell_bsc_no = '0'
    nok_cell_lac_name = '0'
    nok_cell_lac_no = '0'
    nok_cell_mcc = '0'
    nok_cell_mnc = '0'
    nok_cell_ci = '0'
    nok_cell_stat = '0'
    nok_cell_rz = '0'
    nok_cell_cdr = '0'

    nok_cell_mss_pars = [nok_cell_mss_name, nok_cell_mss_date, nok_cell_mss_time]
    nok_cell_pars = [nok_cell_name, nok_cell_no, nok_cell_bsc_name, nok_cell_bsc_no, nok_cell_lac_name,nok_cell_lac_no,
                        nok_cell_mcc, nok_cell_mnc, nok_cell_ci, nok_cell_stat, nok_cell_rz, nok_cell_cdr]

    nok_cell_idx = 0
    nok_cell_pos = 0
    nok_cell_count = 0

    # Open & Load NOKIA logfile
    nok_logfile = open_file(log_file_path)

    # Create & Init & Set the NOKIA pd.DataFrame
    nok_col_names = ['MSS','Date','Time','CELL_NAME','CELL_NO','NE','NE_No','LAC_Name','MCC','MNC','LAC','CI','Status','RZ', 'CDR']
    df_nok_2g_cell_full = pd.DataFrame(columns=nok_col_names)
    df_nok_2g_cell_full.loc[0] = [nok_cell_mss_name, nok_cell_mss_date, nok_cell_mss_time, nok_cell_name, nok_cell_no, 
                                    nok_cell_bsc_name, nok_cell_bsc_no, nok_cell_lac_name, nok_cell_lac_no, nok_cell_mcc,
                                    nok_cell_mnc, nok_cell_ci, nok_cell_stat, nok_cell_rz, nok_cell_cdr]

    # Run main block (txt => pd.DataFrame)
    while (nok_cell_idx < len(nok_logfile)-1):
        nok_cell_idx, nok_cell_pos, nok_cell_mss_pars = get_mss_pars(my_file=nok_logfile,
                                                                        start_idx=nok_cell_idx,
                                                                        my_cmd='ZEPO;')
        while (nok_cell_idx < len(nok_logfile)-1) and (not nok_cell_pos == 999):
            nok_cell_idx, nok_cell_pos, nok_cell_pars = get_zepo_2g_cell_pars(my_file=nok_logfile,
                                                                                start_idx=nok_cell_idx)
            if (nok_cell_pos >= 0) and (not nok_cell_pos == 999):
                new_cell = nok_cell_mss_pars + nok_cell_pars
                df_nok_2g_cell_full.loc[nok_cell_count] = new_cell
                nok_cell_count = nok_cell_count + 1
        nok_cell_idx = nok_cell_idx + 1

    # DataFrame => Drop some columns to get just the most important ones.
    df_nok_2g_cell_summ = df_nok_2g_cell_full
    df_nok_2g_cell_full['MSS'] = df_nok_2g_cell_full['MSS'].str.replace(r'0', '')
    df_nok_2g_cell_summ['MSS'] = df_nok_2g_cell_summ['MSS'].str.replace(r'0', '')
    df_nok_2g_cell_full['LAI'] = df_nok_2g_cell_full['MCC'] + '-' + \
                                    df_nok_2g_cell_full['MNC'] + '-' + \
                                    df_nok_2g_cell_full['LAC']
    df_nok_2g_cell_full['MSS-LAI'] = df_nok_2g_cell_full['MSS'] + '-' + \
                                        df_nok_2g_cell_full['LAI']
    df_nok_2g_cell_summ['CGI'] =  df_nok_2g_cell_summ['MCC'] + '-' + \
                                    df_nok_2g_cell_summ['MNC'] + '-' + \
                                    df_nok_2g_cell_summ['LAC'] + '-' + \
                                    df_nok_2g_cell_summ['CI']
    nok_drop_col = ['Date', 'Time', 'NE_No', 'LAC_Name', 'Status', 'RZ', 'CDR']
    df_nok_2g_cell_summ = df_nok_2g_cell_summ.drop(columns=nok_drop_col)
    nok_col_summ = ['MSS', 'NE', 'CELL_NAME', 'CELL_NO', 'MCC', 'MNC', 'LAC', 'CI', 'CGI']
    df_nok_2g_cell_summ = df_nok_2g_cell_summ[nok_col_summ]

    return df_nok_2g_cell_full, df_nok_2g_cell_summ

###############################################################################################################################################
def get_2g_cell_eri(log_file_path):
    '''
    Function:   
        + Process a log_file with all the 2G cells of ERICSSON's MSSs
    Arguments:      
        + log_file_path => path to the log_file
    Output:     
        + df_full       => DataFrame with full 2G cells of ERICSSON's MSSs information
        + df_summ       => DataFrame with summarized 2G cells of ERICSSON's MSSs information
    '''
    
    # Variable control
    assert isinstance(log_file_path, str),'Path to look for the file must be string'
    assert len(log_file_path) > 0, 'File is empty'

    ###################################################### Code

    # Init ERICSSON Variables
    eri_cell_mss_name = '0'
    eri_cell_mss_date = '0'
    eri_cell_mss_time = '0'
    eri_cell_name = '0'
    eri_cell_cgi = '0'
    eri_cell_mcc = '0'
    eri_cell_mnc = '0'
    eri_cell_lac = '0'
    eri_cell_ci = '0'
    eri_cell_bsc = '0'
    eri_cell_co = '0'
    eri_cell_ro = '0'
    eri_cell_ncs = '0'
    eri_cell_ea = '0'

    eri_mss_pars = [eri_cell_mss_name, eri_cell_mss_date, eri_cell_mss_time]
    eri_cell_pars = [eri_cell_name, eri_cell_cgi, eri_cell_mcc, eri_cell_mnc, eri_cell_lac,
                        eri_cell_ci, eri_cell_bsc, eri_cell_co, eri_cell_ro, eri_cell_ncs, eri_cell_ea]

    eri_cell_idx = 0
    eri_cell_pos = 0
    eri_cell_count = 0

    # Open & Load ERICSSON logfile
    eri_logfile = open_file(log_file_path)

    # Create & Init & Set the ERICSSON pd.DataFrame
    eri_col_names = ['MSS','Date','Time','CELL_NAME','CGI','MCC','MNC','LAC','CI','NE','CO','RO','NCS','EA']
    df_eri_2g_cell_full = pd.DataFrame(columns=eri_col_names)
    df_eri_2g_cell_full.loc[0] = [eri_cell_mss_name, eri_cell_mss_date, eri_cell_mss_time, eri_cell_name, eri_cell_cgi,
                                    eri_cell_mcc, eri_cell_mnc, eri_cell_lac, eri_cell_ci, eri_cell_bsc, eri_cell_co,
                                    eri_cell_ro, eri_cell_ncs, eri_cell_ea]

    # Run the main program (txt => pd.DataFrame)
    while (eri_cell_idx < len(eri_logfile)-1):
        eri_cell_idx, eri_cell_pos, eri_mss_pars = get_mss_pars(eri_logfile, eri_cell_idx,'eaw')
        if (eri_cell_pos >= 0) and (not eri_cell_pos == 999) and (not eri_cell_pos == 998):
            eri_cell_idx, eri_cell_pos, eri_cell_pars = get_mgcep_cell_pars(eri_logfile, eri_cell_idx)
            while(eri_cell_pos >= 0) and (not eri_cell_pos == 999) and (not eri_cell_pos == 998):
                eri_cell_idx, eri_cell_pos, eri_cell_pars = get_mgcep_cell_pars(eri_logfile, eri_cell_idx)
                if(eri_cell_pos >= 0) and (not eri_cell_pos == 999) and (not eri_cell_pos == 998):
                    new_CELL = eri_mss_pars + eri_cell_pars
                    df_eri_2g_cell_full.loc[eri_cell_count] = new_CELL
                    eri_cell_count += 1
                eri_cell_idx += 1
        eri_cell_idx += 1

    # DataFrame => Drop some columns to get just the most important ones.
    df_eri_2g_cell_full['CELL_NO'] = 'N/A'
    eri_col_names = ['MSS','Date','Time','CELL_NAME','CELL_NO','CGI','MCC','MNC','LAC','CI','NE','CO','RO','NCS','EA']
    df_eri_2g_cell_full = df_eri_2g_cell_full[eri_col_names]
    df_eri_2g_cell_summ = df_eri_2g_cell_full
    df_eri_2g_cell_full['LAI'] = df_eri_2g_cell_full['MCC'] + '-' + \
                                    df_eri_2g_cell_full['MNC'] + '-' + \
                                    df_eri_2g_cell_full['LAC']
    df_eri_2g_cell_full['MSS-LAI'] = df_eri_2g_cell_full['MSS'] + '-' + \
                                        df_eri_2g_cell_full['LAI']
    eri_drop_col = ['Date', 'Time', 'CO', 'RO', 'NCS', 'EA']
    df_eri_2g_cell_summ = df_eri_2g_cell_summ.drop(columns=eri_drop_col)
    eri_col_summ = ['MSS', 'NE', 'CELL_NAME', 'CELL_NO', 'MCC', 'MNC', 'LAC', 'CI', 'CGI']
    df_eri_2g_cell_summ = df_eri_2g_cell_summ[eri_col_summ]

    return df_eri_2g_cell_full, df_eri_2g_cell_summ

###############################################################################################################################################
def get_lai_x_rnc_nok(log_file_path):
    '''
    Function:   
        + Process a log_file with all the LAI x RNC mapping of NOKIA's MSSs
    Arguments:      
        + log_file_path => path to the log_file
    Output:     
        + df_full       => DataFrame with full LAI x RNC mapping of NOKIA's MSSs
        + df_summ       => DataFrame with summarized LAI x RNC mapping of NOKIA's MSSs
    '''
    
    # Variable control
    assert isinstance(log_file_path, str),'Path to look for the file must be string'
    assert len(log_file_path) > 0, 'File is empty'

    ###################################################### Code

    # Init NOKIA Variables
    nok_lai_mss_name = '0'
    nok_lai_mss_date = '0'
    nok_lai_mss_time = '0'
    nok_lai_rnc_name = '0'
    nok_lai_rnc_mcc = '0'
    nok_lai_rnc_mnc = '0'
    nok_lai_rnc_id = '0'
    nok_lai_rnc_mul_plmn = '0'
    nok_lai_rnc_stat = '0'
    nok_lai_rnc_ostat = '0'
    nok_lai_rnc_lai_mcc = '0'
    nok_lai_rnc_lai_mnc = '0'
    nok_lai_rnc_lai_no = '0'

    nok_mss_pars = [nok_lai_mss_name, nok_lai_mss_date, nok_lai_mss_time]
    nok_rnc_pars = [nok_lai_rnc_name, nok_lai_rnc_mcc, nok_lai_rnc_mnc, nok_lai_rnc_id, nok_lai_rnc_mul_plmn, 
                        nok_lai_rnc_stat, nok_lai_rnc_ostat]
    nok_rnc_lai_pars = [nok_lai_rnc_lai_mcc, nok_lai_rnc_lai_mnc, nok_lai_rnc_lai_no]

    nok_lai_idx = 0
    nok_lai_pos = 0
    nok_lai_rnc_count = 0
    nok_lai_rnc_flag = 0

    # Open & Load NOKIA logfile
    nok_logfile = open_file(log_file_path)

    # Create & Init & Set the NOKIA pd.DataFrame
    nok_col_names = ['MSS','Date','Time','RNC','RNC_MCC','RNC_MNC','RNC_ID','RNC_MULT_PLMN',
                        'RNC_STAT','RNC_OP_STAT','MCC','MNC','LAC']
    df_nok_lai_x_rnc_full = pd.DataFrame(columns=nok_col_names)
    df_nok_lai_x_rnc_full.loc[0] = [nok_lai_mss_name, nok_lai_mss_date, nok_lai_mss_time, nok_lai_rnc_name,
                                        nok_lai_rnc_mcc, nok_lai_rnc_mnc, nok_lai_rnc_id, nok_lai_rnc_mul_plmn, nok_lai_rnc_stat,
                                        nok_lai_rnc_ostat, nok_lai_rnc_lai_mcc, nok_lai_rnc_lai_mnc, nok_lai_rnc_lai_no]

    # Run the main program (txt => pd.DataFrame)
    while (nok_lai_idx < len(nok_logfile)-1):
        nok_lai_idx, nok_lai_pos, nok_mss_pars = get_mss_pars(nok_logfile, nok_lai_idx,'ZE2I::RT=ALL;')
        while (nok_lai_idx < len(nok_logfile)-1) and (not nok_lai_pos == 999):
            nok_lai_idx, nok_lai_pos, nok_rnc_pars = get_ze2i_rnc_pars(nok_logfile, nok_lai_idx)
            while (nok_lai_idx < len(nok_logfile)-1) and (not nok_lai_pos == 999):
                nok_lai_idx, nok_lai_pos, nok_lai_rnc_flag, nok_rnc_lai_pars = get_ze2i_rnc_lac_pars(nok_logfile, nok_lai_idx, nok_lai_rnc_flag)
                if nok_lai_pos == 999:                                          # if 'COMMAND EXECUTED'
                    nok_lai_idx += 1                                            # Increase index to read next line
                    break
                else:
                    if (nok_lai_rnc_flag == 1):
                        new_rnc_lai = nok_mss_pars + nok_rnc_pars + nok_rnc_lai_pars
                        df_nok_lai_x_rnc_full.loc[nok_lai_rnc_count] = new_rnc_lai
                        nok_lai_rnc_count += 1
                    else:
                        break
                
    # DataFrame => Drop some columns to get just the most important ones.
    df_nok_lai_x_rnc_summ = df_nok_lai_x_rnc_full
    df_nok_lai_x_rnc_full['MSS'] = df_nok_lai_x_rnc_full['MSS'].str.replace(r'0', '')
    df_nok_lai_x_rnc_summ['MSS'] = df_nok_lai_x_rnc_summ['MSS'].str.replace(r'0', '')
    df_nok_lai_x_rnc_full['LAI'] = df_nok_lai_x_rnc_full['MCC'] + '-' + \
                                    df_nok_lai_x_rnc_full['MNC'] + '-' + \
                                    df_nok_lai_x_rnc_full['LAC']
    df_nok_lai_x_rnc_full['MSS-LAI'] = df_nok_lai_x_rnc_full['MSS'] + '-' + \
                                        df_nok_lai_x_rnc_full['LAI']
    df_nok_lai_x_rnc_full['NE-LAI'] = df_nok_lai_x_rnc_full['RNC'] + '-' + \
                                        df_nok_lai_x_rnc_full['LAI']
    df_nok_lai_x_rnc_summ['LAI'] = df_nok_lai_x_rnc_summ['MCC'] + '-' + \
                                    df_nok_lai_x_rnc_summ['MNC'] + '-' + \
                                    df_nok_lai_x_rnc_summ['LAC']
    df_nok_lai_x_rnc_summ['MSS-LAI'] = df_nok_lai_x_rnc_summ['MSS'] + '-' + \
                                        df_nok_lai_x_rnc_summ['LAI']
    df_nok_lai_x_rnc_summ['NE-LAI'] = df_nok_lai_x_rnc_summ['RNC'] + '-' + \
                                        df_nok_lai_x_rnc_summ['LAI']
    nok_drop_col = ['RNC_MCC', 'RNC_MNC', 'RNC_MULT_PLMN', 'RNC_STAT', 'RNC_OP_STAT', 'RNC_ID']
    df_nok_lai_x_rnc_summ = df_nok_lai_x_rnc_summ.drop(columns=nok_drop_col)
    nok_col_summ = ['MSS', 'Date', 'Time', 'MCC', 'MNC', 'LAC', 'LAI', 'MSS-LAI', 'NE-LAI', 'RNC']
    df_nok_lai_x_rnc_summ = df_nok_lai_x_rnc_summ[nok_col_summ]

    return df_nok_lai_x_rnc_full, df_nok_lai_x_rnc_summ

###############################################################################################################################################
def get_lai_x_rnc_eri(log_file_path):
    '''
    Function:   
        + Process a log_file with all the LAI x RNC mapping of ERICSSON's MSSs
    Arguments:      
        + log_file_path => path to the log_file
    Output:     
        + df_full       => DataFrame with full LAI x RNC mapping of ERICSSON's MSSs
        + df_summ       => DataFrame with summarized LAI x RNC mapping of ERICSSON's MSSs
    '''
    
    # Variable control
    assert isinstance(log_file_path, str),'Path to look for the file must be string'
    assert len(log_file_path) > 0, 'File is empty'

    ###################################################### Code

    # Init ERICSSON Variables
    eri_lai_mss_name = '0'
    eri_lai_mss_date = '0'
    eri_lai_mss_time = '0'
    eri_rnc_name = '0'
    eri_rnc_lai_mcc = '0'
    eri_rnc_lai_mnc = '0'
    eri_rnc_lai_no = '0'

    eri_mss_pars = [eri_lai_mss_name, eri_lai_mss_date, eri_lai_mss_time]
    eri_rnc_pars = [eri_rnc_name]
    eri_rnc_lai_pars = [eri_rnc_lai_mcc, eri_rnc_lai_mnc, eri_rnc_lai_no]

    eri_lai_idx = 0
    eri_lai_pos = 0
    eri_lai_count = 0
    eri_lai_flag = 0

    # Open & Load ERICSSON logfile
    eri_logfile = open_file(log_file_path)

    # Create & Init & Set the ERICSSON pd.DataFrame
    eri_col_names = ['MSS','Date','Time','RNC','MCC','MNC','LAC']
    df_eri_lai_x_rnc_full = pd.DataFrame(columns=eri_col_names)
    df_eri_lai_x_rnc_full.loc[0] = [eri_lai_mss_name, eri_lai_mss_date, eri_lai_mss_time, eri_rnc_name,
                                        eri_rnc_lai_mcc, eri_rnc_lai_mnc, eri_rnc_lai_no]

    # Run the main program (txt => pd.DataFrame)
    while (eri_lai_idx < len(eri_logfile)-1):
        eri_lai_idx, eri_lai_pos, eri_mss_pars = get_mss_pars(eri_logfile, eri_lai_idx,'eaw')
        while(eri_lai_pos >= 0) and (not eri_lai_pos == 998):
            eri_lai_idx, eri_lai_pos, eri_rnc_pars = get_mgmap_rnc_pars(eri_logfile, eri_lai_idx)
            if (eri_lai_pos >= 0) and (not eri_lai_pos == 999) and (not eri_lai_pos == 998):
                eri_lai_idx, eri_lai_pos, eri_rnc_lai_pars = get_mgmap_rnc_lac_pars(eri_logfile, eri_lai_idx)
                while(eri_lai_pos >= 0) and (not eri_lai_pos == 999) and (not eri_lai_pos == 998):
                    eri_lai_idx, eri_lai_pos, eri_rnc_lai_pars = get_mgmap_rnc_lac_pars(eri_logfile, eri_lai_idx)
                    if(eri_lai_pos >= 0) and (not eri_lai_pos == 999) and (not eri_lai_pos == 998):
                        new_lai_rnc = eri_mss_pars + eri_rnc_pars + eri_rnc_lai_pars
                        df_eri_lai_x_rnc_full.loc[eri_lai_count] = new_lai_rnc
                        eri_lai_count += 1
                    eri_lai_idx += 1
            eri_lai_idx += 1
        eri_lai_idx += 1

    # DataFrame => Drop some columns to get just the most important ones.
    df_eri_lai_x_rnc_summ = df_eri_lai_x_rnc_full
    df_eri_lai_x_rnc_full['LAI'] =  df_eri_lai_x_rnc_full['MCC'] + '-' + \
                                    df_eri_lai_x_rnc_full['MNC'] + '-' + \
                                    df_eri_lai_x_rnc_full['LAC']
    df_eri_lai_x_rnc_full['MSS-LAI'] =  df_eri_lai_x_rnc_full['MSS'] + '-' + \
                                        df_eri_lai_x_rnc_full['LAI']
    df_eri_lai_x_rnc_full['NE-LAI'] =  df_eri_lai_x_rnc_full['RNC'] + '-' + \
                                        df_eri_lai_x_rnc_full['LAI']
    df_eri_lai_x_rnc_summ['LAI'] =  df_eri_lai_x_rnc_summ['MCC'] + '-' + \
                                    df_eri_lai_x_rnc_summ['MNC'] + '-' + \
                                    df_eri_lai_x_rnc_summ['LAC']
    df_eri_lai_x_rnc_summ['MSS-LAI'] =  df_eri_lai_x_rnc_summ['MSS'] + '-' + \
                                        df_eri_lai_x_rnc_summ['LAI']
    df_eri_lai_x_rnc_summ['NE-LAI'] =  df_eri_lai_x_rnc_summ['RNC'] + '-' + \
                                        df_eri_lai_x_rnc_summ['LAI']
    eri_drop_col = []
    df_eri_lai_x_rnc_summ = df_eri_lai_x_rnc_summ.drop(columns=eri_drop_col)
    eri_col_summ = ['MSS', 'Date', 'Time', 'MCC', 'MNC', 'LAC', 'LAI', 'MSS-LAI', 'NE-LAI', 'RNC']
    df_eri_lai_x_rnc_summ = df_eri_lai_x_rnc_summ[eri_col_summ]

    return df_eri_lai_x_rnc_full, df_eri_lai_x_rnc_summ

###############################################################################################################################################
def get_3g_cell_no_ne_nok(log_file_path):
    '''
    Function:   
        + Process a log_file with all the 3G cells of NOKIA's MSSs
    Arguments:      
        + log_file_path => path to the log_file
    Output:     
        + df_full       => DataFrame with full 3G cells of NOKIA's MSSs information
        + df_summ       => DataFrame with summarized 3G cells of NOKIA's MSSs information
    '''
    
    # Variable control
    assert isinstance(log_file_path, str),'Path to look for the file must be string'
    assert len(log_file_path) > 0, 'File is empty'

    ###################################################### Code

    # Init NOKIA Variables
    nok_sa_mss_name = '0'
    nok_sa_mss_date = '0'
    nok_sa_mss_time = '0'
    nok_sa_name = '0'
    nok_sa_no = '0'
    nok_sa_lac_name = '0'
    nok_sa_lac_no = '0'
    nok_sa_mcc = '0'
    nok_sa_mnc = '0'
    nok_sa_ci = '0'
    nok_sa_stat = '0'
    nok_sa_rz = '0'
    nok_sa_cdr = '0'

    nok_mss_pars = [nok_sa_mss_name, nok_sa_mss_date, nok_sa_mss_time]
    nok_sa_pars = [nok_sa_name, nok_sa_no, nok_sa_lac_name, nok_sa_lac_no, nok_sa_mcc, nok_sa_mnc,
                    nok_sa_ci, nok_sa_stat, nok_sa_rz, nok_sa_cdr]

    nok_sa_idx = 0
    nok_sa_pos = 0
    nok_sa_count = 0

    # Open & Load NOKIA logfile
    nok_logfile = open_file(log_file_path)

    # Create & Init & Set the NOKIA pd.DataFrame
    nok_col_names = ['MSS','Date','Time','CELL_NAME','CELL_NO','LAC_Name', 'LAC','MCC','MNC','CI','Status','RZ', 'CDR']
    df_nok_3g_cell_no_ne_full = pd.DataFrame(columns=nok_col_names)
    df_nok_3g_cell_no_ne_full.loc[0] = [nok_sa_mss_name, nok_sa_mss_date, nok_sa_mss_time, nok_sa_name, nok_sa_no,
                                            nok_sa_lac_name, nok_sa_lac_no, nok_sa_mcc, nok_sa_mnc, nok_sa_ci,
                                            nok_sa_stat, nok_sa_rz, nok_sa_cdr]

    # Run the main program (txt => pd.DataFrame)
    while (nok_sa_idx < len(nok_logfile)-1):
        nok_sa_idx, nok_sa_pos, nok_mss_pars = get_mss_pars(nok_logfile, nok_sa_idx,'ZEPO:TYPE=SA;')
        while (nok_sa_idx < len(nok_logfile)-1) and (not nok_sa_pos == 999):
            nok_sa_idx, nok_sa_pos, nok_sa_pars = get_zepo_3g_sa_pars(nok_logfile, nok_sa_idx)
            if (nok_sa_pos >= 0) and (not nok_sa_pos == 999):
                new_SA = nok_mss_pars + nok_sa_pars
                df_nok_3g_cell_no_ne_full.loc[nok_sa_count] = new_SA
                nok_sa_count += 1
        nok_sa_idx += 1

    # DataFrame => Drop some columns to get just the most important ones.
    df_nok_3g_cell_no_ne_summ = df_nok_3g_cell_no_ne_full
    df_nok_3g_cell_no_ne_full['MSS'] = df_nok_3g_cell_no_ne_full['MSS'].str.replace(r'0', '')
    df_nok_3g_cell_no_ne_summ['MSS'] = df_nok_3g_cell_no_ne_summ['MSS'].str.replace(r'0', '')
    df_nok_3g_cell_no_ne_full['LAI'] = df_nok_3g_cell_no_ne_full['MCC'] + '-' + \
                                        df_nok_3g_cell_no_ne_full['MNC'] + '-' + \
                                        df_nok_3g_cell_no_ne_full['LAC']
    df_nok_3g_cell_no_ne_full['MSS-LAI'] = df_nok_3g_cell_no_ne_full['MSS'] + '-' + \
                                            df_nok_3g_cell_no_ne_full['LAI']
    df_nok_3g_cell_no_ne_summ['CGI'] =  df_nok_3g_cell_no_ne_summ['MCC'] + '-' + \
                                            df_nok_3g_cell_no_ne_summ['MNC'] + '-' + \
                                            df_nok_3g_cell_no_ne_summ['LAC'] + '-' + \
                                            df_nok_3g_cell_no_ne_summ['CI']
    nok_drop_col = ['Date', 'Time', 'LAC_Name', 'Status', 'RZ', 'CDR']
    df_nok_3g_cell_no_ne_summ = df_nok_3g_cell_no_ne_summ.drop(columns=nok_drop_col)
    nok_col_summ = ['MSS', 'CELL_NAME', 'CELL_NO', 'MCC', 'MNC', 'LAC', 'CI', 'CGI']
    df_nok_3g_cell_no_ne_summ = df_nok_3g_cell_no_ne_summ[nok_col_summ]
    
    return df_nok_3g_cell_no_ne_full, df_nok_3g_cell_no_ne_summ

###############################################################################################################################################
def get_3g_cell_no_ne_eri(log_file_path):
    '''
    Function:   
        + Process a log_file with all the 3G cells of ERICSSON's MSSs
    Arguments:      
        + log_file_path => path to the log_file
    Output:     
        + df_full       => DataFrame with full 3G cells of ERICSSON's MSSs information
        + df_summ       => DataFrame with summarized 2G cells of ERICSSON's MSSs information
    '''
    
    # Variable control
    assert isinstance(log_file_path, str),'Path to look for the file must be string'
    assert len(log_file_path) > 0, 'File is empty'

    ###################################################### Code

    # Init ERICSSON Variables
    eri_area_mss_name = '0'
    eri_area_mss_date = '0'
    eri_area_mss_time = '0'
    eri_area_name = '0'
    eri_area_cgi = '0'
    eri_area_mcc = '0'
    eri_area_mnc = '0'
    eri_area_lac = '0'
    eri_area_ci = '0'
    eri_area_ro = '0'
    eri_area_co = '0'
    eri_area_ea = '0'

    eri_mss_pars = [eri_area_mss_name, eri_area_mss_date, eri_area_mss_time]
    eri_area_pars = [eri_area_name, eri_area_cgi, eri_area_mcc, eri_area_mnc,
                        eri_area_lac, eri_area_ci, eri_area_ro, eri_area_co, eri_area_ea]

    eri_area_idx = 0
    eri_area_pos = 0
    eri_area_count = 0

    # Open & Load ERICSSON logfile
    eri_logfile = open_file(log_file_path)

    # Create & Init & Set the ERICSSON pd.DataFrame
    eri_col_names = ['MSS','Date','Time','CELL_NAME','CGI','MCC','MNC','LAC','CI','RO','CO','EA']
    df_eri_3g_cell_no_ne_full = pd.DataFrame(columns=eri_col_names)
    df_eri_3g_cell_no_ne_full.loc[0] = [eri_area_mss_name, eri_area_mss_date, eri_area_mss_time,
                                            eri_area_name, eri_area_cgi, eri_area_mcc, eri_area_mnc,
                                            eri_area_lac, eri_area_ci, eri_area_ro, eri_area_co, eri_area_ea]

    # Run the main program (txt => pd.DataFrame)
    while (eri_area_idx < len(eri_logfile)-1):
        eri_area_idx, eri_area_pos, eri_mss_pars = get_mss_pars(eri_logfile, eri_area_idx,'eaw')
        if (eri_area_pos >= 0) and (not eri_area_pos == 999) and (not eri_area_pos == 998):
            eri_area_idx, eri_area_pos, eri_area_pars = get_mgaap_area_pars(eri_logfile, eri_area_idx)
            while(eri_area_pos >= 0) and (not eri_area_pos == 999) and (not eri_area_pos == 998):
                eri_area_idx, eri_area_pos, eri_area_pars = get_mgaap_area_pars(eri_logfile, eri_area_idx)
                if(eri_area_pos >= 0) and (not eri_area_pos == 999) and (not eri_area_pos == 998):
                    new_area = eri_mss_pars + eri_area_pars
                    df_eri_3g_cell_no_ne_full.loc[eri_area_count] = new_area
                    eri_area_count += 1
                eri_area_idx += 1
        eri_area_idx += 1

    # DataFrame => Drop some columns to get just the most important ones.
    df_eri_3g_cell_no_ne_full['CELL_NO'] = 'N/A'
    eri_col_names = ['MSS','Date','Time','CELL_NAME','CELL_NO','CGI','MCC','MNC','LAC','CI','RO','CO','EA']
    df_eri_3g_cell_no_ne_full = df_eri_3g_cell_no_ne_full[eri_col_names]
    df_eri_3g_cell_no_ne_summ = df_eri_3g_cell_no_ne_full
    df_eri_3g_cell_no_ne_full['LAI'] =  df_eri_3g_cell_no_ne_full['MCC'] + '-' + \
                                        df_eri_3g_cell_no_ne_full['MNC'] + '-' + \
                                        df_eri_3g_cell_no_ne_full['LAC']
    df_eri_3g_cell_no_ne_full['MSS-LAI'] =  df_eri_3g_cell_no_ne_full['MSS'] + '-' + \
                                            df_eri_3g_cell_no_ne_full['LAI']
    eri_drop_col = ['Date', 'Time', 'CO', 'RO', 'EA']
    df_eri_3g_cell_no_ne_summ = df_eri_3g_cell_no_ne_summ.drop(columns=eri_drop_col)
    eri_col_summ = ['MSS', 'CELL_NAME', 'CELL_NO', 'MCC', 'MNC', 'LAC', 'CI', 'CGI']
    df_eri_3g_cell_no_ne_summ = df_eri_3g_cell_no_ne_summ[eri_col_summ]

    return df_eri_3g_cell_no_ne_full, df_eri_3g_cell_no_ne_summ

###############################################################################################################################################
def get_3g_cell_nok(log_file_3g_cell_path, log_file_lai_x_rnc_mapp_path):
    '''
    Function:   
        + Process two log_files with all the 3G cells of NOKIA's MSSs and the LAI<=>RNC mapping
    Arguments:      
        + log_file_3g_cell_path         => path to the 3G cells of NOKIA's MSSs log_file
        + log_file_lai_x_rnc_mapp_path  => path to the LAI<=>RNC mapping of NOKIA's MSSs log_file
    Output:     
        + df_full                       => DataFrame with full 3G cells of NOKIA's MSSs including the LAI<=>RNC mapping
        + df_summ                       => DataFrame with summarized 3G cells of NOKIA's MSSs including the LAI<=>RNC mapping
    '''
    
    # Variable control
    assert isinstance(log_file_3g_cell_path, str),'Path to look for the file must be string'
    assert len(log_file_3g_cell_path) > 0, 'File is empty'
    assert isinstance(log_file_lai_x_rnc_mapp_path, str),'Path to look for the file must be string'
    assert len(log_file_lai_x_rnc_mapp_path) > 0, 'File is empty'

    ###################################################### Code

    df_nok_3g_cell_no_ne_full, df_nok_3g_cell_no_ne_summ = get_3g_cell_no_ne_nok(log_file_3g_cell_path)     # Get the 3G cells (no NE info)
    df_nok_lai_x_rnc_full, df_nok_lai_x_rnc_summ = get_lai_x_rnc_nok(log_file_lai_x_rnc_mapp_path)          # Get the LAI<=>RNC mapping

    ###################################################### Code (join LAI<=>RNC mapping with the 3G cells)
    df_nok_3g_cell_no_ne_summ['LAI'] = df_nok_3g_cell_no_ne_summ['MCC'] + '-' + \
                                        df_nok_3g_cell_no_ne_summ['MNC'] + '-' + \
                                        df_nok_3g_cell_no_ne_summ['LAC']
    df_nok_3g_cell_no_ne_summ['MSS-LAI'] = df_nok_3g_cell_no_ne_summ['MSS'] + '-' + \
                                            df_nok_3g_cell_no_ne_summ['LAI']
    df_nok_3g_cell_no_ne_full['LAI'] = df_nok_3g_cell_no_ne_full['MCC'] + '-' + \
                                        df_nok_3g_cell_no_ne_full['MNC'] + '-' + \
                                        df_nok_3g_cell_no_ne_full['LAC']
    df_nok_3g_cell_no_ne_full['MSS-LAI'] = df_nok_3g_cell_no_ne_full['MSS'] + '-' + \
                                            df_nok_3g_cell_no_ne_full['LAI']

    # Create a dictionary to map MSS-LAI to RNC & mapping on key=MSS-LAI
    my_dict = dict(zip(df_nok_lai_x_rnc_summ['MSS-LAI'], df_nok_lai_x_rnc_summ['RNC']))         # Create a dictionary to map MSS-LAI to RNC
    df_nok_3g_cell_no_ne_full['NE'] = df_nok_3g_cell_no_ne_full['MSS-LAI'].map(my_dict)         # Create a new column NE (RNC) for mapping on key=MSS-LAI
    df_nok_3g_cell_no_ne_summ['NE'] = df_nok_3g_cell_no_ne_summ['MSS-LAI'].map(my_dict)         # Create a new column NE (RNC) for mapping on key=MSS-LAI
    df_nok_3g_cell_full = df_nok_3g_cell_no_ne_full                                    
    df_nok_3g_cell_summ = df_nok_3g_cell_no_ne_summ
    nok_drop_col = ['LAI', 'MSS-LAI']                                                           # Define columns to drop 
    df_nok_3g_cell_summ = df_nok_3g_cell_summ.drop(columns=nok_drop_col)                        # Drop columns
    nok_col_summ = ['MSS', 'NE', 'CELL_NAME', 'CELL_NO', 'MCC', 'MNC', 'LAC', 'CI', 'CGI']      # Define the column's order
    df_nok_3g_cell_summ = df_nok_3g_cell_summ[nok_col_summ]                                     # Order the collumns

    return df_nok_3g_cell_full, df_nok_3g_cell_summ

###############################################################################################################################################
def get_3g_cell_eri(log_file_3g_cell_path, log_file_lai_x_rnc_mapp_path):
    '''
    Function:   
        + Process two log_files with all the 3G cells of ERICSSON's MSSs and the LAI<=>RNC mapping
    Arguments:      
        + log_file_3g_cell_path         => path to the 3G cells of ERICSSON's MSSs log_file
        + log_file_lai_x_rnc_mapp_path  => path to the LAI<=>RNC mapping of ERICSSON's MSSs log_file
    Output:     
        + df_full                       => DataFrame with full 3G cells of ERICSSON's MSSs including the LAI<=>RNC mapping
        + df_summ                       => DataFrame with summarized 3G cells of ERICSSON's MSSs including the LAI<=>RNC mapping
    '''
    
    # Variable control
    assert isinstance(log_file_3g_cell_path, str),'Path to look for the file must be string'
    assert len(log_file_3g_cell_path) > 0, 'File is empty'
    assert isinstance(log_file_lai_x_rnc_mapp_path, str),'Path to look for the file must be string'
    assert len(log_file_lai_x_rnc_mapp_path) > 0, 'File is empty'

    ###################################################### Code

    df_eri_3g_cell_no_ne_full, df_eri_3g_cell_no_ne_summ = get_3g_cell_no_ne_eri(log_file_3g_cell_path)     # Get the 3G cells (no NE info)
    df_eri_lai_x_rnc_full, df_eri_lai_x_rnc_summ = get_lai_x_rnc_eri(log_file_lai_x_rnc_mapp_path)          # Get the LAI<=>RNC mapping

    ###################################################### Code (join LAI<=>RNC mapping with the 3G cells)
    df_eri_3g_cell_no_ne_summ['LAI'] = df_eri_3g_cell_no_ne_summ['MCC'] + '-' + \
                                        df_eri_3g_cell_no_ne_summ['MNC'] + '-' + \
                                        df_eri_3g_cell_no_ne_summ['LAC']
    df_eri_3g_cell_no_ne_summ['MSS-LAI'] = df_eri_3g_cell_no_ne_summ['MSS'] + '-' + \
                                            df_eri_3g_cell_no_ne_summ['LAI']
    df_eri_3g_cell_no_ne_full['LAI'] = df_eri_3g_cell_no_ne_full['MCC'] + '-' + \
                                        df_eri_3g_cell_no_ne_full['MNC'] + '-' + \
                                        df_eri_3g_cell_no_ne_full['LAC']
    df_eri_3g_cell_no_ne_full['MSS-LAI'] = df_eri_3g_cell_no_ne_full['MSS'] + '-' + \
                                            df_eri_3g_cell_no_ne_full['LAI']

    # Create a dictionary to map MSS-LAI to RNC & mapping on key=MSS-LAI
    my_dict = dict(zip(df_eri_lai_x_rnc_summ['MSS-LAI'], df_eri_lai_x_rnc_summ['RNC']))         # Create a dictionary to map MSS-LAI to RNC
    df_eri_3g_cell_no_ne_full['NE'] = df_eri_3g_cell_no_ne_full['MSS-LAI'].map(my_dict)         # Create a new column NE (RNC) for mapping on key=MSS-LAI
    df_eri_3g_cell_no_ne_summ['NE'] = df_eri_3g_cell_no_ne_summ['MSS-LAI'].map(my_dict)         # Create a new column NE (RNC) for mapping on key=MSS-LAI
    df_eri_3g_cell_full = df_eri_3g_cell_no_ne_full                                    
    df_eri_3g_cell_summ = df_eri_3g_cell_no_ne_summ
    nok_drop_col = ['LAI', 'MSS-LAI']                                                           # Define columns to drop 
    df_eri_3g_cell_summ = df_eri_3g_cell_summ.drop(columns=nok_drop_col)                        # Drop columns
    nok_col_summ = ['MSS', 'NE', 'CELL_NAME', 'CELL_NO', 'MCC', 'MNC', 'LAC', 'CI', 'CGI']      # Define the column's order
    df_eri_3g_cell_summ = df_eri_3g_cell_summ[nok_col_summ]                                     # Order the collumns

    return df_eri_3g_cell_full, df_eri_3g_cell_summ

###############################################################################################################################################
def get_def_lai_nok(log_file_path):
    '''
    Function:   
        + Process a log_file with all defined LAIs of NOKIA's MSSs
    Arguments:      
        + log_file_path => path to the log_file
    Output:     
        + df_full       => DataFrame with full defined LAIs of NOKIA's MSSs
        + df_summ       => DataFrame with summarized defined LAIS of NOKIA's MSSs
    '''
    
    # Variable control
    assert isinstance(log_file_path, str),'Path to look for the file must be string'
    assert len(log_file_path) > 0, 'File is empty'

    ###################################################### Code

    # Init NOKIA Variables
    nok_lai_def_mss_name = '0'
    nok_lai_def_mss_date = '0'
    nok_lai_def_mss_time = '0'
    nok_lai_def_mcc = '0'
    nok_lai_def_mnc = '0'
    nok_lai_def_no = '0'
    nok_lai_def_name = '0'
    nok_lai_def_at = '0'
    nok_lai_def_repag = '0'
    nok_lai_def_rngp = '0'
    nok_lai_def_mnc_al = '0'
    nok_lai_def_dsav = '0'
    nok_lai_def_tz = '0'
    nok_lai_def_honla = '0'

    nok_mss_pars = [nok_lai_def_mss_name, nok_lai_def_mss_date, nok_lai_def_mss_time]
    nok_lai_def_pars = [nok_lai_def_mcc, nok_lai_def_mnc, nok_lai_def_no, nok_lai_def_name, nok_lai_def_at,
                        nok_lai_def_repag, nok_lai_def_rngp, nok_lai_def_mnc_al, nok_lai_def_dsav,
                        nok_lai_def_tz, nok_lai_def_honla]

    nok_lai_def_idx = 0
    nok_lai_def_pos = 0
    nok_lai_def_count = 0

    # Open & Load NOKIA logfile
    nok_logfile = open_file(log_file_path)

    # Create & Init & Set the NOKIA pd.DataFrame
    nok_col_names = ['MSS','Date','Time','MCC','MNC','LAC','LAC_NAME','AT','INT','RNGP','MNC_AL','DSAV','TZ','HONLA']
    df_nok_lai_def_mss_full = pd.DataFrame(columns=nok_col_names)
    df_nok_lai_def_mss_full.loc[0] = [nok_lai_def_mss_name, nok_lai_def_mss_date, nok_lai_def_mss_time, nok_lai_def_mcc,
                                        nok_lai_def_mnc, nok_lai_def_no, nok_lai_def_name, nok_lai_def_at,
                                        nok_lai_def_repag, nok_lai_def_rngp, nok_lai_def_mnc_al, nok_lai_def_dsav,
                                        nok_lai_def_tz, nok_lai_def_honla]

    # Run the main program (txt => pd.DataFrame)
    while (nok_lai_def_idx < len(nok_logfile)-1):
        nok_lai_def_idx, nok_lai_def_pos, nok_mss_pars = get_mss_pars(nok_logfile, nok_lai_def_idx,'ZELO;')
        while (nok_lai_def_idx < len(nok_logfile)-1) and (not nok_lai_def_pos == 999):
            nok_lai_def_idx, nok_lai_def_pos, nok_lai_def_pars = get_zelo_lac_pars(nok_logfile,nok_lai_def_idx)
            if nok_lai_def_pos == 999:                              # if 'COMMAND EXECUTED'
                nok_lai_def_idx += 1                                # Increase index to read next line
            else:
                new_lai = nok_mss_pars + nok_lai_def_pars
                df_nok_lai_def_mss_full.loc[nok_lai_def_count] = new_lai
                nok_lai_def_count += 1

    # DataFrame => Drop some columns to get just the most important ones.
    df_nok_lai_def_mss_full['LAC'] =  df_nok_lai_def_mss_full['LAC'].astype(int)
    df_nok_lai_def_mss_full['LAC'] =  df_nok_lai_def_mss_full['LAC'].astype(str)
    df_nok_lai_def_mss_full['MSS'] = df_nok_lai_def_mss_full['MSS'].str.replace(r'0', '')
    df_nok_lai_def_mss_summ = df_nok_lai_def_mss_full
    nok_drop_col = ['AT','INT','RNGP','MNC_AL','DSAV','TZ','HONLA']
    df_nok_lai_def_mss_summ = df_nok_lai_def_mss_summ.drop(columns=nok_drop_col)
    df_nok_lai_def_mss_full['LAI'] =  df_nok_lai_def_mss_full['MCC'] + '-' + \
                                        df_nok_lai_def_mss_full['MNC'] + '-' + \
                                        df_nok_lai_def_mss_full['LAC']
    df_nok_lai_def_mss_full['MSS-LAI'] = df_nok_lai_def_mss_full['MSS'] + '-' + \
                                            df_nok_lai_def_mss_full['LAI']
    df_nok_lai_def_mss_summ['LAI'] =  df_nok_lai_def_mss_summ['MCC'] + '-' + \
                                        df_nok_lai_def_mss_summ['MNC'] + '-' + \
                                        df_nok_lai_def_mss_summ['LAC']
    df_nok_lai_def_mss_summ['MSS-LAI'] = df_nok_lai_def_mss_summ['MSS'] + '-' + \
                                            df_nok_lai_def_mss_summ['LAI']
    nok_col_summ = ['MSS','Date','Time','MCC','MNC','LAC','LAI','MSS-LAI']
    df_nok_lai_def_mss_summ = df_nok_lai_def_mss_summ[nok_col_summ]

    return df_nok_lai_def_mss_full, df_nok_lai_def_mss_summ

###############################################################################################################################################
def get_def_lai_eri(log_file_path):
    '''
    Function:   
        + Process a log_file with all defined LAIs of ERICSSON's MSSs
    Arguments:      
        + log_file_path => path to the log_file
    Output:     
        + df_full       => DataFrame with full defined LAIs of ERICSSON's MSSs
        + df_summ       => DataFrame with summarized defined LAIs of ERICSSON's MSSs
    '''
    
    # Variable control
    assert isinstance(log_file_path, str),'Path to look for the file must be string'
    assert len(log_file_path) > 0, 'File is empty'

    ###################################################### Code

    # Init ERICSSON Variables
    eri_lai_def_mss_name = '0'
    eri_lai_def_mss_date = '0'
    eri_lai_def_mss_time = '0'
    eri_lai_def_mcc = '0'
    eri_lai_def_mnc = '0'
    eri_lai_def_no = '0'
    eri_lai_def = '0'
    eri_lai_pfc = '0'
    eri_lai_prl = '0'
    eri_lai_pool = '0'

    eri_mss_pars = [eri_lai_def_mss_name, eri_lai_def_mss_date, eri_lai_def_mss_time]
    eri_lai_def_pars = [eri_lai_def_mcc, eri_lai_def_mnc, eri_lai_def_no, eri_lai_def, eri_lai_pfc , eri_lai_prl, eri_lai_pool]

    eri_lai_def_idx = 0
    eri_lai_def_pos = 0
    eri_lai_def_count = 0

    # Open & Load ERICSSON logfile
    eri_logfile = open_file(log_file_path)

    # Create & Init & Set the ERICSSON pd.DataFrame
    eri_col_names = ['MSS','Date','Time','MCC','MNC','LAC','LAI','PFC','PRL','POOL']
    df_eri_lai_def_mss_full = pd.DataFrame(columns=eri_col_names)
    df_eri_lai_def_mss_full.loc[0] = [eri_lai_def_mss_name, eri_lai_def_mss_date, eri_lai_def_mss_time, eri_lai_def_mcc,
                                        eri_lai_def_mnc, eri_lai_def_no, eri_lai_def, eri_lai_pfc , eri_lai_prl, eri_lai_pool]

    # Run the main program (txt => pd.DataFrame)
    while (eri_lai_def_idx < len(eri_logfile)-1):
        eri_lai_def_idx, eri_lai_def_pos, eri_mss_pars = get_mss_pars(eri_logfile, eri_lai_def_idx,'eaw')
        if (eri_lai_def_pos >= 0) and (not eri_lai_def_pos == 999) and (not eri_lai_def_pos == 998):
            eri_lai_def_idx, eri_lai_def_pos, eri_lai_def_pars = get_mglap_lac_pars(eri_logfile, eri_lai_def_idx)
            while(eri_lai_def_pos >= 0) and (not eri_lai_def_pos == 999) and (not eri_lai_def_pos == 998):
                RI_index, eri_lai_def_pos, eri_lai_def_pars = get_mglap_lac_pars(eri_logfile, eri_lai_def_idx)
                if(eri_lai_def_pos >= 0) and (not eri_lai_def_pos == 999) and (not eri_lai_def_pos == 998):
                    new_lai = eri_mss_pars + eri_lai_def_pars
                    df_eri_lai_def_mss_full.loc[eri_lai_def_count] = new_lai
                    eri_lai_def_count += 1
                eri_lai_def_idx += 1
        eri_lai_def_idx += 1

    # DataFrame => Drop some columns to get just the most important ones.
    df_eri_lai_def_mss_summ = df_eri_lai_def_mss_full
    eri_drop_col = ['PFC','PRL','POOL']
    df_eri_lai_def_mss_summ = df_eri_lai_def_mss_summ.drop(columns=eri_drop_col)
    df_eri_lai_def_mss_full['MSS-LAI'] = df_eri_lai_def_mss_full['MSS'] + '-' + \
                                            df_eri_lai_def_mss_full['LAI']
    df_eri_lai_def_mss_summ['MSS-LAI'] = df_eri_lai_def_mss_summ['MSS'] + '-' + \
                                            df_eri_lai_def_mss_summ['LAI']
    eri_col_summ = ['MSS','Date','Time','MCC','MNC','LAC','LAI','MSS-LAI']
    df_eri_lai_def_mss_summ = df_eri_lai_def_mss_summ[eri_col_summ]

    return df_eri_lai_def_mss_full, df_eri_lai_def_mss_summ

###############################################################################################################################################
def get_r30k_lai_nok(log_file_path):
    '''
    Function:   
        + Process a log_file with all R30k LAIs of NOKIA's MSSs
    Arguments:      
        + log_file_path => path to the log_file
    Output:     
        + df_full       => DataFrame with full R30k LAIs of NOKIA's MSSs
        + df_summ       => DataFrame with summarized R30k LAIS of NOKIA's MSSs
    '''
    
    # Variable control
    assert isinstance(log_file_path, str),'Path to look for the file must be string'
    assert len(log_file_path) > 0, 'File is empty'

    ###################################################### Code

    # Init NOKIA Variables
    nok_lai_r30k_mss_name = '0'
    nok_lai_r30k_mss_date = '0'
    nok_lai_r30k_mss_time = '0'
    nok_lai_r30k_no = '0'
    nok_lai_r30k_name = '0'
    nok_lai_r30k_zc0 = '0'
    nok_lai_r30k_zc1 = '0'
    nok_lai_r30k_zc2 = '0'
    nok_lai_r30k_zc3 = '0'
    nok_lai_r30k_zc4 = '0'
    nok_lai_r30k_zc5 = '0'

    nok_mss_pars = [nok_lai_r30k_mss_name, nok_lai_r30k_mss_date, nok_lai_r30k_mss_time]
    nok_lai_r30k_pars = [nok_lai_r30k_no, nok_lai_r30k_name, nok_lai_r30k_zc0, nok_lai_r30k_zc1, nok_lai_r30k_zc2, nok_lai_r30k_zc3,
                        nok_lai_r30k_zc4, nok_lai_r30k_zc5]

    nok_lai_r30k_idx = 0
    nok_lai_r30k_pos = 0
    nok_lai_r30k_count = 0

    # Open & Load NOKIA logfile
    nok_logfile = open_file(log_file_path)

    # Create & Init & Set the NOKIA pd.DataFrame
    nok_col_names = ['MSS','Date','Time', 'LAC','LAC_NAME', 'Claro_Roam', 'Vivo_Roam', 'Oi_Roam', 'Tim_Roam', 'CTBC_Roam', 'Next_Roam']
    df_nok_lai_r30k_mss_full = pd.DataFrame(columns=nok_col_names)
    df_nok_lai_r30k_mss_full.loc[0] = [nok_lai_r30k_mss_name, nok_lai_r30k_mss_date, nok_lai_r30k_mss_time, nok_lai_r30k_no, 
                                        nok_lai_r30k_name, nok_lai_r30k_zc0, nok_lai_r30k_zc1, nok_lai_r30k_zc2, nok_lai_r30k_zc3,
                                        nok_lai_r30k_zc4, nok_lai_r30k_zc5]

    # Run the main program (txt => pd.DataFrame)
    while (nok_lai_r30k_idx < len(nok_logfile)-1):
        nok_lai_r30k_idx, nok_lai_r30k_pos, nok_mss_pars = get_mss_pars(nok_logfile, nok_lai_r30k_idx, 'ZEKO:LAC')
        while (nok_lai_r30k_idx < len(nok_logfile)-1) and (not nok_lai_r30k_pos == 999):
            nok_lai_r30k_idx, nok_lai_r30k_pos, nok_lai_r30k_pars = get_zeko_lac_pars(nok_logfile, nok_lai_r30k_idx)
            if nok_lai_r30k_pos == 999:                                 # if 'COMMAND EXECUTED'
                nok_lai_r30k_idx = nok_lai_r30k_idx + 1                 # Increase index to read next line
            else:
                new_lai = nok_mss_pars + nok_lai_r30k_pars
                df_nok_lai_r30k_mss_full.loc[nok_lai_r30k_count] = new_lai
                nok_lai_r30k_count = nok_lai_r30k_count + 1

    # DataFrame => Drop some columns to get just the most important ones.
    df_nok_lai_r30k_mss_full['MCC'] =  '724'
    df_nok_lai_r30k_mss_full['MNC'] =  '05'
    df_nok_lai_r30k_mss_full['LAC'] =  df_nok_lai_r30k_mss_full['LAC'].astype(int)
    df_nok_lai_r30k_mss_full['LAC'] =  df_nok_lai_r30k_mss_full['LAC'].astype(str)
    df_nok_lai_r30k_mss_full['MSS'] = df_nok_lai_r30k_mss_full['MSS'].str.replace(r'0', '')
    df_nok_lai_r30k_mss_full.loc[df_nok_lai_r30k_mss_full.LAC_NAME.str.contains('RS'), 'MNC'] = '28'    # Looks up for RS and replace MNC by 28
    df_nok_lai_r30k_mss_full.loc[df_nok_lai_r30k_mss_full.LAC_NAME.str.contains('FAKE'), 'MNC'] = '11'  # Looks up for FAKE and replace MNC by 11
    df_nok_lai_r30k_mss_full['LAI'] = df_nok_lai_r30k_mss_full['MCC'] + '-' + \
                                        df_nok_lai_r30k_mss_full['MNC'] + '-' + \
                                        df_nok_lai_r30k_mss_full['LAC']
    df_nok_lai_r30k_mss_full['MSS-LAI'] = df_nok_lai_r30k_mss_full['MSS'] + '-' + \
                                            df_nok_lai_r30k_mss_full['LAI']
    df_nok_lai_r30k_mss_summ = df_nok_lai_r30k_mss_full
    nok_drop_col = ['LAC_NAME']
    df_nok_lai_r30k_mss_summ = df_nok_lai_r30k_mss_summ.drop(columns=nok_drop_col)
    nok_col_summ = ['MSS','Date','Time', 'LAC', 'Claro_Roam', 'Vivo_Roam', 'Oi_Roam', 'Tim_Roam', 'CTBC_Roam', 'Next_Roam','LAI','MSS-LAI']
    df_nok_lai_r30k_mss_summ = df_nok_lai_r30k_mss_summ[nok_col_summ]

    return df_nok_lai_r30k_mss_full, df_nok_lai_r30k_mss_summ

###############################################################################################################################################
def get_r30k_lai_eri(log_file_path):
    '''
    Function:   
        + Process a log_file with all R30k LAIs of ERICSSON's MSSs
    Arguments:      
        + log_file_path => path to the log_file
    Output:     
        + df_full       => DataFrame with full R30k LAIs of ERICSSON's MSSs
        + df_summ       => DataFrame with summarized R30k LAIs of ERICSSON's MSSs
    '''
    
    # Variable control
    assert isinstance(log_file_path, str),'Path to look for the file must be string'
    assert len(log_file_path) > 0, 'File is empty'

    ###################################################### Code

    # Init ERICSSON Variables
    eri_lai_r30k_mss_name = '0'
    eri_lai_r30k_mss_date = '0'
    eri_lai_r30k_mss_time = '0'
    eri_lai_r30k_no = '0'
    eri_lai_r30k_name = '0'
    eri_lai_r30k_zc0 = '0'
    eri_lai_r30k_zc1 = '0'
    eri_lai_r30k_zc2 = '0'
    eri_lai_r30k_zc3 = '0'
    eri_lai_r30k_zc4 = '0'
    eri_lai_r30k_zc5 = '0'

    eri_mss_pars = [eri_lai_r30k_mss_name, eri_lai_r30k_mss_date, eri_lai_r30k_mss_time]
    eri_lai_r30k_pars = [eri_lai_r30k_no, eri_lai_r30k_name, eri_lai_r30k_zc0, eri_lai_r30k_zc1, eri_lai_r30k_zc2 , eri_lai_r30k_zc3,
                            eri_lai_r30k_zc4, eri_lai_r30k_zc5]

    eri_lai_r30k_idx = 0
    eri_lai_r30k_pos = 0
    eri_lai_r30k_count = 0

    # Open & Load ERICSSON logfile
    eri_logfile = open_file(log_file_path)

    # Create & Init & Set the ERICSSON pd.DataFrame
    eri_col_names = ['MSS','Date','Time', 'LAC_NO', 'LAC_NAME', 'Claro_Roam', 'Vivo_Roam', 'Oi_Roam', 'Tim_Roam', 'CTBC_Roam', 'Next_Roam']
    df_eri_lai_r30k_mss_full = pd.DataFrame(columns=eri_col_names)
    df_eri_lai_r30k_mss_full.loc[0] = [eri_lai_r30k_mss_name, eri_lai_r30k_mss_date, eri_lai_r30k_mss_time, eri_lai_r30k_no, eri_lai_r30k_name,
                                        eri_lai_r30k_zc0, eri_lai_r30k_zc1, eri_lai_r30k_zc2 , eri_lai_r30k_zc3,
                                        eri_lai_r30k_zc4, eri_lai_r30k_zc5]

    # Run the main program (txt => pd.DataFrame)
    while (eri_lai_r30k_idx < len(eri_logfile)-1):
        eri_lai_r30k_idx, eri_lai_r30k_pos, eri_mss_pars = get_mss_pars(eri_logfile, eri_lai_r30k_idx,'eaw')
        if (eri_lai_r30k_pos >= 0) and (not eri_lai_r30k_pos == 999) and (not eri_lai_r30k_pos == 998):
            eri_lai_r30k_idx, eri_lai_r30k_pos, eri_lai_r30k_pars = get_mgnrp_lac_pars(eri_logfile, eri_lai_r30k_idx)
            while(eri_lai_r30k_pos >= 0) and (not eri_lai_r30k_pos == 999) and (not eri_lai_r30k_pos == 998):
                RI_index, eri_lai_r30k_pos, eri_lai_r30k_pars = get_mgnrp_lac_pars(eri_logfile, eri_lai_r30k_idx)
                if(eri_lai_r30k_pos >= 0) and (not eri_lai_r30k_pos == 999) and (not eri_lai_r30k_pos == 998):
                    new_lai = eri_mss_pars + eri_lai_r30k_pars
                    df_eri_lai_r30k_mss_full.loc[eri_lai_r30k_count] = new_lai
                    eri_lai_r30k_count += 1
                eri_lai_r30k_idx += 1
        eri_lai_r30k_idx += 1

    # DataFrame => Drop some columns to get just the most important ones.
    df_eri_lai_r30k_mss_full[['MCC','MNC','LAC']] =  df_eri_lai_r30k_mss_full['LAC_NAME'].str.split('-', 2, expand=True)
    df_eri_lai_r30k_mss_full['LAI'] =  df_eri_lai_r30k_mss_full['LAC_NAME']
    df_eri_lai_r30k_mss_full['MSS-LAI'] =  df_eri_lai_r30k_mss_full['MSS'] + '-' + \
                                            df_eri_lai_r30k_mss_full['LAI']
    df_eri_lai_r30k_mss_summ = df_eri_lai_r30k_mss_full
    eri_drop_col = ['MCC','MNC','LAC_NAME']
    df_eri_lai_r30k_mss_summ = df_eri_lai_r30k_mss_summ.drop(columns=eri_drop_col)
    eri_col_summ = ['MSS', 'Date', 'Time', 'LAC', 'Claro_Roam', 'Vivo_Roam', 'Oi_Roam', 'Tim_Roam', 'CTBC_Roam', 'Next_Roam','LAI', 'MSS-LAI']
    df_eri_lai_r30k_mss_summ = df_eri_lai_r30k_mss_summ[eri_col_summ]

    return df_eri_lai_r30k_mss_full, df_eri_lai_r30k_mss_summ


###############################################################################################################################################
#################################     Command Generation Functions     ########################################################################
###############################################################################################################################################

###############################################################################################################################################
def change_lai_2g_eri(my_df, my_cmd='change'):
    '''
    Function:   
        + Generates the commands to change/fallback the change of LAI of 2G cells in ERICSSON's MSSs
    Arguments:      
        + my_df         => DataFrame with the information needed for change/fallback
        + my_cmd        => string coommand to return the change commands or the corrspondent fallback
    Output:     
        + None          => None - just analyze and print the commands
    '''

    # Variable control
    assert isinstance(my_df, pd.DataFrame),'Received argument must be a pd.DataFrame'
    assert isinstance(my_cmd, str),'Received argument must be a pd.DataFrame'
    assert len(my_cmd) > 0, 'Command (change or fallback) can not be empty'


    ###################################################### Code
    if (my_cmd == 'change'):
        list_of_muni = my_df['Municipio'].unique()

        for i in range(len(list_of_muni)):
            idx=0
            count=0
            mun0 = list_of_muni[i]
            for j in range(len(my_df)):
                mun1 = my_df['Municipio'][j]
                if (mun0 == mun1):
                    idx = j
                    count += 1

            lai_from_to = my_df['DE-PARA'][idx-count+1]
            print('! ' + mun0 + ' | Change ' + lai_from_to)
            print('!--------------------------------------------------------------------------------------')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'BA': cell_name = my_df['CELL_NAME'][t].replace(r'BA', '9', 1)
                print('MGCEP:CELL=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'BA': cell_name = my_df['CELL_NAME'][t].replace(r'BA', '9', 1)
                print('MGRCP:CELL=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'BA': cell_name = my_df['CELL_NAME'][t].replace(r'BA', '9', 1)
                print('MGCEE:CELL=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'BA': cell_name = my_df['CELL_NAME'][t].replace(r'BA', '9', 1)
                bsc_name = my_df['NE'][t]
                new_cgi = my_df['New CGI'][t]
                print('MGCEI:CELL=' + cell_name + ',BSC=' + bsc_name + ',CGI=' + new_cgi + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'BA': cell_name = my_df['CELL_NAME'][t].replace(r'BA', '9', 1)
                new_lai = my_df['New LAC'][t]
                cell_ea = new_lai[-2:]
                print('MGCEC:CELL=' + cell_name + ',EA=' + cell_ea + ';')
            
            print('\n! Generate emerceny center commands with AXE Tool\n')

    if (my_cmd == 'fallback'):
        list_of_muni = my_df['Municipio'].unique()

        for i in range(len(list_of_muni)):
            idx=0
            count=0
            mun0 = list_of_muni[i]
            for j in range(len(my_df)):
                mun1 = my_df['Municipio'][j]
                if (mun0 == mun1):
                    idx = j
                    count += 1

            lai_from_to = my_df['DE-PARA'][idx-count+1]
            print('! ' + mun0 + ' | Fallback ' + lai_from_to)
            print('!--------------------------------------------------------------------------------------')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'BA': cell_name = my_df['CELL_NAME'][t].replace(r'BA', '9', 1)
                print('MGCEP:CELL=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'BA': cell_name = my_df['CELL_NAME'][t].replace(r'BA', '9', 1)
                print('MGRCP:CELL=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'BA': cell_name = my_df['CELL_NAME'][t].replace(r'BA', '9', 1)
                print('MGCEE:CELL=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'BA': cell_name = my_df['CELL_NAME'][t].replace(r'BA', '9', 1)
                bsc_name = my_df['NE'][t]
                old_cgi = my_df['CGI'][t]
                print('MGCEI:CELL=' + cell_name + ',BSC=' + bsc_name + ',CGI=' + old_cgi + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'BA': cell_name = my_df['CELL_NAME'][t].replace(r'BA', '9', 1)
                new_lai = my_df['New LAC'][t]
                cell_ea = new_lai[-2:]
                print('MGCEC:CELL=' + cell_name + ',EA=' + cell_ea + ';')
            
            print('\n! Generate emerceny center commands with AXE Tool\n')
    
    return True

###############################################################################################################################################
def change_lai_3g_eri(my_df, my_cmd='change'):
    '''
    Function:   
        + Generates the commands to change/fallback the change of LAI of 3G cells in ERICSSON's MSSs
    Arguments:      
        + my_df         => DataFrame with the information needed for change/fallback
        + my_cmd        => string coommand to return the change commands or the corrspondent fallback
    Output:     
        + None          => None - just analyze and print the commands
    '''

    # Variable control
    assert isinstance(my_df, pd.DataFrame),'Received argument must be a pd.DataFrame'
    assert isinstance(my_cmd, str),'Received argument must be a pd.DataFrame'
    assert len(my_cmd) > 0, 'Command (change or fallback) can not be empty'


    ###################################################### Code
    if (my_cmd == 'change'):
        list_of_muni = my_df['Municipio'].unique()

        for i in range(len(list_of_muni)):
            idx=0
            count=0
            mun0 = list_of_muni[i]
            for j in range(len(my_df)):
                mun1 = my_df['Municipio'][j]
                if (mun0 == mun1):
                    idx = j
                    count += 1

            lai_from_to = my_df['DE-PARA'][idx-count+1]
            print('! ' + mun0 + ' | Change ' + lai_from_to)
            print('!--------------------------------------------------------------------------------------')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'FT': cell_name = cell_name
                if cell_name[0:3] == 'UBA': cell_name = my_df['CELL_NAME'][t].replace(r'UBA', 'I', 1)
                print('MGAAP:AREA=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'FT': cell_name = cell_name
                if cell_name[0:3] == 'UBA': cell_name = my_df['CELL_NAME'][t].replace(r'UBA', 'I', 1)
                print('MGRCP:AREA=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'FT': cell_name = cell_name
                if cell_name[0:3] == 'UBA': cell_name = my_df['CELL_NAME'][t].replace(r'UBA', 'I', 1)
                print('MGAAE:AREA=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'FT': cell_name = cell_name
                if cell_name[0:3] == 'UBA': cell_name = my_df['CELL_NAME'][t].replace(r'UBA', 'I', 1)
                bsc_name = my_df['NE'][t]
                new_cgi = my_df['New CGI'][t]
                print('MGAAI:AREA=' + cell_name + ',SAI=' + new_cgi + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'FT': cell_name = cell_name
                if cell_name[0:3] == 'UBA': cell_name = my_df['CELL_NAME'][t].replace(r'UBA', 'I', 1)
                new_lai = my_df['New LAC'][t]
                cell_ea = new_lai[-2:]
                print('MGAAC:AREA=' + cell_name + ',EA=' + cell_ea + ';')
            
            print('\n! Generate emerceny center commands with AXE Tool\n')

    if (my_cmd == 'fallback'):
        list_of_muni = my_df['Municipio'].unique()

        for i in range(len(list_of_muni)):
            idx=0
            count=0
            mun0 = list_of_muni[i]
            for j in range(len(my_df)):
                mun1 = my_df['Municipio'][j]
                if (mun0 == mun1):
                    idx = j
                    count += 1

            lai_from_to = my_df['DE-PARA'][idx-count+1]
            print('! ' + mun0 + ' | Fallback ' + lai_from_to)
            print('!--------------------------------------------------------------------------------------')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'FT': cell_name = cell_name
                if cell_name[0:3] == 'UBA': cell_name = my_df['CELL_NAME'][t].replace(r'UBA', 'I', 1)
                print('MGAAP:AREA=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'FT': cell_name = cell_name
                if cell_name[0:3] == 'UBA': cell_name = my_df['CELL_NAME'][t].replace(r'UBA', 'I', 1)
                print('MGRCP:AREA=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'FT': cell_name = cell_name
                if cell_name[0:3] == 'UBA': cell_name = my_df['CELL_NAME'][t].replace(r'UBA', 'I', 1)
                print('MGAAE:AREA=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'FT': cell_name = cell_name
                if cell_name[0:3] == 'UBA': cell_name = my_df['CELL_NAME'][t].replace(r'UBA', 'I', 1)
                bsc_name = my_df['NE'][t]
                old_cgi = my_df['CGI'][t]
                print('MGAAI:AREA=' + cell_name + ',SAI=' + old_cgi + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                if cell_name[0:2] == 'FT': cell_name = cell_name
                if cell_name[0:3] == 'UBA': cell_name = my_df['CELL_NAME'][t].replace(r'UBA', 'I', 1)
                new_lai = my_df['New LAC'][t]
                cell_ea = new_lai[-2:]
                print('MGAAC:AREA=' + cell_name + ',EA=' + cell_ea + ';')
            
            print('\n! Generate emerceny center commands with AXE Tool\n')
    
    return True

###############################################################################################################################################
def change_lai_2g_nok(my_df, my_cmd='change'):
    '''
    Function:   
        + Generates the commands to change/fallback the change of LAI of 2G cells in NOKIAS's MSSs
    Arguments:      
        + my_df         => DataFrame with the information needed for change/fallback
        + my_cmd        => string coommand to return the change commands or the corrspondent fallback
    Output:     
        + None          => None - just analyze and print the commands
    '''

    # Variable control
    assert isinstance(my_df, pd.DataFrame),'Received argument must be a pd.DataFrame'
    assert isinstance(my_cmd, str),'Received argument must be a pd.DataFrame'
    assert len(my_cmd) > 0, 'Command (change or fallback) can not be empty'


    ###################################################### Code
    if (my_cmd == 'change'):
        list_of_muni = my_df['Municipio'].unique()

        for i in range(len(list_of_muni)):
            idx=0
            count=0
            mun0 = list_of_muni[i]
            for j in range(len(my_df)):
                mun1 = my_df['Municipio'][j]
                if (mun0 == mun1):
                    idx = j
                    count += 1

            lai_from_to = my_df['DE-PARA'][idx-count+1]
            print('\n! ' + mun0 + ' | Change ' + lai_from_to)
            print('!--------------------------------------------------------------------------------------')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPO:NAME=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPS:NAME=' + cell_name + ':L;')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                bsc_name = my_df['NE'][t]
                mcc_lai = my_df['MCC'][t]
                mnc_lai = my_df['MNC'][t]
                new_lai = my_df['New LAC'][t]
                #print('ZEPB:NAME=' + cell_name + ':BSCNAME=' + bsc_name + ':LANAME=LAC' + new_lai + ';')
                print('ZEPB:NAME=' + cell_name + ':BSCNAME=' + bsc_name + ':MCC=' + mcc_lai + ',MNC=' + mnc_lai + ',LAC=' + new_lai + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPS:NAME=' + cell_name + ':U;')

    if (my_cmd == 'fallback'):
        list_of_muni = my_df['Municipio'].unique()

        for i in range(len(list_of_muni)):
            idx=0
            count=0
            mun0 = list_of_muni[i]
            for j in range(len(my_df)):
                mun1 = my_df['Municipio'][j]
                if (mun0 == mun1):
                    idx = j
                    count += 1

            lai_from_to = my_df['DE-PARA'][idx-count+1]
            print('\n! ' + mun0 + ' | Fallback ' + lai_from_to)
            print('!--------------------------------------------------------------------------------------')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPO:NAME=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPS:NAME=' + cell_name + ':L;')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                bsc_name = my_df['NE'][t]
                mcc_lai = my_df['MCC'][t]
                mnc_lai = my_df['MNC'][t]
                old_lai = my_df['LAC'][t]
                #print('ZEPB:NAME=' + cell_name + ':BSCNAME=' + bsc_name + ':LANAME=LAC' + old_lai + ';')
                print('ZEPB:NAME=' + cell_name + ':BSCNAME=' + bsc_name + ':MCC=' + mcc_lai + ',MNC=' + mnc_lai + ',LAC=' + old_lai + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPS:NAME=' + cell_name + ':U;')

    return True

###############################################################################################################################################
def change_lai_3g_nok(my_df, my_cmd='change'):
    '''
    Function:   
        + Generates the commands to change/fallback the change of LAI of 3G cells in NOKIAS's MSSs
    Arguments:      
        + my_df         => DataFrame with the information needed for change/fallback
        + my_cmd        => string coommand to return the change commands or the corrspondent fallback
    Output:     
        + None          => None - just analyze and print the commands
    '''

    # Variable control
    assert isinstance(my_df, pd.DataFrame),'Received argument must be a pd.DataFrame'
    assert isinstance(my_cmd, str),'Received argument must be a pd.DataFrame'
    assert len(my_cmd) > 0, 'Command (change or fallback) can not be empty'


    ###################################################### Code
    if (my_cmd == 'change'):
        list_of_muni = my_df['Municipio'].unique()

        for i in range(len(list_of_muni)):
            idx=0
            count=0
            mun0 = list_of_muni[i]
            for j in range(len(my_df)):
                mun1 = my_df['Municipio'][j]
                if (mun0 == mun1):
                    idx = j
                    count += 1

            lai_from_to = my_df['DE-PARA'][idx-count+1]
            print('\n! ' + mun0 + ' | Change ' + lai_from_to)
            print('!--------------------------------------------------------------------------------------')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPO:TYPE=SA,NAME=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPS:TYPE=SA,NAME=' + cell_name + ':L;')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                rnc_name = my_df['NE'][t]
                mcc_lai = my_df['MCC'][t]
                mnc_lai = my_df['MNC'][t]
                new_lai = my_df['New LAC'][t]
                print('ZEPF:TYPE=SA,SANAME=' + cell_name + ':MGWNBR=MSS:MCC=' + mcc_lai + ',MNC=' + mnc_lai + ',LAC=' + new_lai +';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPS:TYPE=SA,NAME=' + cell_name + ':U;')

    if (my_cmd == 'fallback'):
        list_of_muni = my_df['Municipio'].unique()

        for i in range(len(list_of_muni)):
            idx=0
            count=0
            mun0 = list_of_muni[i]
            for j in range(len(my_df)):
                mun1 = my_df['Municipio'][j]
                if (mun0 == mun1):
                    idx = j
                    count += 1

            lai_from_to = my_df['DE-PARA'][idx-count+1]
            print('\n! ' + mun0 + ' | Fallbac ' + lai_from_to)
            print('!--------------------------------------------------------------------------------------')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPO:TYPE=SA,NAME=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPS:TYPE=SA,NAME=' + cell_name + ':L;')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                rnc_name = my_df['NE'][t]
                mcc_lai = my_df['MCC'][t]
                mnc_lai = my_df['MNC'][t]
                old_lai = my_df['LAC'][t]
                print('ZEPF:TYPE=SA,SANAME=' + cell_name + ':MGWNBR=MSS:MCC=' + mcc_lai + ',MNC=' + mnc_lai + ',LAC=' + old_lai +';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPS:TYPE=SA,NAME=' + cell_name + ':U;')


    return True

###############################################################################################################################################
def create_lai_nok(my_df, my_cmd='create'):
    '''
    Function:   
        + Generates the commands to create LAIs in NOKIAS's MSSs
    Arguments:      
        + my_df         => DataFrame with the information needed for creating the LAIs
    Output:     
        + None          => None - just analyze and print the commands
    '''

    # Variable control
    assert isinstance(my_df, pd.DataFrame),'Received argument must be a pd.DataFrame'
    assert isinstance(my_cmd, str),'Received argument must be a pd.DataFrame'
    assert len(my_df) > 0,'Received pd.DataFrame can not be empty'
    assert len(my_cmd) > 0,'Command (change or fallback) can not be empty'

    ###################################################### Code
    if (my_cmd == 'create'):
        mss0=my_df['MSS'][0]
        print('\n! ' + mss0)
        print('!--------------------------------------------------------------------------------------\n')
        print('! Check')
        print('!--------------------------------------------------------------------------------------')
        print('ZELO;')
        print('ZEKO:ZC=0&1&2&3&4&5;')
        print('ZMVF::LAC=ALL,::::;')
        print('ZWVJ;')
        print('ZCWI:NAME=ICMMSS;')

        for lai in range(len(my_df)):
            mss1=my_df['MSS'][lai]
            if not (mss0==mss1):
                print('\n! ' + mss1)
                print('!--------------------------------------------------------------------------------------\n')
                print('! Check')
                print('!--------------------------------------------------------------------------------------')
                print('ZELO;')
                print('ZEKO:ZC=0&1&2&3&4&5;')
                print('ZMVF::LAC=ALL,::::;')
                print('ZWVJ;')
                print('ZCWI:NAME=ICMMSS;')
                mss0=mss1

            lai_mun = my_df['Municipio'][lai]
            lai_ibge = my_df['IBGE'][lai]
            lai_ne = my_df['NE'][lai]
            lai_mcc = my_df['MCC'][lai]
            lai_mnc = my_df['MNC'][lai]
            lai_lac = my_df['LAC'][lai]
            lai_rngp = my_df['RNGP'][lai]
            lai_honla = my_df['HONLA'][lai]
            lai_zc0 = my_df['Claro_Roam'][lai]
            lai_zc1 = my_df['Vivo_Roam'][lai]
            lai_zc2 = my_df['Oi_Roam'][lai]
            lai_zc3 = my_df['Tim_Roam'][lai]
            lai_zc4 = my_df['CTBC_Roam'][lai]
            lai_zc5 = my_df['Next_Roam'][lai]
            lai_lai = my_df['LAI'][lai]
            if(lai_mnc=='05'): lai_name = 'LAC' + lai_lac
            if(lai_mnc=='28'): lai_name = 'LAC' + lai_lac + 'RS'

            print('\n!' + lai_mun +' | NE=' + lai_ne + ' | LAI=' + lai_lai)
            print('!--------------------------------------------------------------------------------------')
            print('ZELC:NAME=' + lai_name + ',MCC=' + lai_mcc + ',MNC=' + lai_mnc +',LAC=' + lai_lac + ';')
            print('ZELE:NAME=' + lai_name + ':RNGP=' + lai_rngp + ',HONLA=' + lai_honla + ';')
            print('ZELP:NAME=' + lai_name + ':AT=001,INT=00600;')
            if (lai_zc0=='1'): print('ZEKA:ZC=0:LANAME=' + lai_name + ':Y;')    # Roaming for Claro
            if (lai_zc1=='1'): print('ZEKA:ZC=1:LANAME=' + lai_name + ':Y;')    # Roaming for Vivo
            if (lai_zc2=='1'): print('ZEKA:ZC=2:LANAME=' + lai_name + ':Y;')    # Roaming for Oi
            if (lai_zc3=='1'): print('ZEKA:ZC=3:LANAME=' + lai_name + ':Y;')    # Roaming for Tim
            if (lai_zc4=='1'): print('ZEKA:ZC=4:LANAME=' + lai_name + ':Y;')    # Roaming for CTBC
            if (lai_zc5=='1'): print('ZEKA:ZC=5:LANAME=' + lai_name + ':Y;')    # Roaming for Nextel (not used)
            if ('RNC' in lai_ne): 
                print('ZE2M:RNCNAME=' + lai_ne + ':LAMCC=' + lai_mcc + ',LAMNC=' + lai_mnc + ',LACLA=' + lai_lac + ';')

    if (my_cmd == 'fallback'):
        mss0=my_df['MSS'][0]
        print('\n! ' + mss0)
        print('!--------------------------------------------------------------------------------------\n')
        print('! Check')
        print('!--------------------------------------------------------------------------------------')
        print('ZELO;')
        print('ZEKO:ZC=0&1&2&3&4&5;')
        print('ZMVF::LAC=ALL,::::;')
        print('ZWVJ;')
        print('ZCWI:NAME=ICMMSS;')

        for lai in range(len(my_df)):
            mss1=my_df['MSS'][lai]
            if not (mss0==mss1):
                print('\n! ' + mss1)
                print('!--------------------------------------------------------------------------------------\n')
                print('! Check')
                print('!--------------------------------------------------------------------------------------')
                print('ZELO;')
                print('ZEKO:ZC=0&1&2&3&4&5;')
                print('ZMVF::LAC=ALL,::::;')
                print('ZWVJ;')
                print('ZCWI:NAME=ICMMSS;')
                mss0=mss1

            lai_mun = my_df['Municipio'][lai]
            lai_ibge = my_df['IBGE'][lai]
            lai_ne = my_df['NE'][lai]
            lai_mcc = my_df['MCC'][lai]
            lai_mnc = my_df['MNC'][lai]
            lai_lac = my_df['LAC'][lai]
            lai_rngp = my_df['RNGP'][lai]
            lai_honla = my_df['HONLA'][lai]
            lai_zc0 = my_df['Claro_Roam'][lai]
            lai_zc1 = my_df['Vivo_Roam'][lai]
            lai_zc2 = my_df['Oi_Roam'][lai]
            lai_zc3 = my_df['Tim_Roam'][lai]
            lai_zc4 = my_df['CTBC_Roam'][lai]
            lai_zc5 = my_df['Next_Roam'][lai]
            lai_lai = my_df['LAI'][lai]
            if(lai_mnc=='05'): lai_name = 'LAC' + lai_lac
            if(lai_mnc=='28'): lai_name = 'LAC' + lai_lac + 'RS'

            print('\n!' + lai_mun +' | NE=' + lai_ne + ' | LAI=' + lai_lai)
            print('!--------------------------------------------------------------------------------------')
            if ('RNC' in lai_ne): 
                print('ZE2M:RNCNAME=' + lai_ne + ':LAMCC=' + lai_mcc + ',LAMNC=' + lai_mnc + ',LACLR=' + lai_lac + ';')
            print('ZELD:NAME=' + lai_name + ',MCC=' + lai_mcc + ',MNC=' + lai_mnc +',LAC=' + lai_lac + ';')


    return True

###############################################################################################################################################
def create_lai_eri(my_df, my_cmd='create'):
    '''
    Function:   
        + Generates the commands to create LAIs in ERICSSON's MSSs
    Arguments:      
        + my_df         => DataFrame with the information needed for creating the LAIs
    Output:     
        + None          => None - just analyze and print the commands
    '''

    # Variable control
    assert isinstance(my_df, pd.DataFrame),'Received argument must be a pd.DataFrame'
    assert isinstance(my_cmd, str),'Received argument must be a pd.DataFrame'
    assert len(my_df) > 0,'Received pd.DataFrame can not be empty'
    assert len(my_cmd) > 0,'Command (change or fallback) can not be empty'

    ###################################################### Code
    if (my_cmd == 'create'):
        mss0=my_df['MSS'][0]
        print('\n! ' + mss0)
        print('!--------------------------------------------------------------------------------------\n')
        print('! Check')
        print('!--------------------------------------------------------------------------------------')
        print('MGLAP;')
        print('MGLXP:LATA=ALL;')
        print('MGNRP:LAI=ALL;')
        print('MGSVP:LAI=ALL;')

        for lai in range(len(my_df)):
            mss1=my_df['MSS'][lai]
            if not (mss0==mss1):
                print('\n! ' + mss1)
                print('!--------------------------------------------------------------------------------------\n')
                print('! Check')
                print('!--------------------------------------------------------------------------------------')
                print('MGLAP;')
                print('MGLXP:LATA=ALL;')
                print('MGNRP:LAI=ALL;')
                print('MGSVP:LAI=ALL;')
                mss0=mss1

            lai_mun = my_df['Municipio'][lai]
            lai_ibge = my_df['IBGE'][lai]
            lai_ne = my_df['NE'][lai]
            lai_mcc = my_df['MCC'][lai]
            lai_mnc = my_df['MNC'][lai]
            lai_lac = my_df['LAC'][lai]
            lai_zc0 = my_df['Claro_Roam'][lai]
            lai_zc1 = my_df['Vivo_Roam'][lai]
            lai_zc2 = my_df['Oi_Roam'][lai]
            lai_zc3 = my_df['Tim_Roam'][lai]
            lai_zc4 = my_df['CTBC_Roam'][lai]
            lai_zc5 = my_df['Next_Roam'][lai]
            lai_lai = my_df['LAI'][lai]
            lai_cn = lai_lac[-2:]
            lai_nrrg = '7&8&9&12&13'
            if(lai_mnc=='05'): lai_name = 'LAC' + lai_lac
            if(lai_mnc=='28'): lai_name = 'LAC' + lai_lac + 'RS'
            if(lai_zc1=='0'): lai_nrrg = '6&' + lai_nrrg    # Roaming for Vivo
            if(lai_zc2=='0'): lai_nrrg = '2&' + lai_nrrg    # Roaming for Oi
            if(lai_zc3=='0'): lai_nrrg = '1&' + lai_nrrg    # Roaming for Tim
            print('\n!' + lai_mun +' | NE=' + lai_ne + ' | LAI=' + lai_lai)
            print('!--------------------------------------------------------------------------------------')
            print('MGLAI:LAI=' + lai_lai + ';')
            print('MGLXI:LATA=' + lai_cn + ',LAI=' + lai_lai + ';')
            print('MGNRI:LAI=' + lai_lai + ',NRRG=' + lai_nrrg + ';')
            if('RNC' in lai_ne): print('MGMAI:LAI=' + lai_lai + ',RNC=' + lai_ne + ';')
    
    if (my_cmd == 'fallback'):
        mss0=my_df['MSS'][0]
        print('\n! ' + mss0)
        print('!--------------------------------------------------------------------------------------\n')
        print('! Check')
        print('!--------------------------------------------------------------------------------------')
        print('MGLAP;')
        print('MGLXP:LATA=ALL;')
        print('MGNRP:LAI=ALL;')
        print('MGSVP:LAI=ALL;')

        for lai in range(len(my_df)):
            mss1=my_df['MSS'][lai]
            if not (mss0==mss1):
                print('\n! ' + mss1)
                print('!--------------------------------------------------------------------------------------\n')
                print('! Check')
                print('!--------------------------------------------------------------------------------------')
                print('MGLAP;')
                print('MGLXP:LATA=ALL;')
                print('MGNRP:LAI=ALL;')
                print('MGSVP:LAI=ALL;')
                mss0=mss1

            lai_mun = my_df['Municipio'][lai]
            lai_ibge = my_df['IBGE'][lai]
            lai_ne = my_df['NE'][lai]
            lai_mcc = my_df['MCC'][lai]
            lai_mnc = my_df['MNC'][lai]
            lai_lac = my_df['LAC'][lai]
            lai_lai = my_df['LAI'][lai]
            lai_cn = lai_lac[-2:]
            if(lai_mnc=='05'): lai_name = 'LAC' + lai_lac
            if(lai_mnc=='28'): lai_name = 'LAC' + lai_lac + 'RS'
            print('\n!' + lai_mun +' | NE=' + lai_ne + ' | LAI=' + lai_lai)
            print('!--------------------------------------------------------------------------------------')
            if('RNC' in lai_ne): print('MGMAE:LAI=' + lai_lai + ',RNC=' + lai_ne + ';')
            print('MGLXE:LATA=' + lai_cn + ',LAI=' + lai_lai + ';')
            print('MGLAE:LAI=' + lai_lai + ';')
    
    return True










###############################################################################################################################################
def rehome_cell_2g_nok(my_df, my_cmd='change'):
    '''
    Function:   
        + Generates the commands to change/fallback to rehome a cell from one NE to another in NOKIAS's MSSs
    Arguments:      
        + my_df         => DataFrame with the information needed for change/fallback
        + my_cmd        => string coommand to return the change commands or the corrspondent fallback
    Output:     
        + None          => None - just analyze and print the commands
    '''

    # Variable control
    assert isinstance(my_df, pd.DataFrame),'Received argument must be a pd.DataFrame'
    assert isinstance(my_cmd, str),'Received argument must be a pd.DataFrame'
    assert len(my_cmd) > 0, 'Command (change or fallback) can not be empty'


    ###################################################### Code
    if (my_cmd == 'change'):
        list_of_muni = my_df['Municipio'].unique()

        for i in range(len(list_of_muni)):
            idx=0
            count=0
            mun0 = list_of_muni[i]
            for j in range(len(my_df)):
                mun1 = my_df['Municipio'][j]
                if (mun0 == mun1):
                    idx = j
                    count += 1

            cell_from_to = my_df['DE-PARA'][idx-count+1]
            print('\n! ' + mun0 + ' | Change ' + cell_from_to)
            print('!--------------------------------------------------------------------------------------')

            for t in range(idx-count+1,idx+1):
                if my_df['MSS'][t] == my_df['para_MSS'][t]:
                    name_cell = my_df['para_CELL_NAME'][t]
                    print('ZEPO:NAME=' + name_cell + ';')
                else:
                    name_cell = my_df['para_CELL_NAME'][t]
                    mcc_cell = my_df['para_MCC'][t]
                    mnc_cell = my_df['para_MNC'][t]
                    lai_cell = my_df['para_LAC'][t]
                    ci_cell = my_df['para_CI/SA'][t]
                    no_cell = my_df['para_CELL_NO'][t]
                    print('ZEPC:NAME=' + name_cell + ',NO=' + no_cell + ':MCC=' + mcc_cell + ',MNC=' + mnc_cell + ',LAC=' + lai_cell + ',CI=' + ci_cell + ';')

            for t in range(idx-count+1,idx+1):
                if my_df['MSS'][t] == my_df['para_MSS'][t]:
                    name_cell = my_df['para_CELL_NAME'][t]
                    print('ZEPS:NAME=' + name_cell + ':L;')
                else:
                    name_cell = my_df['para_CELL_NAME'][t]
                    ne_cell = my_df['para_NE'][t]
                    print('ZEPB:NAME=' + name_cell + ':BSCNAME=' + ne_cell + ';')

            for t in range(idx-count+1,idx+1):
                if my_df['MSS'][t] == my_df['para_MSS'][t]:
                    name_cell = my_df['para_CELL_NAME'][t]
                    ne_cell = my_df['para_NE'][t]
                    mcc_cell = my_df['para_MCC'][t]
                    mnc_cell = my_df['para_MNC'][t]
                    lai_cell = my_df['para_LAC'][t]
                    print('ZEPB:NAME=' + name_cell + ':BSCNAME=' + ne_cell + ':MCC=' + mcc_cell + ',MNC=' + mnc_cell + ',LAC=' + lai_cell + ';')
                else:
                    name_cell = my_df['para_CELL_NAME'][t]
                    rz_cell = my_df['para_RZ'][t]
                    cn_cell = my_df['para_LAC'][t]
                    cn_cell = cn_cell[-2:]
                    print('ZEPR:NAME=' + name_cell + ':RZ=' + rz_cell + ',CDR=' + cn_cell + ';')

            for t in range(idx-count+1,idx+1):
                if my_df['MSS'][t] == my_df['para_MSS'][t]:
                    name_cell = my_df['para_CELL_NAME'][t]
                    print('ZEPS:NAME=' + name_cell + ':U;')
                else:
                    name_cell = my_df['para_CELL_NAME'][t]
                    print('ZEPS:NAME=' + name_cell + ':U;')



    if (my_cmd == 'fallback'):
        list_of_muni = my_df['Municipio'].unique()

        for i in range(len(list_of_muni)):
            idx=0
            count=0
            mun0 = list_of_muni[i]
            for j in range(len(my_df)):
                mun1 = my_df['Municipio'][j]
                if (mun0 == mun1):
                    idx = j
                    count += 1

            cell_from_to = my_df['DE-PARA'][idx-count+1]
            print('\n! ' + mun0 + ' | Fallback ' + cell_from_to)
            print('!--------------------------------------------------------------------------------------')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPO:NAME=' + cell_name + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPS:NAME=' + cell_name + ':L;')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                old_ne = my_df['NE'][t]
                mcc_lai = my_df['MCC'][t]
                mnc_lai = my_df['MNC'][t]
                old_lai = my_df['LAC'][t]
                #print('ZEPB:NAME=' + cell_name + ':BSCNAME=' + bsc_name + ':LANAME=LAC' + old_lai + ';')
                print('ZEPB:NAME=' + cell_name + ':BSCNAME=' + old_ne + ':MCC=' + mcc_lai + ',MNC=' + mnc_lai + ',LAC=' + old_lai + ';')

            for t in range(idx-count+1,idx+1):
                cell_name = my_df['CELL_NAME'][t]
                print('ZEPS:NAME=' + cell_name + ':U;')

    return True
