import sys
from reader import read_log
import temp.sorting as sorting
from filters import (
    get_entries_by_addr, get_entries_by_code, get_failed_reads, get_entries_by_extension)
from dictionaries import (entry_to_dict, log_to_dict, print_dict_entry_dates)

def main():
    # 2a
    logs = read_log()
    print_logs_formatted(logs)

    # 2b
    # sorted_logs = sorting.sort_log(logs, 11)
    # print_logs_formatted(sorted_logs)

    #2c problem jest tqki ze nazwa domenowa hosta to ip??
    # matches_ip = get_entries_by_addr(logs, "192.168.204.45")
    # matches_ip = get_entries_by_addr(logs, "www.wikipedia.org")
    # print_logs_formatted(matches_ip)

    # 2d
    # matches_status = get_entries_by_code(logs, 401)
    # print_logs_formatted(matches_status)

    # 2e
    # failed_status = get_failed_reads(logs)
    # print_logs_formatted(failed_status[0])
    # print_logs_formatted(failed_status[1])
    
    # or combine = True then it connects both 4xx and 5xx list (4xx elements first)
    # failed_status2 = get_failed_reads(logs, True)
    # print_logs_formatted(failed_status2)

    # 2f
    # extenstions = get_entries_by_extension(logs, "csv")
    # print_logs_formatted(extenstions)

    # 3a
    # entry_as_dict = entry_to_dict(logs[1])
    # print(entry_as_dict)

    # 3b
    # log_as_dict = log_to_dict(logs)
    # print(log_as_dict)

    # 3c  
    # log_as_dict = log_to_dict(logs)
    # print_dict_entry_dates(log_as_dict)






    



def print_logs_formatted(entries: list):
    # i = 0
    for entry in entries:
        # if i < 150: 
            try:
                (
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
                ) = entry
                
                print(f"""
    Timestamp      : {timestamp}
    UID            : {uid}
    Origin IP/Port : {orig_h} : {orig_p}
    Target IP/Port : {resp_h} : {resp_p}
    Method         : {method}
    Host           : {host}
    URI            : {uri}
    Status code    : {status_code}
    ------------------------
    """)
                # i += 1
            except ValueError:
                print('error with printing format')


main()