
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 14:22:59 2023

@author: rondin

Implement extended STiMCON when presented with non-isochronous input, 
and save the results of ambiguous input categorisation across 
stimulus onset delays, degrees of ambiguity, and stimulus frequency

(Note that due to length limitations, for CCN we stayed with
results with stimulus frequency = 4Hz)

"""
import sys
sys.path.append("~\\Scripts\\")
import math
import numpy as np
import STiMCON_core_v4 as STiMCON_core
#import STiMCON_plot
import STiMCON_sen
import os
import ColorScheme as cs
cmaps = cs.CCcolormap()
bfi = cs.baseFigInfo()        
                                        
#%% basic information
fs = 1000;
Freq = 4.0;
Freq_stim = 5

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
N = 8 # total no. of nodes, "I eat cake cake cake cake eat __"
#mu = 1/Freq
#sigma = 0.2*(1/Freq)
stimtime = 1/Freq * (np.linspace(0,(N-1),N) + [np.random.uniform(-.25,.25) for i in range(N)])
#stimtime = 1/Freq * (np.linspace(0,(N-1),N) + np.random.normal(mu, sigma, N))
stimtime[-1] = 1/Freq * (N-1) # we tweak the onset delay later
#stimtime = 1/Freq*np.linspace(0,(N-1),N)

#%% define the parameters of the model
parameters = {"Nnodes": Nnodes,
       "OsFreq": Freq,
       "OsAmp": 1,
       "OsOffset": 0.25*math.pi,
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
stimpara = {'word_duration': int(0.5/Freq_stim*fs),
            'onsetdelay': int(0.5/Freq_stim*fs),
            'Nnodes': Nnodes}
#% adjust OsOffset based on the onsetdelay and word_duration:
#peak = (stimpara['word_duration']+stimpara['onsetdelay'])/fs
#parameters['OsOffset'] = peak*Freq*(2*math.pi)

## set all the parameters
senObj = STiMCON_sen.modelSen(stimpara,parameters)

#%% iterate thru different K's (+randomised phase, avg per K per prop)
prop = np.linspace(0,1,12)
delays = np.linspace(0,1,20)/Freq*fs # delays has to be changed with stim freq; but kept here bc length is needed
#ks = [0,10,20,30,40]
ks = [0,5,10,15,20,30,40,50]
stim_Freqs = [2,3,4,5,6,7,8]
os.chdir(r"~\\Data_AmbiguousInput\\Experiment2\\NonIsochronous\\Version2\\")

iterations = 1000 # mainly phase randomisation; per iteration 12(ambiguity)*20(delays)*8(stimfreq) = 320 sub
AllFirstSpTime = np.zeros([len(prop),len(delays),Nnodes,len(ks),iterations,len(stim_Freqs)])
AllFirstSpTime_relStimOnset = np.zeros([len(prop),len(delays),Nnodes,len(ks),iterations,len(stim_Freqs)])
FirstActive = np.zeros([len(prop),len(delays),len(ks),iterations,len(stim_Freqs)])
SensoryInput_Timing = np.zeros([len(prop),len(delays),iterations,len(stimtime),len(stim_Freqs)])
Phases = np.zeros([iterations])

intensity = np.zeros([Nnodes,N]) 
intensity[0,0] = 1; intensity[1,1] = 1; intensity[4,2:-2] = 1; intensity[1,-2] = 1
for iteration in range(0,iterations):
    print(iteration)
    parameters['OsOffset'] = np.random.uniform(0,2)*math.pi
    Phases[iteration] = parameters['OsOffset']
    SI_it = []
    for iF in range(len(stim_Freqs)):
        #parameters["feedbackdelay"] = int(0.9/stim_Freqs[iF]*fs)
        stimtime = 1/stim_Freqs[iF]*(np.linspace(0,(N-1),N) + [np.random.uniform(-.25,.25) for i in range(N)])
        stimpara = {'word_duration': int(0.5/stim_Freqs[iF]*fs),
                    'onsetdelay': int(0.5/stim_Freqs[iF]*fs),
                    'Nnodes': Nnodes}
        delays = np.linspace(0,1,20)/4*fs
        print(iF)
        for cntProp in range(len(prop)): #12
            #print(cntProp)
            for cntDel in range(len(delays)): #20
                 #print(cntDel)
                 lat = stimtime*fs
                 lat[-1] = lat[-2]+ stimpara["onsetdelay"] + stimpara["word_duration"] + delays[cntDel] # delay relative to the offset of N-1
                 #lat[-1] = lat[-1]+delays[cntDel]  
                 # staying with the most predictable two nodes (cake and nice)
                 intensity[3,-1] = 1*prop[cntProp]
                 intensity[4,-1] = 1-intensity[3,-1]
                 seninput = {'stim_ord': list(),
                             'intensity': intensity,
                             'stim_time': lat,            
                             'tot_length': lat[-1]+3/Freq*fs}
                 senObj = STiMCON_sen.modelSen(stimpara,parameters)
                 sensory_input = senObj.create_stim_vartimethres(seninput)
                 # save the sensory input timing
                 SensoryInput_Timing[cntProp,cntDel,iteration,:,iF] = lat
                 
                 onsetLast = int(lat[-1:]+stimpara['onsetdelay']) # time point to start calculate first active = sensory input + input duration
                 STiMCON_var = STiMCON_core.modelPara(parameters)
                 for ind_k in range(len(ks)):
                     #print(ind_k)
                     k = ks[ind_k]
                     out = STiMCON_var.runsingle(sensory_input,k)           
                     for senoi in range(Nnodes):
                        inxpl = np.where(out['spiketimes'][senoi][onsetLast:]==2)
                        if len(inxpl[0])>0:
                            AllFirstSpTime[cntProp,cntDel,senoi,ind_k,iteration,iF] = inxpl[0][0]+onsetLast-len(lat)/Freq*fs # relative to last stim onset??
                            AllFirstSpTime_relStimOnset[cntProp,cntDel,senoi,ind_k,iteration,iF] = inxpl[0][0]
                        else:
                            AllFirstSpTime[cntProp,cntDel,senoi,ind_k,iteration,iF] = np.nan
                            AllFirstSpTime_relStimOnset[cntProp,cntDel,senoi,ind_k,iteration,iF] = np.nan                        
                     try:
                        FirstActive[cntProp,cntDel,ind_k,iteration,iF] = np.nanargmin(AllFirstSpTime_relStimOnset[cntProp,cntDel,:,ind_k,iteration,iF]) # get the node that spikes earliest
                        val = AllFirstSpTime_relStimOnset[cntProp,cntDel,int(FirstActive[cntProp,cntDel,ind_k,iteration,iF]),ind_k,iteration,iF] # get the first spike time
                        checkdouble = np.argwhere(AllFirstSpTime_relStimOnset[cntProp,cntDel,:,ind_k,iteration,iF] == val) # double check which node？
                        if len(checkdouble)>1: # if there is more than one node spiking first
                            aclev = np.zeros(len(checkdouble))
                            for it in range(len(checkdouble)): # it = item (node)                   
                                inx = AllFirstSpTime_relStimOnset[cntProp,cntDel,checkdouble[it],ind_k,iteration,iF]
                                aclev[it] = out['activation'][checkdouble[it],onsetLast+int(inx)] # activation value
                            FirstActive[cntProp,cntDel,ind_k,iteration,iF] = checkdouble[np.argmax(aclev)]
                            if aclev[0]==aclev[1]:
                                FirstActive[cntProp,cntDel,ind_k,iteration,iF]=np.nan 
                     except:
                        FirstActive[cntProp,cntDel,ind_k,iteration,iF] = np.nan
    # for saving the data each iteration
    AFST_it =  AllFirstSpTime[:,:,:,:,iteration,:]
    AFST_relStimOnset_it = AllFirstSpTime_relStimOnset[:,:,:,:,iteration,:]
    FA_it = FirstActive[:,:,:,iteration,:]
    Phase = parameters['OsOffset']       
    np.save(file=r"data_VarRhy_AllFirstSpTime_RandomInput_it{}.npy".format(iteration+1),arr=AFST_it)
    np.save(file=r"data_VarRhy_AllFirstSpTime_rel_RandomInput_it{}.npy".format(iteration+1),arr=AFST_relStimOnset_it)
    np.save(r"data_VarRhy_FirstActive_RandomInput_it{}.npy".format(iteration+1),arr=FA_it)
    SI_it = SensoryInput_Timing[:,:,iteration,:,:]
    np.save(r"data_VarRhy_SensoryInput_RandomInput_it{}.npy".format(iteration+1),arr=SI_it)
    np.save("data_VarRhy_Phases_RandomInput_it{}.npy".format(iteration+1),arr=Phase)
