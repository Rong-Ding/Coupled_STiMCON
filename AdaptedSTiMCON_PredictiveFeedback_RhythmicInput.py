
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 14:22:59 2023

@author: rondin

Implement extended STiMCON when presented with rhythmic input, 
and save the data of feedback activation for each word node
"""
import sys
import os
sys.path.append("~\\Scripts\\")
import math
import numpy as np
import STiMCON_core_v4 as STiMCON_core
import STiMCON_plot
import STiMCON_sen
import matplotlib.pyplot as plt
import seaborn as sns
import ColorScheme as cs
cmaps = cs.CCcolormap()
bfi = cs.baseFigInfo()         
                             
#%% basic information
fs = 1000;
Freq = 4.0;
#Freq = 5.0;

#%% create the language model constrainst:
# model is: I eat very nice cake
LMnames = np.array(['I','eat','very','nice','cake'])
feedbackmat = np.zeros([5,5])
feedbackmat[0] = [0, 1, 0, 0, 0]
feedbackmat[1] = [0, 0, 0.2, 0.3, 0.5]
feedbackmat[2] = [0, 0, 0, 1, 0]
feedbackmat[3] = [0, 0, 0, 0, 1]
feedbackmat[4] = [0, 0, 0, 0, 0]

Nnodes = len(feedbackmat)

#%% define the parameters of the model
parameters = {"Nnodes": Nnodes,
       "OsFreq": Freq,
       "OsAmp": 1,
       "OsOffset": np.random.uniform(0,2)*math.pi, #20230823: tweak this? instead of 0.25*math.pi
       "activation_threshold": 1,
       "feedbackmat": feedbackmat,
       "feedbackinf": 1.5,
       "feedbackdecay": 0.01,
       "feedbackdelay": int(0.9/Freq*fs),
       "latinhibstrength": 0,
       "selfexitation": 0,
       "Inhib": -0.2,
       "fs": fs,
       'LMnames': LMnames}

#%% define the parameters for the sensory input
stimpara = {'word_duration': int(0.5/Freq*fs),
            'onsetdelay': int(0.5/Freq*fs), # the onset delay depends only on the stimtime
            'Nnodes': Nnodes}

## set all the parameters
senObj = STiMCON_sen.modelSen(stimpara,parameters)

#%%########################################
########## MODEL IMPLEMENTATION  ##########
###########################################

# create pseudorandomised stimulus onsets
N = 7 # total no. of nodes
#mu = 1/Freq
#sigma = 0.2*(1/Freq)
stimtime = 1/Freq * (np.linspace(0,(N-1),N))
#stimtime = 1/Freq * (np.linspace(0,(N-1),N) + np.random.normal(mu, sigma, N))

iterations = 1000
ks = [0,5,10,15,20,30,40,50]
Phases = np.zeros([iterations])
AllFirstSpTime = np.zeros([iterations,3,len(ks)])
# Iterations across different starting phases (to cancel this variable out in the future)
# K: coupling strength; we selected multiple values from 0 to 50 to compare between no/weak/strong coupling
for it in range(iterations):
    print(it)
    # randomise the starting phase
    parameters['OsOffset'] = np.random.uniform(0,2)*math.pi # randomise the starting phase
    stimtime = 1/Freq * (np.linspace(0,(N-1),N))
    #parameters['OsOffset'] = 7/8*math.pi
    Phases[it] = parameters['OsOffset']
    seninput = {'stim_ord': np.array([0,1,4,4,4,4,1]),
                'stim_time': stimtime[(0,1,2,3,4,5,6),]*fs,
                'tot_length': 10/Freq*fs} # lengthen the plotting period
    sensory_input = senObj.create_stim(seninput)
    i=0
    for k in ks:
        STiMCON_var = STiMCON_core.modelPara(parameters)
        out = STiMCON_var.runsingle(sensory_input,k)
        spikes = out["spiketimes"]
        # find after the onset the time point where a feedback peak occurs, after 'I eat'
        for inode in range(2,5):
            inx = np.where(spikes[inode][int(stimtime[(6),]*fs):]==1)[0]
            if len(inx) == 0:
                AllFirstSpTime[it][inode-2][i] = np.nan
            else:
                AllFirstSpTime[it][inode-2][i] = inx[0]/fs
        i+=1

#%% save the data
os.chdir(r"~\\Experiment1\\")

np.save(file=r"data_PredictiveFeedback_RhythmicInput_Uniform_AFST.npy",arr=AllFirstSpTime)
np.save("data_PredictiveFeedback_RhythmicInput_Uniform_Phases.npy",arr=Phases)
