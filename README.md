# coupled_STiMCON 
This repository describes the scripts from the second doctoral project of Rong Ding. This project is currently moving towards submission to a peer-reviewed journal.

This project is a Python-based simulation project which investigates how moderate coupling to external sensory stimuli affects the ability of an intrinsic oscillator model to track and process speech.

In the current project, we adapted the STiMCON model by Ten Oever and Martin (2021) (DOI: <i>https://doi.org/10.7554/eLife.68066</i>) which included a fixed intrinsic oscillator not affected by external inputs. 
To couple the model with external sensory stimuli, we introduced the Stuart-Landau process. 

## Explanation
The repository consists of scripts belonging to simulations of the Stuart-Landau process, a new Oscillator module (which we used in STiMCON to accommodate the Stuart-Landau process), the adapted STiMCON model, and result plots.

### Stuart-Landau related files:
<b>stuart_landau_STiMCON.py:</b>\
This script implements the Stuart-Landau process over a predefined time period.

### Oscillator related files:
<b>oscillator.py:</b>\
This script defines an oscillator with parameters.

### STiMCON related files:
<b>STiMCON_Fig4_Fig5_Fig8A.py</b>\
Shows the basic behavior of STiMCON (Figure 4), the threshold/timing of activation (Figure 5) and ambiguous daga overall simulations (Figure 8A)

<b>STiMCON_Fig6.py</b>\
Shows how acoustic time and model time is not the same in STiMCON (Figure 6)

<b>STiMCON_Fig8C.py</b>\
Fitting of the da/ga data using the first active node as output (Figure 8C)

<b>STiMCON_Fig8D.py</b>\
Fitting of the da/ga data using the relative node activation as output (Figure 8D)

<b>STiMCON_core.py</b>\
Core script for the STiMCON model which has all the low-level code

<b>STiMCON_plot.py</b>\
Plotting output of the STiMCON

<b>STiMCON_sen.py</b>\
Creating sensory input going into the STiMCON
