# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 14:14:52 2015

@author: lindsey
"""
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
from expyfun import stimuli
from expyfun import ExperimentController, analyze
from expyfun.visual import FixationDot, Circle



### attempts at making flashes ###
# Using 'basic_experiment' expyfun example to work from #

# set configuration
fs = 24414.  # default for ExperimentController
dur = 1.0
tone = np.sin(2 * np.pi * 1000 * np.arange(int(fs * dur)) / float(fs))
tone *= 0.01 * np.sqrt(2)  # Set RMS to 0.01

with ExperimentController('testExp', participant='foo', session='001',
                          output_dir=None) as ec:
    ec.screen_prompt('Press a button when you hear the tone', max_wait=1)

    #dot = FixationDot()
    flash = Circle(ec, radius=0.1, )
    ec.clear_buffer()
    ec.load_buffer(tone)
    #dot.draw()
    flash.draw()
    screenshot = ec.screenshot()  # only because we want to show it in the docs

    ec.identify_trial(ec_id='tone', ttl_id=[0, 0])
    ec.start_stimulus()
    presses = ec.wait_for_presses(dur)
    ec.stop()
    ec.trial_ok()
    print('Presses:\n{}'.format(presses))


plt.ion()
analyze.plot_screen(screenshot)


###############################################################

# Things to do:

# have circle actually be a circle and not a blasted oval
# make it flash 
# make it flash over different areas of screen
# move fixation dot off of midline