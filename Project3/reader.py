import sys
from datetime import datetime, UTC
import entries

def read_log() -> list:
    """function that reads logs fron standard input and returns array of logs divided into tuples"""
    entries = []
    internal_id = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue  # pomiń puste linie

        fields = line.split('\t')
        if len(fields) < 27:
            continue  # pomiń linie niekompletne

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

            # Krotka z istotnymi danymi
            entry = (
                internal_id,
                timestamp,       # datetime.datetime
                uid,             # str
                orig_h,         # str
                orig_p,       # int
                resp_h,         # str
                resp_p,       # int
                method,  
                host,        # str
                uri,             # str
            )
            # if internal_id == 0:
            #     print(entry)
            entries.append(entry) 
            internal_id += 1
        except Exception as e:
            entries.append(f"Error with reading log: '{internal_id}")

    return entries


if __name__ == "__main__":
    read_log()