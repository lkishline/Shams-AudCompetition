# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 13:35:10 2015

@author: lindsey
"""
import numpy as np
from scipy import io as sio
import scipy.signal as signal
from expyfun import stimuli
import matplotlib.pyplot as plt

fs = 24414.             # Sampling rate - how many samples per second
dur = 1.0               # duration of stimulus

tone = np.sin(2 * np.pi * 100 * np.arange(int(fs * dur)) / float(fs))
    # a tone at a 100 Hz - just think how often a multiple of 2pi arrives
tone *= 0.01 * np.sqrt(2)  # Set RMS to 0.01

ramp = 0.006

sig = stimuli._stimuli.window_edges(tone, fs, ramp)

# plt.plot(sig)

### Tone complex ###

tonecomp = np.zeros(24414, float)
fund = 250.0 # fundamental frequency
for x in xrange(1, 5):
    freq = fund*x
    tonecomp = tonecomp + np.sin(freq * 2 * np.pi * np.arange(int(fs * dur)) / float(fs))

tonecomp_ramped = stimuli._stimuli.window_edges(tonecomp, fs, ramp, -1, 'hamming')

plt.plot(tonecomp_ramped)

