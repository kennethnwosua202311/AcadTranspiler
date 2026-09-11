""" 🏫 AcadTranspiler."""
import sys
import csv
import re
import json
from pathlib import Path


def main():
    """The main function that brings every bit of the project together."""

    # My exclusive functions 😁😎
    def intro():
        """Intro for this CS50P Final Project."""
        print("""
        =============================================================================================== =+
        ||                                                                                                  =+
        ||                                  🏫 ACADTRANSPILER                               +=  for CS50P     =+
        ||                          Academic Curriculum Compiler 📖🖥️                             =+     =+     =+
        ||                                                                                      by Ken  +=      =+
        ===============================================================================================     =+
        """)

    def outro():
        print("""
===================================================================================================================
Thank you for using AcadTranspiler. If you have any issues or contributions,
feel free to contact me using my email: kennethnwosua202110@gmail.com.
===================================================================================================================
""")

    def deformat(course_dict):
        """Takes in our course dictionary and makes it a str."""
        course = []
        course_values = course_dict.values()
        for value in course_values:
            course.append(value)
        course = str(course).strip("[]").replace("'", "").replace(", ", ",")
        return course

    def get_results(curriculum):
        """Return results for generate_report(results)."""

        results = []

        # First stage of result analysis
        first_stage_results = validate_curriculum(curriculum)
        for problem in first_stage_results:
            if problem.startswith("ERROR"):
                pattern = r"((?:[A-Z]+)(?:[A-Z]+)(?:[A-Z]+)(?:[0-9]+)(?:[0-9]+)(?:[0-9]+))"
                if matches := re.search(pattern, problem):
                    results.append(["duplicate error", matches.group(1)])
            if problem.startswith("WARNING"):
                pattern = r"((?:[A-Z]+)(?:[A-Z]+)(?:[A-Z]+)(?:[0-9]+)(?:[0-9]+)(?:[0-9]+))"
                group = list(dict.fromkeys(re.findall(pattern, problem)))
                results.append(["broken prerequisite", group])

        # Second stage of result analysis
        course_count = 0
        for _ in curriculum:
            course_count += 1
        results.append(["course_count", course_count])

        # Third stage of result analysis
        for course in curriculum:
            problems = validate_course(course)
            if problems:
                problems = [problem.lower() for problem in problems]
                for problem in problems:
                    results.append(["structure", problem])

        # Fourth stage of result analysis
        prereq_relationship_prep = build_dependency_graph(curriculum)
        pattern = r"((?:[A-Z]+)(?:[A-Z]+)(?:[A-Z]+)(?:[0-9]+)(?:[0-9]+)(?:[0-9]+))"
        preq_relationship = re.findall(pattern, prereq_relationship_prep)
        preq_relationship_count = len(preq_relationship) - 1
        results.append(["dependencies: prereq", preq_relationship_count])

        # Fifth stage of result analysis
        fifth_stage_results = validate_curriculum(curriculum)

        if not fifth_stage_results:
            results.append(["dependencies: cycles", "False"])
        else:
            for problem in fifth_stage_results:
                if "requires" in problem:
                    results.append(["dependencies: cycles", "True"])
                    break
                results.append(["dependencies: cycles", "False"])
                break

        return results

    def export_lint(report):
        with open("output/lint_report.txt", "w", encoding="utf-8") as file:
            file.write(report)

    POSITIVE = ("y", "yes", "yeah")

    # sys.argv's
    if len(sys.argv) == 3:
        if sys.argv[1] == "validate":
            intro()
            curriculum_file = sys.argv[2]
            report = generate_report(get_results(load_curriculum(curriculum_file)))
            print(report)
            print("Saved in file...(lint_report.txt)")
            output_folder = Path("output")
            output_folder.mkdir(parents=True, exist_ok=True)
            export_lint(report)
            question_4 = input("Would you like to us to transpile your curriculum (Y/N)? ").lower()
            if question_4 in POSITIVE:
                export_json(load_curriculum(curriculum_file))
                print("Compilation complete!")
                outro()
                sys.exit()
            else:
                outro()
    elif len(sys.argv) == 1:
        pass
    else:
        intro()
        print("Not a valid AcadTranspiler command")
        outro()

    # main section
    intro()
    curriculum = input("Please enter a curriculum file for compilation> ")
    if curriculum == "":
        curriculum = "curriculum.csv"
    curriculum = load_curriculum(curriculum)
    for i, course in enumerate(curriculum):
        problems = validate_course(parse_course(deformat(course)))
        if not problems:
            print(f"Seems like line {i + 1} of your curriculum is fine.")
            continue
        for problem in problems:
            print(f"Seems like you have an {problem.lower()} on line {i + 1}")

    question_1 = input("Would you like the transpiler to validate your entire curriculum  (Y/N)? ").lower()
    if question_1 in POSITIVE:
        problems = validate_curriculum(curriculum)
        if not problems:
            print("Seems like everything is fine here!")
        for problem in problems:
            print(problem)
    else:
        pass

    question_2 = input("Would you like to get a dependency graph from your curriculum (Y/N)? ").lower()
    if question_2 in POSITIVE:
        print(build_dependency_graph(curriculum))
    else:
        pass

    question_3 = input("Would you love to get an official AcadTranspiler report for your curriculum (Y/N)? ").lower()
    if question_3 in POSITIVE:
        print("In order to use our lint feature, you have to run the command: `python project.py validate curriculum.csv`.\n NOTE: In order to use the transpile feature, the lint command must be ran.")
    else:
        pass
    outro()
    sys.exit("©️  KenTech")

