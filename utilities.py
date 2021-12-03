
import math
import os


## Terniary rounding will round to the integral precision specified, but it will
## take the decimal place of the precision (should be only one significant 
## digit) and if it's less than that distance from an "extreme" it will round
## one more digit.
def terniary_round(number, precision):
    
    if math.floor(float(number)) == float(number):
        return number
    
    base_precision = math.floor(precision)
    tern_precision = math.floor((precision - base_precision) * 10)
    base_number = round(number, base_precision)
    numeric_base = pow(10, base_precision)
    
    number = round(number, base_precision);
    mod_number = round(((number * numeric_base / 10) % 1) * 10)
    number = math.floor(number * (numeric_base / 10))
    
    if mod_number <= tern_precision:
        mod_number = 0
    elif mod_number >= 10 - tern_precision:
        mod_number = 1
    else:
        mod_number /= 10
    
    number += mod_number
    number /= (numeric_base / 10)
    number = round(number, math.floor(precision))
    
    return number


## Encode an unsigned int to base64. Signed ints will be converted. Used to 
## generate unique IDs that are compressed.
def uintbase62encode(number):
    number = abs(number)
    b62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base36 = ""

    if number == 0:
        return "0"

    while number != 0:
        number, i = divmod(number, len(b62))
        base36 = b62[i] + base36

    return base36



## Gets a default
def priority_dict_value(key, preferred_dict, default_dict, default_value):
    if key in preferred_dict:
        return preferred_dict[key]
    elif key in default_dict:
        return default_dict[key]
    else:
        return default_value


##
def csv_to_list (value):
    values = value.split(",")
    output = []

    for v in values:
        v = v.strip(" \n\r\t")
        
        if len(v) > 0:
            output.append(v)
            
    return output


##
def key_to_dict (key, dictionary):
    output = {}
    for raw in dictionary:
        raw = raw.strip()
        if raw.startswith(key + '["') and raw.endswith('"]'):
            arrlist = raw[len(key) + 2:-2].replace("::", "=").split('"]["')
            list_to_dict_path(arrlist, output, dictionary[raw])
    return output


##
def list_to_dict_path (list_items, output, terminal_value):
    current_item = list_items.pop(0)
    if current_item in output:
        if len(list_items) == 0:
            output[current_item] = terminal_value
        else:
            output[current_item] = list_to_dict_path(list_items, output[current_item], terminal_value)
    else:
        if len(list_items) == 0:
            output[current_item] = terminal_value
        else:
            output[current_item] = {}
            output[current_item] = list_to_dict_path(list_items, output[current_item], terminal_value)
    return output


##
def compare_dicts (dict_a, dict_b):
    output = dict()
    for key in dict_a:
        if (key in dict_b and dict_a[key] == dict_b[key]):
            output[key] = dict_a[key]
    return output



##
FILE_CACHE = {}

def get_file_contents (filename):
    global FILE_CACHE
    
    if not os.path.isfile(filename):
        raise Exception('Missing file: ' + filename)
    
    if filename not in FILE_CACHE:
        f = open(filename, "r")
        FILE_CACHE[filename] = f.read()

    return FILE_CACHE[filename]



##
BUILD_LOG  = []

def log_icon_state (status, data):
    global BUILD_LOG
    log = {
        "status":  status,
        "icon":    data["icon"] if "icon" in data else "",
        "size":    data["size"] if "size" in data else "",
        "context": data["context"] if "context" in data else "",
        "message": data["message"] if "message" in data else "",
    }
    
    BUILD_LOG.append(log)

    print("[" + status + "]", columnize(log["icon"], 32), "  ", columnize(log["size"], 4), "  ", columnize(log["context"], 12), "  ", log["message"])
    

def columnize (string, length):
    if len(string) > length:
        string = string[:length - 3] + "..."
    return string.ljust(length)