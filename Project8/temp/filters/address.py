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


if __name__ == "__main__":
    log = reader.read_log()  
    results_ip = get_entries_by_addr(log, "192.168.28.100")
    for r in results_ip:
        print(r)