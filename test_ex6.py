from wave_editor import *
import math
from wave_helper import load_wave

def test_create_melody():
    origin = load_wave("sample1.wav")
    ours = melody_flow("sample1.txt")
    if len(origin[1]) == len(ours):
        print("length equal")
    for i in range(len(origin[1])):
        print("hi")
        assert origin[1][i] == ours[i]