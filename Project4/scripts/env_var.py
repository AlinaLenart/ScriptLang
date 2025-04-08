import os
import sys

# displays environmental variables, if filters in input then find everything connected
def display_env_vars(filters = None):
    env_vars = os.environ
    if filters:
        filtered_vars = {
            name: value for name, value in env_vars.items()
            if any(f in name for f in filters)
        }
    else:
        filtered_vars = env_vars

    for var in sorted(filtered_vars.keys()):
        print(f"{var} = {filtered_vars[var]}")

def main():
    # form input line
    filters = sys.argv[1:] if len(sys.argv) > 1 else None
    display_env_vars(filters)

if __name__ == "__main__":
    main()