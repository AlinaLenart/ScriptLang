import os
import sys
import argparse
from utils import find_media_files, convert_file

# parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Convert media files using ffmpeg.")
    parser.add_argument("directory", help="Path to directory with media files")
    parser.add_argument("--format", "-f", required=True, help="Target format (e.g. mp4, mp3, webm)")
    return parser.parse_args()

def main():
    args = parse_args()

    # check if input directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory.")
        sys.exit(1)

     # find media files to convert
    media_files = find_media_files(args.directory)

    if not media_files:
        print("No media files found")
        return

    # convert each file to the selected format
    for file_path in media_files:
        convert_file(file_path, args.format)

if __name__ == "__main__":
    main()
