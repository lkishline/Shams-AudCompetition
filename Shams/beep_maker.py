# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 16:20:52 2015

@author: lindsey
"""

import numpy as np
from scipy import io as sio
from scipy.fftpack import rfft, irfft, fftfreq
import scipy.signal as signal
import matplotlib.pyplot as plt
from expyfun import stimuli 





fs = 24414.             # Sampling rate - how many samples per second
dur = 1.0               # a duration of 1 (second)


### Making a simple tone (beep) ###


tone = np.sin(2 * np.pi * 100 * np.arange(int(fs * dur)) / float(fs))
    # a tone at a 100 Hz - just think how often a multiple of 2pi arrives
tone *= 0.01 * np.sqrt(2)  # Set RMS to 0.01
#plt.plot(tone)


### Tone complex ###

tonecomp = np.zeros(24414, float)
fund = 250.0 # fundamental frequency
for x in xrange(1, 5):
    freq = fund*x
    tonecomp = tonecomp + np.sin(freq * 2 * np.pi * np.arange(int(fs * dur)) / float(fs))
    
plt.plot(tonecomp)

# look in frequency domain ### doesn't work due to fft function ??
#freqindex = np.arange(int(fs - 1))
#powerFT = abs(np.fft(tonecomp))  # abs value of fourier components
#plt.plot(freqindex, powerFT)


### Making envelopes and applying to tone burst ###

env = np.cos(2 * np.pi * np.arange(int(fs * dur)) / float(fs))
env = env * -1
env = env + 1
env = env / 2
#plt.plot(env)

stim = np.multiply(env, tone)
plt.plot(stim)


### Making white noise ###

  # Gaussian/white noise?
noiseburst = np.random.normal(0, 1.0, int(fs * 1.0))  # 1 secs


# Filtering with a lowpass cut-off freq of 1500Hz using 100th order Hamming
#fltnoiseburst = stimuli._filter(noiseburst, )

flteredburst = stimuli.get_env(noiseburst, fs, 100, 1500) # not right obvi
plt.plot(flteredburst)

### Making two beeps seperated by some amount of time ###
