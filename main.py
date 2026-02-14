import sys
from src.models.family_tree import FamilyTree
from src.core.seeder import seed_data

def main():
    if len(sys.argv) < 2:
        return

    tree = FamilyTree()
    seed_data(tree)

    try:
        with open(sys.argv[1], 'r') as file:
            for line in file:
                parts = line.strip().split()
                if not parts: continue
                
                command = parts[0]
                if command == "ADD_CHILD":
                    print(tree.add_child(parts[1], parts[2], parts[3]))
                elif command == "GET_RELATIONSHIP":
                    print(tree.get_relationship(parts[1], parts[2]))
    except Exception:
        pass

if __name__ == "__main__":
    main()
