import wave_helper
import math
from typing import *

MAX_VOL = 32767
MIN_VOL = -32768

DEFAULT_SAMPLE_RATE = 2000

OPTION_REVERSE = '1'
OPTION_NEGATE = '2'
OPTION_ACC = '3'
OPTION_DEC = '4'
OPTION_VOL_INC = '5'
OPTION_VOL_DEC = '6'
OPTION_LOW_PASS = '7'
OPTION_END = '8'

OPTION_CHANGE = "1"
OPTION_MELODY = "2"
OPTION_EXIT = "3"

SPEED_MULTIPLY = 1.2

TIME_UNITS = 1/16

USER_MENU = f'Select one of the options:\n' \
            f'{OPTION_REVERSE} Reverse the audio\n' \
            f'{OPTION_NEGATE} Negate the audio\n' \
            f'{OPTION_ACC} Speed acceleration\n' \
            f'{OPTION_DEC} Speed deceleration\n' \
            f'{OPTION_VOL_INC} Increase the volume\n' \
            f'{OPTION_VOL_DEC} Decrease the volume \n' \
            f'{OPTION_LOW_PASS} Low pass filter\n' \
            f'{OPTION_END} Go to the end menu\n'

NOTES = {'A' : 440, 'B' : 494, 'C' : 523, 'D' : 587, 'E' : 659, 'F' : 698, 'G' : 784, 'Q' : 0}


def get_samples_list_for_note(frequency : int, time : int) -> List[[int, int]]:

    num_of_samples = int(time * TIME_UNITS * DEFAULT_SAMPLE_RATE)

    sample_list = []
    samples_per_cycle = DEFAULT_SAMPLE_RATE / frequency
    for i in range(num_of_samples):
        sample_value = get_sample_value(i, samples_per_cycle)
        if sample_value > MAX_VOL:
            sample_value = MAX_VOL
        elif sample_value < MIN_VOL:
            sample_value = MIN_VOL
        sample_list.append([sample_value]*2)

    return sample_list


def get_sample_value(i: int, samples_per_cycle: float) -> int:
    """

    :param i:
    :param samples_per_cycle:
    :return:
    """
    return int(MAX_VOL* math.sin(math.pi*2*(i/samples_per_cycle)))


def melody_flow():
    """
    The set of methods to be run once the user decides to create a new melody
    :return: the audio data of the melody for further actions
    """
    filename = input("enter the melody file name")

    with open(filename) as melody_file:
        data = melody_file.read().replace(" ","").replace("\n","")

    audio_data = create_audio_data(data)
    return audio_data


def create_audio_data(data):
    """
    Receives a melody's data and converts it to a list of sound samples to be
    converted to a wav file
    :param data: the melody's data from the input file
    :return: returns a list of sound samples to be converted to a wav file
    """
    notes = convert_file_to_list(data)
    audio_data = []
    for note in notes:
        note_letter = note[0]
        frequency = NOTES[note_letter]
        time = note[1]
        audio_data += get_samples_list_for_note(frequency, time)

    return audio_data


def convert_file_to_list(data):
    """
    Receives a string containing all the data of a melody and creates a list
    of notes and durations for further calculations
    :param data: the string with the melody file data
    :return: a list of notes (as letters) and durations
    """
    notes = []
    note = ""
    time = ""
    for index, char in enumerate(data):

        if char in NOTES:

            if note != "":
                # if the note we've reached isn't the first note then we need
                # to add the previous note and duration to the list
                notes.append([note, int(time)])

            note = char
            time = ""
        else:
            time += char

        # if this is the last characters then the objects note and time hold
        # the data of the last note in the melody and they need to be added to
        # the list
        if index == len(data) - 1:
            notes.append([note, int(time)])
    return notes


def action_flow(audio_data = None):
    sample_rate = DEFAULT_SAMPLE_RATE
    if audio_data is None:
        filename = input('enter file name')
        test_file = wave_helper.load_wave(filename)
        while test_file == -1:
            filename = input('The file is invalid enter file name')
            test_file = wave_helper.load_wave(filename)
        sample_rate, audio_data = wave_helper.load_wave(filename)

    action_chosen = 0
    while action_chosen != OPTION_END:
        action_chosen = input(USER_MENU)
        if action_chosen == OPTION_REVERSE:
            audio_data = reverse_audio(audio_data)
        if action_chosen == OPTION_NEGATE:
            audio_data = negate_the_audio(audio_data)
        if action_chosen == OPTION_ACC:
            audio_data = speed_acceleration(audio_data)
        if action_chosen == OPTION_DEC:
            audio_data = speed_deceleration(audio_data)
        if action_chosen == OPTION_VOL_INC:
            audio_data = increase_the_volume(audio_data)
        if action_chosen == OPTION_VOL_DEC:
            audio_data = decrease_the_volume(audio_data)
        if action_chosen == OPTION_LOW_PASS:
            audio_data = low_pass_filter(audio_data)

    output_filename = input("How would you like to name the new file?")
    wave_helper.save_wave(sample_rate, audio_data, output_filename)


def reverse_audio(audio_data):
    return list(reversed(audio_data))


def negate_the_audio(audio_data):
    for i in range(len(audio_data)):
        for j in range(2):
            if audio_data[i][j] != MIN_VOL:
                audio_data[i][j] = audio_data[i][j] * -1
            else:
                audio_data[i][j] = MAX_VOL
    return audio_data


def speed_acceleration(audio_data):
    return audio_data[::2]


def speed_deceleration(audio_data):
    result = [audio_data[0]]
    for i in range(1, len(audio_data)):
        avg1 = int((audio_data[i][0] + audio_data[i - 1][0]) / 2)
        avg2 = int((audio_data[i][1] + audio_data[i - 1][1]) / 2)
        result.append([avg1, avg2])
        result.append(audio_data[i])
    return result


def increase_the_volume(audio_data):
    for i in range(len(audio_data)):
        for j in range(2):
            if MAX_VOL >= audio_data[i][j] * SPEED_MULTIPLY >= MIN_VOL:
                audio_data[i][j] = int(audio_data[i][j] * SPEED_MULTIPLY)
            elif audio_data[i][j] * SPEED_MULTIPLY > MAX_VOL:
                audio_data[i][j] = MAX_VOL
            else:
                audio_data[i][j] = MIN_VOL
    return audio_data


def decrease_the_volume(audio_data):
    for i in range(len(audio_data)):
        for j in range(2):
            audio_data[i][j] = int(audio_data[i][j] / SPEED_MULTIPLY)
    return audio_data


def low_pass_filter(audio_data: List[List[int]]) -> List[List[int]]:
    new_list = []
    for i in range(len(audio_data)):
        count = 1
        sum1 = audio_data[i][0]
        sum2 = audio_data[i][1]

        if i < len(audio_data)-1:
            sum1 += audio_data[i+1][0]
            sum2 += audio_data[i+1][1]
            count += 1

        if i>0:
            sum1 += audio_data[i-1][0]
            sum1 += audio_data[i-1][1]
            count += 1

        pair = [int(sum1/count), int(sum2/count)]
        new_list.append(pair)
    return new_list


def main():
    input_user = input('Select one of the three options:\n'
                       '1 to change the file\n'
                       '2 to compose a melody\n'
                       '3 to finish\n')
    if input_user == '1':
        action_flow()
    if input_user == '2':
        audio_data = melody_flow()
        action_flow(audio_data)

def print_helper(str, ind):
    print(str[ind])
    if(ind < len(str)-1):
        print_helper(str, ind+1)

def print_vertically(str):
    print_helper(str, 0)

if __name__ == '__main__':
    print_vertically("HELLO")