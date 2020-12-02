import subprocess
import pytest
import wave_helper
import time
from test_main import INTEREPETER_PATH, PATH, SAMPLE_PATH


def run_program_with_instructions(file_name, path):
    print("Running for " + file_name)
    input_file = open(path + file_name + '.txt')
    output_file = open(path + 'output.txt', "w")

    child = subprocess.Popen(
        [INTEREPETER_PATH, "wave_editor.py"],
        stdin=input_file, stdout=output_file)
    output, error = child.communicate()
    return_code = child.returncode

    input_file.close()
    output_file.close()
    time.sleep(0.5)
    return return_code


def test_slow_speed():
    # Takes a sample, slows it down and speeds it up repeatedly
    # Expects the output to be the input again
    file_name = "integrated_slow_speed"

    file_name_1 = file_name + '1'
    run_program_with_instructions(file_name_1, PATH)
    try:
        f = open(PATH + file_name_1 + '.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data_og = wave_helper.load_wave(SAMPLE_PATH + '1.wav')
    rate, audio_data_new = wave_helper.load_wave(PATH + file_name_1 + '.wav')

    assert audio_data_og == audio_data_new

    file_name_2 = file_name + '2'
    run_program_with_instructions(file_name_2, PATH)
    try:
        f = open(PATH + file_name_2 + '.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data_og = wave_helper.load_wave(SAMPLE_PATH + '2.wav')
    rate, audio_data_new = wave_helper.load_wave(PATH + file_name_2 + '.wav')

    assert audio_data_og == audio_data_new


def test_negative_reverse():
    # Takes a sample, makes it negative then reverses it repeatedly
    # Expects the output to be the input again
    file_name = "integrated_negative_reverse"

    file_name_1 = file_name + '1'
    run_program_with_instructions(file_name_1, PATH)
    try:
        f = open(PATH + file_name_1 + '.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data_og = wave_helper.load_wave(SAMPLE_PATH + '1.wav')
    rate, audio_data_new = wave_helper.load_wave(PATH + file_name_1 + '.wav')

    assert audio_data_og == audio_data_new

    file_name_2 = file_name + '2'
    run_program_with_instructions(file_name_2, PATH)
    try:
        f = open(PATH + file_name_2 + '.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data_og = wave_helper.load_wave(SAMPLE_PATH + '2.wav')
    rate, audio_data_new = wave_helper.load_wave(PATH + file_name_2 + '.wav')

    assert audio_data_og == audio_data_new


def test_create_and_edit():
    # Create a file then slow it down and speed it up
    # Expects the output to be the input again
    file_name = "create_and_edit"

    run_program_with_instructions(file_name, PATH)
    try:
        f = open(PATH + file_name + '.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data_og = wave_helper.load_wave(SAMPLE_PATH + '2.wav')
    rate, audio_data_new = wave_helper.load_wave(PATH + file_name + '.wav')

    assert audio_data_og == audio_data_new


def test_wrong_wav_name():
    # Inserts a non-existent wav file to edit, expects you to keep prompting
    # for it until a valid one is inserted
    file_name = "edit_wrong_wav_name"

    return_code = run_program_with_instructions(file_name, PATH)
    if return_code == 1:
        pytest.fail("You did not handle a bad wav file given by the user")
    try:
        f = open(PATH + file_name + '.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")


def test_wrong_instructions_name():
    # Inserts a non-existent instructions file to edit, expects you to keep prompting
    # for it until a valid one is inserted
    file_name = "create_wrong_instructions_name"

    return_code = run_program_with_instructions(file_name, PATH)
    if return_code == 1:
        pytest.fail(
            "You did not handle a bad instructions file given by the user")
    try:
        f = open(PATH + file_name + '.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")

def test_wrong_main_menu_options():
    # Inserts unvalid options to main menu
    file_name = "wrong_main_menu_options"

    return_code = run_program_with_instructions(file_name, PATH)
    if return_code == 1:
        pytest.fail(
            "You did not handle unvalid inputs for main menu")
    try:
        f = open(PATH + file_name + '.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")

def test_wrong_edit_menu_options():
    # Inserts unvalid options to edit menu
    file_name = "wrong_edit_menu_options"

    return_code = run_program_with_instructions(file_name, PATH)
    if return_code == 1:
        pytest.fail(
            "You did not handle unvalid inputs for edit menu")
    try:
        f = open(PATH + file_name + '.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")


def test_create_empty_test():
    # tests an empty instructions file
    file_name = "create_empty_test"

    return_code = run_program_with_instructions(file_name, PATH)
    if return_code == 1:
        pytest.fail(
            "You did not handle a bad instructions file given by the user")
    try:
        f = open(PATH + file_name + '.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")





def test_filename_remains():
    # Checks if the user's filename remains the same when saved
    # otherwise pre-submit might throw you an error
    file_name = "filename_remains"

    return_code = run_program_with_instructions(file_name, PATH)
    try:
        f = open(PATH + file_name)
    except FileNotFoundError:
        pytest.fail("Fails for given file name without .wav extension")



#
# def test_EOFE():
#     # Inserts a non-existent instructions file to edit, expects you to keep prompting
#     # for it until a valid one is inserted
#     file_name = "integrated_EOFE"
#
#     return_code = run_program_with_instructions(file_name, PATH)
#     if return_code == 1:
#         pytest.fail("You did not handle a EOFE case when loading a file")
