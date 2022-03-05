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


###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
########################################     General/ Common Functions     ####################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

###############################################################################################################################################
def open_file(path):
    '''
    Function:   Opens the file from the path passed as argument of the function
    Input:      Path of the file
    Output:     List of the strings where each item is a line of the txt file
    '''
    with open(path) as my_file:                             # Opening this way it is not necessary to close the file to release resources
        my_file_as_list_of_strings = my_file.readlines()    # Reads the entire file. Each index is a string whit the corresponding line 
    
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
def get_mss_pars(file, start_idx, str):
    '''
    Function:   Looks for the MSS parameters in the file passed as argument, starting at the specified index
    Input:      File as list of strings, index for starting the search and the string to search (allows reuse the function)
    Output:     MSS parameters as strings and the current index
    '''

    #### INITIALIZE LOCAL VARIABLES
    MS_Name = '0'
    MS_Date = '0'
    MS_Time = '0'
    Data = [MS_Name, MS_Date, MS_Time]                                  # Initialize Data: list of strings containing data
    cmd = str                       

    if (cmd == 'ZEKO:LAC') or (cmd == 'ZELO;') or \
        (cmd == 'ZEPO;') or (cmd == 'ZE2I::RT=ALL;') or \
        (cmd == 'ZEPO:TYPE=SA;'):                                       # IF NOKIA                    
        idx = start_idx                                                 # Sets the startin index to a local variable
        idx, pos = string_search_nok(file, idx, cmd)                    # Searchs for 'cmd' - string to allow reuse the code
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):     # if found and not EOF and not 'COMMAND EXECUTED'=>
            idx, pos = string_search_nok(file, idx, 'MSSBA')            # Searchs for 'MSSBA'
            if (pos >= 0) and (idx < len(file)-1) and (not pos == 999): # if found and not EOF and not 'COMMAND EXECUTED'=>
                my_line = file[idx]                                     # Reads the line and extracts data
                MS_Name = my_line[10:21:].strip()
                MS_Date = my_line[35:47:].strip()
                MS_Time = my_line[48:58:].strip()
                Data = [MS_Name, MS_Date, MS_Time]                      # Update Data: list of strings containing data

    if (cmd == 'eaw'):                                                  # IF ERICSSON
        idx = start_idx                                                 # Sets the startin index to a local variable
        idx, pos = string_search_eri(file, idx, cmd)                    # Searchs for 'cmd' - string to allow reuse the code
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999) and (not pos == 998):     # if found and not EOF and not 'COMMAND EXECUTED'=>
            idx, pos = string_search_eri(file, idx, 'MSSBA')            # Searchs for 'MSSBA'
            if (pos >= 0) and (idx < len(file)-1) and (not pos == 999) and (not pos == 998): # if found and not EOF and not 'COMMAND EXECUTED'=>
                my_line = file[idx]                                     # Reads the line and extracts data
                MS_Name = my_line[21:30:].strip()
                MS_Date = '0000-00-00'                                  # Mantain '0' as ther is no timestamp in Ericsson
                MS_Time = '00:00:00'                                    # Mantain '0' as ther is no timestamp in Ericsson
                Data = [MS_Name, MS_Date, MS_Time]                      # Update Data: list of strings containing data

    return idx, pos, Data


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
def get_zepo_2g_cell_pars(file, start_idx):
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
                CELL_CI, CELL_STAT, CELL_RZ, CELL_CDR]                                      # Initialize Data: list of strings

    idx = start_idx                                                                         # Sets the starting index to a local variable
    idx, pos = string_search_nok(file, idx, 'BASE TRANSCEIVER STATION')                     # Searchs for 'BASE TRANSCEIVER STATION'
    if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                             # if found and not EOF and not 'COMMAND EXECUTED'=>
        idx, pos = string_search_nok(file, idx, 'BTS   NAME')                               # Searchs for 'BTS   NAME'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            CELL_NAME = my_line[12:30:].strip()
            CELL_NO = my_line[50:60:].strip()

        idx, pos = string_search_nok(file, idx, 'BSC   NAME')                               # Searchs for 'BTS   NAME'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            CELL_BSC_NAME = my_line[12:30:].strip()
            CELL_BSC_NO = my_line[50:60:].strip()

        idx, pos = string_search_nok(file, idx, 'LA    NAME')                               # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            CELL_LAC_NAME = my_line[12:30:].strip()
            CELL_LAC_NO = my_line[50:60:].strip()

        idx, pos = string_search_nok(file, idx, 'MOBILE COUNTRY')                           # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            CELL_MCC = my_line[50:60:].strip()

        idx, pos = string_search_nok(file, idx, 'MOBILE NETWORK')                           # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            CELL_MNC = my_line[50:60:].strip()

        idx, pos = string_search_nok(file, idx, 'CELL IDENTITY')                            # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            CELL_CI = my_line[50:60:].strip()

        idx, pos = string_search_nok(file, idx, 'BTS ADM')                                  # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            CELL_STAT = my_line[50:60:].strip()

        idx, pos = string_search_nok(file, idx, 'ROUTING ZONE')                             # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            CELL_RZ = my_line[50:60:].strip()

        idx, pos = string_search_nok(file, idx, 'CELL DEPENDENT')                           # Searchs for 'xxxxxxxxx'
        if (pos >= 0) and (idx < len(file)-1) and (not pos == 999):                         # if found and not EOF and not 'COMMAND EXECUTED'=>
            my_line = file[idx]                                                             # Reads the line and extracts data
            CELL_CDR = my_line[50:60:].strip()

    Data = [CELL_NAME, CELL_NO, CELL_BSC_NAME, CELL_BSC_NO,
                CELL_LAC_NAME, CELL_MCC, CELL_MNC, CELL_LAC_NO,
                CELL_CI, CELL_STAT, CELL_RZ, CELL_CDR]                                      # Assign to return

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
        CELL_CGI = my_line[9:26:].strip()
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