def load_curriculum(filename):
    """Load curriculum from a CSV/text file."""

    # accumulator array
    curriculum_output = []

    if filename.endswith(".csv"):
        with open(f"data/{filename}", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file) # Returns a dictionary
            for row in reader:
                curriculum_output.append(row)
    elif filename.endswith(".txt"):
        with open(f"data/{filename}", "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file]

            for i in range(0, len(lines), 7):
                code = lines[i]
                title = lines[i + 1]
                unit = lines[i + 2].removesuffix("Units").rstrip()
                level = lines[i + 3].removesuffix("Level").rstrip()
                semester = lines[i + 4].removesuffix("Semester").rstrip()
                prereq = lines[i + 5].removeprefix("Prerequisites:").lstrip()
                row = f"{code},{title},{unit},{level},{semester},{prereq}"
                row = parse_course(row)
                curriculum_output.append(row)
    return curriculum_output


def parse_course(row):
    """Parse a course row and returns a properly formatted output (course)."""
    row = row.strip()
    code, title, units, level, semester, prerequisites = row.split(",")

    # The structured format
    row_output = {
        "code": code,
        "title": title,
        "units": units,
        "level": level,
        "semester": semester,
        "prerequisites": prerequisites
    }

    return row_output


def validate_course(course):
    """Validates course by making sure content is in it's expected state."""
    problems = []

    # Check for course code validity
    course_code_pattern = r"^(?:[A-Z]+)(?:[A-Z]+)(?:[A-Z]+)(?:[0-9]+)(?:[0-9]+)(?:[0-9]+)$"

    if not re.search(course_code_pattern, course["code"]):
        problems.append("Invalid code")

    # Check for course title availability
    if course["title"] == "":
        problems.append("Missing title")

    # Check for course units validity
    if int(course["units"]) not in tuple((range(1, 6))):
        problems.append("Invalid units")

    # Check for course level validity
    if int(course["level"]) not in tuple(range(100, 500, 100)):
        problems.append("Invalid level")

    # Check for course semester accuracy
    if course["semester"].lower() not in ("alpha", "omega"):
        problems.append("Invalid semester")

    # Check for course prerequisite code validity
    if not re.search(course_code_pattern, course["prerequisites"]):
        if course["prerequisites"] != "":
            problems.append("Invalid prerequisite")

    # Hope this returns no problem 😅
    return problems

def validate_curriculum(courses):
    """Validates courses (curriculum) by making sure content it's in its expected state."""
    problems = []
    course_codes = [course["code"] for course in courses]

    # Check for duplicate courses
    seen = set()
    duplicates = set()

    for course in courses:
        if course["code"] in seen:
            duplicates.add(course["code"])
        else:
            seen.add(course["code"])

    if duplicates != set():
        for duplicate in duplicates:
            problems.append(f"ERROR: Duplicate course code {duplicate}")

    # Check for broken prerequisites
    for course in courses:
        if course["prerequisites"] != "" and course["prerequisites"] not in course_codes:
            problems.append(f"WARNING: {course["code"]} requires {course["prerequisites"]}, but {course["prerequisites"]} does not exist in this curriculum.")

    graph_dictionary = {}

    for course in courses:
        graph_dictionary[course["code"]] = [course["prerequisites"]]

    # Detect circular dependencies
    def detect_cycles(graph_dictionary):
        """Use depth-first search to find cycles."""
        visited = set()
        path = []

        def dfs(node):
            if node in path:
                cycle_start = path.index(node)
                return path[cycle_start:] + [node]

            if node in visited:
                return None

            path.append(node)

            for neighbor in graph_dictionary.get(node, []):
                if neighbor:
                    cycle = dfs(neighbor)

                    if cycle:
                        return cycle

            path.pop()
            visited.add(node)

            return None

        for node in graph_dictionary:
            cycle = dfs(node)

            if cycle:
                return cycle

        return None

    # Check for circular dependencies
    if detect_cycles(graph_dictionary) is None:
        pass
    else:
        circular_dependencies = detect_cycles(graph_dictionary)
        for i, _ in enumerate(circular_dependencies): # type: ignore
            if i != (len(circular_dependencies) - 1): # type: ignore
                problems.append(f"{circular_dependencies[i]} requires {circular_dependencies[i + 1]}") # type: ignore

     # Hope this returns no problem 😅
    return problems

def build_dependency_graph(courses):
    """Builds the dependency graph for the curriculum"""
    graph_dictionary = {}

    for course in courses:
        graph_dictionary[course["code"]] = [course["prerequisites"]]

    # Dictionary info
    graph_dictionary_keys = list(graph_dictionary)

    # My exclusive functions 😁😎
    diagram = []
    def diagrammatise(graph_dictionary):
        def dfs(node):
            # Thank God I knew about Depth-First Search from personal CS study
            if not node:
                return
            diagram.append(node)

            for neighbor in graph_dictionary.get(node, []):
                if neighbor == "":
                    continue
                dfs(neighbor)

        dfs(graph_dictionary_keys[-1])

        def deformat_and_diagrammatise(course_list):
            courses = ""
            course_list.reverse()
            for course in course_list:
                courses += f"{course} ➡  "
            courses = courses.strip()[:-1]
            return courses


        return deformat_and_diagrammatise(diagram)

    return diagrammatise(graph_dictionary).removesuffix(" ")


def generate_report(results):
    """Takes in results in a specified format and generate an official AcadTranspiler report"""
    course_count = 0

    # warnings
    warnings = []
    for error, victim in results:
        if error == "duplicate error":
            warnings.append(f"Duplicate course code: {victim}")

        if error == "broken prerequisite":
            patient = victim[0]
            prereq = victim[1]
            warnings.append(f"{patient} references unknown {prereq}")

    # COURSES ANALYSED
    for info_cat, info in results:
        if info_cat == "course_count":
            course_count = info

    # structures
    issues = []
    seen = set()

    for issue in issues:
        if issue in seen:
            pass
        else:
            seen.add(issue)

    issues = list(seen)
    structure_template = {
        "Courses code valid": "❌",
        "Titles complete": "❌",
        "Other info valid": "❌",
    }

    if not any(item[0] == "structure" for item in results):
        for key, _ in structure_template.items():
            structure_template[key] = "✔️"

    for structure, issue in results:
        if structure == "structure":
            issues.append(issue)
        else:
            structure_template["All required fields present"] = "✔️"

    for issue in issues:
        if issue == "invalid code":
            break
        structure_template["Courses code valid"] = "✔️"

    for issue in issues:
        if issue == "missing title":
            break
        structure_template["Titles complete"] = "✔️"

    for issue in issues:
        for issue in ("invalid semester", "invalid level", "invalid prerequisites", "invalid units"):
            if issue in issues:
                break
            structure_template["Other info valid"] = "✔️"
        break

    #  dependencies
    dependencies = []
    for dependence, value in results:
        if dependence.startswith("dependencies"):
            dependencies.append(value)

    def display_structures():
        structures_display = ""
        for key, value in structure_template.items():
            structures_display += f"{value}  {key}\n"

        structures_display = structures_display.removesuffix("\n")

        return structures_display


    def display_warnings():
        for i, warning in enumerate(warnings):
            text = warning.strip()
            text = "⚠️   " + warning
            warning = text
            warnings[i] = warning

        if not warnings:
            return "0 warnings found. We're good 👍!"

        warning_display = ""
        for warning in warnings:
            warning_display += f"{warning}\n"

        warning_display = warning_display.removesuffix("\n")

        return warning_display

    def display_dependencies():
        for i, dependence in enumerate(dependencies):
            dependence = str(dependence)
            if dependence.isdigit():
                dependencies[i] = f"{dependence} prerequisite relationship"
            elif dependence == "True":
                dependencies[i] = "Circular dependencies present"
            elif dependence == "False":
                dependencies[i] = "No circular dependencies"

        for i, dependence in enumerate(dependencies):
            text = dependence.strip()
            text = "✔️  " + dependence
            dependence = text
            dependencies[i] = dependence

        dependencies_display = ""
        for dependency in dependencies:
            dependencies_display += f"{dependency}\n"

        dependencies_display = dependencies_display.removesuffix("\n")
        return dependencies_display

    return f"""
==================================================================================
                            ACADTRANSPILER REPORT
==================================================================================

CURRICULUM
Courses analysed: {course_count}

STRUCTURE
{display_structures()}

WARNING
{display_warnings()}

DEPENDENCIES
{display_dependencies()}
"""


def export_json(courses):
    """Exports to json based on given params"""
    json_file_content = json.dumps(courses, indent=2)
    with open("output/curriculum.json", "w", encoding="utf-8") as file:
        file.write(json_file_content)

if __name__ == "__main__":
    def close():
        """sys.exit with a closing msg."""
        sys.exit("""
        =========================================================================================
        -----+++++++++++------------------------+++++++++++-------------------------+++++++++++++
        Seems like something went wrong! Consider checking your inputs and your use of this app.
        If the problem persists, feel free to contact the developer at
        kennethnwosua202110@gmail.com
        -----+++++++++++------------------------+++++++++++-------------------------+++++++++++++
        =========================================================================================
        """)
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSeems like your keyboard interrupted the process.")
        close()
    except Exception:
        close()


#🫩 The most dominant logic I've ever proposed so far in my coding journey.
# At least it's a proof of bite-sized growth, compounding over these few years 🚀

# Thank You very much Prof. David Malan and Prof. Brian Yu 🙏🏻🫂 from Harvard University.
