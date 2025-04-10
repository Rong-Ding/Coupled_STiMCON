
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 14:22:59 2023

@author: rondin

Analyse and plot data of feedback activation per word node by implementing extended STiMCON 
with rhythmic (ischronous) and randomised (non-isocrhonous) sensory inputs
"""
import sys
import os
sys.path.append("~\\Scripts\\")
import math
import numpy as np
import STiMCON_sen
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import ColorScheme as cs
cmaps = cs.CCcolormap()
bfi = cs.baseFigInfo()       
# Set Arial font globally
matplotlib.rcParams['font.family'] = 'Arial'
                  
#%% Run all model-relevant variables again to retrieve and analyse the data
fs = 1000;
Freq = 4.0;
#Freq = 5.0;

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

# define the parameters of the model
parameters = {"Nnodes": Nnodes,
       "OsFreq": Freq,
       "OsAmp": 1,
       "OsOffset": np.random.uniform(0,2)*math.pi,
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

# define the parameters for the sensory input
stimpara = {'word_duration': int(0.5/Freq*fs),
            'onsetdelay': int(0.5/Freq*fs), # the onset delay depends only on the stimtime
            'Nnodes': Nnodes}

## set all the parameters
senObj = STiMCON_sen.modelSen(stimpara,parameters)

N = 7 # total no. of nodes

#%% Figure 1A: comparison Percentage activation
# plotting: both rhythmic and random in one go
# import data
os.chdir(r"~\\Experiment1\\")
AFST_rhy = np.load(file=r"data_PredictiveFeedback_RhythmicInput_Uniform_AFST.npy")
AFST_ran = np.load(file=r"data_PredictiveFeedback_RandomInput_Uniform_AFST.npy")

ks = [0,5,10,15,20,30,40,50]

#%% Figure 1A: plotting
# rhythmic
nans_k_rhy = np.zeros([len(ks),3])
for k_i in range(len(ks)):
    for inode in range(3):
        nans_k_rhy[k_i,inode] = np.count_nonzero(~np.isnan(AFST_rhy[:,inode,k_i]))     
print(nans_k_rhy)
# random
nans_k_ran = np.zeros([len(ks),3])
for k_i in range(len(ks)):
    for inode in range(3):
        nans_k_ran[k_i,inode] = np.count_nonzero(~np.isnan(AFST_ran[:,inode,k_i]))     
print(nans_k_ran)

# plotting: two images, sharing the same x-axis 
x_pos = np.arange(len(ks))
lbl = ['very','nice','cake']
# Set fixed width and maintain square aspect ratio
fig_width = bfi.figsize.Col1
fig_height = fig_width * 2  # Maintain proportionality

# Create subplots with shared x-axis
fig_perc, axs = plt.subplots(2, 1, figsize=(fig_width, fig_height), sharex=True, gridspec_kw={'hspace': 0.1})

# Plot for rhythmic data
width = 0.2
for inode in range(3):
    axs[0].bar(x_pos + (inode - 1) * width, nans_k_rhy[:, inode]/10, width=width)
#axs[0].set_title("Feedback Activation - Rhythmic", fontsize=14, fontname='Arial')
axs[0].tick_params(axis='y', labelsize=8)

# Plot for random data
for inode in range(3):
    axs[1].bar(x_pos + (inode - 1) * width, nans_k_ran[:, inode]/10, width=width)
#axs[1].set_title("Feedback Activation - Random", fontsize=14, fontname='Arial')
axs[1].tick_params(axis='y', labelsize=8)

# Shared x-axis labels
axs[1].set_xlabel('Coupling strength K', fontsize=10, fontname='Arial')
plt.xticks(x_pos, ks, fontsize=8, fontname='Arial')

# General y-axis label
fig_perc.text(0.005, 0.5, 'Percentage feedback activation', va='center', rotation='vertical', 
              fontsize=10, fontname='Arial')

# Shared legend positioned closer to the x-axis
fig_perc.legend(lbl, loc='lower center', bbox_to_anchor=(0.5, 0.01), fontsize=8, ncol=3)

# Adjust layout to fit elements nicely
plt.tight_layout(rect=[0.05, 0.08, 1, 1])  # Leave space for the shared y-label and legend

# Add titles per subplot
axs[0].set_title("Isochronous", fontsize=10, fontname='Arial')  # Added title
axs[1].set_title("Non-Isochronous", fontsize=10, fontname='Arial')  # Added title

# Show the figure
plt.show()

#%% Figure 2A: save
fig2A = fig_perc
figloc = "~\\Figures\\"
filenames = 'Figure2A'
fig2A.savefig(figloc + filenames+ '.pdf', format='pdf',bbox_inches='tight')

#%% Figure 1B: phase code timing (violin plot)
figsize=(fig_width, fig_height)

# Define coupling strengths and labels
ks = [0, 5, 10, 15, 20, 30, 40, 50]
k_labels = ['0', '5', '10', '15', '20', '30', '40', '50']
k_i = len(ks)

# Set color palette
colors = sns.color_palette("Set3", len(ks))
positions = np.arange(len(ks))

# Create figure with two subplots (shared x-axis & y-axis)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(bfi.figsize.Col1, bfi.figsize.Col1*2), dpi=600, sharex=True, sharey=True)

# Function to plot violin while keeping the distribution unchanged
def plot_violin(ax, data_matrix, title):
    for i, k in enumerate(ks):
        data = data_matrix[:, i]
        valid_data = data[~np.isnan(data)]  # Remove NaNs

        # Draw full violin using all valid data
        parts = ax.violinplot(valid_data, positions=[positions[i]], showmeans=True, showmedians=False, widths=0.8)
        
        for pc in parts['bodies']:
            pc.set_facecolor(colors[i])
            pc.set_edgecolor('black')
            pc.set_alpha(0.7)

        parts['cmeans'].set_color('red')
        parts['cmeans'].set_linewidth(2)

        # Sample a subset of points for scatter plot only (keeping distribution intact)
        sample_size = min(len(valid_data), 100)  # Show max 100 points
        sampled_data = np.random.choice(valid_data, sample_size, replace=False) if len(valid_data) > 50 else valid_data
        
        # Apply jitter only to the displayed scatter points
        jitter = (np.random.rand(len(sampled_data)) - 0.5) * 0.4
        ax.scatter(np.full(len(sampled_data), positions[i]) + jitter, sampled_data, alpha=0.6, color=colors[i], edgecolor='black', s=20, zorder=3)

    ax.set_title(title, fontsize=10)
    ax.grid(True, which='both', axis='y', linestyle='--', alpha=0.6)
    ax.tick_params(axis='both', labelsize=10)  # Ensure y-tick font size is 10
    
# Plot for AFST_rhy (isochronous)
plot_violin(ax1, AFST_rhy[:, 2, :] - AFST_rhy[:, 1, :], "Isochronous")

# Plot for AFST_ran (random)
plot_violin(ax2, AFST_ran[:, 2, :] - AFST_ran[:, 1, :], "Non-isochronous")

# Customize x-axis labels
ax2.set_xticks(positions)
ax2.set_xticklabels(k_labels, fontsize=10)
ax2.set_xlabel('Coupling strength', fontsize=10)

# Shared y-axis label for the whole figure
fig.text(0.03, 0.5, "Feedback activation difference ('cake' - 'nice') (s)", va='center', ha='center', rotation='vertical', fontsize=10)

# Set uniform y-axis limits dynamically, ignoring NaNs
#y_min = np.nanmin([np.nanmin(AFST_rhy[:, 2, :] - AFST_rhy[:, 1, :]), np.nanmin(AFST_ran[:, 2, :] - AFST_ran[:, 1, :])])
#y_max = np.nanmax([np.nanmax(AFST_rhy[:, 2, :] - AFST_rhy[:, 1, :]), np.nanmax(AFST_ran[:, 2, :] - AFST_ran[:, 1, :])])
#ax1.set_ylim([y_min, y_max])
#ax2.set_ylim([y_min, y_max])

# Ensure layout is clean
plt.tight_layout(rect=[0.05, 0.05, 1, 1])
plt.show()

#%% Figure 1B: save
fig2Bii = fig
figloc = "~\\Figures\\"
filenames = 'Figure2Bii'
fig2Bii.savefig(figloc + filenames+ '.pdf', format='pdf',bbox_inches='tight')
