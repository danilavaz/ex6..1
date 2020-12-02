import pytest

# NOTE!
# This tests were written by a fellow student.
# They might have bugs
# They are 100% not covering every thing the official tests check
# They might test functionality which is different from what's instructed
# USE THEM AT YOUR OWN RISK AND JUDGMENT
# Best of luck <3


# Instructions:
# 1. Extract the content of the folder to your root directory
#     so the tests and the test_files folder are at the same level with
#     the wave_editor.py file
# 2. Change the INTEREPETER_PATH to your python.exe interpeter path
# 3. Install pytest (pip install pytest)
# 4. In the command line (terminal tab on pycharm) run "pytest -s"
#     Make sure you do so from the root directory
# 5. Pass all tests!

# Troubleshooting:
# 1. There are 4 test files:
#     test_main - checks for vital files and holds this configs
#     test_change_wav - tests the edit wav file functionality
#     test_create_wav - tests the create wav file functionality
#     test_integration - tests a sequence of actions, also bad user inputs
# 2. If a test has failed, go to the test file and read the test description
#     in the test function
# 3. For further investigation, go to the test_files folder and read the .txt
#     file with the same name as the file_name in the test
#     this file contains the input the user is inserting
# 4. You can also look at the output.txt, but bare in mind it only holds the
#      last test that was run

INTEREPETER_PATH = "C:\\Program Files\\winpy2\\WPy64-3771\\python-3.7.7.amd64\\python.exe"
PATH = 'C:\\Users\\Alon\\PycharmProjects\\ex6..1\\test_files\\'
SAMPLE_PATH = PATH + 'samples\\sample'


def test_check_exists_description():
    try:
        f = open("description.txt")
    except FileNotFoundError:
        pytest.fail("No description file")


def test_check_exists_wave_editor():
    try:
        f = open("wave_editor.py")
    except FileNotFoundError:
        pytest.fail("No wave_editor file")


def test_check_exists_authors():
    try:
        f = open("AUTHORS")
    except FileNotFoundError:
        pytest.fail("No AUTHORS file")
