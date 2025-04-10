
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 14:22:59 2023

@author: rondin

Analyse and plot data of ambiguous input categorisation implementing 
extended STiMCON with rhythmic (ischronous) and randomised (non-isocrhonous) 
sensory inputs

"""
import sys
sys.path.append("C:\\Users\\rondin\\Desktop\\Projects\\Project 2\\STiMCON-main\\STiMCON-main\\Scripts\\")
import os
import math
import numpy as np
#import STiMCON_plot
import STiMCON_sen
import matplotlib.pyplot as plt
import ColorScheme as cs
cmaps = cs.CCcolormap()
bfi = cs.baseFigInfo()        
import matplotlib
# Set Arial font globally
matplotlib.rcParams['font.family'] = 'Arial'                                  
#%% basic information
fs = 1000;
Freq = 4.0;

#%% Word-node level ambiguity
# create the language model constrainst:
# model is: I eat very nice cake
LMnames = np.array(['I','eat','very','nice','cake'])
feedbackmat = np.zeros([5,5])
feedbackmat[0] = [0, 1, 0, 0, 0]
feedbackmat[1] = [0, 0, 0.2, 0.3, 0.5]
feedbackmat[2] = [0, 0, 0, 1, 0]
feedbackmat[3] = [0, 0, 0, 0, 1]
feedbackmat[4] = [0, 0, 0, 0, 0]

Nnodes = len(feedbackmat)

#%% example specification
# create pseudorandomised stimulus onsets
#N = 5 # total no. of nodes
N = 8 # total no. of nodes, "I eat cake cake cake cake eat AMB"
#stimtime = 1/Freq * (np.linspace(0,(N-1),N) + [np.random.uniform(0,1) for i in range(N)])
stimtime = 1/Freq*np.linspace(0,(N-1),N)

#%% define the parameters of the model
parameters = {"Nnodes": Nnodes,
       "OsFreq": Freq,
       "OsAmp": 1,
       "OsOffset": 0.25*math.pi, #20230823: tweak this? instead of 0.25*math.pi
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
            'onsetdelay': int(0.5/Freq*fs),
            'Nnodes': Nnodes}

## set all the parameters
senObj = STiMCON_sen.modelSen(stimpara,parameters)

#%% read the data
os.chdir(r"C:\\Users\\rondin\\Desktop\\Projects\\Project 2\\STiMCON-main\\STiMCON-main\\Data_AmbiguousInput\\Experiment1\\Isochronous\\")
Freq = 4
fs = 1000
N = 8
stimtime = 1/Freq * np.linspace(0,(N-1),N) # for the length
prop = np.linspace(0,1,12)
delays = np.linspace(-0.25,0.75,20)/Freq*fs # just to get the number
ks = [0,5,10,15,20,30,40,50]

iterations = 100
AllFirstSpTime = np.zeros([len(prop),len(delays),Nnodes,len(ks),iterations])
AllFirstSpTime_relStimOnset = np.zeros([len(prop),len(delays),Nnodes,len(ks),iterations])
FirstActive = np.zeros([len(prop),len(delays),len(ks),iterations])
Phases = np.zeros([iterations])

for iteration in range(iterations):
    AFST_it=np.load(file=r"data_AllFirstSpTime_RandomInput_it{}.npy".format(iteration+1))
    AFST_relStimOnset_it=np.load(file=r"data_AllFirstSpTime_rel_RandomInput_it{}.npy".format(iteration+1))
    FA_it=np.load(file=r"data_FirstActive_RandomInput_it{}.npy".format(iteration+1))
    phi=np.load(file=r"data_Phases_RandomInput_it{}.npy".format(iteration+1))
    # write into original variables
    AllFirstSpTime[:,:,:,:,iteration] = AFST_it
    AllFirstSpTime_relStimOnset[:,:,:,:,iteration] = AFST_relStimOnset_it
    FirstActive[:,:,:,iteration] = FA_it
    Phases[iteration] = phi
    print(iteration)

#%% Single plot across time relative to isochronous (x-axis)
# y-axis: proportion of word node 'cake' in the ambiguous input
# averaged across: iterations
# separately for each K
CH = plt.cm.get_cmap('bwr', 300)

# Define delays
delays = np.linspace(-0.25, 0.75, 20) / Freq * fs
ind_k = 0 # K=20 as example

# Adjust x to only plot valid data
x = (FirstActive - 3) * 2 - 1
x = np.nan_to_num(x, nan=0.0, copy=True)
x = np.mean(x, axis=3)  # Average across phase iterations
x = x[:, :, ind_k]
FirstActiveIt = x

# Create figure
fig = plt.figure(constrained_layout=True, figsize=(bfi.figsize.Col1, 2.2))
gs = fig.add_gridspec(3, 9)
axs = [fig.add_subplot(gs[0:3, 0:5])]

# Flip image upside down
extent = [0, len(delays), 0, len(prop)]
pos = axs[0].imshow(FirstActiveIt[::-1, :], aspect='auto', interpolation='none', origin='lower',
                    cmap=CH, extent=extent)

# Customize y-ticks
ytick_positions = [0, 6, len(prop) - 1]
ytick_labels = [0, 0.5, 1]
axs[0].set_yticks(ytick_positions)
axs[0].set_yticklabels(ytick_labels)

# Colorbar and clim
fig.colorbar(pos, ticks=np.linspace(-1, 1, 3))
pos.set_clim([-1, 1])

# Customize x-axis
x_ticks = np.linspace(delays[0], delays[-1], 5).astype(int)
axs[0].set_xticks(np.linspace(0, len(delays), len(x_ticks)))
axs[0].set_xticklabels(x_ticks)

# Customize y-axis
y_labels = np.around(np.linspace(prop[0], prop[-1], 6), 1)
axs[0].set_yticks(np.linspace(0, len(prop), len(y_labels)))
axs[0].set_yticklabels(y_labels)

# Update title and axis labels
axs[0].set_title(f'First node active (K = {ks[ind_k]})', fontsize=bfi.fontsize.axes)
axs[0].set_xlabel('stim time relative')
axs[0].set_ylabel('proportion "cake" stimulus')  # Updated label

plt.show()

#%% Plot a subplot each time, put the together afterwards
CH = plt.cm.get_cmap('bwr', 300)

# Define delays
delays = np.linspace(-0.25, 0.75, 20) / Freq * fs
ind_k = 7 #[0,1,3,5,7]

# Adjust x to only plot valid data
x = (FirstActive - 3) * 2 - 1
x = np.nan_to_num(x, nan=0.0, copy=True)
x = np.mean(x, axis=3)  # Average across phase iterations
x = x[:, :, ind_k]
FirstActiveIt = x

# Create figure
fig = plt.figure(constrained_layout=True, figsize=(bfi.figsize.Col1, 2.2))
gs = fig.add_gridspec(3, 9)
axs = [fig.add_subplot(gs[0:3, 0:5])]

# Flip image upside down
extent = [0, len(delays), 0, len(prop)]
pos = axs[0].imshow(FirstActiveIt[::-1, :], aspect='auto', interpolation='none', origin='lower',
                    cmap=CH, extent=extent)

# Customize y-ticks
ytick_positions = [0, 6, len(prop) - 1]
ytick_labels = [0, 0.5, 1]
axs[0].set_yticks(ytick_positions)
#axs[0].set_yticklabels([])
axs[0].set_yticklabels(ytick_labels,fontsize=10)

# Colorbar and clim
fig.colorbar(pos, ticks=np.linspace(-1, 1, 3))
pos.set_clim([-1, 1])

# Customize x-axis
x_ticks = np.linspace(delays[0], delays[-1], 5).astype(int)
axs[0].set_xticks(np.linspace(0, len(delays), len(x_ticks)))
axs[0].set_xticklabels(x_ticks,fontsize=10)
#axs[0].set_xticklabels([])  # Hide x-axis labels
# Customize y-axis
y_labels = np.around(np.linspace(prop[0], prop[-1], 6), 1)
axs[0].set_yticks(np.linspace(0, len(prop), len(y_labels)))
axs[0].set_yticklabels(y_labels,fontsize=10)
#axs[0].set_yticklabels([])
# Update title and axis labels
#axs[0].set_title(f'First node active (K = {ks[ind_k]})', fontsize=bfi.fontsize.axes)
#axs[0].set_xlabel('stim time relative')
#axs[0].set_ylabel('proportion "cake" stimulus')  # Updated label

#%% save each subplot (w/o tick labels)
figloc = "C:\\Users\\rondin\\Desktop\\Projects\\Project 2\\writeup\\Figures\\"
fig2D = fig
filenames = 'Figure2D'
fig2D.savefig(figloc + filenames+ '_K={}_i.pdf'.format(ks[ind_k]), format='pdf')

#%% read in non-isochronous data
import os
import glob
import numpy as np
Freq = 4
fs = 1000
prop = np.linspace(0,1,12)
delays = np.linspace(-0.25,0.75,20)/Freq*fs # just to get the number
ks = [0,5,10,15,20,30,40,50]
#ks = [0,5,10,15,20,30,40,50]
stim_Freqs = [2,3,4,5,6,7,8]
Nnodes = 5

# Find current directory
os.chdir(r"C:\\Users\\rondin\\Desktop\\Projects\\Project 2\\STiMCON-main\\STiMCON-main\\Data_AmbiguousInput\\Experiment2\\NonIsochronous\\Version2\\")
# Define the pattern to search for files
file_pattern = '*data_VarRhy_FirstActive_RandomInput_it*'
# Get a list of all files matching the pattern
file_list = glob.glob(file_pattern)

iterations = len(file_list)
AllFirstSpTime = np.zeros([len(prop),len(delays),Nnodes,len(ks),iterations,len(stim_Freqs)])
AllFirstSpTime_relStimOnset = np.zeros([len(prop),len(delays),Nnodes,len(ks),iterations,len(stim_Freqs)])
FirstActive = np.zeros([len(prop),len(delays),len(ks),iterations,len(stim_Freqs)])
SI_all = [] # to save all the sensory input
Phases = np.zeros([iterations])

for iteration in range(len(file_list)):
    filename = file_list[iteration]
    #AFST_it=np.load(file=filename)
    #AFST_relStimOnset_it=np.load(file=r"data_AllFirstSpTime_rel_RandomInput_long_it{}.npy".format(iteration+1))
    FA_it=np.load(file=filename)
    #phi=np.load(file=r"data_Phases_RandomInput_long_it{}.npy".format(iteration+1))
    #SI_it=np.load(file=r"data_SensoryInput_RandomInput_long_it{}.npy".format(iteration+1))
    # write into original variables
    #AllFirstSpTime[:,:,:,:,iteration,:] = AFST_it
    #AllFirstSpTime_relStimOnset[:,:,:,:,iteration,:] = AFST_relStimOnset_it
    FirstActive[:,:,:,iteration,:] = FA_it
    #Phases[iteration] = phi
    #SI_all.append(SI_it)
    print(iteration)

#%% plot one subplot each time and put together
CH = plt.cm.get_cmap('bwr', 300)

# Define delays
ind_k = 7 #[0,1,3,5,7]
stim = 5 # fixed or [0,2,4,5]; max. 6; [2,3,4,5,6,7,8]
delays = np.linspace(0,1,20)/4*fs

# Adjust x to only plot valid data
x = (FirstActive - 3) * 2 - 1
x = np.nan_to_num(x, nan=0.0, copy=True)
x = np.mean(x, axis=3)  # Average across phase iterations
x = x[:,:,ind_k,stim]
FirstActiveIt = x

# Create figure
fig = plt.figure(constrained_layout=True, figsize=(bfi.figsize.Col1, 2.2))
gs = fig.add_gridspec(3, 9)
axs = [fig.add_subplot(gs[0:3, 0:5])]

# Flip image upside down
extent = [0, len(delays), 0, len(prop)]
pos = axs[0].imshow(FirstActiveIt[::-1, :], aspect='auto', interpolation='none', origin='lower',
                    cmap=CH, extent=extent)

# Customize y-ticks
ytick_positions = [0, 6, len(prop) - 1]
ytick_labels = [0, 0.5, 1]
axs[0].set_yticks(ytick_positions)
#axs[0].set_yticklabels([])
axs[0].set_yticklabels(ytick_labels,fontsize=10)

# Colorbar and clim
fig.colorbar(pos, ticks=np.linspace(-1, 1, 3))
pos.set_clim([-1, 1])

# Customize x-axis
x_ticks = np.linspace(delays[0], delays[-1], 5).astype(int)
axs[0].set_xticks(np.linspace(0, len(delays), len(x_ticks)))
axs[0].set_xticklabels(x_ticks,fontsize=10)
#axs[0].set_xticklabels([])  # Hide x-axis labels
# Customize y-axis
y_labels = np.around(np.linspace(prop[0], prop[-1], 6), 1)
axs[0].set_yticks(np.linspace(0, len(prop), len(y_labels)))
axs[0].set_yticklabels(y_labels,fontsize=10)
#axs[0].set_yticklabels([])
# Update title and axis labels
#axs[0].set_title(f'First node active (K = {ks[ind_k]})', fontsize=bfi.fontsize.axes)
#axs[0].set_xlabel('stim time relative')
#axs[0].set_ylabel('proportion "cake" stimulus')  # Updated label

#%% save each subplot (w/o tick labels)
figloc = "C:\\Users\\rondin\\Desktop\\Projects\\Project 2\\writeup\\Figures\\"
fig2D = fig
filenames = 'Figure2D'
fig2D.savefig(figloc + filenames+ '_K={}_iii.pdf'.format(ks[ind_k]), format='pdf')