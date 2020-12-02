import subprocess
import pytest
import wave_helper
import time
from test_main import INTEREPETER_PATH, PATH


def run_program_with__hard_coded_audio_data(file_name, path, original):
    print("Running for " + file_name)
    wave_helper.save_wave(2000, original, path + file_name + '.wav')
    input_file = open(path + file_name + '.txt')
    output_file = open(path + 'output.txt', "w")

    subprocess.Popen(
        [INTEREPETER_PATH, "wave_editor.py"],
        stdin=input_file, stdout=output_file)
    input_file.close()
    output_file.close()
    time.sleep(0.5)


def test_reverse_wav():
    # Tests the reverse option (1)
    file_name = "edit_reverse_test"

    original = [[5, 1], [4, 2]]
    result = [[4, 2], [5, 1]]
    run_program_with__hard_coded_audio_data(file_name, PATH, original)
    try:
        f = open(PATH + file_name + '_done.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data = wave_helper.load_wave(PATH + file_name + '_done.wav')

    assert audio_data == result


def test_negative_wav():
    # Tests the negative option (2)
    file_name = "edit_negative_test"

    original = [[3500, 5000], [-2000, -700]]
    result = [[-3500, -5000], [2000, 700]]
    run_program_with__hard_coded_audio_data(file_name, PATH, original)
    try:
        f = open(PATH + file_name + '_done.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data = wave_helper.load_wave(PATH + file_name + '_done.wav')

    assert audio_data == result

    original = [[3500, -5000], [-2000, 700]]
    result = [[-3500, 5000], [2000, -700]]
    run_program_with__hard_coded_audio_data(file_name, PATH, original)
    try:
        f = open(PATH + file_name + '_done.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data = wave_helper.load_wave(PATH + file_name + '_done.wav')

    assert audio_data == result

    original = [[-3500, 5000], [2000, -700]]
    result = [[3500, -5000], [-2000, 700]]
    run_program_with__hard_coded_audio_data(file_name, PATH, original)
    try:
        f = open(PATH + file_name + '_done.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data = wave_helper.load_wave(PATH + file_name + '_done.wav')

    assert audio_data == result


def test_speed_up():
    # Tests the speed up option (3)
    file_name = "edit_speed_up_test"

    original = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]
    result = [[1, 1], [3, 3], [5, 5]]
    run_program_with__hard_coded_audio_data(file_name, PATH, original)
    try:
        f = open(PATH + file_name + '_done.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data = wave_helper.load_wave(PATH + file_name + '_done.wav')

    assert audio_data == result


def test_slow_down():
    # Tests the slow down option (4)
    file_name = "edit_slow_down_test"

    original = [[10, 10], [20, 30], [30, 50], [40, 60]]
    result = [[10, 10], [15, 20], [20, 30], [25, 40], [30, 50], [35, 55],
              [40, 60]]

    run_program_with__hard_coded_audio_data(file_name, PATH, original)
    try:
        f = open(PATH + file_name + '_done.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data = wave_helper.load_wave(PATH + file_name + '_done.wav')

    assert audio_data == result

    original = [[100, 200], [300, 400], [50, 90], [150, 1000]]
    result = [[100, 200], [200, 300], [300, 400], [175, 245], [50, 90],
              [100, 545], [150, 1000]]
    run_program_with__hard_coded_audio_data(file_name, PATH, original)
    try:
        f = open(PATH + file_name + '_done.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data = wave_helper.load_wave(PATH + file_name + '_done.wav')

    assert audio_data == result


def test_increase_volume_wav():
    # Tests the volume increase option (5)
    file_name = "edit_volume_up_test"

    original = [[-32760, -100], [-55, -55], [0, 0], [4, -2017],
                [32767, 10002]]
    result = [[-32768, -120], [-66, -66], [0, 0], [4, -2420], [32767, 12002]]
    run_program_with__hard_coded_audio_data(file_name, PATH, original)
    try:
        f = open(PATH + file_name + '_done.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved under")
    rate, audio_data = wave_helper.load_wave(PATH + file_name + '_done.wav')

    assert audio_data == result


def test_decrease_volume_wav1():
    # Tests the volume decrease option (6)
    file_name = "edit_volume_down_test"

    original = [[-32760, -100], [-55, -55], [0, 0], [4, -2017],
                [32767, 10002]]
    result = [[-27300, -83], [-45, -45], [0, 0], [3, -1680], [27305, 8335]]
    run_program_with__hard_coded_audio_data(file_name, PATH, original)
    try:
        f = open(PATH + file_name + '_done.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data = wave_helper.load_wave(PATH + file_name + '_done.wav')
    assert audio_data == result


def test_dim_wav():
    # Tests the dim \ low pass filter option (7)
    file_name = "edit_dim_test"

    original = [[1, 1], [7, 7], [20, 20], [9, 9], [-12, -12]]
    result = [[4, 4], [9, 9], [12, 12], [5, 5], [-1, -1]]
    run_program_with__hard_coded_audio_data(file_name, PATH, original)
    try:
        print("file is: ",PATH + file_name + '_done.wav')
        f = open(PATH + file_name + '_done.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data = wave_helper.load_wave(PATH + file_name + '_done.wav')

    assert audio_data == result

def test_empty_wav():
    # Tests an empty wav file
    file_name = "edit_empty_test"

    original = []
    result = []
    run_program_with__hard_coded_audio_data(file_name, PATH, original)
    try:
        f = open(PATH + file_name + '_done.wav')
    except FileNotFoundError:
        pytest.fail("No wav file was saved")
    rate, audio_data = wave_helper.load_wave(PATH + file_name + '_done.wav')

    assert audio_data == result


# def test_validate_audio_data():
#     assert validate_audio_data([[50000, 10], [20, 30], [50, 80000], [40, 60]]) \
#            == [[32767, 10], [20, 30], [50, 32767], [40, 60]]
#     assert validate_audio_data(
#         [[-50000, 10], [20, 30], [50, -80000], [40, 60]]) \
#            == [[-32768, 10], [20, 30], [50, -32768], [40, 60]]
#     assert validate_audio_data(
#         [[50000, 10], [20, 30], [50, -80000], [40, 60]]) \
#            == [[32767, 10], [20, 30], [50, -32768], [40, 60]]
