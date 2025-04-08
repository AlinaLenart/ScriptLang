import reader

def get_failed_reads(log: list, combine: bool = False):
    errors_4xx = []
    errors_5xx = []

    for entry in log:
        try:
            if 400 <= entry[9] <= 499:
                errors_4xx.append(entry)
            elif 500 <= entry[9] <= 599:
                errors_5xx.append(entry)
        # skipping incorrectly formatted entreies
        except (IndexError, TypeError):
            continue  

    if combine:
        # or combine = true then it connects both 4xx and 5xx list (4xx elements first)
        return errors_4xx + errors_5xx
    else:
        # returns tuple with both tables
        return (errors_4xx, errors_5xx)


if __name__ == "__main__":
    log = reader.read_log()  
    errors = get_failed_reads(log, combine=True)
    for e in errors:
        print(e)