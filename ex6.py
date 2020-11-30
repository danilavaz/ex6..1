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

VOL_MULTIPLY = 1.2

TIME_UNITS = 1/16

MAIN_MENU = f'Select one of the three options:\n' \
            f'{OPTION_CHANGE} to change the file\n' \
            f'{OPTION_MELODY} 2 to compose a melody\n' \
            f'{OPTION_EXIT} 3 to finish\n'

USER_MENU = f'Select one of the options:\n' \
            f'{OPTION_REVERSE} Reverse the audio\n' \
            f'{OPTION_NEGATE} Negate the audio\n' \
            f'{OPTION_ACC} Speed acceleration\n' \
            f'{OPTION_DEC} Speed deceleration\n' \
            f'{OPTION_VOL_INC} Increase the volume\n' \
            f'{OPTION_VOL_DEC} Decrease the volume \n' \
            f'{OPTION_LOW_PASS} Low pass filter\n' \
            f'{OPTION_END} Go to the end menu\n'

Sample = List[int]
AudioList = List[Sample]

# Dictionary with keys as representing musical notes and values representing
# the same note's frequency
NOTES = {'A' : 440, 'B' : 494, 'C' : 523, 'D' : 587, 'E' : 659, 'F' : 698, 'G' : 784, 'Q' : 0}


def get_samples_list_for_note(frequency : int, time : int) -> AudioList:
    """
    Creates a list of samples for a certain note given its frequency and
    duration
    :param frequency: the frequency of the note we are sampling
    :param time: the duration of the note
    :return: a list of samples built according to the given note and its
    duration
    """
    num_of_samples = int(time * TIME_UNITS * DEFAULT_SAMPLE_RATE)

    sample_list = []
    samples_per_cycle = DEFAULT_SAMPLE_RATE / frequency
    for i in range(num_of_samples):
        sample_value = get_sample_value(i, samples_per_cycle)
        handle_volume_bounds(sample_value)
        sample_list.append([sample_value]*2)

    return sample_list


