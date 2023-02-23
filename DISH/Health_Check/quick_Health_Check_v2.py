###############################################################################################################################################
########################################     IMPORTS     ######################################################################################
###############################################################################################################################################
import requests
import csv
from datetime import datetime

###############################################################################################################################################
########################################     DEFINE FUNCITIONS     ############################################################################
###############################################################################################################################################
def open_file(my_file_path, flag='txt'):
    '''
    Function:   
        + Opens a txt file and converts it into a list with all fields read as string (except NaN)
    Input:
        + my_file_path  => Path of the file
    Output:
        + my_file_as_list => list (each text line is an element of the list)
    '''

    # Variable control
    assert isinstance(my_file_path, str), 'The path to the file must be as string'
    assert len(my_file_path) > 0, 'Path is empty'
    assert isinstance(flag, str), 'Flag must be a string (csv or txt in this version of the function)'
    assert (flag == 'txt') or (flag == 'csv'), 'Flag must be txt in this version of the function'

    # Code
    if flag == 'txt':
        try:
            with open(my_file_path,'r') as my_file: # Opening this way it is not necessary to close the file to release resources
                my_file_as_list = my_file.readlines()
                print("txt file loaded")
            return my_file_as_list
        except:
            print('Something went wrong @open_file => flag == txt')
    elif flag == 'csv':
        try:
            with open(my_file_path,'r') as my_file: # Opening this way it is not necessary to close the file to release resources
                my_file_as_obj = csv.reader(my_file, delimiter=',')
                my_file_as_list = list(my_file_as_obj)
                print("csv file loaded")
            return my_file_as_list
        except:
            print('Something went wrong @open_file => flag == csv')
    else:
        print('Flag must be csv or txt in this version of the function')
        return -1

def write_res_to_txt(my_list, my_filename='py_script_output.txt'):
    '''
    Function:   
        + Writes a list to a txt file (line by line)
    Input:
        + my_list       => List of strings
        + my_filename   => Name for the output file
    Output:
        + N/A           => N/A - Writes a txt file
    '''

    # Variable control
    assert isinstance(my_list, list), 'The input must be a list of string'
    assert len(my_list) > 0, 'The input list is empty'
    if not 'txt' in my_filename: my_filename = my_filename + '.txt'

    # Code
    with open(my_filename, 'w') as my_file:
        my_file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        my_file.write('\ncLBA/cLB/cProbe\t\t\t\tResponse (with redirection if any - 3xx)\n\n')
        for i in range(len(my_list)):
            my_file.write(my_list[i] + '\n')

###############################################################################################################################################
###############################################     CODE     ##################################################################################
###############################################################################################################################################

# Path to file
path_to_vm_url = 'vm_url_csv.csv'

# Open file
# Note: format of csv file: vm, vm_url. Example: pro-fe-e1-clb-1131-0,http://localhost:8080/1131/monserver/AjaxClient/index.jsp
vm_url_lst = open_file(path_to_vm_url, flag='csv')
vm_url_res = []

# Test connections
for vm,url in vm_url_lst:
    try:
        with requests.Session() as my_session:
            res = my_session.get(url, timeout=3)
            print(res.status_code, res.history)
            vm_url_res.append(vm + "\t\t" + str(res.status_code) + str(res.history))

    except requests.exceptions.RequestException as e:
        print("connection_error")
        vm_url_res.append(vm + "\t\t" + "connection_error")

# Set name and path for the exported file
today_date = datetime.today().strftime('%Y-%m-%d')
today_date = today_date.replace('-', '')
file_name = today_date + ' - quick_Health_Check_output' + '.txt'

# Export file
write_res_to_txt(vm_url_res, file_name)
