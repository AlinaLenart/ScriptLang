from reader import read_log

def sort_log(log: list, index: int) -> list:
    try:
        # log is empty
        if not log:
            return []

        # valid index value
        if index < 0 or index >= len(log[0]):
            raise IndexError(f"Index {index} is out of bound (max: {len(log[0]) - 1}).")

        # creates new sorted list, key specify what to sort by
        # anonymous func to sort each entry by entry[index] element position inside tuple
        return sorted(log, key=lambda entry: entry[index])

    except ValueError as e:
        print(f"Input value error: {e}")
    except Exception as e:
        print(f"Unexpected exception: {e}")

    return []




if __name__ == "__main__":
    log = read_log()
    sorted_log = sort_log(log, 1)
    print(sorted_log)
