import reader
import ipaddress

def get_entries_by_addr(log: list, addr) -> list:
    filtered_by_ip = []
    is_ip_addr = False

    try:
        ipaddress.ip_address(addr)
        is_ip_addr = True
    except ValueError:
        pass  

    for entry in log:
        try:
            if is_ip_addr:
                # index of ip_orig_h
                if entry[2] == addr:  
                    filtered_by_ip.append(entry)
            else:
                # index of hostname (*sometimes its basically ip address)
                if entry[7] == addr:
                    filtered_by_ip.append(entry)
        # skip invalid formatted entries
        except IndexError:
            continue  

    return filtered_by_ip

def get_entries_by_code(log: list, status_code: int) -> list:
    #valid status code is between 100 and 599
    if not (status_code == 0 or 100 <= status_code <= 599):
        raise ValueError(f"Code status expected between 100-599 but given: {status_code}")

    filtered_by_code = []

    for entry in log:
        try:
            if entry[9] == status_code:
                filtered_by_code.append(entry)
        # skipping incorrectly formatted entries, if entry dont have index of status code
        except IndexError:
            continue  

    return filtered_by_code

if __name__ == "__main__":
    log = reader.read_log()  
    results_ip = get_entries_by_addr(log, "192.168.28.100")
    for r in results_ip:
        print(r)