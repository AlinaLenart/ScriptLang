import os
import subprocess
import datetime
import json
# import shutil

def get_audio_extensions():
    return ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']

def get_video_extensions():
    return ['.mp4', '.avi', '.mkv', '.mov', '.webm', '.flv', '.wmv']

# list of supported audio and video file extensions
def get_supported_extensions():
    return get_audio_extensions() + get_video_extensions()

# recursively find media files
def find_media_files(directory):
    media_files = []
    for root, _, files in os.walk(directory):
        # skip converted folder
        if "converted" in root:
            continue  

        for file in files:
            if os.path.splitext(file)[1].lower() in get_supported_extensions():
                media_files.append(os.path.join(root, file))
    return media_files

# check file type
def is_audio_file(file_path):
    return os.path.splitext(file_path)[1].lower() in get_audio_extensions()

def is_video_file(file_path):
    return os.path.splitext(file_path)[1].lower() in get_video_extensions()

# create output filename with timestamp and original name
def create_output_filename(input_file, output_format):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    name = os.path.splitext(os.path.basename(input_file))[0]
    return f"{timestamp}-{name}.{output_format}"

# get the output directory from ENV or default to ./converted/
def get_output_directory():
    output_dir = os.environ.get('CONVERTED_DIR', os.path.join(os.getcwd(), 'converted'))
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

# get path to the history.jsobn file
def get_history_path():
    return os.path.join(get_output_directory(), "history.json")

def load_history():
    path = get_history_path()
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# save updated history back to file
def save_history(history):
    with open(get_history_path(), 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

#add a new entry to conversion history
def add_history_entry(input_path, output_path, output_format):
    history = load_history()
    history.append({
        "date_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original_file": input_path,
        "output_format": output_format,
        "output_file": output_path
    })
    save_history(history)

# run ffmpeg to convert the file
def convert_file(input_path, output_format):
    output_dir = get_output_directory()
    output_filename = create_output_filename(input_path, output_format)
    output_path = os.path.join(output_dir, output_filename)

    # here put your path to ffmpeg
    ffmpeg_path = r"E:\ffmpeg\bin\ffmpeg.exe"  

    # exception if ffmpeg is not found
    if not os.path.exists(ffmpeg_path):
        raise RuntimeError(f"Nie znaleziono ffmpeg pod: {ffmpeg_path}")

    # prepare the ffmpeg command
    ffmpeg_command = [ffmpeg_path, "-i", input_path, "-y", output_path]
    print("FFmpeg command:", ffmpeg_command)

    #run the conversion process
    result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(f"Converted: {input_path} → {output_path}")
        add_history_entry(input_path, output_path, output_format)
    else:
        print(f"Error converting {input_path}:\n{result.stderr}")
