import wave_helper
from typing import *
OPTION_REVERSE = '1'
OPTION_NAGATE = '2'
OPTION_ACC = '3'
OPTION_DEC = '4'
OPTION_VOL_INC = '5'
OPTION_VOL_DEC ='6'
OPTION_LOW_PASS = '7'
OPTION_END_MENU = '8'
USER_MENU = 'Select one of the options:\n' \
            '1 Reverse the audio\n' \
            '2 Negate the audio\n' \
            '3 Speed acceleration\n' \
            '4 Speed deceleration\n' \
            '5 Increase the volume\n' \
            '6 Decrease the volume \n' \
            '7 Low pass filter\n' \
            '8 Go to the end menu'


def main():
    input_user = input('Select one of the three options:\n'
                       '1 to change the file\n'
                       '2 to compose a melody\n'
                       '3 to finish')
    if input_user == '1':
        action_flow()

def action_flow():
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
    wave_helper.save_wave(sample_rate, audio_data, filename)


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
            if audio_data[i][j] * 1.2 <= 32767 and audio_data[i][j] * 1.2 >= -32768:
                audio_data[i][j] = int(audio_data[i][j] * 1.2)
            elif audio_data[i][j] * 1.2 > 32767:
                audio_data[i][j] = 32767
            else:
                audio_data[i][j] = -32768
    return audio_data

def decrease_the_volume(audio_data):
    for i in range(len(audio_data)):
        for j in range(2):
            audio_data[i][j] = int(audio_data[i][j] / 1.2)
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
    print(negate_the_audio([[1,2], [2,3], [3,4], [4,5]]))