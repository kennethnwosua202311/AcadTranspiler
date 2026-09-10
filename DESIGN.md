# AcadTranspiler

## `> DESIGN_INTENT`

AcadTranspiler is a CS50P final project and a record of me learning how to think more deliberately about programs.

I am still a beginner. That matters to the design because I chose readability over cleverness, small functions over one very large `main()` function, and explicit steps over abstractions I could not yet explain. The goal was not to pretend that the project was production-ready. The goal was to build something real enough to make me confront parsing, validation, testing, file handling, and graph relationships.

The central question behind the project is:

> Can university curriculum information be made understandable to software?

AcadTranspiler explores one small answer: turn curriculum records into structured data, validate their assumptions, analyse their prerequisite relationships, and produce useful output.

## `> ARCHITECTURE`

The program has two entry points:

1. **Interactive mode** starts when `project.py` is run without command-line arguments.
2. **Validation mode** starts with a command such as `python project.py validate curriculum.csv` and generates a report.

The shared processing functions are organised around this pipeline:

```text
INPUT FILE
    |
    v
load_curriculum()
    |
    +--> CSV: csv.DictReader()
    |
    +--> TXT: fixed-layout extraction -> parse_course()
    |
    v
COURSE DICTIONARIES
    |
    +--> validate_course()
    |
    +--> validate_curriculum()
    |
    +--> build_dependency_graph()
    |
    v
REPORTING / JSON EXPORT
```

The functions have deliberately narrow responsibilities:

| Function | Responsibility |
| --- | --- |
| `load_curriculum()` | Read CSV or TXT curriculum data from the `data/` directory. |
| `parse_course()` | Convert one comma-separated course row into a dictionary. |
| `validate_course()` | Check one course's code, title, units, level, semester, and prerequisite. |
| `validate_curriculum()` | Check duplicate codes, missing prerequisites, and circular dependencies. |
| `build_dependency_graph()` | Follow prerequisite links and render a readable dependency chain. |
| `get_results()` | Collect validation and dependency information for the report. |
| `generate_report()` | Turn collected results into a human-readable report. |
| `export_json()` | Save curriculum dictionaries as formatted JSON. |

This separation makes the program easier to reason about and makes the core functions possible to test without running the whole command-line interface.

## `> DATA_MODEL`

Each course is represented as a dictionary with six fields:

```python
{
    "code": "CSC301",
    "title": "Artificial Intelligence",
    "units": "3",
    "level": "300",
    "semester": "Alpha",
    "prerequisites": "CSC201"
}
```

The values remain strings because they first come from CSV or text input. Validation then checks whether those strings represent acceptable values. This keeps parsing and validation as separate ideas: parsing answers *what did the input say?*, while validation answers *is that acceptable?*

## `> VALIDATION_DECISIONS`

`validate_course()` checks the rules that apply to one record:

- course codes must follow the expected three-letter, three-digit pattern;
- titles must not be empty;
- units must be between 1 and 5;
- levels must be 100, 200, 300, or 400;
- semesters must be `Alpha` or `Omega`; and
- a non-empty prerequisite must look like a valid course code.

`validate_curriculum()` checks relationships between records:

- duplicate course codes are reported as errors;
- prerequisites that are not present in the curriculum are reported as warnings; and
- depth-first search is used to look for circular prerequisite relationships.

These checks are intentionally simple. They are enough to demonstrate the difference between validating one object and validating a collection of related objects.

## `> GRAPH_DECISION`

Prerequisites form a directed graph. If `CSC201` requires `CSC102`, the relationship can be represented as:

```text
CSC102 -> CSC201
```

The implementation stores each course code with its prerequisite and uses depth-first search to follow the links. For cycle detection, the program keeps track of both visited nodes and the current path. A node appearing again in the current path indicates a circular dependency.

The display function follows a chain and reverses it so that the prerequisite appears before the course that depends on it:

```text
CSC101 ➡ CSC102 ➡ CSC201
```

This is a readable first version of dependency analysis, rather than a complete graph-visualisation system.

