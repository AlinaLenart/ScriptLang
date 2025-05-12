import reader

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
    results_404 = get_entries_by_code(log, 404)
    for r in results_404:
        print(r)
