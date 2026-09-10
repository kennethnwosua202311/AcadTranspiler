"""Testing module for project"""
from project import parse_course, validate_course, validate_curriculum, build_dependency_graph

# parse_course_test_cases
def test_parse_course_valid():
    """Unit test for validity of parse_course function"""
    assert parse_course("TMC111,Introduction to Total Man Concept,3,100,Alpha,") == {
        "code": "TMC111",
        "title": "Introduction to Total Man Concept",
        "units": "3",
        "level": "100",
        "semester": "Alpha",
        "prerequisites": ""
    }
    assert parse_course("COS111,Introduction to Computing Sciences,3,100,Alpha,") == {
        "code": "COS111",
        "title": "Introduction to Computing Sciences",
        "units": "3",
        "level": "100",
        "semester": "Alpha",
        "prerequisites": ""
    }
    assert parse_course("MTH111,Elementary Mathematics,2,100,Alpha,") == {
        "code": "MTH111",
        "title": "Elementary Mathematics",
        "units": "2",
        "level": "100",
        "semester": "Alpha",
        "prerequisites": ""
    }
    assert parse_course("PHY119,General Practical Physics I,1,100,Alpha,") == {
        "code": "PHY119",
        "title": "General Practical Physics I",
        "units": "1",
        "level": "100",
        "semester": "Alpha",
        "prerequisites": ""
    }
    assert parse_course("CSC301,Artificial Intelligence,3,300,Alpha,CSC201") == {
        "code": "CSC301",
        "title": "Artificial Intelligence",
        "units": "3",
        "level": "300",
        "semester": "Alpha",
        "prerequisites": "CSC201"
    }

def test_parse_course_missing_code():
    """Unit tests for continuity although missing code"""
    assert parse_course("CSC293Covenant,Deep Learning & Neural Networks,8,400,Omega,CSC343") == {
        "code": "CSC293Covenant",
        "title": "Deep Learning & Neural Networks",
        "units": "8",
        "level": "400",
        "semester": "Omega",
        "prerequisites": "CSC343"
    }
    assert parse_course("CSC222Covenant,Systems Design,6,200,Alpha,CSC200") == {
            "code": "CSC222Covenant",
            "title": "Systems Design",
            "units": "6",
            "level": "200",
            "semester": "Alpha",
            "prerequisites": "CSC200"
        }
    assert parse_course("GST11&*,Communication In English,3,100,Alpha,") == {
            "code": "GST11&*",
            "title": "Communication In English",
            "units": "3",
            "level": "100",
            "semester": "Alpha",
            "prerequisites": ""
        }

def test_parse_course_other_invalidities():
    """Unit tests for continuity although invalidities"""
    assert parse_course("STA111,,8,700,2nd,") == {
            "code": "STA111",
            "title": "",
            "units": "8",
            "level": "700",
            "semester": "2nd",
            "prerequisites": ""
        }


# validate_course_test_cases
def test_validate_course_valid():
    """Unit tests for validate_course valid test cases"""
    assert not validate_course(parse_course("TMC111,Introduction to Total Man Concept,3,100,Alpha,"))
    assert not validate_course(parse_course("COS111,Introduction to Computing Sciences,3,100,Alpha,"))
    assert not validate_course(parse_course("MTH111,Elementary Mathematics,2,100,Alpha,"))
    assert not validate_course(parse_course("PHY119,General Practical Physics I,1,100,Alpha,"))
    assert not validate_course(parse_course("CSC301,Artificial Intelligence,3,300,Alpha,CSC201"))

def test_validate_course_invalid_units():
    """Unit tests for validate_course invalid units test cases"""
    assert ["Invalid units"] == validate_course(parse_course("CSC112,Computer Application Packages I,8,200,Alpha,"))
    assert ["Invalid units"] == validate_course(parse_course("PHY120,General Practical Physics II,9,300,Alpha,"))

def test_validate_other_invalidities():
    """Unit tests for validate_course invalidities test cases"""
    assert set(["Missing title", "Invalid code"]) == set(validate_course(parse_course("EDS,,2,300,Omega,")))
    assert set(["Invalid semester", "Invalid level", "Invalid prerequisite"]) == set(validate_course(parse_course("CSC241,Python Programming Language I,3,600,1st,CS50P")))


# validate_curriculum_test_cases
def test_validate_curriculum_duplicates():
    """Unit test for validate_curriculum duplicates test case"""
    assert validate_curriculum([
        {
            "code": "CSC125",
            "title": "Operating Systems",
            "units": "3",
            "level": "200",
            "semester": "Omega",
            "prerequisites": ""
        },
        {
            "code": "CSC125",
            "title": "Kernels",
            "units": "1",
            "level": "200",
            "semester": "Omega",
            "prerequisites": ""
        }
    ]) == ["ERROR: Duplicate course code CSC125"]

def test_validate_curriculum_broken_prereq():
    """Unit test for validate_curriculum broken prerequisites test cases."""
    assert validate_curriculum([
        {
            "code": "CSC125",
            "title": "Operating Systems",
            "units": "3",
            "level": "200",
            "semester": "Omega",
            "prerequisites": "CSC100"
        },
        {
            "code": "CSC401",
            "title": "Compiler Construction",
            "units": "3",
            "level": "400",
            "semester": "Omega",
            "prerequisites": "CSC125"
        }
    ]) == ["WARNING: CSC125 requires CSC100, but CSC100 does not exist in this curriculum."]

def test_build_dependency_graph():
    """Unit test for build_dependency_graph"""
    assert build_dependency_graph([
        {
            "code": "CSC125",
            "title": "Operating Systems",
            "units": "3",
            "level": "200",
            "semester": "Omega",
            "prerequisites": "CSC100"
        },
        {
            "code": "CSC401",
            "title": "Compiler Construction",
            "units": "3",
            "level": "400",
            "semester": "Omega",
            "prerequisites": "CSC125"
        }
    ]) == "CSC100 ➡  CSC125 ➡  CSC401"

assert build_dependency_graph([{
    "code": "CSC102",
    "title": "Programming Fundamentals",
    "units": "3",
    "level": "100",
    "semester": "Omega",
    "prerequisites": "CSC101"
  },
  {
    "code": "CSC201",
    "title": "Data Structures",
    "units": "3",
    "level": "200",
    "semester": "Alpha",
    "prerequisites": "CSC102"
  }]) == "CSC101 ➡  CSC102 ➡  CSC201"

# I still don't get this testing stuff actually.
# Well I'll still take CS50x and see if there could be any improvements.
