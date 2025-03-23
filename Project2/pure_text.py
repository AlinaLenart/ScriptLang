import sys

END_PREMABLE_EMPTY_LINES = 2

def extract_content(text: str) -> str:
    result = ""
    in_preamble = True
    in_content = False
    empty_line_count = 0
    # buffor for manually build lines
    line = ""  

    for char in text:
        # creating lines, using splitlines() would increase memory usage
        if char == "\n":
            stripped_line = line.strip()

            # check end of preamble (next 2 lines are empty in first 10 lines)
            if in_preamble and empty_line_count < END_PREMABLE_EMPTY_LINES:
                # if empty line encountered increase conuter
                if stripped_line == "":
                    empty_line_count += 1
                    if empty_line_count >= END_PREMABLE_EMPTY_LINES:
                        # end of preamble
                        in_preamble = False
                        in_content = True
                else:
                    empty_line_count = 0
                # reset line buffor
                line = ""
                # skip preamble, dont write it down
                continue 
            # once empty lines counter reaches END_PREMABLE_EMPTY_LINES it means we are not longer in preamble
            elif empty_line_count >= END_PREMABLE_EMPTY_LINES:
                in_preamble = False
                in_content = True

            # ignore release info, five -
            if stripped_line.startswith("-----"):
                # dont write down release info
                break  

            # if in books content, append lines to result
            if in_content:
                result += line + "\n"  
            # reset line bufor
            line = "" 
        else:
            # create line char by char
            line += char  

    #remove \n
    return result.strip()

if __name__ == "__main__":
    input_text = sys.stdin.read()
    processed_text = extract_content(input_text)
    print(processed_text)
