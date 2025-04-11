import sys
from datetime import datetime, UTC

def read_log() -> list:
    entries = []

    for line in sys.stdin:
        line = line.strip()
        # skipping empty lines
        if not line:
            continue  

        # fields are separted by tabs in line
        fields = line.split('\t')

        # if missing elements complete with empty value fe. while writting log server connection was lost
        if len(fields) < 15:
            fields += [''] * (15 - len(fields)) 

        # assigning default value in case format of entry is invalid fe. port status code is string or -
        timestamp_float = safe_float(fields, 0)
        timestamp = datetime.fromtimestamp(timestamp_float, tz=UTC)
        uid = safe_str(fields, 1)
        orig_h = safe_str(fields, 2)
        orig_p = safe_int(fields, 3)
        resp_h = safe_str(fields, 4)
        resp_p = safe_int(fields, 5)
        method = safe_str(fields, 7)
        host = safe_str(fields, 8)
        uri = safe_str(fields, 9)
        status_code = safe_int(fields, 14)

        entry = (
            timestamp,       
            uid,             
            orig_h,         
            orig_p,       
            resp_h,         
            resp_p,       
            method,         
            host,        
            uri,            
            status_code
        )
        entries.append(entry) 

    return entries

def safe_float(fields, index):
    try:
        return float(fields[index])
    except Exception:
        return 0.0


def safe_int(fields, index):
    try:
        return int(float(fields[index])) 
    except Exception:
        return 0


def safe_str(fields, index):
    try:
        return fields[index]
    except Exception:
        return "-"


if __name__ == "__main__":
    print(read_log())