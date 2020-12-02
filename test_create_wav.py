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


def test_creation_sample_1():
    file_name = "create_sample1"

    run_program_with_instructions(file_name, PATH)
    try:
        f = open(PATH + file_name + '.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data_og = wave_helper.load_wave(SAMPLE_PATH + '1.wav')
    rate, audio_data_new = wave_helper.load_wave(PATH + file_name + '.wav')

    assert audio_data_og == audio_data_new

def test_creation_sample_2():
    file_name = "create_sample2"

    run_program_with_instructions(file_name, PATH)
    try:
        f = open(PATH + file_name + '.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data_og = wave_helper.load_wave(SAMPLE_PATH + '2.wav')
    rate, audio_data_new = wave_helper.load_wave(PATH + file_name + '.wav')

    assert audio_data_og == audio_data_new

def test_create_quiet():
    file_name = "create_sample3"

    run_program_with_instructions(file_name, PATH)
    try:
        f = open(PATH + file_name + '.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data_og = wave_helper.load_wave(SAMPLE_PATH + '3.wav')
    rate, audio_data_new = wave_helper.load_wave(PATH + file_name + '.wav')

    assert audio_data_og == audio_data_new
