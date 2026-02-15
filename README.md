# Lengaburu Family Tree

This project is a Python based application that models the Lengaburu family tree. It allows users to define family relationships, add children to existing members, and query various relationships between family members (e.g., "Maternal-Uncle", "Siblings", "Granddaughter").

## How to Run

The application takes an input file containing a list of commands.

1. Ensure you have Python installed.
2. Run the script from the root directory:

```bash
python3 main.py input.txt
```

### Input Format
The input file should contain commands in the following format:
- `ADD_CHILD [MotherName] [ChildName] [Gender]`
- `GET_RELATIONSHIP [Name] [RelationshipType]`

## Running Tests

To verify the correctness of the solution, you can run the comprehensive unit test suite included in the `tests/` directory.

Run this command from the project root:

```bash
python3 -m unittest ./tests/test_family_tree.py
```


## Project Structure

The project is organized into modular components to ensure maintainability and scalability:

- **`main.py`**: The entry point of the application. It handles file I/O, parses commands, and invokes the necessary actions on the `FamilyTree`.
- **`src/models/`**: Contains the core data structures (`Person`, `FamilyTree`, `Gender` enum).
- **`src/relationships/`**: Contains the logic for determining relationships, implemented using the Strategy Pattern.
- **`src/core/`**: Contains utility modules like `seeder.py` (to initialize the tree with default data) and custom exceptions.
- **`tests/`**: Contains unit tests to ensure the correctness of the application.

## Architectural Decisions & Design Patterns

The codebase involves several professional software design patterns to handle the complexity of family relationships cleanly.

### 1. Strategy Pattern (`src/relationships/strategies.py`)
Instead of writing a massive `if-else` or `switch` statement to handle dozens of relationship types (e.g., Paternal-Uncle, Sister-In-Law), I implemented the **Strategy Pattern**.

*   **Why?** This allows each relationship logic to be encapsulated in its own class (e.g., `MaternalUncleStrategy`, `SiblingStrategy`).
*   **Benefit:** It adheres to the **Open/Closed Principle**. If we need to add a new relationship type (e.g., "Cousin"), we simply create a new class without modifying existing code. It makes the code easier to read, test, and maintain.

### 2. Factory Pattern (`src/relationships/factory.py`)
A `RelationFactory` is used to manage and retrieve the correct strategy based on the command string.

*   **Why?** It decouples the client code (`FamilyTree`) from the specific implementation of the strategies. The `FamilyTree` doesn't need to know *how* `Maternal-Aunt` is calculated; it just asks the factory for the object that handles "Maternal-Aunt".
*   **Benefit:** Centralized logic for object creation and lookup.

### 3. Separation of Concerns
The application logic is strictly separated:
*   **Models** only hold data and basic state validation.
*   **Strategies** contain the business logic for traversal.
*   **Main** handles input parsing and output formatting.

## Execution Flow

1.  **Initialization**: When `main.py` starts, the `FamilyTree` is initialized. The `seed_data` function populates the tree with the predefined King Arthur family structure.
2.  **Command Parsing**: The script reads `input.txt` line by line.
3.  **Processing**:
    *   **ADD_CHILD**: The `FamilyTree` validates the request (e.g., checks if the mother exists) and adds a new `Person` object.
    *   **GET_RELATIONSHIP**: The `FamilyTree` asks the `RelationFactory` for the correct strategy strategy (e.g., `PaternalUncleStrategy`). The strategy traverses the tree starting from the given person and returns a list of relatives.
4.  **Output**: The result is printed to the console. If an error occurs (e.g., "PERSON_NOT_FOUND"), a distinct message is displayed.
