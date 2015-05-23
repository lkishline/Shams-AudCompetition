# -*- coding: utf-8 -*-
"""
Created on Thu May 21 13:16:46 2015

@author: lindsey
"""



from os import path as op
import numpy as np
from scipy.io import savemat, wavfile
import matplotlib.pyplot as plt
import scipy.signal as sig
from expyfun._tdt_controller import get_tdt_rates
from expyfun.stimuli import convolve_hrtf, play_sound, window_edges

print(__doc__)


def generate_stimuli(num_trials=10, stim_dur=0.08, fs=24414., rms=0.01,
                     ramp_noise=0.03, ramp_tone=0.06,
                     output_dir=None, save_as='mat', rand_seed=0):
    """Make stimuli and save in various formats. Optimized for saving
    as MAT files, but can also save directly as WAV files, or can return a
    python dictionary with sinewave data as values.
    Parameters
    ----------
    num_trials : int
        Number of trials you want in your experiment. Ignored if save_as is
        not 'mat'.
    stim_dur : float
        Duration of the tones in seconds.
    ramp_noise : float
        Duration of the onset and offset ramps in seconds for noiseburst stim.
    ramp_tone : float
        Duration of the onset and offset ramps in seconds for tonecomplex stim.
    fs : float | None
        Sampling frequency of resulting sinewaves.  Defaults to 24414.0625 (a
        standard rate for TDTs) if no value is specified.
    rms : float
        RMS amplitude to which all sinwaves will be scaled.
    output_dir : str | None
        Directory to output the files into. If None, the current directory
        is used.
    save_as : str
        Format in which to return the sinewaves. 'dict' returns sinewave arrays
        as values in a python dictionary; 'wav' saves them as WAV files at
        sampling frequency 'fs'; 'mat' saves them as a MAT file along with
        related variables 'fs', 'freqs', 'trial_order', and 'rms'.
    rand_seed : int | None
        Seed for the random number generator.
    Returns
    -------
    wavs : dict | None
        If `save_as` is `'dict'`, then this will be a dict, else None.
    finalstim_tc :
    finalstim_nb :
    """
    if rand_seed is None:
        rng = np.random.RandomState()
    else:
        rng = np.random.RandomState(rand_seed)

    # check input arguments
    if save_as not in ['dict', 'wav', 'mat']:
        raise ValueError('"save_as" must be "dict", "wav", or "mat"')

    if fs is None:
        fs = get_tdt_rates()['25k']

    # General params:
    n = int(stim_dur * fs)    # total number of samples
    t = np.linspace(0, stim_dur, n, endpoint=False)    # time index for ploting

#### make tone complex#########################################################

    tonecomp = np.zeros(24414. * stim_dur, float)
    fund = 250.0                                # fundamental frequency
    for x in xrange(1, 5):
        freq = fund*x
        tonecomp = tonecomp + np.sin(freq * 2 * np.pi * np.arange
                                     (int(fs * stim_dur)) / float(fs))
    # windowing and onset/offset
    finalstim_tc = window_edges(tonecomp, fs, ramp_tone, -1, 'hamming')

    return finalstim_tc

##### make noise burst#########################################################

    # add 50 points extra
    nb = np.random.normal(0, 1.0, int(fs * stim_dur) + 50)

    ### highpass cut-off freq of 1500Hz using 100th order Hamming ###
    b = sig.firwin(101, 1500. / (fs / 2), pass_zero=False)  # False - highpass
                                                        # nyq_rate = fs / 2
                                                        # have to add '1' order
    filtered_stim = sig.lfilter(b, 1.0, nb)

    ### cut off extra 50 points from noiseburst ###
    filtered_stim = filtered_stim[50:]
    # windowing and onset/offset
    nb_ramped = window_edges(nb[50:], fs, ramp_noise, -1, 'hamming')
    finalstim_nb = np.multiply(nb_ramped, filtered_stim)

    return finalstim_nb


def onetwo_beep_gen(numbeep, interval, finalstim_tc, finalstim_nb):
    """ Puts together the correct number of beeps within one auditory stream
    -------------
    Parameters:
    numbeep : int
        Number of beeps wanted within an auditory stream
    interval : float
        Time interval between beeps or after beep.
    -------------
    Returns:
    onebeep_tc
    onebeep_nb
    twobeep_tc
    twobeep_nb
    """
##### if one beep:#############################################################

    # 8ms + 50ms + 8ms = 195 + 1220 + 195 which is a total of 1610 samples
    interval = 0.050
    gap = np.zeros(24414. * interval, float)
    onebeep_tc = np.concatenate((finalstim_tc, gap), axis=1)
    onebeep_nb = np.concatenate((finalstim_nb, gap), axis=1)
    return onebeep_tc, onebeep_nb
##### if two beep:#############################################################

    twobeep_tc = np.append(onebeep_tc, finalstim_tc, axis=1)
    twobeep_nb = np.append(onebeep_nb, finalstim_tc, axis=1)
    return twobeep_tc, twobeep_nb

def stim_conditions(angles, onebeep_nb, twobeep_nb, onebeep_tc, twobeep_tc):
    """ Takes completed stimuli from above functions and makes all of the
    conditions for the flash beep with three possible locations and azmuith
    angles.
    """
##### make single auditory stim################################################

    #conditions_1A = [-30_1A, 0_1A, 30_1A, -30_2A, 0_2A, 30_2A]
    spatials = ('-30', '0', '30')
    beep_combos_1a = ('onebeep_nb', 'twobeep_nb', 'onebeep_tc', 'twobeep_tc')

##### make competing auditory stim#############################################

    #conditions_2A = []
    spatials = ('-30x0', '0x30', '-30x30')
    beep_combos_2a = ('onebeep_nbxonebeep_tc', 'twobeep_nbxonebeep_tc',
                      'onebeep_nbxtc2', 'twobeep_nbxtwobeep_tc')

    all_spatials = [s.split('x') for s in spatials]
    for s in all_spatials[1:]:
        all_spatials[0] += s
    all_spatials = all_spatials[0]
    all_spatials = list(np.unique([float(s) for s in all_spatials]))

    all_combos = [ss.split('x') for ss in beep_combos_2a]
    for ss in all_combos[1:]:
        all_combos[0] += ss
    all_combos = all_combos[0]
    all_combos = list(np.unique([float(ss) for ss in all_combos]))

##### convolve with HRTF at appropriate angles ################################

    move_sig = np.concatenate([convolve_hrtf(stim, fs, ang)
                              for ang in range(-30, 30)], axis=1)
    return move_sig

##### make and store wav files - make dictionary of all info ##################

    

basic_stim = generate_stimuli()
multi_beeps = onetwo_beep_gen()
completed_stimset = stim_conditions()
