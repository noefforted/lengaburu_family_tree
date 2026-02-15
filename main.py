import sys
import os
from src.models.family_tree import FamilyTree
from src.core.seeder import seed_data

def main():
    # ensure user provides the input file path as an argument
    if len(sys.argv) != 2:
        print("Error: Use right command 'python3 main.py input.txt'", file=sys.stderr)
        sys.exit(1)
    input_file = sys.argv[1]
    # check if the file exists before attempting to open it
    if not os.path.exists(input_file):
        print(f"Error: File not found", file=sys.stderr)
        sys.exit(1)
    # initialize family tree and populate it with the default members
    tree = FamilyTree()
    seed_data(tree)
    # mapping string commands to family tree methods
    commands = {
            "ADD_CHILD": lambda args: tree.add_child(args[0], args[1], args[2]),
            "GET_RELATIONSHIP": lambda args: tree.get_relationship(args[0], args[1])
        }
    # read input file line by line to process family tree operations
    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            # skip empty lines
            if not parts: continue
            cmd_name = parts[0]
            cmd_args = parts[1:]
            # execute command if it exists in the commands dictionary
            action = commands.get(cmd_name)
            if action:
                print(action(cmd_args))
            else:
                # handle unrecognized command names
                print(f"ERROR: Command {cmd_name} unknown")

if __name__ == "__main__":
    main()