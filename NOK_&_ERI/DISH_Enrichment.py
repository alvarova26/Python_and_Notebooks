###### IMPORTs
import pandas as pd
import numpy as np
from datetime import datetime

###### FUNCTIONs
def open_file(my_file_path):
    '''
    Function:   
        + Opens a csv file and converts it into a pandas dataframe with all fields read as string (except NaN)
    Input:
        + my_file_path  => Path of the file
    Output:
        + my_file_as_df => Pandas dataframe
    '''

    # Variable control
    assert isinstance(my_file_path, str), 'The path to the file must be as string'
    assert len(my_file_path) > 0, 'Path is empty'

    # Code
    with open(my_file_path) as my_file: # Opening this way it is not necessary to close the file to release resources
        my_file_as_df = pd.read_csv(my_file, dtype=str)
    
    return my_file_as_df

def export_to_xlsx(path, df):
    with pd.ExcelWriter(path) as writer:
        df.to_excel(writer, sheet_name='py_export', index=False)

def padding(NR_Cell_ID_dec, NR_Cell_ID_dec_len):
    if NR_Cell_ID_dec_len == 10: return '313340' + NR_Cell_ID_dec
    elif NR_Cell_ID_dec_len == 9: return '313340' + '0' + NR_Cell_ID_dec
    elif NR_Cell_ID_dec_len == 8: return '313340' + '00' + NR_Cell_ID_dec
    elif NR_Cell_ID_dec_len == 7: return '313340' + '000' + NR_Cell_ID_dec
    elif NR_Cell_ID_dec_len == 6: return '313340' + '0000' + NR_Cell_ID_dec
    elif NR_Cell_ID_dec_len == 5: return '313340' + '00000' + NR_Cell_ID_dec
    elif NR_Cell_ID_dec_len == 4: return '313340' + '000000' + NR_Cell_ID_dec
    elif NR_Cell_ID_dec_len == 3: return '313340' + '0000000' + NR_Cell_ID_dec
    elif NR_Cell_ID_dec_len == 2: return '313340' + '00000000' + NR_Cell_ID_dec
    elif NR_Cell_ID_dec_len == 1: return '313340' + '000000000' + NR_Cell_ID_dec
    else: return 'error'

###### LOAD FILE
path_to_n1_acdm = 'C:/Users/alvaro.mendoza/Desktop/N1 ACDM Export/20220825113059.csv'
df_n1_acdm = open_file(path_to_n1_acdm)


###### CLEAN UP & DATA MANIPULATION
n1_acdm_col = ['NR Cell ID', 'Cell Site Common Name', 'Cell Name'] # 20220825113059
df_n1_acdm = df_n1_acdm[n1_acdm_col]
df_n1_acdm = df_n1_acdm.sort_values(by=['Cell Site Common Name', 'Cell Name'], ignore_index=True)
df_n1_acdm = df_n1_acdm.dropna(subset=['NR Cell ID'])
df_n1_acdm = df_n1_acdm.drop_duplicates(subset=['NR Cell ID'], keep='first')
df_n1_acdm['NR Cell ID'] = df_n1_acdm['NR Cell ID'].astype(str)

df_n1_acdm['NR Cell ID len'] = df_n1_acdm['NR Cell ID'].apply(len)
df_n1_acdm['NR Cell ID'] = df_n1_acdm['NR Cell ID'].str.lower()
df_n1_acdm['NR Cell ID'] = '0x' + df_n1_acdm['NR Cell ID']
df_n1_acdm['NR Cell ID dec'] = df_n1_acdm['NR Cell ID'].apply(int, base=16)
df_n1_acdm['NR Cell ID dec'] = df_n1_acdm['NR Cell ID dec'].astype(str)
df_n1_acdm['NR Cell ID dec len'] = df_n1_acdm['NR Cell ID dec'].apply(len)
df_n1_acdm['NR CGI dec'] = df_n1_acdm.apply(lambda x: padding(x['NR Cell ID dec'], x['NR Cell ID dec len']), axis = 1)

###### EXPORT
today_date = datetime.today().strftime('%Y-%m-%d')
today_date = today_date.replace('-', '')
file_name_acdm = today_date + ' - 20220825113059_v2_py' + '.xlsx'
export_path_acdm = 'C:/Users/alvaro.mendoza/Desktop/N1 ACDM Export/'
file_exp_path_acdm = export_path_acdm + file_name_acdm
export_to_xlsx(file_exp_path_acdm, df_n1_acdm)
