from reader import read_log

def entry_to_dict(entry: tuple) -> dict:
    # no need to catch index error then
    if len(entry) != 10:
        raise ValueError("Log entry should contain 10 elements")
    
    # creating entry dictionary with key string and value from given tuple
    entry_dict = {
        "ts" : entry[0],
        "uid" : entry[1],
        "id_orig_h" : entry[2],
        "id_orig_p" : entry[3],
        "id_resp_h" : entry[4],
        "id_resp_p" : entry[5],
        "method" : entry[6],
        "host" : entry[7],
        "uri" : entry[8],
        "status_code" : entry[9]
    }

    return entry_dict


if __name__ == "__main__":
    logs = read_log()
    print(entry_to_dict(logs[1]))
    