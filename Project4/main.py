import sys
import os
import json
import subprocess
from aggregator import aggregate_statistics

def main():
    analyser_file_name = "analyze_file.py"

    # require exactly one argument the directory path
    if len(sys.argv) < 2:
        sys.exit("Usage: python main.py <path_to_directory>")
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        sys.exit(f"{directory} is not a valid directory.")
    
    results = []
    # only process files ending with .txt
    for filename in os.listdir(directory):
        if not filename.lower().endswith('.txt'):
            continue
        file_path = os.path.join(directory, filename)
        # skip if not a regular file
        if os.path.isfile(file_path):
            try:
                # run analyze_file.py passing file path via STDIN
                proc = subprocess.run(
                    [sys.executable, analyser_file_name], 
                    input=file_path + "\n",  
                    text=True,
                    capture_output=True,
                    check=True
                )
                # parse JSON result from analyze_file.py
                result = json.loads(proc.stdout)
                results.append(result)
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] File: {file_path}", file=sys.stderr)
                print(f"[STDERR]: {e.stderr}", file=sys.stderr)
                print(f"[STDOUT]: {e.stdout}", file=sys.stderr)
            except json.JSONDecodeError as e:
                print(f"Decoding JSON file error {file_path}: {e}", file=sys.stderr)
    
    if not results:
        sys.exit("No files proccessed")
    
    aggregated = aggregate_statistics(results)
    print(json.dumps(aggregated, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
