from reader import read_log
from collections import defaultdict
from .convert_log import log_to_dict


def print_dict_entry_dates(log_dict: dict):
    # creating dictionary for key "host" : value "empty timestamps list" to then find min and max
    host_data = defaultdict(list) 
    # creating dictionary with default values 0
    method_counter = defaultdict(int)
    status_2xx_counter = 0
    total_entries = 0

    # walking down all uids in dictionary
    for uid in log_dict:
        # take list of entries with given uid
        entries = log_dict[uid]
        for entry in entries:
            host = entry["host"]
            ts = entry["ts"]
            method = entry["method"]
            status = entry["status_code"]

            # collecting timestamps for each host if exists
            if host != "-":
                host_data[host].append(ts)

            # updating methods, status and all entries counter
            method_counter[method] += 1

            if 200 <= status < 300:
                status_2xx_counter += 1

            total_entries += 1

    print_hosts(host_data)
    print_entry_counts(host_data)
    print_entry_dates(host_data)
    print_method_usage(method_counter, total_entries)
    print_success_ratio(status_2xx_counter, total_entries)


def print_hosts(host_data: dict):
    print("1. Hosts domain names/IP:")
    for host in host_data:
        print(f"  - {host}")
    print("\n" + "-" * 40)


def print_entry_counts(host_data: dict):
    print("2. Amount of entries with hosts:")
    for host, timestamps in host_data.items():
        print(f"  - {host}: {len(timestamps)} entries")
    print("\n" + "-" * 40)


def print_entry_dates(host_data: dict):
    print("3. First and last entry by each host:")
    for host, timestamps in host_data.items():
        first = min(timestamps)
        last = max(timestamps)
        print(f"  - {host}: from {first} to {last}")
    print("\n" + "-" * 40)


def print_method_usage(method_counter: dict, total_entries: int):
    print("4. Method usage in percent:")
    if total_entries == 0:
        print("No entries to compare")
        return

    for method, count in method_counter.items():
        percent = (count / total_entries) * 100
        if percent > 0.001:
            print(f" {method}: {count} ({percent:.4f}%)")
    print("\n" + "-" * 40)


def print_success_ratio(status_2xx_counter: int, total_entries: int):
    print(f"5. Entries with status code 2xx to all entries: {status_2xx_counter} / {total_entries}")
    print("-" * 40)
    

if __name__ == "__main__":
    logs = read_log()
    log_dict = log_to_dict(logs)
    print_dict_entry_dates(log_dict)


