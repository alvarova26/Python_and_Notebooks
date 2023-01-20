###############################################################################################################################################
########################################     IMPORTS     ######################################################################################
###############################################################################################################################################
import pandas as pd
import numpy as np
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
    assert isinstance(flag, str), 'Flag must be a string (csv or xls in this version of the function)'
    assert (flag == 'csv') or (flag == 'xls'), 'Flag must be csv or xls in this version of the function'

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
    else:
        print('Flag must be csv or xls in this version of the function')
        return -1

def export_to_xlsx(path, df):
    with pd.ExcelWriter(path) as writer:
        df.to_excel(writer, sheet_name='py_export', index=False)

def export_to_csv(path, df):
    df.to_csv(path, index=False)

def export_meta_data(path):
    '''
    Function:   
        + Export metadata
    Input:
        + my_file_path                  => Path of the file
    Output:
        + export    => List of the strings where each item is a line of the txt file
    '''
    
    # Metadata
    source_lines = [
        'Columns Dictionary                  =>  20220825113059.csv\n',
        '\n',
        'ADD/CHANGE/DELETE                   = Not used\n',
        'Technology                          = Not used\n',
        'MCC                                 = Not used\n',
        'MNC                                 = Not used\n',
        'NR Tracking Area Code               = Not used\n',
        'NR Cell ID                          = Used in the ENRICHMENT TABLE to generate the CGI\n',
        'gNodeB Identity Bit Length          = Not used\n',
        'NR PCI                              = Not used\n',
        'Cell Site Common Name               = Used in the ENRICHMENT TABLE as PKEY for left join of 20220825113059.csv with 20% AOI SITE INFO.xlsx\n',
        'Carrier Cell ID Cascade ID          = Not used\n',
        'Market (AOI)                        = Not used\n',
        'Street Address                      = Not used\n',
        'City                                = Not used\n',
        'State                               = Not used\n',
        'County                              = Not used\n',
        'Latitude (degrees)                  = Used in the ENRICHMENT TABLE (as is)\n',
        'Longitude (degrees)                 = Used in the ENRICHMENT TABLE (as is)\n',
        'Cell Portion ID                     = Not used\n',
        'Frequency Band Class                = Not used\n',
        'Frequency                           = Not used\n',
        'Antenna Location                    = Not used\n',
        'Antenna Position Altitude (meters)  = Not used\n',
        'Antenna Height (meters)             = Not used\n',
        'Sector Azimuth (degrees N=0)        = Not used\n',
        'Beam Width (degrees)                = Not used\n',
        'Vertical Beam Width                 = Not used\n',
        'Sector Radius                       = Not used\n',
        'Unit of Radius                      = Not used\n',
        'Antenna Tilt                        = Not used\n',
        'DAS                                 = Not used\n',
        'Repeater                            = Not used\n',
        'Antenna Manufacturer                = Not used\n',
        'Antenna Model #                     = Not used\n',
        'Small Cell                          = Not used\n',
        'Cell Name                           = Used in the ENRICHMENT TABLE (as is)\n',
        '\n',
        '\n']

    aoi_lines = [
        'Columns Dictionary              =>  20% AOI SITE INFO.xlsx\n',
        '\n',
        'Site Name                       = Used in the ENRICHMENT TABLE as FKEY\n',
        'CIQ  gNodeB ID                  = Not used\n',
        'Region                          = Not used\n',
        'AWS LZ                          = Used in the ENRICHMENT TABLE (as TOWN)\n',
        'AOI								= Not used\n',
        'AOI Name                        = Used in the ENRICHMENT TABLE (as CLUSTERNAME)\n',
        'Market                          = Used in the ENRICHMENT TABLE (as market)\n',
        'CU CP ID                        = Not used\n',
        'CU UP ID                        = Not used\n',
        'DU ID                           = Not used\n',
        'NDC Region                      = Used in the ENRICHMENT TABLE (as PROVINCE)\n',
        'NDC MCMS EKS Cluster Name       = Not used\n',
        'BEDC Region                     = Used in the ENRICHMENT TABLE (as division)\n',
        'AWS                             = Not used\n',
        '\n',
        '\n']

    enrich_lines = [
        'Columns Dictionary  => ENRICHMENT FINAL TABLE\n',
        '\n',
        'ID                  = Index (needed by DB, generated by us)\n',
        'TIME_STAMP          = Any valid date (could be today, generated by us)\n',
        'CURRENT_STATUS      = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'CGI                 = 313340 + NR Cell ID transformed to decimal\n',
        '                    = 313340 is the MCC + MNC of DISH\n',
        '                    = NR Cell ID from 20220825113059.csv (provided by DISH, column is in hex format)\n',
        'CELL_NAME           = From 20220825113059.csv (provided by DISH)\n',
        'SITE_NAME           = From 20220825113059.csv (provided by DISH)\n',
        'CELL_TYPE           = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'RAT_TYPE            = NR - CHECK WITH MARTIN WHERE IT IS COMING FROM!!!!!!!!!!!\n',
        'RNC_BSC_NAME        = Filled with '' - cotlumn not in 20220825113059.csv - where it is coming from)\n',
        'SGSN_NAME           = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'CELL_REGION         = VALID VALUES - CHECK WITH MARTIN WHERE IT IS COMING FROM!!!!!!!!!!!\n',
        'LONGITUDE           = From 20220825113059.csv (provided by DISH)\n',
        'LATITUDE            = From 20220825113059.csv (provided by DISH)\n',
        'ANALYZ              = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'CELL_THROUGHPUT     = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'TOWN                = From 20% AOI SITE INFO.xlsx (AWS LZ)\n',
        'TOWN2               = Same as before but with _BEDC at the end (e.g. New York  => New York_BEDC)\n',
        'VENDOR_NAME         = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'PROVINCE            = From 20% AOI SITE INFO.xlsx (NDC Region)\n',
        'PROVINCE2           = Same as before but with _NDC at the end (e.g. east-1  => east-1_NDC)\n',
        'AZIMUTH_ANGLE       = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'AZIMUTH_LENGTH      = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'AZIMUTH_DIRECTION   = Filled with '' - column no in 20220825113059.csv - where it is coming from)\n',
        'TAC                 = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'HEIGHT              = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'ANTENNA_NAME        = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'PCI                 = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'RSI                 = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'ENODEBID            = VALID VALUES - CHECK WITH MARTIN WHERE IT IS COMING FROM!!!!!!!!!!!\n',
        'SECTOR_ID           = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'DL_CARRIER_NUMBER   = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'BAND                = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'CARRIER_BW          = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'EDT                 = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'MDT                 = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'CLUSTERNAME         = From 20% AOI SITE INFO.xlsx (AOI Name)\n',
        'CLUSTERNAME2        = Same as before but with _AOI at the end (e.g. Albuquerque => Albuquerque_AOI)\n',
        'GC_CODE             = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'ZONE                = Filled with '' - column not in 20220825113059.csv - where it is coming from)\n',
        'market              = From 20% AOI SITE INFO.xlsx (Market)\n',
        'market2             = Same as before but with _Market at the end (e.g. Phoenix => Phoenix_Market)\n',
        'division            = From 20% AOI SITE INFO.xlsx (BEDC Region)\n',
        'division2           = Same as before but with _RDC at the end (e.g. west-2 => west-2_2_RDC)\n',
        '\n',
        'Obs.: When this ENRICHMENT FINAL TABLE exported to csv, the values of the columns ending in 2 will be\n',
        'assinged to the original name, then dropped (e.g. values of market2 => market then drop market2 so\n',
        'only will remain market but with the values of market2).\n',
        '\n',
        '\n']


    # Code
    with open(path, "w") as my_file:                        # Opening this way it is not necessary to close the file to release resources
        my_file.writelines(enrich_lines)
        my_file.writelines(source_lines)
        my_file.writelines(aoi_lines)
        my_file.close()

