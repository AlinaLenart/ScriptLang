import os
import sys

# gets env variable and splits it into directories list
def get_path_directories():
    path_var = os.environ.get("PATH", "")
    directories = path_var.split(os.pathsep)
    return directories

# returns list of files that are executed in this directory, depends on the os system
def list_executables(directory):
    executables = []
    try:
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isfile(full_path):
                #windows
                if os.name == "nt":
                    ext = os.path.splitext(item)[1].lower()
                    if ext in [".exe", ".bat", ".cmd"]:
                        executables.append(item)
                else:
                    #unix-like
                    if os.access(full_path, os.X_OK):
                        executables.append(item)
    # occuring any error => skip the directory (fe. no access)                    
    except Exception:
        pass
    return executables

# dislays directories from PATH variable, if list_exec = False displays only directories, otherwise for every dir shows also executable files
def display_path_directories(list_exec = False):
    directories = get_path_directories()
    if list_exec:
        for directory in directories:
            print(f"{directory}:")
            exec_files = list_executables(directory)
            if exec_files:
                for exe in exec_files:
                    print(f"  {exe}")
            else:
                print("!No executable files!")
            print()  
    else:
        for directory in directories:
            print(directory)

def main():
    # if using -e  it will also shows executable files
    flag = False
    if len(sys.argv) > 1 and sys.argv[1] in ("-e", "--executables"):
        flag = True
    display_path_directories(list_exec=flag)

if __name__ == "__main__":
    main()
