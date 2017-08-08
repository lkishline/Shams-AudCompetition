# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 13:18:50 2016

@author: lindsey
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 10:57:56 2016

@author: lindsey
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 14:30:04 2015

@author: lindsey
"""
import expyfun as ea
from expyfun.analyze import barplot
import numpy as np
from os import path as op
from expyfun.io import read_hdf5
import matplotlib.pyplot as mpl
from scipy import stats
mpl.ion()  # interact w/ plot

#num_subjects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

Master_data_array_fission = np.zeros((6, 4))
Master_data_array_fusion = np.zeros((6, 4))
Master_data_array_control = np.zeros((6, 8))
#TEST = np.zeros(18)
Master_data_array_RT = np.zeros(18)
Master_data_array_noisevtone_illu = np.zeros(2)
Master_data_array_centerpull = np.zeros(2)


Master_data_dict = {300: ('fission_count', 'fusion_count', 'reaction_times', 'reaction_times_fission', 'reaction_times_fusion', 'reaction_times_noillu', 'control_illusion_count')}
Master_data_dict_fission = {300: ('c_c_count', 'c_nc_count', 'o_c_1a_count',
                                   'o_nc_1a_count', 'o_c_2a_count',
                                   'o_nc_2a_count')}
Master_data_dict_fusion = {300: ('c_c_count_fusion', 'c_nc_count_fusion',
                                 'o_c_1a_count_fusion', 'o_nc_1a_count_fusion',
                                 'o_c_2a_count_fusion', 'o_nc_2a_count_fusion')}
Master_data_dict_control = {300: ('c_c_count_control', 'c_nc_count_control',
                                 'o_c_1a_count_control', 'o_nc_1a_count_control',
                                 'o_c_2a_count_control', 'o_nc_2a_count_control')}
Master_data_dict_ReactionTime = {300: ('avg_c_c_rt', 'avg_c_nc_rt', 'avg_o_c_1a_rt', 'avg_o_nc_1a_rt',
                                     'avg_o_c_2a_rt', 'avg_o_nc_2a_rt', 'avg_c_c_fission_rt', 'avg_c_nc_fission_rt', 'avg_o_c_1a_fission_rt', 'avg_o_nc_1a_fission_rt',
                                     'avg_o_c_2a_fission_rt', 'avg_o_nc_2a_fission_rt', 'avg_c_c_fusion_rt', 'avg_c_nc_fusion_rt', 'avg_o_c_1a_fusion_rt',
                                     'avg_o_nc_1a_fusion_rt', 'avg_o_c_2a_fusion_rt', 'avg_o_nc_2a_fusion_rt',
                                     'c_c_fusion_rt', 'c_nc_fusion_rt', 'o_c_1a_fusion_rt', 'o_nc_1a_fusion_rt', 'o_c_2a_fusion_rt', 'o_nc_2a_fusion_rt',
                                     'c_c_rt_fission', 'c_nc_rt_fission', 'o_c_1a_rt_fission', 'o_nc_1a_rt_fission', 'o_c_2a_rt_fission', 'o_nc_2a_rt_fission',
                                     'c_c_rt', 'c_nc_rt', 'o_c_1a_rt', 'o_nc_1a_rt', 'o_c_2a_rt', 'o_nc_2a_rt')}
Master_data_dict_centerPull = {300: ('F_A_C_count', 'F_A_S_count')}


illu_post_1flash = []
illu_post_2flash = []

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
### Control trial counts ### marked with control bool

Possible_control_trials = [1, 25, 38, 14, 3, 27, 40, 16, 5, 29, 42, 18, 7, 31,
                           44, 20, 9, 33, 46, 22, 11, 35, 48, 24, 37, 13, 2,
                           26, 39, 15, 4, 28, 41, 17, 6, 30, 43, 19, 8, 32,
                           45, 21, 10, 34, 47, 23, 12, 36]

center_control_trials = [13, 26, 41, 6, 19, 32, 47, 12, 25, 14, 5, 42, 31, 20, 11, 48]
center_congruent_control = [13, 26, 47, 12, 25, 14, 11, 48]
center_noncongruent_control = [41, 6, 19, 32, 5, 42, 31, 20]

outside_control_trials = [37, 2, 39, 15, 4, 28, 17, 30, 43, 8, 45, 21, 10, 34,
                         23, 36, 1, 38, 3, 27, 40, 16, 29, 18, 7, 44, 9, 33,
                         46, 22, 35, 24]
outside_congruent_1away_control = [17, 30, 43, 8, 29, 18, 7, 44]
outside_noncongruent_1away_control = [37, 2, 23, 36, 1, 38, 35, 24]
outside_congruent_2away_control = [15, 28, 45, 10, 27, 16, 9, 46]
outside_noncongruent_2away_control = [39, 4, 21, 34, 3, 40, 33, 22] 

### POST HOC analysis for center pull with Flashbeep 1.0:

Possible_center_pull = [1, 37, 38, 2, 29, 17, 18, 30, 7, 43, 44, 8, 35, 23, 24, 36]

False_auditory_in_center = [1, 38, 2, 17, 30, 43, 8, 35, 24]
False_auditory_on_side = [37, 29, 18, 7, 44, 23, 36]

MasterRaw = []
for cue in ['NOCUE', 'WITHCUE']:
    for sbj in [0, 1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22]:
        # identify subject and block number
        if sbj <= 9:
            subj_num = '40%s' % sbj
        else:
            subj_num = '4%s' % sbj
        work_dir = ('/home/lindsey/Desktop/PythonFiles/Shams/Flashbeeps2.0/%s/Blocks' % cue)
        
        # things we will need:
        Blocks = []
        fission_count = []
        fusion_count = []
        control_count = []
        reaction_times = []
        reaction_times_fission = []
        reaction_times_fusion = []
        reaction_times_noillu = []
        timing_validate = []
        delete_due_to_noresp = []
        delete_due_to_LongRT =[]
        delete_due_to_timing = []
        condition_type_master = []
    
        
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
            Blocks.append(current_block)
            condition_type = d['condition_stamp']
            condition_type_master.append(condition_type)
            control = current_block[::, 3]
            
            #one back analysis:########################################
            #get control bool, presses, and flash num in one array:
            oneback_array = np.vstack((control, flashed))
            foo = [x[0] for x in presses]
            oneback_array = np.vstack((foo, oneback_array))
    
            for p in range(1,108,1):
                if oneback_array[0][p] is None:
                    print 'dangit'
                elif int(oneback_array[0][p]) == 2:    #if presses == 2
                    if int(oneback_array[2][p]) == 1:   # and if flashed == 1
                        if int(oneback_array[2][p-1]) == 1:  # and if the previous flashed was == 1:
                            illu_post_1flash.append([1])    #mark as illusion after one physical flash
                        if int(oneback_array[2][p-1]) == 2:   #and if the previous flashed was == 2:
                            illu_post_2flash.append([2])    #mark as illusion after two physical flashes
            
            
        ### check timing:
            for it in range(108):
                if bool(control[it]) is False:
                    cur_trial_timing_log = flash_timing[it]
                    play_stamp = cur_trial_timing_log[1][0]
                    first_flip = cur_trial_timing_log[0][1]
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
                        third_flip = cur_trial_timing_log[0][3]
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
                        delete_due_to_timing.append([bi, it])
                    else:
                        # if timing is good - check for illusion/fusion trials:
                        p = current_block[:, 0]
                        f = current_block[:, 1]
                        assert p[it] == played[it]
                        
                        
                    
                        if bool(control[it]) is False:
                            if int(flashed[it]) == 1:
                                if presses[it][0] is None:
                                    print bi, it, sbj
                                    delete_due_to_noresp.append([bi, it])
                                elif int(presses[it][0]) == 2:
                                    fission_count.append(int(condition_type[it]))
                                    #MasterRaw.append([sbj, presses[it][0], int(condition_type[it]), 1])
    # RT for fission trials:                                
                                    RT = presses[it][1]
                                    RT = (RT - .116)
                                    if RT <= 1.5 :
                                        reaction_times_fission.append((RT, int(condition_type[it])))
                                        MasterRaw.append([sbj, presses[it][0], int(condition_type[it]), 1, RT])
                                    else:
                                        delete_due_to_LongRT.append([bi, it])
    # RT for no illusion
                                elif int(presses[it][0]) == 1:
                                    RT = presses[it][1]
                                    RT = (RT - .116)
                                    if RT <= 1.5:
                                        reaction_times_noillu.append((RT, int(condition_type[it])))
                                        MasterRaw.append([sbj, presses[it][0], int(condition_type[it]), 0, RT])
                                    else:
                                        delete_due_to_LongRT.append([bi, it])
    
                        if bool(control[it]) is False:
                            if int(flashed[it]) == 2:
                                if presses[it][0] is None:
                                    print bi, it, sbj
                                    delete_due_to_noresp.append([bi, it])
                                elif int(presses[it][0]) == 1:
                                    fusion_count.append(int(condition_type[it]))
                                    #MasterRaw.append([sbj, presses[it][0], int(condition_type[it]), 1])
    # RT for fusion trials:                                
                                    RT = presses[it][1]
                                    RT = (RT - .116)
                                    if RT <= 1.5:
                                        reaction_times_fusion.append((RT, int(condition_type[it])))
                                        MasterRaw.append([sbj, presses[it][0], int(condition_type[it]), 1, RT])
                                    else:
                                        delete_due_to_LongRT.append([bi, it])
    # RT for no illusion
                                elif int(presses[it][0]) == 2:
                                    RT = presses[it][1]
                                    RT = (RT - .116)
                                    if RT <= 1.5:
                                        reaction_times_noillu.append((RT, int(condition_type[it])))
                                        MasterRaw.append([sbj, presses[it][0], int(condition_type[it]), 0, RT])
                                    else:
                                        delete_due_to_LongRT.append([bi, it])
        
                        # pull out reaction times:
                        if bool(control[it]) is False:
                            if presses[it][0] is None:
                                    print "same"
                            else:
                                RT = presses[it][1]
                                RT = (RT - .116)
                                reaction_times.append((RT, int(condition_type[it])))
                                
                if bool(control[it]) is True:    # counting control trial acccuracy
                    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                    if int(flashed[it]) == 2:
                        if presses[it][0] is None:
                            print bi, it, sbj
                            delete_due_to_noresp.append([bi, it])
                        elif int(presses[it][0]) == 1:
                            control_count.append(int(condition_type[it]))
                        if int(flashed[it]) == 1:
                            if presses[it][0] is None:
                                print bi, it, sbj
                                delete_due_to_noresp.append([bi, it])
                            elif int(presses[it][0]) == 2:
                                control_count.append(int(condition_type[it]))
    
            Master_data_dict[subj_num] = [fission_count, fusion_count, reaction_times, reaction_times_fission, reaction_times_fusion, reaction_times_noillu, control_count]
        #Master_data_array_oneback = np.vstack((illu_post_1flash, illu_post_2flash))
        F_A_C_count = []
        F_A_S_count =[]
        counts = []
        for pit in Possible_center_pull:
            if pit in fission_count:
                a = fission_count.count(pit)
                counts.append((a, pit))
            else:
                b = fusion_count.count(pit)
                counts.append((b, pit))
        for cc in counts:
            num_times = int(cc[0])
            type_cc = int(cc[1])
            if type_cc in False_auditory_in_center:
                F_A_C_count.append(num_times)
            if type_cc in False_auditory_on_side:
                F_A_S_count.append(num_times)
        
        Master_data_dict_centerPull[subj_num] = [F_A_C_count, F_A_S_count]
        total_trials_per_FAC = 270.
        total_trials_per_FAS = 210.
        FAC_percentage = ((sum(F_A_C_count)) / total_trials_per_FAC)
        FAS_percentage = ((sum(F_A_S_count)) / total_trials_per_FAS)
        # creat percentage of illusion trials:
            # catigorize into collapsable types
        c_c_count = []
        c_nc_count = []
        o_c_1a_count = []
        o_nc_1a_count = []
        o_c_2a_count = []
        o_nc_2a_count = []
        
        noise_illu_count = []
        tone_illu_count = []
        # read in fission_count and mark how many of each illusion condition occured
        counts = []
        for pit in Possible_fission_trials:
            a = fission_count.count(pit)
            counts.append((a, pit))
        for cc in counts:
            num_times = int(cc[0])
            type_cc = int(cc[1])
            if type_cc in center_fission_trials:
                if type_cc in center_congruent:
                    c_c_count.append(num_times)
                if type_cc in center_noncongruent:
                    c_nc_count.append(num_times)
            if type_cc in outside_fission_trials:
                if type_cc in outside_congruent_1away:
                    o_c_1a_count.append(num_times)
                if type_cc in outside_noncongruent_1away:
                    o_nc_1a_count.append(num_times)
                if type_cc in outside_congruent_2away:
                    o_c_2a_count.append(num_times)
                if type_cc in outside_noncongruent_2away:
                    o_nc_2a_count.append(num_times)
            if type_cc in Possible_illu_2noise_trials:
                noise_illu_count.append(num_times)
            if type_cc in Possible_illu_2tone_trials:
                tone_illu_count.append(num_times)
    
        # run from this point for graphs:
        total_trials_per_fission_point = 120.
        c_c_t = ((sum(c_c_count)) / total_trials_per_fission_point)
        c_nc_t = ((sum(c_nc_count)) / total_trials_per_fission_point)
        o_c_1a_t = ((sum(o_c_1a_count)) / total_trials_per_fission_point)
        o_nc_1a_t = ((sum(o_nc_1a_count)) / total_trials_per_fission_point)
        o_c_2a_t = ((sum(o_c_2a_count)) / total_trials_per_fission_point)
        o_nc_2a_t = ((sum(o_nc_2a_count)) / total_trials_per_fission_point)
    
        Master_data_dict_fission[subj_num] = [c_c_count, c_nc_count, o_c_1a_count,
                                               o_nc_1a_count, o_c_2a_count, o_nc_2a_count]
        
        ## read in fusion_count and mark how many of each fusion condition occured
        c_c_count_fusion = []
        c_nc_count_fusion = []
        o_c_1a_count_fusion = []
        o_nc_1a_count_fusion = []
        o_c_2a_count_fusion = []
        o_nc_2a_count_fusion = []
        counts = []
        for pit in Possible_Fusion_trials:
            a = fusion_count.count(pit)
            counts.append((a, pit))
        # creat percentage of fusion trials:
            # catigorize into collapsable types
        for cc in counts:
            num_times = int(cc[0])
            type_cc = int(cc[1])
            if type_cc in center_fusion_trials:
                if type_cc in center_congruent_fusion:
                    c_c_count_fusion.append(num_times)
                if type_cc in center_noncongruent_fusion:
                    c_nc_count_fusion.append(num_times)
            if type_cc in outside_fusion_trials:
                if type_cc in outside_congruent_1away_fusion:
                    o_c_1a_count_fusion.append(num_times)
                if type_cc in outside_noncongruent_1away_fusion:
                    o_nc_1a_count_fusion.append(num_times)
                if type_cc in outside_congruent_2away_fusion:
                    o_c_2a_count_fusion.append(num_times)
                if type_cc in outside_noncongruent_2away_fusion:
                    o_nc_2a_count_fusion.append(num_times)
        
        # run from this point for graphs:
        total_trials_per_fusion_point = 120.
        c_c_t_f = ((sum(c_c_count_fusion)) / total_trials_per_fusion_point)
        c_nc_t_f = ((sum(c_nc_count_fusion)) / total_trials_per_fusion_point)
        
        o_c_1a_t_f = ((sum(o_c_1a_count_fusion)) / total_trials_per_fusion_point)
        o_nc_1a_t_f = ((sum(o_nc_1a_count_fusion)) / total_trials_per_fusion_point)
        o_c_2a_t_f = ((sum(o_c_2a_count_fusion)) / total_trials_per_fusion_point)
        o_nc_2a_t_f = ((sum(o_nc_2a_count_fusion)) / total_trials_per_fusion_point)
        
        Master_data_dict_fusion[subj_num] = [c_c_count_fusion, c_nc_count_fusion, o_c_1a_count_fusion,
                                   o_nc_1a_count_fusion, o_c_2a_count_fusion, o_nc_2a_count_fusion]
        
        #read in control counts and mark how many illusion trials happened in control condition
        c_c_count_control = []
        c_nc_count_control = []
        o_c_1a_count_control = []
        o_nc_1a_count_control = []
        o_c_2a_count_control = []
        o_nc_2a_count_control = []
        counts = []
        for pit in Possible_control_trials:
            a = control_count.count(pit)
            counts.append((a, pit))
        # creat percentage of fusion trials:
            # catigorize into collapsable types
        for cc in counts:
            num_times = int(cc[0])
            type_cc = int(cc[1])
            if type_cc in center_control_trials:
                if type_cc in center_congruent_control:
                    c_c_count_control.append(num_times)
                if type_cc in center_noncongruent_control:
                    c_nc_count_control.append(num_times)
            if type_cc in outside_control_trials:
                if type_cc in outside_congruent_1away_control:
                    o_c_1a_count_control.append(num_times)
                if type_cc in outside_noncongruent_1away_control:
                    o_nc_1a_count_control.append(num_times)
                if type_cc in outside_congruent_2away_control:
                    o_c_2a_count_control.append(num_times)
                if type_cc in outside_noncongruent_2away_control:
                    o_nc_2a_count_control.append(num_times)
        
        # run from this point for graphs:
        total_trials_per_control_point = 30.
        c_c_t_c = ((sum(c_c_count_control)) / total_trials_per_control_point)
        c_nc_t_c = ((sum(c_nc_count_control)) / total_trials_per_control_point)
        
        o_c_1a_t_c = ((sum(o_c_1a_count_control)) / total_trials_per_control_point)
        o_nc_1a_t_c = ((sum(o_nc_1a_count_control)) / total_trials_per_control_point)
        o_c_2a_t_c = ((sum(o_c_2a_count_control)) / total_trials_per_control_point)
        o_nc_2a_t_c = ((sum(o_nc_2a_count_control)) / total_trials_per_control_point)
        
        Master_data_dict_control[subj_num] = [c_c_count_control, c_nc_count_control,
                                    o_c_1a_count_control, o_nc_1a_count_control,
                                    o_c_2a_count_control, o_nc_2a_count_control]
    
    ### REACTION TIME CALCULATIONS AND PLOTS #####################################
    
        c_c_fusion_rt = []
        c_nc_fusion_rt = []
        o_c_1a_fusion_rt = []
        o_nc_1a_fusion_rt = []
        o_c_2a_fusion_rt = []
        o_nc_2a_fusion_rt = []
        
        c_c_rt_fission = []
        c_nc_rt_fission = []
        o_c_1a_rt_fission = []
        o_nc_1a_rt_fission = []
        o_c_2a_rt_fission = []
        o_nc_2a_rt_fission = []
        
        c_c_rt = []
        c_nc_rt = []
        o_c_1a_rt = []
        o_nc_1a_rt = []
        o_c_2a_rt = []
        o_nc_2a_rt = []
        
        for cc in reaction_times_fusion:
            R_times = float(cc[0])
            type_cc = int(cc[1])
            if type_cc in center_fusion_trials:
                if type_cc in center_congruent_fusion:
                    c_c_fusion_rt.append(R_times)
                if type_cc in center_noncongruent_fusion:
                    c_nc_fusion_rt.append(R_times)
            if type_cc in outside_fusion_trials:
                if type_cc in outside_congruent_1away_fusion:
                    o_c_1a_fusion_rt.append(R_times)
                if type_cc in outside_noncongruent_1away_fusion:
                    o_nc_1a_fusion_rt.append(R_times)
                if type_cc in outside_congruent_2away_fusion:
                    o_c_2a_fusion_rt.append(R_times)
                if type_cc in outside_noncongruent_2away_fusion:
                    o_nc_2a_fusion_rt.append(R_times)
        for cc in reaction_times_fission:
            R_times = float(cc[0])
            type_cc = int(cc[1])
            if type_cc in center_fission_trials:
                if type_cc in center_congruent:
                    c_c_rt_fission.append(R_times)
                if type_cc in center_noncongruent:
                    c_nc_rt_fission.append(R_times)
            if type_cc in outside_fission_trials:
                if type_cc in outside_congruent_1away:
                    o_c_1a_rt_fission.append(R_times)
                if type_cc in outside_noncongruent_1away:
                    o_nc_1a_rt_fission.append(R_times)
                if type_cc in outside_congruent_2away:
                    o_c_2a_rt_fission.append(R_times)
                if type_cc in outside_noncongruent_2away:
                    o_nc_2a_rt_fission.append(R_times)
        for cc in reaction_times_noillu:
            R_times = float(cc[0])
            type_cc = int(cc[1])
            if type_cc in center_fission_trials:
                if type_cc in center_congruent:
                    c_c_rt.append(R_times)
                if type_cc in center_noncongruent:
                    c_nc_rt.append(R_times)
            if type_cc in outside_fission_trials:
                if type_cc in outside_congruent_1away:
                    o_c_1a_rt.append(R_times)
                if type_cc in outside_noncongruent_1away:
                    o_nc_1a_rt.append(R_times)
                if type_cc in outside_congruent_2away:
                    o_c_2a_rt.append(R_times)
                if type_cc in outside_noncongruent_2away:
                    o_nc_2a_rt.append(R_times)
            if type_cc in center_fusion_trials:
                if type_cc in center_congruent_fusion:
                    c_c_rt.append(R_times)
                if type_cc in center_noncongruent_fusion:
                    c_nc_rt.append(R_times)
            if type_cc in outside_fusion_trials:
                if type_cc in outside_congruent_1away_fusion:
                    o_c_1a_rt.append(R_times)
                if type_cc in outside_noncongruent_1away_fusion:
                    o_nc_1a_rt.append(R_times)
                if type_cc in outside_congruent_2away_fusion:
                    o_c_2a_rt.append(R_times)
                if type_cc in outside_noncongruent_2away_fusion:
                    o_nc_2a_rt.append(R_times)
        
        # average reaction times per condition
        if c_c_rt_fission:
            avg_c_c_fission_rt = np.median(c_c_rt_fission)
        if not c_c_rt_fission:
            avg_c_c_fission_rt = 0.0
        if c_nc_rt_fission:
            avg_c_nc_fission_rt = np.median(c_nc_rt_fission)
        if not c_nc_rt_fission:
            avg_c_nc_fission_rt = 0.0
        if o_c_1a_rt_fission:
            avg_o_c_1a_fission_rt = np.median(o_c_1a_rt_fission)
        if not o_c_1a_rt_fission:
            avg_o_c_1a_fission_rt = 0.0
        if o_nc_1a_rt_fission:
            avg_o_nc_1a_fission_rt = np.median(o_nc_1a_rt_fission)
        if not o_nc_1a_rt_fission:
            avg_o_nc_1a_fission_rt = 0.0
        if o_c_2a_rt_fission:
            avg_o_c_2a_fission_rt = np.median(o_c_2a_rt_fission)
        if not o_c_2a_rt_fission:
            avg_o_c_2a_fission_rt = 0.0
        if o_nc_2a_rt_fission:
            avg_o_nc_2a_fission_rt = np.median(o_nc_2a_rt_fission)
        if not o_nc_2a_rt_fission:
            avg_o_nc_2a_fission_rt = 0.0
        if c_c_fusion_rt:
            avg_c_c_fusion_rt = np.median(c_c_fusion_rt)
        if not c_c_fusion_rt:
            avg_c_c_fusion_rt = 0.0
        if c_nc_fusion_rt:
            avg_c_nc_fusion_rt = np.median(c_nc_fusion_rt)
        if not c_nc_fusion_rt:
            avg_c_nc_fusion_rt = 0.0
        if o_c_1a_fusion_rt:
            avg_o_c_1a_fusion_rt = np.median(o_c_1a_fusion_rt)
        if not o_c_1a_fusion_rt:
            avg_o_c_1a_fusion_rt = 0.0
        if o_nc_1a_fusion_rt:
            avg_o_nc_1a_fusion_rt = np.median(o_nc_1a_fusion_rt)
        if not o_nc_1a_fusion_rt:
            avg_o_nc_1a_fusion_rt = 0.0
        if o_c_2a_fusion_rt:
            avg_o_c_2a_fusion_rt = np.median(o_c_2a_fusion_rt)
        if not o_c_2a_fusion_rt:
            avg_o_c_2a_fusion_rt = 0.0
        if o_nc_2a_fusion_rt:
            avg_o_nc_2a_fusion_rt = np.median(o_nc_2a_fusion_rt)
        if not o_nc_2a_fusion_rt:
            avg_o_nc_2a_fusion_rt = 0.0
        
        avg_c_c_rt = np.median(c_c_rt)
        avg_c_nc_rt = np.median(c_nc_rt)
        avg_o_c_1a_rt = np.median(o_c_1a_rt)
        avg_o_nc_1a_rt = np.median(o_nc_1a_rt)
        avg_o_c_2a_rt = np.median(o_c_2a_rt)
        avg_o_nc_2a_rt = np.median(o_nc_2a_rt)
    
        Master_data_dict_ReactionTime[subj_num] = [avg_c_c_rt, avg_c_nc_rt, avg_o_c_1a_rt, avg_o_nc_1a_rt,
                                         avg_o_c_2a_rt, avg_o_nc_2a_rt,avg_c_c_fission_rt, avg_c_nc_fission_rt, avg_o_c_1a_fission_rt, avg_o_nc_1a_fission_rt,
                                         avg_o_c_2a_fission_rt, avg_o_nc_2a_fission_rt, avg_c_c_fusion_rt, avg_c_nc_fusion_rt, avg_o_c_1a_fusion_rt,
                                         avg_o_nc_1a_fusion_rt, avg_o_c_2a_fusion_rt, avg_o_nc_2a_fusion_rt,
                                         c_c_fusion_rt, c_nc_fusion_rt, o_c_1a_fusion_rt, o_nc_1a_fusion_rt, o_c_2a_fusion_rt, o_nc_2a_fusion_rt,
                                         c_c_rt_fission, c_nc_rt_fission, o_c_1a_rt_fission, o_nc_1a_rt_fission, o_c_2a_rt_fission, o_nc_2a_rt_fission,
                                         c_c_rt, c_nc_rt, o_c_1a_rt, o_nc_1a_rt, o_c_2a_rt, o_nc_2a_rt]
    
        A = np.array((c_c_count, c_nc_count, o_c_1a_count, o_nc_1a_count, o_c_2a_count, o_nc_2a_count))
        B = np.array((c_c_count_fusion, c_nc_count_fusion, o_c_1a_count_fusion, o_nc_1a_count_fusion, o_c_2a_count_fusion, o_nc_2a_count_fusion))
        C = np.array((avg_c_c_rt, avg_c_nc_rt, avg_o_c_1a_rt, avg_o_nc_1a_rt, avg_o_c_2a_rt, avg_o_nc_2a_rt, avg_c_c_fusion_rt, avg_c_nc_fusion_rt, avg_o_c_1a_fusion_rt, avg_o_nc_1a_fusion_rt, avg_o_c_2a_fusion_rt, avg_o_nc_2a_fusion_rt, avg_c_c_fission_rt, avg_c_nc_fission_rt, avg_o_c_1a_fission_rt, avg_o_nc_1a_fission_rt, avg_o_c_2a_fission_rt, avg_o_nc_2a_fission_rt))
        D = np.array((np.sum(noise_illu_count), np.sum(tone_illu_count)))
    #    E = np.array(c_c_fusion_rt, c_nc_fusion_rt, o_c_1a_fusion_rt, o_nc_1a_fusion_rt, o_c_2a_fusion_rt, o_nc_2a_fusion_rt,
    #                  c_c_rt_fission, c_nc_rt_fission, o_c_1a_rt_fission, o_nc_1a_rt_fission, o_c_2a_rt_fission, o_nc_2a_rt_fission,
    #                  c_c_rt, c_nc_rt, o_c_1a_rt, o_nc_1a_rt, o_c_2a_rt, o_nc_2a_rt)
        F = np.array((c_c_count_control, c_nc_count_control, o_c_1a_count_control, o_nc_1a_count_control, o_c_2a_count_control, o_nc_2a_count_control))
        G = np.array((FAC_percentage, FAS_percentage))
            
        Master_data_array_fission = np.vstack((Master_data_array_fission, A))
        Master_data_array_fusion = np.vstack((Master_data_array_fusion, B))
        Master_data_array_RT = np.vstack((Master_data_array_RT, C))
        Master_data_array_control = np.vstack((Master_data_array_control, F))
        Master_data_array_noisevtone_illu = np.vstack((Master_data_array_noisevtone_illu, D))
        Master_data_array_centerpull = np.vstack((Master_data_array_centerpull, G))
        #TEST = np.vstack((TEST, E))
    
    print 'finished'
##################################################################################################################################

#### Reaction time averages across subjects:###################################
# delete first row of  zeros from array:
Master_data_array_RT = Master_data_array_RT[1:39]

RT_avg_fisfus_NOCUE = Master_data_array_RT[0:19]
fustest_nocue = RT_avg_fisfus_NOCUE[:,[6, 7, 8, 9, 10, 11]]
fistest_nocue = RT_avg_fisfus_NOCUE[:,[12, 13, 14, 15, 16, 17]]

RT_avg_fisfus_WITHCUE = Master_data_array_RT[19:39]
fustest_withcue = RT_avg_fisfus_WITHCUE[:,[6, 7, 8, 9, 10, 11]]
fistest_withcue = RT_avg_fisfus_WITHCUE[:,[12, 13, 14, 15, 16, 17]]

RT_avg_illusion_NOCUE = np.mean((fustest_nocue, fistest_nocue),axis=0)
RT_avg_illusion_WITHCUE = np.mean((fustest_withcue, fistest_withcue),axis=0)

# average columns (collapse across subjects):
RT_avg_across_conditions_NOCUE = np.median(Master_data_array_RT[0:19], axis=0)
RT_avg_across_conditions_WITHCUE = np.median(Master_data_array_RT[19:39], axis=0)
# plot RT mean across 12 conditions:
#x1 = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]])
#mpl.plot(x1[0,:], RT_avg_across_conditions, 'ro-')
#mpl.show()

# throw out two subjects with long RT times and replot:
#Altered_Master_data_array_RT = np.delete(Master_data_array_RT, (3), axis=0)
#Altered_Master_data_array_RT = np.delete(Altered_Master_data_array_RT, (3), axis=0)
#Altered_RT_avg_across_conditions = np.mean(Altered_Master_data_array_RT, axis=0)

#mpl.plot(x1[0,:], np.squeeze(Altered_RT_avg_across_conditions), 'ro-')
#mpl.show()

RT_avg_across_conditions_NOCUE = np.reshape(RT_avg_across_conditions_NOCUE, (1,18))
RT_avg_across_conditions_WITHCUE = np.reshape(RT_avg_across_conditions_WITHCUE, (1,18))
# plot all subject means with overall mean:
#y1 = (Altered_Master_data_array_RT[0:1])
#y2 = (Altered_Master_data_array_RT[1:2])
#y3 = (Altered_Master_data_array_RT[2:3])
#y4 = (Altered_Master_data_array_RT[3:4])
#y5 = (Altered_Master_data_array_RT[4:5])
#y6 = (Altered_Master_data_array_RT[5:6])

#mpl.plot(x1[0,:], np.squeeze(y1), 'go--')
#mpl.plot(x1[0,:], np.squeeze(y2), 'go--')
#mpl.plot(x1[0,:], np.squeeze(y3), 'go--')
#mpl.plot(x1[0,:], np.squeeze(y4), 'go--')
#mpl.plot(x1[0,:], np.squeeze(y5), 'go--')
#mpl.plot(x1[0,:], np.squeeze(y6), 'go--')
#mpl.plot(x1[0,:], np.squeeze(Altered_RT_avg_across_conditions), 'ro-')
#mpl.show()

### RT congruent vs. Noncongruent:
#RT_avg_congru = np.mean(np.squeeze(Altered_RT_avg_across_conditions)[0:14:2])
#RT_avg_noncongru = np.mean(np.squeeze(Altered_RT_avg_across_conditions)[1:14:2])
#mpl.plot(RT_avg_congru, 'go')
#mpl.plot(RT_avg_noncongru, 'ro')
#mpl.show()


### RT center vs. peripheri:
#RT_avg_center = np.mean(np.squeeze(Altered_RT_avg_across_conditions)[[0, 1, 6, 7]])
#RT_avg_periph = np.mean(np.squeeze(Altered_RT_avg_across_conditions)[[2, 3, 4, 5, 8, 9, 10, 11]])
#mpl.plot(RT_avg_center, 'go')
#mpl.plot(RT_avg_periph, 'ro')
#mpl.show()
#
#from scipy import stats
## legit barplots:
#
#n_groups = 2
#
#means_illusion_RT = tuple(RT_avg_center)
#std_illu_RT = stats.sem(Altered_RT_avg_across_conditions[:,[0,1,6,7]])
#
#means_fusion_RT = tuple(RT_avg_periph)
#std_fus_RT = stats.sem(Altered_RT_avg_across_conditions[:,[2, 3, 4, 5, 8, 9, 10, 11]])
#
#fig, ax = mpl.subplots()
#
#index = np.arange(n_groups)
#bar_width = 0.35
#
#opacity = 0.4
#error_config = {'ecolor': '0.3'}
#
#rects1 = mpl.bar(index, means_illusion_RT, bar_width,
#                 alpha=opacity,
#                 color='b',
#                 yerr=std_illu_RT,
#                 error_kw=error_config,
#                 label='Illusion RT')
#
#rects2 = mpl.bar(index + bar_width, means_fusion_RT, bar_width,
#                 alpha=opacity,
#                 color='r',
#                 yerr=std_fus_RT,
#                 error_kw=error_config,
#                 label='Fusion RT')
#
#mpl.xlabel('Condition')
#mpl.ylabel('Seconds')
#mpl.title('Reaction time Center vs. Periphery')
#mpl.xticks(index + bar_width, ('C','P'))
#mpl.legend(loc=3)
#
#mpl.tight_layout()
#mpl.show()

### RT illusion vs. fusion:
#RT_overallavg_illusion = np.mean(np.squeeze(Altered_RT_avg_across_conditions)[[0, 1, 2, 3, 4, 5]])
#RT_overallavg_fusion = np.mean(np.squeeze(Altered_RT_avg_across_conditions)[[6, 7, 8, 9, 10, 11]])
#mpl.plot(RT_overallavg_illusion, 'go')
#mpl.plot(RT_overallavg_fusion, 'ro')
#mpl.show()
RT_avg_across_conditions_NOCUE_noillu = RT_avg_across_conditions_NOCUE[:,[0, 1, 2, 3, 4, 5]]
RT_avg_across_conditions_NOCUE_fusion = RT_avg_across_conditions_NOCUE[:,[6, 7, 8, 9, 10, 11]]
RT_avg_across_conditions_NOCUE_fission = RT_avg_across_conditions_NOCUE[:,[12, 13, 14, 15, 16, 17]]

#RT_avg_across_conditions_NOCUE_Illusion = np.mean(RT_avg_across_conditions_NOCUE[:,[6, 7, 8, 9, 10, 11]], RT_avg_across_conditions_NOCUE[:,[12, 13, 14, 15, 16, 17]])

RT_avg_across_conditions_WITHCUE_noillu = RT_avg_across_conditions_WITHCUE[:,[0, 1, 2, 3, 4, 5]]
RT_avg_across_conditions_WITHCUE_fusion = RT_avg_across_conditions_WITHCUE[:,[6, 7, 8, 9, 10, 11]]
RT_avg_across_conditions_WITHCUE_fission = RT_avg_across_conditions_WITHCUE[:,[12, 13, 14, 15, 16, 17]]

#RT_avg_across_conditions_WITHCUE_Illusion = np.mean(RT_avg_across_conditions_WITHCUE[:,[6, 7, 8, 9, 10, 11]], RT_avg_across_conditions_WITHCUE[:,[12, 13, 14, 15, 16, 17]])
#Altered_RT_avg_across_conditions_illusion = np.mean((np.vstack((Altered_RT_avg_across_conditions_fusion,Altered_RT_avg_across_conditions_fission))), axis=0)

#Altered_RT_avg_across_conditions_noillu = [5.996190282146857120e-01, 6.016852339205163158e-01, 6.236619811175836414e-01, 6.299984896311288107e-01, 6.292734008080895780e-01, 6.278867691713501120e-01]
#Altered_RT_avg_across_conditions_fusion = [6.362971061271498474e-01, 7.290366915067980624e-01, 7.225559741127328683e-01, 7.003186497493808504e-01, 7.416741616811025617e-01, 7.108707399529350379e-01]
#Altered_RT_avg_across_conditions_fission = [5.882876451817855568e-01, 6.011257930348857803e-01, 6.615607085396681963e-01, 7.298764679692294477e-01, 7.587036021380031414e-01, 7.923393451662690268e-01]
RT_avg_across_conditions_NOCUE_noillu[0].tolist()
RT_avg_across_conditions_NOCUE_fusion[0].tolist()
RT_avg_across_conditions_NOCUE_fission[0].tolist()

RT_avg_across_conditions_WITHCUE_noillu[0].tolist()
RT_avg_across_conditions_WITHCUE_fusion[0].tolist()
RT_avg_across_conditions_WITHCUE_fission[0].tolist()
OverAll_RT_avg_across_conditions_NOCUE = np.mean([RT_avg_across_conditions_NOCUE_fusion, RT_avg_across_conditions_NOCUE_fission], axis=0)
OverAll_RT_avg_across_conditions_WITHCUE = np.mean([RT_avg_across_conditions_WITHCUE_fusion, RT_avg_across_conditions_WITHCUE_fission], axis=0)
#from scipy import stats
## legit barplots:
#
errorbararray_WITHCUE = np.mean([Master_data_array_RT[19:39,[6,7,8,9,10,11]], Master_data_array_RT[19:39,[12, 13, 14, 15, 16, 17]]], axis=0)
errorbararray_NOCUE = np.mean([Master_data_array_RT[0:19,[6,7,8,9,10,11]], Master_data_array_RT[0:19,[12, 13, 14, 15, 16, 17]]], axis=0)

mpl.legend(bbox_to_anchor=(1,1), bbox_transform=mpl.gcf().transFigure)
n_groups = 6

NOCUERT_noillu = tuple(np.reshape((RT_avg_across_conditions_NOCUE_noillu), (6,)))
NOCUERT_std_noillu_RT = stats.sem(Master_data_array_RT[0:19,[0,1,2,3,4,5]])

NOCUERT_fusfis = tuple(np.reshape((OverAll_RT_avg_across_conditions_NOCUE), (6,)))
NOCUERT_std_overall_illu_RT = stats.sem(errorbararray_NOCUE)

WITHCUERT_noillu = tuple(np.reshape((RT_avg_across_conditions_WITHCUE_noillu), (6,)))
WITHCUERT_std_noillu_RT = stats.sem(Master_data_array_RT[19:39,[0,1,2,3,4,5]])

WITHCUERT_fusfis = tuple(np.reshape((OverAll_RT_avg_across_conditions_WITHCUE), (6,)))
WITHCUERT_std_overall_illu_RT = stats.sem(errorbararray_WITHCUE)


fig, ax = mpl.subplots()

index = np.arange(n_groups)
bar_width = 0.2

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = mpl.bar(index, NOCUERT_noillu, bar_width,
                 alpha=opacity,
                 color='grey',
                 yerr=NOCUERT_std_noillu_RT,
                 error_kw=error_config,
                 label='NO CUE No Illusion RT')
                 
rects2 = mpl.bar(index + bar_width, NOCUERT_fusfis, bar_width,
                 alpha=opacity,
                 color='black',
                 yerr=NOCUERT_std_overall_illu_RT,
                 error_kw=error_config,
                 label='NO CUE Illusion RT')

#rects3 = mpl.bar(index + bar_width + bar_width, WITHCUERT_fusfis, bar_width,
#                 alpha=opacity,
#                 color='blue',
#                 yerr=WITHCUERT_std_overall_illu_RT,
#                 error_kw=error_config,
#                 label='WITH CUE Illusion RT')
rects3 = mpl.bar(index + bar_width + bar_width, WITHCUERT_noillu, bar_width,
                 alpha=opacity,
                 color='lightblue',
                 yerr=WITHCUERT_std_noillu_RT,
                 error_kw=error_config,
                 label='WITH CUE No Illusion RT')
                 
#rects4 = mpl.bar(index + bar_width + bar_width + bar_width, WITHCUERT_noillu, bar_width,
#                 alpha=opacity,
#                 color='lightblue',
#                 yerr=WITHCUERT_std_noillu_RT,
#                 error_kw=error_config,
#                 label='WITH CUE No Illusion RT')
rects4 = mpl.bar(index + bar_width + bar_width + bar_width, WITHCUERT_fusfis, bar_width,
                 alpha=opacity,
                 color='blue',
                 yerr=WITHCUERT_std_overall_illu_RT,
                 error_kw=error_config,
                 label='WITH CUE Illusion RT')

#mpl.xlabel('Condition')
mpl.xticks(index + bar_width + bar_width, ('C', 'Ce', 'L', 'La', 'Lat', 'Lat'))
mpl.legend(bbox_to_anchor=(1.02,1),loc=2, borderaxespad=0.)
mpl.tight_layout()
mpl.show()

#mpl.plot(NOCUE_Added_Fu_Illu_array.T, '-ko')
#mpl.show()
#
#mpl.plot(WITHCUE_Added_Fu_Illu_array.T, '-bo')
#mpl.show()

#n_groups = 6
#
#no_illusion_RT = tuple(Altered_RT_avg_across_conditions_noillu)
#std_noillu_RT = stats.sem(Altered_Master_data_array_RT[:,[0,1,2,3,4,5]])
#
#means_fusion_RT = tuple(Altered_RT_avg_across_conditions_fusion)
#std_fus_RT = stats.sem(Altered_Master_data_array_RT[:,[6,7,8,9,10,11]])
#
#means_fission_RT = tuple(Altered_RT_avg_across_conditions_fission)
#std_fis_RT = stats.sem(Altered_Master_data_array_RT[:,[12, 13, 14, 15, 16, 17]])

#fig, ax = mpl.subplots()
#
#index = np.arange(n_groups)
#bar_width = 0.30
#
#opacity = 0.4
#error_config = {'ecolor': '0.3'}
#
#rects1 = mpl.bar(index, no_illusion_RT, bar_width,
#                 alpha=opacity,
#                 color='b',
#                 yerr=std_noillu_RT,
#                 error_kw=error_config,
#                 label='No Illusion RT')
#
#rects2 = mpl.bar(index + bar_width, means_fusion_RT, bar_width,
#                 alpha=opacity,
#                 color='r',
#                 yerr=std_fus_RT,
#                 error_kw=error_config,
#                 label='Fusion RT')
#
#rects3 = mpl.bar(index + bar_width + bar_width, means_fission_RT, bar_width,
#                 alpha=opacity,
#                 color='g',
#                 yerr=std_fis_RT,
#                 error_kw=error_config,
#                 label='Fission RT')
#
#mpl.xlabel('Condition')
#mpl.ylabel('Seconds')
#mpl.title('Reaction time across Condition')
#mpl.xticks(index + bar_width, ('C', 'C', 'P', 'P', 'P', 'P'))
##mpl.legend(loc=3)
#
#mpl.tight_layout()
#mpl.show()

### RT tone vs. noise:
#avg_Master_data_array_noisevtone_illu = np.mean(Master_data_array_noisevtone_illu, axis=0)
#
#### Center pull ##############################################################
#Altered_Master_data_array_centerpull = Master_data_array_centerpull[1:]
#Overall_pull = np.mean(Altered_Master_data_array_centerpull, axis=0)
#n_groups = 2
#
#means_centerpull = tuple(Overall_pull)
#std_centerpull = stats.sem(Altered_Master_data_array_centerpull)
#
#fig, ax = mpl.subplots()
#
#index = np.arange(n_groups)
#bar_width = 0.35
#
#opacity = 0.4
#error_config = {'ecolor': '0.3'}
#
#rects1 = mpl.bar(index, means_centerpull, bar_width,
#                 alpha=opacity,
#                 color='green',
#                 yerr=std_centerpull,
#                 error_kw=error_config,
#                 label='No Illusion')
#
#
#mpl.xlabel('Center vs. Side pull')
#mpl.ylabel('Proportion Illusion')
##mpl.title('Percent Illusion across conditions')
#mpl.xticks(index + bar_width, ('False Aud Center', 'False Aud Side'))
##mpl.legend()
#
#mpl.tight_layout()
#mpl.show()


### Illusion #################################################################
#clip first six empty rows:
Master_data_array_fission = Master_data_array_fission[6:]
#split into NOCUE and WITHCUE:
NOCUE_data_array_fission = Master_data_array_fission[:114]
WITHCUE_data_array_fission = Master_data_array_fission[114:228]
# sum across rows
NOCUE_Altered_data_array_fission = np.sum(NOCUE_data_array_fission, axis=1)/120.
WITHCUE_Altered_data_array_fission = np.sum(WITHCUE_data_array_fission, axis=1)/120.
# reshape so can average across subjects:
NOCUE_Altered_data_array_fission = np.reshape(NOCUE_Altered_data_array_fission, (19, 6))
WITHCUE_Altered_data_array_fission = np.reshape(WITHCUE_Altered_data_array_fission, (19, 6))
#avg across subjects to six conditions:
NOCUE_avg_altered_fission = np.mean(NOCUE_Altered_data_array_fission, axis=0)
WITHCUE_avg_altered_fission = np.mean(WITHCUE_Altered_data_array_fission, axis=0)
#mpl.plot(avg_altered_fission, 'go')
#mpl.show()

### Fusion ###################################################################
#clip first six empty rows:
Master_data_array_fusion = Master_data_array_fusion[6:]
#split into NOCUE and WITHCUE:
NOCUE_data_array_fusion = Master_data_array_fusion[:114]
WITHCUE_data_array_fusion = Master_data_array_fusion[114:228]
# sum across rows
NOCUE_Altered_data_array_fusion = np.sum(NOCUE_data_array_fusion, axis=1)/120.
WITHCUE_Altered_data_array_fusion = np.sum(WITHCUE_data_array_fusion, axis=1)/120.
# reshape so can average across subjects:
NOCUE_Altered_data_array_fusion = np.reshape(NOCUE_Altered_data_array_fusion, (19, 6))
WITHCUE_Altered_data_array_fusion = np.reshape(WITHCUE_Altered_data_array_fusion, (19, 6))
#avg across subjects to six conditions:
NOCUE_avg_altered_fusion = np.mean(NOCUE_Altered_data_array_fusion, axis=0)
WITHCUE_avg_altered_fusion = np.mean(WITHCUE_Altered_data_array_fusion, axis=0)
#mpl.plot(avg_altered_fission, 'go')
#mpl.show()

### Overall illu/fu ##########################################################
# add together fusion and illusion trials:
NOCUE_Added_Fu_Illu_array = ((np.sum(NOCUE_data_array_fission, axis=1)) + (np.sum(NOCUE_data_array_fusion, axis=1)))/240.
WITHCUE_Added_Fu_Illu_array = ((np.sum(WITHCUE_data_array_fission, axis=1)) + (np.sum(WITHCUE_data_array_fusion, axis=1)))/240.

# reshape so can average across subjects:
NOCUE_Added_Fu_Illu_array = np.reshape(NOCUE_Added_Fu_Illu_array, (19, 6))
WITHCUE_Added_Fu_Illu_array = np.reshape(WITHCUE_Added_Fu_Illu_array, (19, 6))
#avg across subjects to six conditions:
NOCUE_avg_Added_Fu_Illu_array = np.mean(NOCUE_Added_Fu_Illu_array, axis=0)
WITHCUE_avg_Added_Fu_Illu_array = np.mean(WITHCUE_Added_Fu_Illu_array, axis=0)
#mpl.plot(avg_Added_Fu_Illu_array, 'go')
#mpl.show()

#NoIllusioncounts = np.zeros(6)
#sbjnums = [301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316]
##sbjnums = [301]
#conditions = 6
#for subj in sbjnums:
#    RAW = Master_data_dict_ReactionTime['%s' % subj]
#    NoIRAW = RAW[30:36]
#    cond6 = []
#    for c in range(conditions):
#        cond_lengths = len(NoIRAW[c])
#        cond_lengthavg = cond_lengths/240.
#        cond6.append(cond_lengthavg)
#    NoIllusioncounts = np.vstack((NoIllusioncounts, cond6))
##cut off first row of zeros:
#NoIllusioncounts = NoIllusioncounts[1:]
#avg_NoIllusioncounts = np.mean(NoIllusioncounts, axis = 0)

### Overall control trials:

#Altered_data_array_control = np.sum(Master_data_array_control, axis=1)/30.
#Altered_data_array_control = Altered_data_array_control[6:]
#Altered_data_array_control = np.reshape(Altered_data_array_control, (16,6))
#avg_altered_control = np.mean(Altered_data_array_control, axis=0)


n_groups = 6

NOCUE_means_illusion = tuple(NOCUE_avg_Added_Fu_Illu_array)
NOCUE_std_illusion = stats.sem(NOCUE_Added_Fu_Illu_array)

WITHCUE_means_illusion = tuple(WITHCUE_avg_Added_Fu_Illu_array)
WITHCUE_std_illu = stats.sem(WITHCUE_Added_Fu_Illu_array)

fig, ax = mpl.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = mpl.bar(index, NOCUE_means_illusion, bar_width,
                 alpha=opacity,
                 color='black',
                 yerr=NOCUE_std_illusion,
                 error_kw=error_config,
                 label='NO CUE Illusion')

rects2 = mpl.bar(index + bar_width, WITHCUE_means_illusion, bar_width,
                 alpha=opacity,
                 color='b',
                 yerr=WITHCUE_std_illu,
                 error_kw=error_config,
                 label='WITH CUE Illusion')

#mpl.xlabel('Condition')
mpl.ylabel('Percent Illusion')
mpl.title('Percent Illusion Across Conditions')
mpl.xticks(index + bar_width, ('CenterCongru', 'CenterIncongru', 'LateralNearCongru', 'LateralNearIncongru', 'LateralFarCongru', 'LateralFarIncongru'))
mpl.legend(loc=3)

mpl.tight_layout()
mpl.show()

#mpl.plot(NOCUE_Added_Fu_Illu_array.T, '-ko')
#mpl.show()
#
#mpl.plot(WITHCUE_Added_Fu_Illu_array.T, '-bo')
#mpl.show()

a = NOCUE_Added_Fu_Illu_array.flatten()
b = WITHCUE_Added_Fu_Illu_array.flatten()

c = np.empty((a.size + b.size,), dtype=a.dtype)
c[0::2] = a
c[1::2] = b
c = c.reshape((19,12))
mpl.plot(c.T)
mpl.show()



e = NOCUE_avg_Added_Fu_Illu_array.flatten()
f = WITHCUE_avg_Added_Fu_Illu_array.flatten()

g = np.empty((e.size + f.size,), dtype=a.dtype)
g[0::2] = e
g[1::2] = f

h = NOCUE_Added_Fu_Illu_array.flatten()
i = WITHCUE_Added_Fu_Illu_array.flatten()

j = np.empty((h.size + i.size,), dtype=a.dtype)
j[0::2] = h
j[1::2] = i
j = j.reshape((19,12))

n_groups = 12

NOCUE_means_illusion = tuple(g)
NOCUE_std_illusion = stats.sem(j)


fig, ax = mpl.subplots()

index = np.arange(n_groups)
bar_width = 0.50

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = mpl.bar(index - (bar_width/2), NOCUE_means_illusion, bar_width,
                 alpha=opacity,
                 color='black',
                 yerr=NOCUE_std_illusion,
                 error_kw=error_config,
                 label='Percent Illusion')


#mpl.xlabel('Condition')
mpl.ylabel('Percent Illusion')
mpl.title('Percent Illusion Across Conditions')
mpl.xticks(index - (bar_width/2), ('NOCUECC', 'WITHCUECC', 'NOCUECInc', 'WITHCUECInc', 'NOCUELNC', 'WITHCUELNC', 'NOCUELNInc', 'WITHCUELNInc', 'NOCUELFC', 'WITHCUELFC', 'NOCUELFInc', 'WITHCUELFInc'))
#mpl.legend(loc=3)

mpl.tight_layout()
mpl.show()

a = NOCUE_Added_Fu_Illu_array.flatten()
b = WITHCUE_Added_Fu_Illu_array.flatten()

c = np.empty((a.size + b.size,), dtype=a.dtype)
c[0::2] = a
c[1::2] = b
c = c.reshape((19,12))
mpl.plot(c.T)
mpl.show()

ea.analyze.barplot()
#n_groups = 6
#
#means_illusion = tuple(avg_Added_Fu_Illu_array)
#std_illu = stats.sem(Added_Fu_Illu_array)
#
#means_control = tuple(avg_altered_control)
#std_control = stats.sem(Altered_data_array_control)
#
#fig, ax = mpl.subplots()
#
#index = np.arange(n_groups)
#bar_width = 0.35
#
#opacity = 0.4
#error_config = {'ecolor': '0.3'}
#
#rects1 = mpl.bar(index, means_illusion, bar_width,
#                 alpha=opacity,
#                 color='b',
#                 yerr=std_illu,
#                 error_kw=error_config,
#                 label='Illusion')
#
#rects2 = mpl.bar(index, means_control, bar_width,
#                 alpha=opacity,
#                 color='r',
#                 yerr=std_control,
#                 error_kw=error_config,
#                 label='Control')
#
#mpl.xlabel('Condition')
#mpl.ylabel('Percent Illusion')
#mpl.title('Percent Illusion across conditions')
#mpl.xticks(index + bar_width, ('C', 'C', 'P', 'P', 'P', 'P'))
#mpl.legend()
#
#mpl.tight_layout()
#mpl.show()

# overall individual subjects:
#mpl.plot(Added_Fu_Illu_array.T)
#mpl.show()
#
#
#
#

# legit barplots:

n_groups = 6

means_illusion = tuple(avg_altered_fission)
std_illu = stats.sem(Altered_data_array_fission)

means_fusion = tuple(avg_altered_fusion)
std_fus = stats.sem(Altered_data_array_fusion)

fig, ax = mpl.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = mpl.bar(index, means_illusion, bar_width,
                 alpha=opacity,
                 color='b',
                 yerr=std_illu,
                 error_kw=error_config,
                 label='Fission')

rects2 = mpl.bar(index + bar_width, means_fusion, bar_width,
                 alpha=opacity,
                 color='r',
                 yerr=std_fus,
                 error_kw=error_config,
                 label='Fusion')

mpl.xlabel('Condition')
mpl.ylabel('Percent Illusion')
mpl.title('Percent illusion across conditions')
mpl.xticks(index + bar_width, ('C', 'C', 'P', 'P', 'P', 'P'))
mpl.legend()

mpl.tight_layout()
mpl.show()

subtract_from_mean_fission = Altered_data_array_fission.T - Altered_data_array_fission.mean(axis=1, keepdims=True).T
subtract_from_mean_fusion = Altered_data_array_fusion.T - Altered_data_array_fusion.mean(axis=1, keepdims=True).T

#mpl.plot(subtract_from_mean_fusion, subtract_from_mean_fission)  # people suceptable to fission also to fusion
#mpl.show()

#mpl.plot(Altered_data_array_illusion.T - Altered_data_array_illusion.mean(axis=1, keepdims=True).T)
#mpl.show()

#mpl.plot(Altered_data_array_fusion.T - Altered_data_array_fusion.mean(axis=1, keepdims=True).T)
#mpl.show()

overall_illusion_array = (Altered_data_array_fission + Altered_data_array_fusion)/2
#mpl.plot(overall_illusion_array.T - overall_illusion_array.mean(axis=1, keepdims=True).T)
#mpl.show()

# Chi-squared fit for reaction times:
# data for no illusion across six conditions:
import itertools
sbjnums = [301, 302]
Fus = []
Fis = []
Noi = []
for subj in sbjnums:
    RAW = Master_data_dict_ReactionTime['%s' % subj]
    RAW_fusion = RAW[18:24]
    Fus.append(RAW_fusion)
    RAW_fission = RAW[24:30]
    Fis.append(RAW_fission)
    RAW_noillu = RAW[30:37]
    Noi.append(RAW_noillu)


from expyfun.analyze import rt_chisq
np.column_stack()
#chi_fit_for301 = rt_chisq(, axis=0)
# verify that it worked:
mpl.ion()
x = np.abs(np.random.randn(10000) + 1)
lsp = np.linspace(np.floor(np.amin(x)), np.ceil(np.amax(x)), 100)
df, loc, scale = stats.chi2.fit(x, floc=0)
pdf = stats.chi2.pdf(lsp, df, scale=scale)
mpl.plot(lsp, pdf)
mpl.hist(x, normed=True)