###############################################################################################################################################
########################################     LOAD SOURCE FILES     ############################################################################
###############################################################################################################################################
path_to_n1_acdm = 'C:/Users/alvaro.mendoza/Desktop/DISH_Enrichment/N1 ACDM Export/20220825113059.csv'
path_to_aoi_20 = 'C:/Users/alvaro.mendoza/Desktop/DISH_Enrichment/20% AOI SITE INFO.xlsx'

###############################################################################################################################################
########################################     DATA MANIPULATION     ############################################################################
###############################################################################################################################################
#### ACDM File
df_n1_acdm = open_file(path_to_n1_acdm, flag='csv')
n1_acdm_col = ['Cell Site Common Name', 'Cell Name', 'NR Cell ID', 'Longitude (degrees)', 'Latitude (degrees)'] # 20220825113059 for ENRICHMENT FINAL TABLE
df_n1_acdm = df_n1_acdm[n1_acdm_col]
df_n1_acdm = df_n1_acdm.sort_values(by=['Cell Site Common Name', 'Cell Name'], ignore_index=True)
df_n1_acdm = df_n1_acdm.dropna(subset=['NR Cell ID'])
df_n1_acdm = df_n1_acdm.drop_duplicates(subset=['NR Cell ID'], keep='first')
df_n1_acdm = df_n1_acdm.reset_index(drop=True)
df_n1_acdm['NR Cell ID'] = df_n1_acdm['NR Cell ID'].astype(str)
df_n1_acdm['NR Cell ID'] = df_n1_acdm['NR Cell ID'].str.lower()
df_n1_acdm['NR Cell ID'] = '0x' + df_n1_acdm['NR Cell ID']
df_n1_acdm['NR Cell ID dec'] = df_n1_acdm['NR Cell ID'].apply(int, base=16)
df_n1_acdm['NR Cell ID dec'] = df_n1_acdm['NR Cell ID dec'].astype(str)
df_n1_acdm['NR CGI dec'] = '313340' + df_n1_acdm['NR Cell ID dec']
df_n1_acdm['NR CGI dec'] = df_n1_acdm['NR CGI dec'].astype(str)

