# -*- coding: utf-8 -*-

"""
hmmlogo.api
~~~~~~~~~~~

This module implements the hmmlogo API.

"""

from . import plot
from . import hmm

def get_svg(accession, **kwargs):
    logoplot = plot.LogoPlot(accession, **kwargs)
    svg = logoplot.get_svg()
    return svg

def save_svg(accession, filename, **kwargs):
    logoplot = plot.LogoPlot(accession, **kwargs)
    logoplot.fig.savefig(filename, format='svg')
