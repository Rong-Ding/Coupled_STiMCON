# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 10:36:03 2023

@author: rondin

The Oscillator module used in STiMCON to accommodate the Stuart-Landau process
"""

import numpy as np
import matplotlib.pyplot as plt

class Oscillator:
    """
    :param omega: natural frequency
    :param amplitude: max amplitude
    :param lamb, sigma, gamma: control parameters for damping, etc.
    :param starting_phase: 
        starting phase of the oscillator (we need this to implement simulations
        across different starting phases and see the average effect)
    :param coupled_oscillators: 
        a dictionary var storing coupling strength between each two oscillators
        (can be changed using Osc2.change_coupling_strength(Osc1,K))
        Note: we did not use this as external sensory inputs were separately
              defined in STiMCON
    """
    def __init__(self, omega, amplitude=1, lamb=None, sigma=None,
                 gamma=1, starting_phase=0,
                 coupled_oscillators={}):
        self.omega = omega

        self.amplitude = amplitude
        self.lamb = lamb
        self.sigma = sigma
        self.gamma = gamma
        self.starting_phase = starting_phase

        self.coupled_oscillators = coupled_oscillators

    def change_coupling_strength(self, oscillator, coupling_strength):
        self.coupled_oscillators[oscillator] = coupling_strength

    def plot_osc(self, time_range=np.linspace(0, 3, 3000)): # to plot an oscillator
        y = self.amplitude * np.sin(2 * np.pi * self.omega * time_range + self.starting_phase)
        plt.plot(time_range, y)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.show()