#### AOI File
df_aoi_20 = open_file(path_to_aoi_20, flag='xls')
aoi_20_col = ['Site Name', 'AWS LZ', 'NDC Region', 'AOI Name', 'Market', 'BEDC Region'] # 20% AOI SITE INFO.xlsx
df_aoi_20 = df_aoi_20[aoi_20_col]
df_aoi_20 = df_aoi_20.dropna(subset=['Site Name'])
df_aoi_20 = df_aoi_20.drop_duplicates(subset=['Site Name'], keep='first')
df_aoi_20 = df_aoi_20.reset_index(drop=True)

###############################################################################################################################################
########################################     JOIN/MERGE (create enrichment table     ##########################################################
###############################################################################################################################################
#### Merge Files
df_enrich = pd.merge(df_n1_acdm, df_aoi_20, how='left', left_on='Cell Site Common Name', right_on='Site Name')

#### Adjust column names & Clean Up
df_enrich = df_enrich.drop(columns=['Site Name','NR Cell ID','NR Cell ID dec'])
df_enrich = df_enrich.rename(columns={'Cell Name':'CELL_NAME'})
df_enrich = df_enrich.rename(columns={'Cell Site Common Name':'SITE_NAME'})
df_enrich = df_enrich.rename(columns={'Longitude (degrees)':'LONGITUDE'})
df_enrich = df_enrich.rename(columns={'Latitude (degrees)':'LATITUDE'})
df_enrich = df_enrich.rename(columns={'NR CGI dec':'CGI'})
df_enrich = df_enrich.rename(columns={'AWS LZ':'TOWN'})
df_enrich = df_enrich.rename(columns={'NDC Region':'PROVINCE'})
df_enrich = df_enrich.rename(columns={'AOI Name':'CLUSTERNAME'})
df_enrich = df_enrich.rename(columns={'Market':'market'})
df_enrich = df_enrich.rename(columns={'BEDC Region':'division'})

