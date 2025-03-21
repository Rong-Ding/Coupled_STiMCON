# coupled_STiMCON 
This repository describes the scripts from the second doctoral project of Rong Ding. This project is currently moving towards submission to a peer-reviewed journal.

This project is a Python-based simulation project investigating how moderate coupling to external sensory stimuli affects the ability of an intrinsic oscillator model to track/process speech.

In the current project, we adapted the STiMCON model by Ten Oever and Martin (2021) (DOI: <i>https://doi.org/10.7554/eLife.68066</i>) which included a fixed intrinsic oscillator unaffected by external inputs. 
To couple the model with external sensory stimuli, we introduced the Stuart-Landau process which allowed us to quantify the coupling strength with a scalar value K. 

## Explanation
The repository consists of scripts belonging to simulations of the Stuart-Landau process, a new Oscillator module (which we used in STiMCON to accommodate the Stuart-Landau process), the adapted STiMCON model, and result analyses/plots.

### Stuart-Landau related files:
<b>stuart_landau_STiMCON.py:</b>\
This script implements the Stuart-Landau process over a predefined time period.

### Oscillator related files:
<b>oscillator.py:</b>\
This script defines an oscillator with parameters.

### STiMCON related files:

<b>STiMCON_core_v4.py</b>\
Core script for the STiMCON model which has all the low-level code, adapted from Ten Oever and Martin (2021).

<b>STiMCON_plot.py</b>\
Plotting output of the STiMCON, from Ten Oever and Martin (2021)

<b>STiMCON_sen.py</b>\
Creating sensory input going into the STiMCON
