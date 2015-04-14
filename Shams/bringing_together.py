# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 11:38:16 2015

@author: lindsey
"""

import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
from expyfun import stimuli

fs = 24414.
dur = 1.0

### Tone complex ###
tonecomp = np.zeros(24414, float)
fund = 250.0                                # fundamental frequency
for x in xrange(1, 5):
    freq = fund*x
    tonecomp = tonecomp + np.sin(freq * 2 * np.pi * np.arange(int(fs * dur)) / float(fs))

### Making white noise ###
nb = np.random.normal(0, 1.0, int(fs * 1.0))

### highpass cut-off freq of 1500Hz using 100th order Hamming ###
b = sig.firwin(101, 1500. / (fs / 2), pass_zero=False)  # False for highpass
                                                        # nyq_rate = fs / 2
filtered_stim = sig.lfilter(b, 1.0, nb)
#plt.plot(filtered_stim)

### windowing - onset and offset ramps ###
toneramp = 0.006
noiseramp = 0.003

nb_ramped = stimuli._stimuli.window_edges(nb, fs, noiseramp, -1, 'hamming')

finalstim_nb = np.multiply(nb_ramped, filtered_stim)
#plt.plot(finalstim_nb)

finalstim_tc = stimuli._stimuli.window_edges(tonecomp, fs, toneramp, -1, 'hamming')
plt.plot(finalstim_tc)
