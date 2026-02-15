import sys
import shlex
import os
from src.models.family_tree import FamilyTree
from src.core.seeder import seed_data

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m main <absolute_path_to_input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: File not found at {input_file}")
        sys.exit(1)

    tree = FamilyTree()
    seed_data(tree)

    commands = {
            "ADD_CHILD": lambda args: tree.add_child(args[0], args[1], args[2]),
            "GET_RELATIONSHIP": lambda args: tree.get_relationship(args[0], args[1])
        }

    with open(input_file, 'r') as file:
        for line in file:
            parts = shlex.split(line.strip())
            if not parts: continue
            
            cmd_name = parts[0]
            cmd_args = parts[1:]

            # Eksekusi tanpa if/elif
            action = commands.get(cmd_name)
            if action:
                print(action(cmd_args))
            else:
                print(f"ERROR: Command {cmd_name} unknown")

if __name__ == "__main__":
    main()