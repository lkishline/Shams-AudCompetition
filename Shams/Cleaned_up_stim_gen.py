# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 09:28:17 2015

@author: lindsey
"""
from os import path as op
import numpy as np
import scipy.signal as sig
from expyfun.stimuli import convolve_hrtf, window_edges, rms
from expyfun.io import write_hdf5
from expyfun import stimuli as stim
import matplotlib.pyplot as mpl


fs = 24414.  # default for ExperimentController
stim_dur = 0.033   # Biz = 0.030
delay_beeps = 0.05  # gives a gap of 83ms between onset of first beep and 2nd
ramp_noise = 0.003
ramp_tone = 0.006
toneamp = 10**(-1.0)    # from Biz
noiseamp = 10**(-0.5)   # from Biz

# RANDOM NUMBER GENERATOR
rng = np.random.RandomState(0)

work_dir = op.dirname(__file__)

##########################################################################

# White noise burst
nb = np.random.uniform(-0.5, 0.5, (int(fs * stim_dur)))

### highpass cut-off freq of 1500Hz using 100th order Hamming ###
b = sig.firwin(101, 1500. / (fs / 2), pass_zero=False)  # False - highpass
                                                    # nyq_rate = fs / 2
                                                    # have to add '1' order
#filtered_stim = sig.lfilter(b, 1.0, nb)
filtered_stim = np.convolve(nb, b)

#### cut off extra 50 points from noiseburst ###
filtered_stim = filtered_stim[50:-50]   # not sure why I end up with extra

# windowing and onset/offset
finalstim_nb = window_edges(filtered_stim, fs, ramp_noise, -1, 'hamming')
#nb_ramped *= 0.01 * np.sqrt(2) # only works for sine tones
#x /= (xs rms) # sets the rms equal to 1 so then multiply by the target rms

#finalstim_nb = nb_ramped*noiseamp

# check the rms


############################################################################
tonecomp = np.zeros(24414. * stim_dur, float)
fund = 250.0                                # fundamental frequency
for x in xrange(1, 5):
    freq = fund*x
    tonecomp = tonecomp + np.sin(freq * 2 * np.pi * np.arange
                                 (int(fs * stim_dur)) / float(fs))
# windowing and onset/offset
finalstim_tc = window_edges(tonecomp, fs, ramp_tone, -1, 'hamming')
#finalstim_tc *= 0.01 * np.sqrt(2)  # Set RMS to 0.01
#finalstim_tc = finalstim_tc*toneamp

# check the rms:
#tc_rms = rms(finalstim_tc)

# First: HRTF tonebeep and noisebeep at each angle and store #
############################################################################
# add 50ms delay between beeps:
two_beep_delay = np.zeros(24414. * delay_beeps, float)
finalstim_tc_delay = np.append(finalstim_tc, two_beep_delay, axis=1)
finalstim_nb_delay = np.append(finalstim_nb, two_beep_delay, axis=1)

# with delay
one_1_noise_delay = convolve_hrtf(finalstim_nb_delay, fs, -30.0)
one_2_noise_delay = convolve_hrtf(finalstim_nb_delay, fs, 0.0)
one_3_noise_delay = convolve_hrtf(finalstim_nb_delay, fs, 30.0)

one_1_tone_delay = convolve_hrtf(finalstim_tc_delay, fs, -30.0)
one_2_tone_delay = convolve_hrtf(finalstim_tc_delay, fs, 0.0)
one_3_tone_delay = convolve_hrtf(finalstim_tc_delay, fs, 30.0)

#without delay
one_1_noise = convolve_hrtf(finalstim_nb, fs, -30.0)
one_2_noise = convolve_hrtf(finalstim_nb, fs, 0.0)
one_3_noise = convolve_hrtf(finalstim_nb, fs, 30.0)

one_1_tone = convolve_hrtf(finalstim_tc, fs, -30.0)
one_2_tone = convolve_hrtf(finalstim_tc, fs, 0.0)
one_3_tone = convolve_hrtf(finalstim_tc, fs, 30.0)

# rms stuff:
center_rms_noise = rms(one_2_noise, axis=None)
center_rms_tone = rms(one_2_tone, axis=None)
center_rms_noise_delay = rms(one_2_noise_delay, axis=None)
center_rms_tone_delay = rms(one_2_tone_delay, axis=None)


one_2_noise /= center_rms_noise
one_2_tone /= center_rms_tone

#combine to make double beeps:
two_1_noise = np.append(one_1_noise_delay, one_1_noise, axis=1)
two_2_noise = np.append(one_2_noise_delay, one_2_noise, axis=1)
two_3_noise = np.append(one_3_noise_delay, one_3_noise, axis=1)

two_1_tone = np.append(one_1_tone_delay, one_1_tone, axis=1)
two_2_tone = np.append(one_2_tone_delay, one_2_tone, axis=1)
two_3_tone = np.append(one_3_tone_delay, one_3_tone, axis=1)

# visual length testing:
#mpl.ion()
#t = np.arange(two_1_tone.shape[1]) / float(fs)
#mpl.plot(t, two_1_tone.T)
#mpl.xlabel('Time (sec)')

############################################################################
space_conditions = [[1, 2, 0], [1, 0, 2], [0, 1, 2], [2, 1, 0], [2, 0, 1],
                    [0, 2, 1]]

n_tpc = 30     # number of trials per 48 total condition
n_dfc = 2     # number of different flash counts
n_flc = 2     # number of flash locations in a trial count
n_tvb = 2     # tone vs. noise beep in location
n_cond = n_dfc * n_flc

# make single beeps arrays same length as two beeps arrays:
emptystimdur = np.zeros((2, len(one_1_noise[0])), float)
one_1e_tone = np.append(one_1_tone_delay, emptystimdur, axis=1)
one_2e_tone = np.append(one_2_tone_delay, emptystimdur, axis=1)
one_3e_tone = np.append(one_3_tone_delay, emptystimdur, axis=1)
one_1e_noise = np.append(one_1_noise_delay, emptystimdur, axis=1)
one_2e_noise = np.append(one_2_noise_delay, emptystimdur, axis=1)
one_3e_noise = np.append(one_3_noise_delay, emptystimdur, axis=1)

taud_stim = []
nocomp_stim_name = []
control_stim = []

for trial in range(n_tpc):
    for cc in range(n_cond):
        for config, xc in enumerate(space_conditions):
            if config == 0:
                print -30.0, 0.0
                onetone1_twonoise2 = np.nansum([one_1e_tone, two_2_noise],
                                               axis=0)
                fname = ('onetone1_twonoise2_%s_%s_%s.wav' % (config, cc,
                                                              trial))
                taud_stim.append(fname)
                stim.write_wav(fname, onetone1_twonoise2, fs,
                               overwrite=True, verbose=False)
                # control
                if trial <= 4:
                    c_onetone1_twonoise2 = onetone1_twonoise2
                    fname = ('c_onetone1_twonoise2_%s_%s_%s.wav' % (config, cc,
                                                                    trial))
                    control_stim.append(fname)
                    stim.write_wav(fname, c_onetone1_twonoise2, fs,
                                   overwrite=True, verbose=False)

                onenoise1_twotone2 = np.nansum([one_1e_noise, two_2_tone],
                                               axis=0)
                fname = ('onenoise1_twotone2_%s_%s_%s.wav' % (config, cc,
                                                              trial))
                taud_stim.append(fname)
                stim.write_wav(fname, onenoise1_twotone2, fs,
                               overwrite=True, verbose=False)
                # control
                if trial <= 4:
                    c_onenoise1_twotone2 = onenoise1_twotone2
                    fname = ('c_onenoise1_twotone2_%s_%s_%s.wav' % (config, cc,
                                                                    trial))
                    control_stim.append(fname)
                    stim.write_wav(fname, c_onenoise1_twotone2, fs,
                                   overwrite=True, verbose=False)

            elif config == 1:
                print -30.0, 30.0
                onetone1_twonoise3 = np.nansum([one_1e_tone, two_3_noise],
                                               axis=0)
                fname = ('onetone1_twonoise3_%s_%s_%s.wav' % (config, cc,
                                                              trial))
                taud_stim.append(fname)
                stim.write_wav(fname, onetone1_twonoise3, fs,
                               overwrite=True, verbose=False)

                if trial <= 4:
                    c_onetone1_twonoise3 = onetone1_twonoise3
                    fname = ('c_onetone1_twonoise3_%s_%s_%s.wav' % (config, cc,
                                                                    trial))
                    control_stim.append(fname)
                    stim.write_wav(fname, c_onetone1_twonoise3, fs,
                                   overwrite=True, verbose=False)

                onenoise1_twotone3 = np.nansum([one_1e_noise, two_3_tone],
                                               axis=0)
                fname = ('onenoise1_twotone3_%s_%s_%s.wav' % (config, cc,
                                                              trial))
                taud_stim.append(fname)
                stim.write_wav(fname, onenoise1_twotone3, fs,
                               overwrite=True, verbose=False)
                if trial <= 4:
                    c_onenoise1_twotone3 = onenoise1_twotone3
                    fname = ('c_onenoise1_twotone3_%s_%s_%s.wav' % (config, cc,
                                                                    trial))
                    control_stim.append(fname)
                    stim.write_wav(fname, c_onenoise1_twotone3, fs,
                                   overwrite=True, verbose=False)

            elif config == 2:
                print 0.0, 30.0
                onetone2_twonoise3 = np.nansum([one_2e_tone, two_3_noise],
                                               axis=0)
                fname = ('onetone2_twonoise3_%s_%s_%s.wav' % (config, cc,
                                                              trial))
                taud_stim.append(fname)
                stim.write_wav(fname, onetone2_twonoise3, fs,
                               overwrite=True, verbose=False)
                if trial <= 4:
                    c_onetone2_twonoise3 = onetone2_twonoise3
                    fname = ('c_onetone2_twonoise3_%s_%s_%s.wav' % (config, cc,
                                                                    trial))
                    control_stim.append(fname)
                    stim.write_wav(fname, c_onetone2_twonoise3, fs,
                                   overwrite=True, verbose=False)

                onenoise2_twotone3 = np.nansum([one_2e_noise, two_3_tone],
                                               axis=0)
                fname = ('onenoise2_twotone3_%s_%s_%s.wav' % (config, cc,
                                                              trial))
                taud_stim.append(fname)
                stim.write_wav(fname, onenoise2_twotone3, fs,
                               overwrite=True, verbose=False)
                if trial <= 4:
                    c_onenoise2_twotone3 = onenoise2_twotone3
                    fname = ('c_onenoise2_twotone3_%s_%s_%s.wav' % (config, cc,
                                                                    trial))
                    control_stim.append(fname)
                    stim.write_wav(fname, c_onenoise2_twotone3, fs,
                                   overwrite=True, verbose=False)

            elif config == 3:
                print -30.0, 0.0
                twotone1_onenoise2 = np.nansum([two_1_tone, one_2e_noise],
                                               axis=0)
                fname = ('twotone1_onenoise2_%s_%s_%s.wav' % (config, cc,
                                                              trial))
                taud_stim.append(fname)
                stim.write_wav(fname, twotone1_onenoise2, fs,
                               overwrite=True, verbose=False)
                if trial <= 4:
                    c_twotone1_onenoise2 = twotone1_onenoise2
                    fname = ('c_twotone1_onenoise2_%s_%s_%s.wav' % (config, cc,
                                                                    trial))
                    control_stim.append(fname)
                    stim.write_wav(fname, c_twotone1_onenoise2, fs,
                                   overwrite=True, verbose=False)

                twonoise1_onetone2 = np.nansum([two_1_noise, one_2e_tone],
                                               axis=0)
                fname = ('twonoise1_onetone2_%s_%s_%s.wav' % (config, cc,
                                                              trial))
                taud_stim.append(fname)
                stim.write_wav(fname, twonoise1_onetone2, fs,
                               overwrite=True, verbose=False)
                if trial <= 4:
                    c_twonoise1_onetone2 = twonoise1_onetone2
                    fname = ('c_twonoise1_onetone2_%s_%s_%s.wav' % (config, cc,
                                                                    trial))
                    control_stim.append(fname)
                    stim.write_wav(fname, c_twonoise1_onetone2, fs,
                                   overwrite=True, verbose=False)

            elif config == 4:
                print -30.0, 30.0
                twotone1_onenoise3 = np.nansum([two_1_tone, one_3e_noise],
                                               axis=0)
                fname = ('twotone1_onenoise3_%s_%s_%s.wav' % (config, cc,
                                                              trial))
                taud_stim.append(fname)
                stim.write_wav(fname, twotone1_onenoise3, fs,
                               overwrite=True, verbose=False)
                if trial <= 4:
                    c_twotone1_onenoise3 = twotone1_onenoise3
                    fname = ('c_twotone1_onenoise3_%s_%s_%s.wav' % (config, cc,
                                                                    trial))
                    control_stim.append(fname)
                    stim.write_wav(fname, c_twotone1_onenoise3, fs,
                                   overwrite=True, verbose=False)

                twonoise1_onetone3 = np.nansum([two_1_noise, one_3e_tone],
                                               axis=0)
                fname = ('twonoise1_onetone3_%s_%s_%s.wav' % (config, cc,
                                                              trial))
                taud_stim.append(fname)
                stim.write_wav(fname, twonoise1_onetone3, fs,
                               overwrite=True, verbose=False)
                if trial <= 4:
                    c_twonoise1_onetone3 = twonoise1_onetone3
                    fname = ('c_twonoise1_onetone3_%s_%s_%s.wav' % (config, cc,
                                                                    trial))
                    control_stim.append(fname)
                    stim.write_wav(fname, c_twonoise1_onetone3, fs,
                                   overwrite=True, verbose=False)

            elif config == 5:
                print 0.0, 30.0
                twotone2_onenoise3 = np.nansum([two_2_tone, one_3e_noise],
                                               axis=0)
                fname = ('twotone2_onenoise3_%s_%s_%s.wav' % (config, cc,
                                                              trial))
                taud_stim.append(fname)
                stim.write_wav(fname, twotone2_onenoise3, fs,
                               overwrite=True, verbose=False)
                if trial <= 4:
                    c_twotone2_onenoise3 = twotone2_onenoise3
                    fname = ('c_twotone2_onenoise3_%s_%s_%s.wav' % (config, cc,
                                                                    trial))
                    control_stim.append(fname)
                    stim.write_wav(fname, c_twotone2_onenoise3, fs,
                                   overwrite=True, verbose=False)

                twonoise2_onetone3 = np.nansum([two_2_noise, one_3e_tone],
                                               axis=0)
                fname = ('twonoise2_onetone3_%s_%s_%s.wav' % (config, cc,
                                                              trial))
                taud_stim.append(fname)
                stim.write_wav(fname, twonoise2_onetone3, fs,
                               overwrite=True, verbose=False)
                if trial <= 4:
                    c_twonoise2_onetone3 = twonoise2_onetone3
                    fname = ('c_twonoise2_onetone3_%s_%s_%s.wav' % (config, cc,
                                                                    trial))
                    control_stim.append(fname)
                    stim.write_wav(fname, c_twonoise2_onetone3, fs,
                                   overwrite=True, verbose=False)

###########################################################################
# 2 sets of 48 conditions gives 96 experimental trials per block
# plus an additional 12 trials per block for controls
# giving 108 trials per block with controls

total_trials = n_tvb * n_flc * n_dfc * len(space_conditions) * n_tpc + len(control_stim)
trials_per_block = 96 + 12    # 96 experimental trials, 12 control

# number of flashes occuring
n_flashes = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2,
             2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
flashes = np.tile(n_flashes, 60)

# flash locations
flash_locations = [1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2,
                   2, 2, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3,
                   2, 2, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3,
                   1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2]
flash_locs = np.tile(flash_locations, 30)

# make sure to stamp experimental trials as non-control
if_controle = ["", "", "", "", "", "", "", "", "",
               "", "", "", "", "", "", "", "", "",
               "", "", "", "", "", ""]
control_E = np.tile(if_controle, 60)

# stamp 1-48 for diff conditions
condition_stamp = np.array((range(1, 49)))
c_stamp = np.tile(condition_stamp, 30)

c = np.vstack(([taud_stim], [flashes], [flash_locs], [control_E], [c_stamp])).T
##############################################################################
# control trials:
if_controlc = [True, True, True, True, True, True, True, True, True,
               True, True, True, True, True, True, True, True, True,
               True, True, True, True, True, True]
control_C = np.tile(if_controlc, 10)

# create control flashes and locations
c_flashes = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2,
             2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
cflashes = np.tile(c_flashes, 10)
c_flash_locations = [1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2,
                     2, 2, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3,
                     2, 2, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3,
                     1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2]
c_flash_locs = np.tile(c_flash_locations, 5)
condition_stamp_controls = np.array((range(1, 49)))
c_stamp_controls = np.tile(condition_stamp, 5)
cc = np.vstack(([control_stim], [cflashes], [c_flash_locs], [control_C],
                [c_stamp_controls])).T

############################################################################
# create and store the blocks (should be 15)
blocks = {}
bn = ['Block1', 'Block2', 'Block3', 'Block4', 'Block5', 'Block6', 'Block7',
      'Block8', 'Block9', 'Block10', 'Block11', 'Block12', 'Block13',
      'Block14', 'Block15']
blocks.fromkeys(bn)
n_blocks = total_trials / trials_per_block
for bi in range(1, 16):
    d = c[0:96]    # iter over this to stack into blocks
    stack = cc[:12]
    dd = np.append(d, stack, 0)
    blocks["Block{0}".format(bi)] = rng.permutation(dd)
    np.delete(c, np.s_[:96], 0)
    np.delete(cc, np.s_[:12], 0)


# write out result:
print('Saving stimuli variables')
Stim_vars = dict(space_conditions=space_conditions,
                 nocomp_stim_name=nocomp_stim_name, taud_stim=taud_stim,
                 blocks=blocks, flashes=flashes)
np.savez('stim', **Stim_vars)
write_hdf5(op.join(work_dir, 'Stim_vars.hdf5'), Stim_vars, overwrite=True)
