# Coupled_STiMCON 
This repository describes the scripts from the second doctoral project of Rong Ding. This project is currently moving towards submission to a peer-reviewed journal.

This project is a Python-based simulation project investigating how moderate coupling to external sensory stimuli affects the ability of an intrinsic oscillator model to track/process speech.

In the current project, we adapted the STiMCON model by Ten Oever and Martin (2021) (DOI: <i>https://doi.org/10.7554/eLife.68066</i>) which included a fixed intrinsic oscillator unaffected by external inputs. 
To couple the model with external sensory stimuli, we introduced the Stuart-Landau process which allowed us to quantify the coupling strength with a scalar value K. 

## Explanation
The repository consists of scripts belonging to simulations of the Stuart-Landau process, a new Oscillator module (which we used in STiMCON to accommodate the Stuart-Landau process), the adapted STiMCON model, and result generation & plots. 

Note that, in terms of result scripts, as an example I have only uploaded the model implementation when it is presented with randomised stimulus inputs and is expected to generate a feedback activation (or not) depending on the predictability of each word node at a chosen time point. In the result plotting script, you will see the code snippets for analysing data from both rhythmic and randomised inputs, and the figure attached alongside the scripts here demonstrates what we found.

### Stuart-Landau related files:
<b>stuart_landau_STiMCON.py:</b>\
This script implements the Stuart-Landau process over a predefined time period.

### Oscillator related files:
<b>oscillator.py:</b>\
This script defines an oscillator with parameters.

### STiMCON related files:

<b>STiMCON_core_v4.py</b>\
Core script for the STiMCON model which has all the low-level code, adapted from Ten Oever and Martin (2021).

<b>AdaptedSTiMCON_PredictiveFeedback_RandomisedInput.py</b>\
Implementing extended STiMCON when presenting randomised input, and saving the data of feedback activation per word node.

<b>AdaptedSTiMCON_plotting_PredictiveFeedback.py</b>\
Analysing and plotting data of feedback activation per word node by implementing extended STiMCON with rhythmic (isochronous) and randomised (non-isochronous) sensory inputs.

<b>Figure2_4Hz_v2.jpg</b>\
The resulting figure of AdaptedSTiMCON_plotting_PredictiveFeedback.py. Shown here as evidence of our work.

<b>STiMCON_sen.py</b>\
Creating sensory input going into the STiMCON, from Ten Oever and Martin (2021).

The original scripts of Ten Oever and Martin (2021) can be found here: <i>https://github.com/sannetenoever/STiMCON/tree/main</i>.
