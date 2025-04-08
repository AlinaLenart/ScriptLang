from reader import read_log
from .convert_entry import entry_to_dict

def log_to_dict(entries: list) -> dict:
    log_dict = {}

    for entry in entries:
        # create single entry as dictionary using previous function
        entry_as_dict = entry_to_dict(entry)
        uid = entry_as_dict["uid"]

        # key "uid number" : value [list of entry_as_dict]
        # if uid haven't appeared yet
        if uid not in log_dict:
            log_dict[uid] = []

        # adding entry dictionary at the end of list of entries
        log_dict[uid].append(entry_as_dict)

    return log_dict


if __name__ == "__main__":
    logs = read_log()
    log_dict = log_to_dict(logs)
