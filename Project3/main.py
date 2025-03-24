import sys
from datetime import datetime, UTC
import sorting
import entries #zmien nazwe na filter

def main():
    logs = read_log()
    #print_logs_formatted(logs)

    # matches_ip = entries.get_entries_by_addr(logs, "192.168.202.79")
    # print_logs_formatted(matches_ip)

    #dla status code czyli 9 nie dziala
    # sorted_logs = sorting.sort_log(logs, 8)
    # print_logs_formatted(sorted_logs)

    # problem jest tqki ze nazwa domenowa hosta to ip??
    # matches_host = entries.get_entries_by_addr(logs, "192.168.229.251")
    # print_logs_formatted(matches_host)

    # matches_status = entries.get_entries_by_code(logs, 401)
    # print_logs_formatted(matches_status)

    # nie dziala
    # failed_status = entries.get_failed_reads(logs)
    # print_logs_formatted(failed_status)
    
    #lub combine=True
    # failed_status2 = entries.get_failed_reads(logs, True)
    # print_logs_formatted(failed_status2)

    # extenstions = entries.get_entries_by_extension(logs, "csv")
    # print_logs_formatted(extenstions)

    
    


def read_log() -> list:
    """function that reads logs fron standard input and returns array of logs divided into tuples"""
    entries = []

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue  # pomiń puste linie

        fields = line.split('\t')
        #if len(fields) < 27:
            #continue  # pomiń linie niekompletne

        try:
            # Parsowanie odpowiednich pól
            timestamp_float = float(fields[0])
            timestamp = datetime.fromtimestamp(timestamp_float, tz=UTC)
            uid = fields[1]
            orig_h = fields[2]
            orig_p = int(fields[3])
            resp_h = fields[4]
            resp_p = int(fields[5])
            method = fields[7]
            host = fields[8]
            uri = fields[9]
            status_code = int(float(fields[14]))

            # Krotka z istotnymi danymi
            entry = (
                timestamp,       # datetime.datetime
                uid,             # str
                orig_h,         # str
                orig_p,       # int
                resp_h,         # str
                resp_p,       # int
                method,  
                host,        # str
                uri,             # str
                status_code
            )
            # if internal_id == 0:
            #     print(entry)
            entries.append(entry) 
        except Exception as e:
            entries.append(f"Error with reading log")

    return entries


def print_logs_formatted(entries: list):
    i = -1
    for entry in entries:
        i += 1
        if i < 10:
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
    ======   Log Entry   ======
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
                
            except ValueError:
                print(" Invalid log entry format, skipping\n")


main()