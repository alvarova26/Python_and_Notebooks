
from functools import reduce
import json
import sys
import os

# dirname = "/hpadir/healthalarms/"
# filename = "hpaHealthAlarms1.log"
# log_name = os.path.join(dirname,filename) DIRNAME = "/hpadir/healthalarms/"

FILEMASK = "hpaHealthAlarms"

def get_last_file(dir, filemask):
     '''It will return the last file based on the mask file'''
    files = [ {os.path.getmtime(dir+file): file} for file in os.listdir(dir) if file.__contains__(filemask)]
    file = json.dumps(max(files)).split('"')[3]
    return file

def test_get_last_file():
    print(get_last_file(DIRNAME, FILEMASK))

def is_json(string_value):
    try:
        json.loads(string_value)
    except ValueError as e:
        return False
    return True

def main():
    if len(sys.argv) >= 3 :
        field_name = sys.argv[1]
        field_sub_name = sys.argv[2]
        filename = get_last_file(DIRNAME, FILEMASK)
        log_name = os.path.join(DIRNAME,filename)
        kpi_history = [json.loads(line) for line in open(log_name,'r') if is_json(line)]
        last_line=kpi_history[-1]
        try:
            kpi = last_line[field_name][field_sub_name]
            print(kpi)
        except KeyError as error:
            print("Informe um KPI ou KPI com SubKPI valido!")
	elif len(sys.argv) == 2:
        field_name = sys.argv[1]
        filename = get_last_file(DIRNAME, FILEMASK)
        log_name = os.path.join(DIRNAME,filename)
        kpi_history = [json.loads(line) for line in open(log_name,'r') if is_json(line)]
        last_line=kpi_history[-1]
        try:
            kpi = last_line[field_name]
            print(kpi)
        except KeyError as error:
            print("Informe um KPI ou KPI com SubKPI valido!")
	else:
        print("Informe um argumento!")

if __name__ == "__main__":
    main()














from functools import reduce
import json
import sys
import os

# dirname = "/hpadir/healthalarms/"
# filename = "hpaHealthAlarms1.log"
# log_name = os.path.join(dirname,filename) DIRNAME = "/hpadir/healthalarms/"
FILEMASK = "hpaHealthAlarms"
def get_last_file(dir, filemask):
    '''It will return the last file based on the mask file'''
    files = [ {os.path.getmtime(dir+file): file} for file in os.listdir(dir) if file.__contains__(filemask)]
    file = json.dumps(max(files)).split('"')[3]
    return file

def test_get_last_file():
    print(get_last_file(DIRNAME, FILEMASK))
    
def is_json(string_value):
    try:
        json.loads(string_value)
    except ValueError as e:
    return False

return True def main():
if len(sys.argv) >= 3 :
field_sub_name = sys.argv[2]
filename = get_last_file(DIRNAME, FILEMASK)
field_name = sys.argv[1]
 log_name = os.path.join(DIRNAME,filename)         kpi_history = [json.loads(line) for line in open(log_name,'r') if is_json(line)]
 last_line=kpi_history[-1]
 try:
 kpi = last_line[field_name][field_sub_name]
 print(kpi)
 except KeyError as error:
 print("Informe um KPI ou KPI com SubKPI valido!")     elif len(sys.argv) == 2:
 field_name = sys.argv[1]
 filename = get_last_file(DIRNAME, FILEMASK)
 log_name = os.path.join(DIRNAME,filename)
 kpi_history = [json.loads(line) for line in open(log_name,'r') if is_json(line)]
 last_line=kpi_history[-1]
 try:
 kpi = last_line[field_name]
 print(kpi)
 except KeyError as error:
 print("Informe um KPI ou KPI com SubKPI valido!")     else:
 print("Informe um argumento!") if __name__ == "__main__":
 main()

