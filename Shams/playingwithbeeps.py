# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:49:11 2015

@author: lindsey
"""
import numpy as np

# stim stuff
fs = 24144.
dur = .05
freq = 250

#tone stuff
t = np.linspace(0, 0.1, fs * dur)
tone = np.sin(2 * np.pi * freq * t)

# onset and offset gating
gatedur = 0.005    # the duration of the gate in seconds (6ms)
ongate = np.cos(np.linspace(np.pi, 2*np.pi, fs * gatedur))
ongate = ongate + 1
ongate = ongate / 2
offgate = np.fliplr([ongate])[0]
sustain = np.zeros((len(tone) - 2 * len(ongate)))
env = []   # 
tone = np.multiply(tone, env)
