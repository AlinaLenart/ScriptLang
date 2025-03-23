import sys
from . import pure_text

def main():
    input_text = sys.stdin.read()
    processed_text = pure_text.extract_content(input_text)
    print(processed_text)
    

main()
   

