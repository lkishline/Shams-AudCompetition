# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 11:38:16 2015

@author: lindsey
"""

import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
from expyfun import stimuli
from expyfun.stimuli import convolve_hrtf, play_sound, window_edges

fs = 24414.
dur = 0.008
n = int(dur * fs)    # total number of samples
t = np.linspace(0, dur, n, endpoint=False)    # time index

### Tone complex ###
tonecomp = np.zeros(24414. * dur, float)
fund = 250.0                                # fundamental frequency
for x in xrange(1, 5):
    freq = fund*x
    tonecomp = tonecomp + np.sin(freq * 2 * np.pi * np.arange(int(fs * dur)) / float(fs))

### Making white noise ###
nb = np.random.normal(0, 1.0, int(fs * dur)+ 50)     # add 50 points extra

### highpass cut-off freq of 1500Hz using 100th order Hamming ###
b = sig.firwin(101, 1500. / (fs / 2), pass_zero=False)  # False for highpass
                                                        # nyq_rate = fs / 2
                                                        # have to add '1' order
filtered_stim = sig.lfilter(b, 1.0, nb)
#plt.plot(filtered_stim)

### cut off extra 50 points from noiseburst ###

filtered_stim = filtered_stim[50:]

### windowing - onset and offset ramps ###
toneramp = 0.006
noiseramp = 0.003

nb_ramped = window_edges(nb[50:], fs, noiseramp, -1, 'hamming')
finalstim_nb = np.multiply(nb_ramped, filtered_stim)

finalstim_tc = window_edges(tonecomp, fs, toneramp, -1, 'hamming')


### create a two beep stimulus ###
# 8ms + 50ms + 8ms = 195 + 1220 + 195 which is a total of 1610 samples
interval = 0.050
gap = np.zeros(24414. * interval, float)

# if one beep:
onebeep = np.concatenate((finalstim_nb, gap), axis=1)


# if two beep:
twobeep = np.append(onebeep, finalstim_nb, axis=1)


### convolve with HRTF at appropriate angles ###



### play sound ###
play_sound(twobeep, fs, norm=True, wait=True)

### plots to check frequencies and timing/windowing ###

#plt.plot(t, finalstim_nb)
#plt.plot(t, finalstim_tc)
plt.plot(twobeep)
#plt.plot(onebeep)