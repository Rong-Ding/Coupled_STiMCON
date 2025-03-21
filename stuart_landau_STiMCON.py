# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 18:55:07 2023

@author: rondin

The Stuart Landau process
"""

from oscillator import Oscillator
import numpy as np

def stuart_landau_STiMCON(osc_d: Oscillator, osc_id, time_range, k):
    """
    :param osc_d: the 'dependent' oscillator that gets influenced by the independent oscillator
    :param osc_id: the independent oscillator that influences the dependent oscillator
    """
    ExtStim = np.empty((2,len(osc_id[0])))
    ExtStim[0] = k * np.sum(osc_id,0)
    ExtStim[1] = np.zeros(len(osc_id[0]))
    osc_id = ExtStim # here we updated osc_id into a form identical to osc_d
    
    def stabilize(lambdas, ws, coo):
        """
        updates the oscillator's state iteratively over a period, 
        allowing transient behaviors to decay and the system to settle into its 
        natural oscillatory pattern
        
        :param lambdas: the lambda value of the dependent oscillator
        :param ws: the omega of the dependent oscillator
        :param coo: the starting coordinates for the dependent oscillator
        :return:
         stabilised coordinates
        """
        stabilize_time = np.arange(0, 50.001, 0.001) # we assumed fs=1000, thus timestep=0.001
        for t in stabilize_time:
            distance = np.linalg.norm(coo)**2
            derivative_matrix = np.array([[lambdas - distance, -ws],
                                          [ws, lambdas - distance]])
            #print(derivative_matrix @ coo)
            coo = coo + 0.001 * (derivative_matrix @ coo)
        return coo

    coo_d = [[np.cos(osc_d.starting_phase)], [np.sin(osc_d.starting_phase)]]
    start_coo = stabilize(osc_d.lamb, 2 * np.pi * osc_d.omega, coo_d)

    def placeholder_name(coo, x_y):
        """
        :param coo: stabilised starting coordinates
        :param x_y: the coordinates of the independent oscillator during the time range
        :return:
         coordinates for the dependent oscillator, atm mostly for plotting
        """
        coo_store = np.array([[],[]])
        #print(x_y[:, 0])
        for i in range(len(time_range)):
            ws = 2 * np.pi * osc_d.omega
            distance = osc_d.gamma*np.linalg.norm(coo)**2

            derivative_matrix = np.array([[osc_d.lamb - distance, -ws],
                                          [ws, osc_d.lamb - distance]])
            #print(derivative_matrix)
            #print(coo)
            #print((derivative_matrix @ coo))
            coo = coo + 0.001 * np.sum([[(derivative_matrix @ coo)[:, 0], x_y[:, i]]], axis=1).T
            coo_store = np.hstack((coo_store, coo))
        return coo_store

    coo_end = placeholder_name(start_coo, osc_id)
    #print(coo_end)
    
    # extract only phase while getting rid of k/amplitude (external stim's 
    # amplitude is being affected by k)
    phi = np.unwrap(np.angle(coo_end[0,:]+coo_end[1,:]*1j))
    coo_end = np.array(np.sin(phi))
    return coo_end