def get_sample_value(i: int, samples_per_cycle: float) -> int:
    """
    calculates the sample value for a certain sampling position
    :param i: the no. of the sample we are calculating
    :param samples_per_cycle: the amount of samples per cycle
    :return: the value of the sample according to the equation
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


def create_audio_data(data: str) -> AudioList:
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


def convert_file_to_list(data: str) -> List[List[Union[str, int]]]:
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


def handle_action_choices(audio_data: AudioList):
    """
    handles the choices of the user and changes the audio file accordingly
    :param audio_data: the audio data before committed changes
    :return: the audio data after all the changes that have been done
    """
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

    return audio_data


def action_flow(audio_data: Optional[AudioList] = None) \
        -> Tuple[int, AudioList]:
    """
    The flow that is presented if the user decides to change a file
    :param audio_data: the audio data created if we have entered this flow
    after the melody flow
    :return: returns the sample rate and audio data of the audio file so it
    can be saved in the end flow
    """
    sample_rate = DEFAULT_SAMPLE_RATE
    if audio_data is None:
        filename = input('enter file name')
        test_file = wave_helper.load_wave(filename)
        while test_file == -1:
            filename = input('The file is invalid enter a new file name')
            test_file = wave_helper.load_wave(filename)
        sample_rate, audio_data = wave_helper.load_wave(filename)

    audio_data = handle_action_choices(audio_data)

    return sample_rate, audio_data


def save_audio(sample_rate: int = DEFAULT_SAMPLE_RATE,
               audio_data: AudioList = None):
    """
    saves the audio data after the user decides to end the manipulations
    :param sample_rate: the sample rate of the file to be saved
    :param audio_data: the audio data to be saved
    """
    if audio_data:
        output_filename = input("How would you like to name the new file?")
        while wave_helper.save_wave(sample_rate, audio_data, output_filename) \
                == -1:
            output_filename = input("Something went wrong, please enter a "
                                    "new filename")


def reverse_audio(audio_data: AudioList) -> AudioList:
    """
    returns a list representing a reversed audio part
    :param audio_data: the audio to be reversed
    :return: a reversed list of the audio data
    """
    return list(reversed(audio_data))


def negate_the_audio(audio_data: AudioList) -> AudioList:
    """
    negates the samples in the audio data
    :param audio_data: the audio data to be negated
    :return: a list of the negated audio data
    """
    for i in range(len(audio_data)):
        for j in range(2):
            audio_data[i][j] *= -1
            handle_volume_bounds(audio_data[i][j])
    return audio_data


def speed_acceleration(audio_data: AudioList) -> AudioList:
    """
    "accelerates" an audio part by removing half of its samples
    :param audio_data: the audio data to be accelerated
    :return: the accelerated audio data
    """
    return audio_data[::2]


def speed_deceleration(audio_data: AudioList) -> AudioList:
    """
    "decelerates" an audio part by adding more samples
    :param audio_data: the audio data to be decelerated
    :return: the decelerated audio data
    """
    result = [audio_data[0]]
    for i in range(1, len(audio_data)):
        avg1 = int((audio_data[i][0] + audio_data[i - 1][0]) / 2)
        avg2 = int((audio_data[i][1] + audio_data[i - 1][1]) / 2)
        result.append([avg1, avg2])
        result.append(audio_data[i])
    return result


def handle_volume_bounds(sample):
    """
    handles cases in which we've created an audio sample that exceeds the
    volume bounds
    :param sample: the sample that is being checked
    """
    if sample > MAX_VOL:
        sample = MAX_VOL
    elif sample < MIN_VOL:
        sample = MIN_VOL


def increase_the_volume(audio_data: AudioList) -> AudioList:
    """
    increases audio data volume by multiplying its samples by a constant
    :param audio_data: the audio data to be increased
    :return: the audio data with increased volume
    """
    for i in range(len(audio_data)):
        for j in range(2):
            audio_data[i][j] = int(audio_data[i][j] * VOL_MULTIPLY)
            handle_volume_bounds(audio_data[i][j])

    return audio_data


def decrease_the_volume(audio_data: AudioList) -> AudioList:
    """
    decreases audio data volume by dividing its samples by a constant
    :param audio_data: the audio data to be increased
    :return: the audio data with increased volume
    """
    for i in range(len(audio_data)):
        for j in range(2):
            audio_data[i][j] = int(audio_data[i][j] / VOL_MULTIPLY)
    return audio_data


def low_pass_filter(audio_data: AudioList) -> AudioList:
    """
    applies a low pass filter on the audio data by changing its samples to
    average values
    :param audio_data: the audio data to change
    :return: audio data after applying the filter
    """
    new_list = []
    for i in range(len(audio_data)):
        count = 1
        sum1 = audio_data[i][0]
        sum2 = audio_data[i][1]

        if i < len(audio_data)-1:
            sum1 += audio_data[i+1][0]
            sum2 += audio_data[i+1][1]
            count += 1

        if i > 0:
            sum1 += audio_data[i-1][0]
            sum1 += audio_data[i-1][1]
            count += 1

        pair = [int(sum1/count), int(sum2/count)]
        new_list.append(pair)
    return new_list


def main():
    """
    the main function. will execute variuose flows according to the user's
    input
    """
    input_user = 0
    while True:
        input_user = input(MAIN_MENU)
        sample_rate = DEFAULT_SAMPLE_RATE
        audio_data = None

        if input_user == OPTION_EXIT:
            break

        if input_user == OPTION_CHANGE:
            sample_rate, audio_data = action_flow()
        if input_user == OPTION_MELODY:
            audio_data = melody_flow()
            sample_rate, audio_data = action_flow(audio_data)
        save_audio(sample_rate, audio_data)



if __name__ == '__main__':
    main()