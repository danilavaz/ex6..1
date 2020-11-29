# אם אתה רואה את זה זאת הגרסה הנכונה

import wave_helper
import math
from typing import *

MAX_VOL = 32767
MIN_VOL = -32768

DEFAULT_SAMPLE_RATE = 2000

OPTION_REVERSE = '1'
OPTION_NAGATE = '2'
OPTION_ACC = '3'
OPTION_DEC = '4'
OPTION_VOL_INC = '5'
OPTION_VOL_DEC ='6'
OPTION_LOW_PASS = '7'
OPTION_END_MENU = '8'

SPEED_MULTIPLY = 1.2

USER_MENU = 'Select one of the options:\n' \
            '1 Reverse the audio\n' \
            '2 Negate the audio\n' \
            '3 Speed acceleration\n' \
            '4 Speed deceleration\n' \
            '5 Increase the volume\n' \
            '6 Decrease the volume \n' \
            '7 Low pass filter\n' \
            '8 Go to the end menu\n'

NOTES = {'A' : 440, 'B': 494, 'C': 523, 'D': 587, 'E': 659, 'F': 698, 'G': 784, 'Q': 0}


def create_melody():
    pass


def get_samples_list_for_note(frequency, time): # note is a list with ["A",254]


    # time is in 1/16 of a second units. 1 second = 2000 samples
    num_of_samples = int(time/16 * DEFAULT_SAMPLE_RATE)

    sample_list = []
    samples_per_cycle = DEFAULT_SAMPLE_RATE / frequency
    for i in range(num_of_samples):
        sample_value = int(MAX_VOL* math.sin(math.pi*2*(i/samples_per_cycle)))
        if sample_value > MAX_VOL:
            sample_value = MAX_VOL
        if sample_value < MIN_VOL:
            sample_value = MIN_VOL
        sample_list.append([sample_value]*2)

    return sample_list


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
    if input_user == '3':
        return


def melody_flow():

    filename = input("enter the melody file name")

    with open(filename) as melody_file:
        data = melody_file.read().replace(" ","").replace("\n","")

    input_notes = convert_file_to_list(data) # turns the file data to a list of notes and times
    audio_data = create_audio_data(input_notes) # creates a list of audio_data from a list of notes

    return audio_data


def create_audio_data(notes):
    audio_data = []
    for note in notes:
        note_letter = note[0]
        frequency = NOTES[note_letter]
        time = note[1]
        audio_data += get_samples_list_for_note(frequency, time)

    return audio_data


def convert_file_to_list(data):
    notes = []
    note = ""
    time = ""
    for index, char in enumerate(data):
        if char in NOTES:
            if note != "":
                notes.append([note, int(time)])
            note = char
            time = ""
        else:
            time += char

        if index == len(data) - 1:
            notes.append([note, int(time)])
    return notes


def action_flow(audio_data = None):
    sample_rate = DEFAULT_SAMPLE_RATE
    if audio_data == None:
        filename = input('enter file name')
        test_file = wave_helper.load_wave(filename)
        while test_file == -1:
            filename = input('The file is invalid enter file name')
            test_file = wave_helper.load_wave(filename)
        sample_rate, audio_data = wave_helper.load_wave(filename)
    action_chosen = 0
    while action_chosen != OPTION_END_MENU:
        action_chosen = input(USER_MENU)
        if action_chosen == OPTION_REVERSE:
            audio_data = reverse_audio(audio_data)
        if action_chosen == OPTION_NAGATE:
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
    while output_filename == -1:
        output_filename = input("How would you like to name the new file?")
    wave_helper.save_wave(sample_rate, audio_data, output_filename)
    main()


def reverse_audio(audio_data):
    return list(reversed(audio_data))

def negate_the_audio(audio_data):
    for i in range(len(audio_data)):
        for j in range(2):
            if audio_data[i][j] != -32768:
                audio_data[i][j] = audio_data[i][j] * -1
            else:
                audio_data[i][j] = 32767
    return audio_data

def speed_acceleration(audio_data):
    return audio_data[::2]


def speed_deceleration(audio_data):
    result = [audio_data[0]]
    for i in range(1, len(audio_data)):
        pair = []
        pair.append(int((audio_data[i][0] + audio_data[i - 1][0]) / 2))
        pair.append(int((audio_data[i][1] + audio_data[i - 1][1]) / 2))
        result.append(pair)
        result.append(audio_data[i])
    return result

def increase_the_volume(audio_data):
    for i in range(len(audio_data)):
        for j in range(2):
            if audio_data[i][j] * SPEED_MULTIPLY <= MAX_VOL and audio_data[i][j] * SPEED_MULTIPLY >= MIN_VOL:
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
            pair = []
            if i == 0 or i == len(audio_data) - 1:
                pair_index = 1  # will be 1 if i==0 and -1 if i==len(audio_data)-1
                if i > 0:
                    pair_index = -1
                pair.append(int((audio_data[i][0] + audio_data[i + pair_index][0]) / 2))
                pair.append(int((audio_data[i][1] + audio_data[i + pair_index][1]) / 2))
            else:
                pair.append(int((audio_data[i][0] + audio_data[i + 1][0] + audio_data[i - 1][0]) / 3))
                pair.append(int((audio_data[i][1] + audio_data[i + 1][1] + audio_data[i - 1][1]) / 3))
            new_list.append(pair)
        return new_list








if __name__ == '__main__':
    main()
