"""
import os
import tempfile
import ProjectManager.Controller as controller
import traceback
import glob

os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "src", "scripts"))
print("current directory: " + str(os.getcwd()))

from Database.Database import Database

# First test
def test_database_creation_software_opening():
    ""
    Tests the creation of the database file at software opening
    ""
    database = Database(None, True)
    folder = database.folder
    database_folder = os.path.join(folder, "database", "mia2.db")
    assert os.path.exists(database_folder) == True

# Second test
def test_database_creation_new_project():
    ""
    Tests the creation of the database file at new project
    ""
    entire_path = os.path.relpath(os.path.join("..", "..", "..", "..", "test"))
    path, name = os.path.split(entire_path)
    relative_subpath = os.path.relpath(path)
    controller.createProject(name, relative_subpath, relative_subpath)
    database = Database(entire_path, True)
    database_folder = os.path.join(entire_path, "database", "mia2.db")
    assert os.path.exists(database_folder) == True

total_tests = 0
failed_tests = []

# First test
try:
    total_tests += 1
    test_database_creation_software_opening()
except Exception as e:
    traceback.print_exc()
    failed_tests.append("database_creation_software_opening")

# Second test
try:
    total_tests += 1
    test_database_creation_new_project()
except Exception as e:
    traceback.print_exc()
    failed_tests.append("database_creation_new_project")

# Printing if failed tests
if len(failed_tests) > 0:
    errorMessage = "Some tests failed.\n"
    errorMessage += str(len(failed_tests)) + "/" + str(total_tests)  + " tests failed.\n"
    errorMessage += "Here is a list of the tests that failed:\n"
    for failed in failed_tests:
        errorMessage += "\t" + failed + "\n"
    raise Exception(errorMessage)
"""