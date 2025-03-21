# -*- coding: utf-8 -*-
"""
The extended/adapted STiMCON model
"""

import numpy as np
import math
import sys
sys.path.append("C:\\Users\\rondin\\Desktop\\Projects\\Project 2\\oscillator\\")
from oscillator import Oscillator
from stuart_landau_STiMCON import *

#%% define class for single layer activation parameters
class modelPara(object):
    
    def __init__(self, parameters):
        """
        :params: described in the comments below
        """
        self.Nnodes = parameters['Nnodes'] # no. of nodes
        self.oscFreq = parameters['OsFreq'] # natural frequency oscillator
        self.oscAmp = parameters['OsAmp'] # amplitude oscillator
        self.oscOffset = parameters['OsOffset'] # starting phase
        self.latAct_thres = parameters['activation_threshold'] # activation thereshold (same across nodes)    
        self.feedbackInfluence = parameters['feedbackinf'] # 
        self.feedbackDecay = parameters['feedbackdecay'] # how late feedback starts decaying
        self.feedbackDelay = parameters['feedbackdelay'] # how late feedback starts after stim onset
        self.feedbackMat = parameters['feedbackmat'] # feedback connection between a node and the feedback layer
        self.latLatinhib = parameters['latinhibstrength'] # lateral inhibition strength between two nodes
        self.latSelexc = parameters['selfexitation'] # self excitation strength
        self.latInhib = parameters['Inhib'] # baseline inhibition     
        self.fs = parameters['fs'] # modelled sampling frequency    
        
    def runsingle(self, sensory_input, k): # coupling strength k added
        # define the layers
        semantic_node = np.zeros(self.Nnodes)
        feedback_conn = np.zeros(self.Nnodes)
        feedforward_conn = np.zeros(self.Nnodes)
        inhibT = np.zeros(self.Nnodes)+200*self.fs # time in the inhibition func
        
        # main loop 
        Ntime = np.ma.size(sensory_input,1)
        act = np.zeros([self.Nnodes,int(Ntime)]) # activation
        sptim = np.zeros([self.Nnodes,int(Ntime)]) # spike times (1: through feedback, 2: through feedforward + feedback)
        fbm = np.zeros([self.Nnodes,int(Ntime)]) # feedback input (fbm2 is feedback input including the delay for plotting)
        
        osc = self.oscFun_coupled(sensory_input,k)
        for T in range(0,len(sensory_input[0])):    
           
            for nodecnt in range(0,self.Nnodes): # for each semantic word node
                feedforward_conn[nodecnt] = feedforward_conn[nodecnt]-self.feedbackDecay # feedforward might get cancelled out by fb offset
                if feedforward_conn[nodecnt]<0:
                    feedforward_conn[nodecnt] = 0
                inhibT[nodecnt] = inhibT[nodecnt]+1 # timestep count +1 for post-spiking inhibition
                #print(semantic_node[nodecnt]*self.latSelexc)
                #print(fbm[nodecnt,T-self.feedbackDelay])
                #print(self.inhibFun(inhibT[nodecnt]))
                #print(self.oscFun_coupled(sensory_input,k,T))
                #print(sensory_input[nodecnt,T])
                semantic_node[nodecnt] = semantic_node[nodecnt]*self.latSelexc + osc[T] + \
                sensory_input[nodecnt,T] + fbm[nodecnt,T-self.feedbackDelay] + self.inhibFun(inhibT[nodecnt]) # activation??
            semantic_node = self.latin(semantic_node)
            for nodecnt in range(0,self.Nnodes):
                if semantic_node[nodecnt] > self.latAct_thres: # if summed activation goes beyond activation threshold
                    if act[nodecnt][T-1] < self.latAct_thres:
                        inhibT[nodecnt] = 0
                    sptim[nodecnt,T] = 1 # if there's only feedback, spike will only reach 1             
                    if sensory_input[nodecnt,T] > 0:
                        feedforward_conn = np.zeros(self.Nnodes);
                        feedforward_conn[nodecnt] = 1
                        sptim[nodecnt,T] = 2 # if there is actual input, spike reaches 2
                act[nodecnt][T] = semantic_node[nodecnt]
            feedback_conn = self.feedback(feedforward_conn)
            fbm[:,T] = feedback_conn
        fbm2 = np.concatenate((np.zeros([self.Nnodes, self.feedbackDelay]), fbm[:,0:-self.feedbackDelay]), 1)
        
        modelOut = {'activation': act, # overall activation value of a word node
                    'spiketimes': sptim, # whether a node spikes (= 0, 1, or 2) per time point
                    'feedback': fbm, # feedback strength by time point
                    'feedbackdel': fbm2};        
        return modelOut
    
    def oscFun_coupled(self,sensory_input,k): 
        # An internal oscillator coupled to external stimuli, depending on the coupling strength k
        osc_Int = Oscillator(omega=self.oscFreq,lamb=1,starting_phase=self.oscOffset,amplitude=self.oscAmp)    
        time_range = np.arange(0,len(sensory_input[0])/self.fs,1/self.fs)
        actv_coupled = stuart_landau_STiMCON(osc_Int, sensory_input, time_range, k)
        #print(actv_coupled[0,T])
        return actv_coupled
    
    def inhibFun(self,Ti): # to be retained
        inhib = self.latInhib # baseline inhibition
        if Ti < 0.02*self.fs: # fs: the vector of times of an individual node in an inhibition function (inmilliseconds)
            inhib = inhib*-3 # suprathreshold activation
        elif Ti < 0.05*self.fs:
            inhib = inhib*3
        elif Ti < 0.1*self.fs:
            inhib = inhib*3  
        return inhib

    def latin(self, semantic_node):
        latmat = np.zeros([self.Nnodes,self.Nnodes])+self.latLatinhib
        np.fill_diagonal(latmat, 0)
        semantic_node.dot(latmat)
        semantic_node = semantic_node + semantic_node.dot(latmat)
        return semantic_node

    def feedback(self,feedforward_conn):
        feedbackmat = self.feedbackMat*self.feedbackInfluence # feedback connection between a node and the feedback layer
        feedback_conn = feedforward_conn.dot(feedbackmat)
        return feedback_conn