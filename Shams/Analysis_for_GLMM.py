# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 15:33:59 2017

@author: lindsey
"""

import pandas as pd
import numpy as np
from os import path as op
from expyfun.io import read_hdf5

out_dir = ('/home/lindsey/Desktop/PythonFiles/Shams/Flashbeeps2.0')

def listcompare(list1, list2):
    a = [int(i == j) for i,j in zip(list1, list2)]
    return a


#def fisfus(flashed, pressed, illusion):
#    c = []
#    # if there was an illusion indicated, and there was one physical flash
#    # then they must have pressed 2 (indicating fission), else if there was
#    # two physical flashes, then they must have pressed 1 (indicating fusion).
#    # if no illusion then just place a zero
#    for i in flashed:
#        if illusion.loc[i] == 1:
#            if flashed.loc[i] == 1:
#                c.append(1)
#            if flashed.loc[i] == 2:
#                c.append(2)
#        else:
#            c.append(0)
#    return c


def trialtiming(control, flash_timing):
    b = []
    for it in range(108):
        if bool(control[it]) is False:
            cur_trial_timing_log = flash_timing[it]
            play_stamp = cur_trial_timing_log[1][0]
            first_flip = cur_trial_timing_log[0][1]    #can probably combine these next four lines
            second_flip = cur_trial_timing_log[0][2]
            check_flip_1 = first_flip - play_stamp
            check_flip_2 = second_flip - first_flip

            if 0.015 <= check_flip_1 <= 0.018:
                chk1 = 1
            else:
                chk1 = 8
            if 0.015 <= check_flip_2 <= 0.018:
                chk2 = 1
            else:
                chk2 = 8

            if int(flashed[it]) == 2:
                third_flip = cur_trial_timing_log[0][3]     #can probably combine these next four lines into just two
                fourth_flip = cur_trial_timing_log[0][4]
                check_flip_3 = third_flip - second_flip
                check_flip_4 = fourth_flip - third_flip
                if 0.064 <= check_flip_3 <= 0.068:
                    chk3 = 1
                else:
                    chk3 = 8
                if 0.015 <= check_flip_4 <= 0.018:
                    chk4 = 1
                else:
                    chk4 = 8
                timing_validate = [chk1, chk2, chk3, chk4]
            if int(flashed[it]) == 1:
                timing_validate = [chk1, chk2]

            if 8 in timing_validate:
                b.append([0])
            else:
                b.append([1])
        else:
            b.append([2])    # keep track of the control trials place
    return b


def Collapsed_Conditions(row):
    if int(row['condition_type']) in center_congruent:
        return 1
    if int(row['condition_type']) in center_noncongruent:
        return 2
    if int(row['condition_type']) in outside_congruent_1away:
        return 3
    if int(row['condition_type']) in outside_noncongruent_1away:
        return 4
    if int(row['condition_type']) in outside_congruent_2away:
        return 5
    if int(row['condition_type']) in outside_noncongruent_2away:
        return 6
    if int(row['condition_type']) in center_congruent_fusion:
        return 1
    if int(row['condition_type']) in center_noncongruent_fusion:
        return 2
    if int(row['condition_type']) in outside_congruent_1away_fusion:
        return 3
    if int(row['condition_type']) in outside_noncongruent_1away_fusion:
        return 4
    if int(row['condition_type']) in outside_congruent_2away_fusion:
        return 5
    if int(row['condition_type']) in outside_noncongruent_2away_fusion:
        return 6
    return 8


def Vcentmarker(row):
    if int(row['condition_type']) in center_congruent:
        return 1
    if int(row['condition_type']) in center_noncongruent:
        return 1
    if int(row['condition_type']) in outside_congruent_1away:
        return 0
    if int(row['condition_type']) in outside_noncongruent_1away:
        return 0
    if int(row['condition_type']) in outside_congruent_2away:
        return 0
    if int(row['condition_type']) in outside_noncongruent_2away:
        return 0
    if int(row['condition_type']) in center_congruent_fusion:
        return 1
    if int(row['condition_type']) in center_noncongruent_fusion:
        return 1
    if int(row['condition_type']) in outside_congruent_1away_fusion:
        return 0
    if int(row['condition_type']) in outside_noncongruent_1away_fusion:
        return 0
    if int(row['condition_type']) in outside_congruent_2away_fusion:
        return 0
    if int(row['condition_type']) in outside_noncongruent_2away_fusion:
        return 0
    return 8


def Vperiph_Af_centermarker(row):
    if int(row['condition_type']) in center_congruent:
        return 0
    if int(row['condition_type']) in center_noncongruent:
        return 0
    if int(row['condition_type']) in outside_congruent_1away:
        return 1
    if int(row['condition_type']) in outside_noncongruent_1away:
        return 1
    if int(row['condition_type']) in outside_congruent_2away:
        return 0
    if int(row['condition_type']) in outside_noncongruent_2away:
        return 0
    if int(row['condition_type']) in center_congruent_fusion:
        return 0
    if int(row['condition_type']) in center_noncongruent_fusion:
        return 0
    if int(row['condition_type']) in outside_congruent_1away_fusion:
        return 1
    if int(row['condition_type']) in outside_noncongruent_1away_fusion:
        return 1
    if int(row['condition_type']) in outside_congruent_2away_fusion:
        return 0
    if int(row['condition_type']) in outside_noncongruent_2away_fusion:
        return 0
    return 8


def Vperiph_Af_periphmarker(row):
    if int(row['condition_type']) in center_congruent:
        return 0
    if int(row['condition_type']) in center_noncongruent:
        return 0
    if int(row['condition_type']) in outside_congruent_1away:
        return 0
    if int(row['condition_type']) in outside_noncongruent_1away:
        return 0
    if int(row['condition_type']) in outside_congruent_2away:
        return 1
    if int(row['condition_type']) in outside_noncongruent_2away:
        return 1
    if int(row['condition_type']) in center_congruent_fusion:
        return 0
    if int(row['condition_type']) in center_noncongruent_fusion:
        return 0
    if int(row['condition_type']) in outside_congruent_1away_fusion:
        return 0
    if int(row['condition_type']) in outside_noncongruent_1away_fusion:
        return 0
    if int(row['condition_type']) in outside_congruent_2away_fusion:
        return 1
    if int(row['condition_type']) in outside_noncongruent_2away_fusion:
        return 1
    return 8    

def eccmarker(row):
    if int(row['condition_type']) in center_congruent:
        return 0
    if int(row['condition_type']) in center_noncongruent:
        return 0
    if int(row['condition_type']) in center_congruent_fusion:
        return 0
    if int(row['condition_type']) in center_noncongruent_fusion:
        return 0
    if int(row['condition_type']) in outside_congruent_1away:
        return 1
    if int(row['condition_type']) in outside_noncongruent_1away:
        return 1
    if int(row['condition_type']) in outside_congruent_1away_fusion:
        return 1
    if int(row['condition_type']) in outside_noncongruent_1away_fusion:
        return 1
    if int(row['condition_type']) in outside_congruent_2away:
        return 2
    if int(row['condition_type']) in outside_noncongruent_2away:
        return 2
    if int(row['condition_type']) in outside_congruent_2away_fusion:
        return 2
    if int(row['condition_type']) in outside_noncongruent_2away_fusion:
        return 2
    return 8   

def V1A1_or_V2A2marker(row):
    if int(row['condition_type']) in center_congruent:
        return 1
    if int(row['condition_type']) in center_noncongruent:
        return 0
    if int(row['condition_type']) in outside_congruent_1away:
        return 1
    if int(row['condition_type']) in outside_noncongruent_1away:
        return 0
    if int(row['condition_type']) in outside_congruent_2away:
        return 1
    if int(row['condition_type']) in outside_noncongruent_2away:
        return 0
    if int(row['condition_type']) in center_congruent_fusion:
        return 1
    if int(row['condition_type']) in center_noncongruent_fusion:
        return 0
    if int(row['condition_type']) in outside_congruent_1away_fusion:
        return 1
    if int(row['condition_type']) in outside_noncongruent_1away_fusion:
        return 0
    if int(row['condition_type']) in outside_congruent_2away_fusion:
        return 1
    if int(row['condition_type']) in outside_noncongruent_2away_fusion:
        return 0
    return 8   
    

def V1A2marker(row):
    if int(row['condition_type']) in center_congruent:
        return 0
    if int(row['condition_type']) in center_noncongruent:
        return 1
    if int(row['condition_type']) in outside_congruent_1away:
        return 0
    if int(row['condition_type']) in outside_noncongruent_1away:
        return 1
    if int(row['condition_type']) in outside_congruent_2away:
        return 0
    if int(row['condition_type']) in outside_noncongruent_2away:
        return 1
    if int(row['condition_type']) in center_congruent_fusion:
        return 0
    if int(row['condition_type']) in center_noncongruent_fusion:
        return 0
    if int(row['condition_type']) in outside_congruent_1away_fusion:
        return 0
    if int(row['condition_type']) in outside_noncongruent_1away_fusion:
        return 0
    if int(row['condition_type']) in outside_congruent_2away_fusion:
        return 0
    if int(row['condition_type']) in outside_noncongruent_2away_fusion:
        return 0
    return 8


def V2A1marker(row):
    if int(row['condition_type']) in center_congruent:
        return 0
    if int(row['condition_type']) in center_noncongruent:
        return 0
    if int(row['condition_type']) in outside_congruent_1away:
        return 0
    if int(row['condition_type']) in outside_noncongruent_1away:
        return 0
    if int(row['condition_type']) in outside_congruent_2away:
        return 0
    if int(row['condition_type']) in outside_noncongruent_2away:
        return 0
    if int(row['condition_type']) in center_congruent_fusion:
        return 0
    if int(row['condition_type']) in center_noncongruent_fusion:
        return 1
    if int(row['condition_type']) in outside_congruent_1away_fusion:
        return 0
    if int(row['condition_type']) in outside_noncongruent_1away_fusion:
        return 1
    if int(row['condition_type']) in outside_congruent_2away_fusion:
        return 0
    if int(row['condition_type']) in outside_noncongruent_2away_fusion:
        return 1
    return 8


def Ac_typemarker(row):
    if int(row['condition_type']) in Tones:
        return 0
    if int(row['condition_type']) in Noises:
        return 1
    return 8

     
# set into 48 conditions:
# condition #: name of wav file, # of flashes, flash location
condition_log = {1: ['onetone1_twonoise2', 1, 1],
                 25: ['onetone1_twonoise2', 1, 2],
                 37: ['onetone1_twonoise2', 2, 1],
                 13: ['onetone1_twonoise2', 2, 2],
                 38: ['onenoise1_twotone2', 1, 1],
                 14: ['onenoise1_twotone2', 1, 2],
                 2: ['onenoise1_twotone2', 2, 1],
                 26: ['onenoise1_twotone2', 2, 2],
                 3: ['onetone1_twonoise3', 1, 1],
                 27: ['onetone1_twonoise3', 1, 3],
                 39: ['onetone1_twonoise3', 2, 1],
                 15: ['onetone1_twonoise3', 2, 3],
                 40: ['onenoise1_twotone3', 1, 1],
                 16: ['onenoise1_twotone3', 1, 3],
                 4: ['onenoise1_twotone3', 2, 1],
                 28: ['onenoise1_twotone3', 2, 3],
                 5: ['onetone2_twonoise3', 1, 2],
                 29: ['onetone2_twonoise3', 1, 3],
                 41: ['onetone2_twonoise3', 2, 2],
                 17: ['onetone2_twonoise3', 2, 3],
                 42: ['onenoise2_twotone3', 1, 2],
                 18: ['onenoise2_twotone3', 1, 3],
                 6: ['onenoise2_twotone3', 2, 2],
                 30: ['onenoise2_twotone3', 2, 3],
                 7: ['twotone1_onenoise2', 1, 1],
                 31: ['twotone1_onenoise2', 1, 2],
                 43: ['twotone1_onenoise2', 2, 1],
                 19: ['twotone1_onenoise2', 2, 2],
                 44: ['twonoise1_onetone2', 1, 1],
                 20: ['twonoise1_onetone2', 1, 2],
                 8: ['twonoise1_onetone2', 2, 1],
                 32: ['twonoise1_onetone2', 2, 2],
                 9: ['twotone1_onenoise3', 1, 1],
                 33: ['twotone1_onenoise3', 1, 3],
                 45: ['twotone1_onenoise3', 2, 1],
                 21: ['twotone1_onenoise3', 2, 3],
                 46: ['twonoise1_onetone3', 1, 1],
                 22: ['twonoise1_onetone3', 1, 3],
                 10: ['twonoise1_onetone3', 2, 1],
                 34: ['twonoise1_onetone3', 2, 3],
                 11: ['twotone2_onenoise3', 1, 2],
                 35: ['twotone2_onenoise3', 1, 3],
                 47: ['twotone2_onenoise3', 2, 2],
                 23: ['twotone2_onenoise3', 2, 3],
                 48: ['twonoise2_onetone3', 1, 2],
                 24: ['twonoise2_onetone3', 1, 3],
                 12: ['twonoise2_onetone3', 2, 2],
                 36: ['twonoise2_onetone3', 2, 3]}


Tones = [1, 37, 14, 26, 3, 39, 16, 28, 5, 41, 18, 30, 7, 43, 20, 32, 9, 45, 22, 34, 11, 47, 24, 36]
Noises = [25, 13, 38, 2, 27, 15, 40, 4, 29, 17, 42, 6, 31, 19, 44, 8, 33, 21, 46, 10, 35, 23, 48, 12]
### Illusion trial counts. ONE physical flash (subj presses 2 flashes)########
Possible_fission_trials = [1, 25, 38, 14, 3, 27, 40, 16, 5, 29, 42, 18, 7, 31,
                            44, 20, 9, 33, 46, 22, 11, 35, 48, 24]

center_fission_trials = [25, 14, 5, 42, 31, 20, 11, 48]  # flash occurs in the center location
center_congruent = [25, 14, 11, 48]    # flash occurs center - True beep# is congruent
center_noncongruent = [5, 42, 31, 20]    # flash occurs center - True beep# is non-congruent


outside_fission_trials = [1, 38, 3, 27, 40, 16, 29, 18, 7, 44, 9, 33, 46, 22,
                           35, 24]    # flash occurs either in pos 1 or pos 3
outside_congruent_1away = [29, 18, 7, 44]     # flash occurs in pos 1 or pos 3 - True beep is congruent - false beep one away
outside_noncongruent_1away = [1, 38, 35, 24]   # flash occurs in pos 1 or pos 3 - True beep is noncongruent - false beep one away
outside_congruent_2away = [27, 16, 9, 46]     # flash occurs in pos 1 or pos 3 - True beep is congruent - false beep two away
outside_noncongruent_2away = [3, 40, 33, 22]   # flash occurs in pos 1 or pos 3 - True beep is noncongruent - false beep two away

Possible_illu_2noise_trials = [1, 25, 3, 27, 5, 29, 44, 20, 46, 22, 48, 24]
Possible_illu_2tone_trials = [38, 14, 40, 16, 42, 18, 7, 31, 9, 33, 11, 35]
### Fusion trial counts. TWO physical flashes (subj presses 1 flash)##########

Possible_Fusion_trials = [37, 13, 2, 26, 39, 15, 4, 28, 41, 17, 6, 30, 43, 19,
                          8, 32, 45, 21, 10, 34, 47, 23, 12, 36]

center_fusion_trials = [13, 26, 41, 6, 19, 32, 47, 12]  # flashes occurs in the center location
center_congruent_fusion = [13, 26, 47, 12]    # flashes occurs center - True beep# is congruent
center_noncongruent_fusion = [41, 6, 19, 32]    # flashes occurs center - True beep# is non-congruent

outside_fusion_trials = [37, 2, 39, 15, 4, 28, 17, 30, 43, 8, 45, 21, 10, 34,
                         23, 36]    # flashes occurs either in pos 1 or pos 3
outside_congruent_1away_fusion = [17, 30, 43, 8]     # flashes occurs in pos 1 or pos 3 - True beep is congruent - false beeps one away
outside_noncongruent_1away_fusion = [37, 2, 23, 36]   # flashes occurs in pos 1 or pos 3 - True beep is noncongruent - false beeps one away
outside_congruent_2away_fusion = [15, 28, 45, 10]     # flashes occurs in pos 1 or pos 3 - True beep is congruent - false beeps two away
outside_noncongruent_2away_fusion = [39, 4, 21, 34]   # flashes occurs in pos 1 or pos 3 - True beep is noncongruent - false beeps two away


colnames = ['subj_num', 'cue_attn', 'blk_num', 'trial_num', 'condition_num',
            'flash_timing', 'flashed', 'pressed', 'illusion', 'RT']
data = []
keydetection = []
for cue in ['NOCUE', 'WITHCUE']:
#    for sbj in [2, 4]:
    for sbj in [0, 1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 21,
                22]:
        # identify subject and block number
        if sbj <= 9:
            subj_num = '40%s' % sbj
        else:
            subj_num = '4%s' % sbj
        work_dir = ('/home/lindsey/Desktop/PythonFiles/Shams/Flashbeeps2.0/%s/Blocks' % cue)
        # import data file and relevant variables
        for bi in range(1, 16):
            blc_num = bi
            d = read_hdf5(op.join(work_dir, 'subj%s_block%s.hdf5' %
                          (subj_num, blc_num)))

            presses = d['presses']
            played = d['played']
            flashed = d['flashed']
            flash_timing = d['flipplay_times']
            current_block = d['current_block']
            condition_type = d['condition_stamp']

            control = current_block[::, 3]
            wavfile = current_block[::, 1]
            number_pressed = [x for x, _ in presses]
            raw_RT = [x[1] for x in presses]
            timingcheck = trialtiming(control, flash_timing)
            if '3' in number_pressed:
                keydetection.append((sbj, cue, blc_num, number_pressed.count('3')))
                print 'yes'

            if cue == 'NOCUE':
                cue_attn = np.zeros(108)
            else:
                cue_attn = np.ones(108)
            trial_num = np.arange(0, 108, dtype=int)
            subjnum = np.full((108,), subj_num)
            blcnum = np.full((108,), blc_num)

            datastack = {'subjnum': subjnum, 'cue_attn': cue_attn, 'blcnum': blcnum,
                     'trial_num': trial_num, 'condition_type': condition_type,
                     'timingcheck': timingcheck, 'flashed': flashed,
                     'number_pressed': number_pressed,'raw_RT': raw_RT,
                     'control': control}
            D = pd.DataFrame.from_dict(datastack)
            data.append(D)
df = pd.concat(data, axis=0)
#blocks_check = df['blcnum'].tolist()

MasterRaw = df
#foo3 = MasterRaw['number_pressed'].tolist()
# to look at number of times people accidentally pressed '3':
# thing1 = MasterRaw.groupby('number_pressed').count()
# thing2 = thing1['number_pressed']
##################
#data processing:#
##################
numsubj = 19
with_without = 2
trial_multiplier = numsubj*with_without
df.fillna(value=np.nan, inplace=True)   # replace all None type with NaN
foo2 = MasterRaw['number_pressed'].tolist()
# adjust RT:  
df['raw_RT'] = df['raw_RT'].apply(lambda x: x - .116)

# identify illusions:
df['number_pressed'] = df['number_pressed'].convert_objects(convert_numeric=True)
#foo1 = MasterRaw['number_pressed'].tolist()
df['illusion'] = listcompare(df['number_pressed'], df['flashed'])

#choosing not to go into fusion vs fission types for this analysis:
# df['illusion_type'] = fisfus(df['flashed'], df['number_pressed'], df['illusion'])

# identify catch trials properly: 1.0 == catch trial 0.0 == non-catch trial

df['control'] = df['control'].replace(r'\s+',np.nan,regex=True).replace('',np.nan)
df['control'] = df['control'].replace('True', 1 ,regex=True).replace('True', 1)
df['control'] = df['control'].replace(np.nan, 0 ,regex=True).replace(np.nan, 0)
#foo = df['control'].tolist()


# number trials per cue_attn(1620 total) - not per block(108*15)
test = np.arange(1, 1621, dtype=int)
df['trial_num'] = np.tile(test, trial_multiplier)

# add in condition codes 1-6
# 1 = center congruent, 2 = center incongruent, 3 = lateral near congruent,
# 4 = lateral near incongruent, 5 = lateral far congruent,
# 6 = lateral far incongruent

df['collapsed_conditions'] = df.apply(lambda row: Collapsed_Conditions(row),
                                      axis=1)

# Catch trial check:
#control_foo = df['control'].tolist()
#illusion_foo = df['illusion'].tolist()
#
#df['subject_reliability'] = (df['control']>2.0) & (df['illusion']>1.0)
##foo = df['subject_reliability'].tolist()

MasterProcessed = df
#foo2 = MasterProcessed['number_pressed'].tolist()
#############################
# CLEAN DATA
#############################

# remove catch trials:
df = df[df.control < 0.5]    # control trials are marked as 1.0

# RT clean: removes unacceptable reaction time rows
#
df = df[df.raw_RT >= 0.2]
df = df[df.raw_RT <= 1.0]

# remove identified blocks that had keys switched from data:
# subjects 1 withcue blks 3,4
df = df[~((df['subjnum'] == 401) & (df['blcnum'] == 3) & (df['cue_attn'] == 1))]
df = df[~((df['subjnum'] == 401) & (df['blcnum'] == 4) & (df['cue_attn'] == 1))]

# subjects 7 nocue blks 7,8,9,15
df = df[~((df['subjnum'] == 407) & (df['blcnum'] == 7) & (df['cue_attn'] == 0))]
df = df[~((df['subjnum'] == 407) & (df['blcnum'] == 8) & (df['cue_attn'] == 0))]
df = df[~((df['subjnum'] == 407) & (df['blcnum'] == 9) & (df['cue_attn'] == 0))]
df = df[~((df['subjnum'] == 407) & (df['blcnum'] == 15) & (df['cue_attn'] == 0))]

# subjects 8 nocue blks 11
df = df[~((df['subjnum'] == 48) & (df['blcnum'] == 11) & (df['cue_attn'] == 0))]

# subjects 12 nocue blks 12
df = df[~((df['subjnum'] == 412) & (df['blcnum'] == 12) & (df['cue_attn'] == 0))]

# subjects 16 nocue blks 5
df = df[~((df['subjnum'] == 416) & (df['blcnum'] == 5) & (df['cue_attn'] == 0))]

# subjects 17 withcue blks 2
df = df[~((df['subjnum'] == 417) & (df['blcnum'] == 2) & (df['cue_attn'] == 1))]

# subjects 19 nocue blks 6, withcue blks 12
df = df[~((df['subjnum'] == 419) & (df['blcnum'] == 6) & (df['cue_attn'] == 0))]
df = df[~((df['subjnum'] == 419) & (df['blcnum'] == 12) & (df['cue_attn'] == 1))]

# remove '3's from presses:
df = df[df.number_pressed <= 2]
#foo = df['number_pressed'].tolist()


#####################################
### Code coniditions for GLMM #######
#####################################

# Code Vcent, Vperiph_Af_center, Vperiph_Af_periph :

df["Vcent"] = df.apply(lambda row: Vcentmarker(row), axis=1)
df["Vperiph_Af_center"] = df.apply(lambda row: Vperiph_Af_centermarker(row),
                                   axis=1)
df["Vperiph_Af_periph"] = df.apply(lambda row: Vperiph_Af_periphmarker(row),
                                   axis=1)

# code V1A1_or_V2A2, V1A2, V2A1 :

df["V1A1_or_V2A2"] = df.apply(lambda row: V1A1_or_V2A2marker(row), axis=1)
df["V1A2"] = df.apply(lambda row: V1A2marker(row), axis=1)
df["V2A1"] = df.apply(lambda row: V2A1marker(row), axis=1)

df["Ac_type"] = df.apply(lambda row: Ac_typemarker(row), axis=1)


df["ecc"] = df.apply(lambda row: eccmarker(row), axis=1)
# save for GLMM / R formate:

#datastack = {'subjnum': subjnum, 'cue_attn': cue_attn, 'blcnum': blcnum,
#         'trial_num': trial_num, 'condition_type': condition_type, 'flashed': flashed,
#         'number_pressed': number_pressed,'raw_RT': raw_RT,'control': control,
#         'V1A1_or_V2A2': V1A1_or_V2A2, 'V1A2': V1A2, 'V2A1': V2A1, 'Vcent': Vcent,
#         'Vperiph_Af_center': Vperiph_Af_center, 'Vperiph_Af_periph': Vperiph_Af_periph}


#GLMM_frame = pd.DataFrame.from_dict(datastack)

# write to file
df.to_csv(op.join(out_dir, 'GLMMData_ecc.tsv'), sep='\t', index=False)
