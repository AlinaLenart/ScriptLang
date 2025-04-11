import sys
import os

# parsing input line command, --lines=n defines amount of printed lines, search for file_path
def parse_arguments():
    lines_to_print = 10
    file_path = None

    for arg in sys.argv[1:]:
        if arg.startswith('--lines='):
            try:
                lines_to_print = int(arg.split('=', 1)[1])
            except ValueError:
                print("Invalid --lines. Default is 10", file=sys.stderr)
                lines_to_print = 10
        elif not arg.startswith('-'):
            file_path = arg
    return lines_to_print, file_path

# returns ;last count line from lines list and then return all lines
def tail_lines(lines, count):
    if len(lines) <= count:
        return lines
    return lines[-count:]

# reads input lines
def read_input(file_path = None):
    lines = []
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            sys.exit(f"Error occured opening the file s'{file_path}': {e}")
    elif not sys.stdin.isatty():
        lines = sys.stdin.readlines()
    else:
        sys.exit("No input values. Give filepath")
    return [line.rstrip('\n') for line in lines]

def main():
    count, file_path = parse_arguments()
    input_lines = read_input(file_path)
    result = tail_lines(input_lines, count)
    for line in result:
        print(line)

if __name__ == "__main__":
   main()
