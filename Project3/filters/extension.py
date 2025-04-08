import reader

def get_entries_by_extension(log: list, extension: str) -> list:
    if not extension:
        raise ValueError("Enter correct file extenstion or symbol")

    filtered_by_exten = []

    for entry in log:
        try:
            # uri request path is on 8 position in our tuple
            uri = entry[8] 
            # lower case to match entries format (best without dot)
            if isinstance(uri, str) and uri.lower().endswith(f".{extension.lower()}"):
                filtered_by_exten.append(entry)
        # skipping incorrectlu formatted entries
        except IndexError:
            continue  

    return filtered_by_exten


if __name__ == "__main__":
    log = reader.read_log()  
    jpg_entries = get_entries_by_extension(log, ".jpg")
    for j in jpg_entries:
        print(j)