## `> FILE_HANDLING`

The project uses Python's standard library:

- `csv` reads the structured curriculum file;
- `json` exports the parsed curriculum;
- `pathlib.Path` creates the output directory when needed;
- `re` performs course-code checks and extracts information for reporting; and
- `sys` handles command-line arguments and program exits.

The CSV format is the main structured input. The TXT format is supported because it resembles the way a person might read a curriculum document:

```text
CSC101
Introduction to Computing
3 Units
100 Level
Alpha Semester
Prerequisites:
```

The TXT loader currently relies on this fixed six-line record layout. That choice kept the project within the scope of a beginner Python project, but it also creates a clear boundary for future improvement.

## `> ERROR_HANDLING`

The command-line entry point catches `EOFError` and `KeyboardInterrupt` so that an interrupted interactive session can close with a message.

It also currently catches general exceptions and displays a generic failure message. I know this is broader than ideal: it can hide the original traceback and make debugging harder. I chose it while learning because I wanted the command-line program to fail in a readable way, but a future version should handle expected input errors specifically and preserve useful diagnostics for unexpected programming errors.

## `> TESTING_APPROACH`

The tests focus on the functions that make the project's decisions:

- valid course parsing;
- parsing unusual but still structurally readable input;
- valid and invalid course fields;
- duplicate course codes;
- broken prerequisite references; and
- dependency graph output.

The tests are intentionally small and direct. Each one asks a narrow question about a function's expected result. Writing them taught me that testing is not only about proving success. It is also a way to make my assumptions visible.

The test suite can be run with:

```bash
python -m pytest
```

## `> KNOWN_LIMITATIONS`

The most notable ignored edge cases are part of the current design boundary:

- `parse_course()` expects exactly six comma-separated fields, so commas inside course titles are not supported.
- Malformed or non-numeric `units` and `level` values can raise exceptions during validation instead of becoming friendly validation messages.
- The CSV loader expects a filename under `data/` rather than accepting arbitrary paths.
- The TXT loader does not parse arbitrary PDFs, documents, images, or variations in document layout.
- A course currently has one prerequisite string, not a full expression supporting alternatives, groups, or multiple prerequisites.
- The dependency display follows the chain beginning with the last loaded course and does not render every disconnected graph in one diagram.
- The report condenses some course-specific validation details into general categories.
- The command-line interface has limited argument parsing and no dedicated help command.

These limitations are not accidental claims that the project is complete. They are useful future-work markers. The next improvements I would make are robust CSV parsing, structured input errors, richer prerequisite modelling, complete graph traversal, and a clearer command-line interface.

## `> DESIGN_TRADE_OFFS`

Several choices were made in favour of learning and readability:

### Small functions

Instead of placing every operation inside `main()`, I separated loading, parsing, validation, graph analysis, reporting, and exporting. This made the code easier to test and gave each stage a name.

### Standard library first

The project has no external runtime dependencies. Python's standard library already provided the tools needed for CSV, TXT, JSON, regular expressions, paths, and command-line arguments.

### Explicit logic

Some parts of the code could be compressed into shorter expressions. I kept several steps visible because I was still learning the underlying algorithms, especially depth-first search and the movement from raw input to structured data.

### Documentation as part of the build

Writing this file forced me to explain decisions I had previously made instinctively. That was useful because unclear documentation often points to unclear thinking.

## `> CURRENT_STATE`

```text
[x] Parse CSV curriculum data
[x] Parse the project's fixed-layout TXT format
[x] Validate individual courses
[x] Validate curriculum relationships
[x] Detect circular dependencies
[x] Generate a lint report
[x] Export JSON
[x] Test the core functions
[~] Improve input and error handling
[ ] Support richer prerequisite expressions
[ ] Provide complete graph visualisation
```

AcadTranspiler is small by design, but it is not empty. It contains the first version of a problem I care about, the mistakes that helped me understand it, and a clear list of questions for the next version.

For the user-facing explanation and setup instructions, see [README.md](README.md).
