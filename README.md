# 🏫 AcadTranspiler

> **A small curriculum compiler built while learning Python, testing, and software design.**

## 🎥 Video Demo

[**My Harvard CS50P Final Project — AcadTranspiler**](https://youtu.be/hiVFjDAsCY4?si=l2LyeMv5eFWPI_5W)

---

## `> WHOAMI`

I'm a beginner programmer from Nigeria working through Harvard's **CS50P: Introduction to Programming with Python**.

For my final project, I wanted to build something that came from a question I genuinely found interesting:

> **Can university curriculum information be made understandable to software?**

AcadTranspiler is my attempt at answering that question.

It is not a production university information system. It is a working prototype that explores how curriculum information can be **parsed, structured, validated, analysed, and exported** using Python.

---

## `> WHAT_IT_DOES`

AcadTranspiler is a Python command-line tool that processes university curriculum data.

It can:

* read curriculum information from CSV files and the project's text format;
* convert individual course records into structured Python data;
* validate course and curriculum information;
* detect duplicate course codes and broken prerequisite references;
* check for circular prerequisite relationships;
* build a prerequisite dependency graph;
* generate a human-readable academic lint report; and
* export structured curriculum data as JSON.

The basic pipeline is:

```text
CURRICULUM DATA
       │
       ▼
     PARSE
       │
       ▼
   STRUCTURE
       │
       ▼
   VALIDATE
       │
       ▼
    ANALYSE
       │
       ├──────────► LINT REPORT
       │
       └──────────► JSON
```

### Example

A curriculum record such as:

```csv
CSC301,Artificial Intelligence,3,300,Alpha,CSC201
```

can be represented internally as:

```json
{
  "code": "CSC301",
  "title": "Artificial Intelligence",
  "units": "3",
  "level": "300",
  "semester": "Alpha",
  "prerequisites": "CSC201"
}
```

Once the information has structure, the program can reason about relationships between courses instead of treating the curriculum as plain text.

For example, if a course references a prerequisite that does not exist, AcadTranspiler can report it:

```text
⚠ CSC301 references unknown prerequisite CSC201
```

It can also detect duplicate course codes and circular prerequisite dependencies.

---

## `> WHY_IT_EXISTS`

Universities publish academic information in formats designed primarily for people to read: tables, documents, PDFs, spreadsheets, and other human-oriented representations.

Software, however, works much better with structured data.

AcadTranspiler explores the bridge between those two worlds:

```text
Human-readable curriculum
            │
            ▼
      AcadTranspiler
            │
            ▼
Machine-readable curriculum
            │
            ▼
Validation + analysis
```

The larger idea is simple:

> **What if curriculum information could be processed more like source code?**

This project is a small experiment built around that question.

---

## `> QUICK_START`

The sample curriculum is stored in:

```text
data/curriculum.csv
```

From the project directory, run:

```bash
python project.py validate curriculum.csv
```

AcadTranspiler will process the curriculum, print a validation report, save:

```text
output/lint_report.txt
```

and ask whether you also want to export:

```text
output/curriculum.json
```

To run the interactive mode:

```bash
python project.py
```

To run the test suite:

```bash
pytest
```

---

## `> CURRICULUM_FORMAT`

AcadTranspiler expects curriculum data in the following CSV structure:

```csv
code,title,units,level,semester,prerequisites
```

For example:

```csv
CSC101,Introduction to Computing,3,100,Alpha,
CSC102,Programming Fundamentals,3,100,Omega,CSC101
CSC201,Data Structures,3,200,Alpha,CSC102
CSC301,Artificial Intelligence,3,300,Alpha,CSC201
```

### Preparing an existing curriculum

Real university curricula may come as PDFs, documents, images, or differently structured tables.

For converting those documents into structured fields, **[Parseur](https://parseur.com/)** can be used as an external document-extraction tool.

Configure the extracted fields as:

```text
code
title
units
level
semester
prerequisites
```

After extraction, review the resulting data and export it as CSV before giving it to AcadTranspiler.

> **Important:** document-extraction tools can make mistakes. Always review the generated data before processing it with AcadTranspiler.

---

## `> WHAT_I_LEARNED`

The most valuable part of this project was not only the final program. It was learning how to break a larger problem into smaller, testable pieces.

Through AcadTranspiler, I learned how to:

* design functions with separate responsibilities;
* read and write files with `pathlib`, `csv`, and `json`;
* transform raw text into structured Python data;
* validate input instead of assuming that every record is correct;
* use regular expressions for simple course-code validation;
* model prerequisites as a directed graph;
* use depth-first search for graph analysis;
* write automated tests with `pytest`; and
* document design decisions, limitations, and trade-offs.

One of my biggest lessons was changing how I think about testing.

A test is not only a way to prove that code works. It is also a question:

> *What do I believe this function should do, and what happens when that belief is wrong?*

---

## `> HONEST_TELEMETRY`

AcadTranspiler is a **CS50P final project and prototype**, not a complete university information system.

The current implementation has several intentional limitations:

* `parse_course()` expects a specific six-field format and does not currently support arbitrary commas inside course titles.
* The CSV loader expects the curriculum to follow the project's expected input structure.
* Some malformed numeric values may currently raise exceptions rather than being converted into user-friendly validation messages.
* The text loader expects a specific layout and is not a general parser for arbitrary PDFs, documents, or images.
* Prerequisites are currently represented in a simplified form rather than supporting complex prerequisite groups and alternatives.
* Dependency visualisation is currently limited compared with a full graph-visualisation system.
* The reporting system is intentionally simple and can be expanded to preserve more detailed course-specific diagnostics.
* The command-line interface has limited argument handling and does not yet provide a full help system.

These limitations define the current boundary of the project and also suggest future improvements, including stronger input parsing, richer prerequisite modelling, better error handling, more complete graph analysis, and a more polished command-line interface.

---

## `> DESIGN_NOTES`

I prioritised readability, small functions, and clear responsibilities because this project was also an exercise in learning how to manage program complexity.

The main flow is:

```text
load_curriculum()
        │
        ▼
parse_course()
        │
        ▼
validate_course()
        │
        ▼
validate_curriculum()
        │
        ▼
build_dependency_graph()
        │
        ▼
generate_report()
        │
        ▼
export_results()
```

The longer design discussion is available in [DESIGN.md](DESIGN.md).

---

## `> PROJECT_STATE`

```text
[x] Curriculum parser
[x] Course validation
[x] Curriculum validation
[x] Dependency analysis
[x] Automated tests for core functions
[x] Human-readable lint report
[x] JSON export
[~] More robust input parsing
[~] Better command-line errors and help
[ ] Richer prerequisite rules
[ ] More complete graph visualisation
```

AcadTranspiler is intentionally a foundation rather than a finished platform.

The idea is:

> **Learn something → build a small version → discover its limits → improve the questions.**

The code is the evidence.
The README is the explanation.

---

## `> CASE_STUDY`

AcadTranspiler can be used with curriculum information from different institutions as long as the information is converted into its expected structure.

For experimentation, the repository includes a synthetic curriculum dataset whose structure is inspired by publicly available university programme tables, including Covenant University's published Computer Science programme structure. It is not Covenant University's curriculum.

---

## `> CONTACT`

AcadTranspiler was built by **Kenneth-Anthony Nwosu** as a Harvard CS50P final project.

Questions, feedback, and thoughtful discussion are welcome at:

[kennethnwosua202110@gmail.com](mailto:kennethnwosua202110@gmail.com)
