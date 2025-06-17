This project is a Python-based simulation project investigating how coupling to external sensory stimuli affects the ability of an intrinsic oscillator model to track/process speech.

In the current project, we adapted the STiMCON model by Ten Oever and Martin (2021) (DOI: <i>https://doi.org/10.7554/eLife.68066</i>) which included a fixed intrinsic oscillator unaffected by external inputs. 
To couple the model with external sensory stimuli, we introduced the Stuart-Landau process, which allowed us to quantify the coupling strength with a scalar value K. 

We found that weak sensory coupling/entrainment, compared to no or strong coupling, helps the oscillator better balance the use of internal language knowledge with the tolerance for unexpectedness in speech processing.

## Explanation
The repository consists of scripts belonging to simulations of the Stuart-Landau process, a new Oscillator module (which we used in STiMCON to accommodate the Stuart-Landau process), the adapted STiMCON model, and result generation & plots. 

### Stuart-Landau related files:
<b>stuart_landau_STiMCON.py:</b>\
This script implements the Stuart-Landau process over a predefined time period.

### Oscillator related files:
<b>oscillator.py:</b>\
This script defines an oscillator with parameters.

### STiMCON related files:

<b>STiMCON_core_v4.py</b>\
Core script for the STiMCON model which has all the low-level code, adapted from Ten Oever and Martin (2021).

<b>AdaptedSTiMCON_PredictiveFeedback_RhythmicInput.py</b>\
Implementing extended STiMCON when presenting isochronous input, and saving the data of feedback activation per word node.

<b>AdaptedSTiMCON_PredictiveFeedback_RandomisedInput.py</b>\
Implementing extended STiMCON when presenting non-isochronous input, and saving the data of feedback activation per word node.

<b>AdaptedSTiMCON_VarRhy_AmbiguousInput_Rhythmic.py</b>\
Implement extended STiMCON when presented with isochronous input, and save the results of ambiguous input categorisation across 
stimulus onset delays, degrees of ambiguity, and stimulus frequency

<b>AdaptedSTiMCON_VarRhy_AmbiguousInput_Randomised.py</b>\
Implement extended STiMCON when presented with non-isochronous input, and save the results of ambiguous input categorisation across 
stimulus onset delays, degrees of ambiguity, and stimulus frequency

<b>AdaptedSTiMCON_plotting_PredictiveFeedback.py</b>\
Analysing and plotting data of feedback activation per word node by implementing extended STiMCON with rhythmic (isochronous) and randomised (non-isochronous) sensory inputs.

<b>AdaptedSTiMCON_plotting_AmbiguousInput.py</b>\
Analyse and plot data of ambiguous input categorisation implementing extended STiMCON with isochronous and non-isochronous sensory inputs

All the original scripts of Ten Oever and Martin (2021) used/called in the scripts above can be found: <i>https://github.com/sannetenoever/STiMCON/tree/main</i>.