#### Prepare enrichment to be exported
df_enrich['ID'] = df_enrich.index + 1
df_enrich['TIME_STAMP'] = datetime.today().strftime('%Y-%m-%d') +' 12:00:00.000'
df_enrich['CURRENT_STATUS'] = "'"
df_enrich['CGI'] = "'" + df_enrich['CGI']
df_enrich['CELL_NAME'] = "'" + df_enrich['CELL_NAME']
df_enrich['SITE_NAME'] = "'" + df_enrich['SITE_NAME']
df_enrich['CELL_TYPE'] = "'"
df_enrich['RAT_TYPE'] = "'NR" # CHECK WITH MARTIN - THERE IS NO INFO WHERE IT SHOULD COME FROM
df_enrich['RNC_BSC_NAME'] = "'"
df_enrich['SGSN_NAME'] = "'"
df_enrich['CELL_REGION'] = "'" # CHECK WITH MARTIN - THERE IS NO INFO WHERE IT SHOULD COME FROM
df_enrich['LONGITUDE'] = "'" + df_enrich['LONGITUDE']
df_enrich['LATITUDE'] = "'" + df_enrich['LATITUDE']
df_enrich['ANALYZ'] = "'"
df_enrich['CELL_THROUGHPUT'] = "'"
df_enrich['TOWN'] = "'" + df_enrich['TOWN'] + "_BEDC"
df_enrich['VENDOR_NAME'] = "'"
df_enrich['PROVINCE'] = "'" + df_enrich['PROVINCE'] + "_NDC"
df_enrich['AZIMUTH_ANGLE'] = "'"
df_enrich['AZIMUTH_LENGTH'] = "'"
df_enrich['AZIMUTH_DIRECTION'] = "'"
df_enrich['TAC'] = "'"
df_enrich['HEIGHT'] = "'"
df_enrich['ANTENNA_NAME'] = "'"
df_enrich['PCI'] = "'"
df_enrich['RSI'] = "'"
df_enrich['ENODEBID'] = "'" # CHECK WITH MARTIN - THERE IS NO INFO WHERE IT SHOULD COME FROM
df_enrich['SECTOR_ID'] = "'"
df_enrich['DL_CARRIER_NUMBER'] = "'"
df_enrich['BAND'] = "'"
df_enrich['CARRIER_BW'] = "'"
df_enrich['EDT'] = "'"
df_enrich['MDT'] = "'"
df_enrich['CLUSTERNAME'] = "'" + df_enrich['CLUSTERNAME'] + "_AOI"
df_enrich['ZONE'] = "'"
df_enrich['GC_CODE'] = "'"
df_enrich['market'] = "'" + df_enrich['market'] + "_Market"
df_enrich['division'] = "'" + df_enrich['division'] + "_RDC"
df_enrich = df_enrich.fillna("'")
final_enrich_col = ['ID','TIME_STAMP','CURRENT_STATUS','CGI','CELL_NAME','SITE_NAME','CELL_TYPE',
                    'RAT_TYPE','RNC_BSC_NAME','SGSN_NAME','CELL_REGION','LONGITUDE','LATITUDE','ANALYZ',
                    'CELL_THROUGHPUT','TOWN','VENDOR_NAME','PROVINCE','AZIMUTH_ANGLE',
                    'AZIMUTH_LENGTH','AZIMUTH_DIRECTION','TAC','HEIGHT','ANTENNA_NAME','PCI','RSI',
                    'ENODEBID','SECTOR_ID','DL_CARRIER_NUMBER','BAND','CARRIER_BW','EDT','MDT','CLUSTERNAME',
                    'GC_CODE','ZONE','market','division']
df_enrich = df_enrich[final_enrich_col]

###############################################################################################################################################
########################################     EXPORT FILES/TABLES     ##########################################################################
###############################################################################################################################################

#### Set filenames & path
today_date = datetime.today().strftime('%Y-%m-%d')
today_date = today_date.replace('-', '')

file_name_acdm_xlsx = today_date + ' - 20220825113059_v2' + '.xlsx'
export_path_acdm = 'C:/Users/alvaro.mendoza/Desktop/DISH_Enrichment/'
file_exp_path_acdm_xlsx = export_path_acdm + file_name_acdm_xlsx

file_name_aoi_xlsx = today_date + ' - 20%_AOI_SITE_INFO_v2' + '.xlsx'
export_path_aoi = 'C:/Users/alvaro.mendoza/Desktop/DISH_Enrichment/'
file_exp_path_aoi_xlsx = export_path_aoi + file_name_aoi_xlsx

file_name_enrich_xlsx = today_date + ' - Enrichment_table_v2' + '.xlsx'
file_exp_path_enrich_table = 'C:/Users/alvaro.mendoza/Desktop/DISH_Enrichment/'
file_exp_path_enrich_xlsx = file_exp_path_enrich_table + file_name_enrich_xlsx

file_name_enrich_csv = today_date + ' - Enrichment_table_v2' + '.csv'
file_exp_path_enrich_table = 'C:/Users/alvaro.mendoza/Desktop/DISH_Enrichment/'
file_exp_path_enrich_csv = file_exp_path_enrich_table + file_name_enrich_csv

file_name_meta_txt = today_date + ' - Enrichment_meta_data_v2' + '.txt'
export_path_meta = 'C:/Users/alvaro.mendoza/Desktop/DISH_Enrichment/'
file_exp_path_meta_txt = export_path_meta + file_name_meta_txt

#### Export files
#export_to_xlsx(file_exp_path_acdm_xlsx, df_n1_acdm)
#export_to_xlsx(file_exp_path_aoi_xlsx, df_aoi_20)
#export_to_xlsx(file_exp_path_enrich_xlsx, df_enrich)
export_to_csv(file_exp_path_enrich_csv, df_enrich)
export_meta_data(file_exp_path_meta_txt)