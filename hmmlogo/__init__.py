# -*- coding: utf-8 -*-

"""
hmmlogo 
~~~~~~~

This package is used to visualize profile hidden Markov models.
Basic usage:

   >>> import hmmlogo
   >>> hmmlogo.get_svg('PF00010')
   <Figure Object>

"""

from .hmm import HiddenMarkovModelLogo
from .plot import LogoPlot

from .api import get_svg, save_svg
