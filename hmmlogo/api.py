# -*- coding: utf-8 -*-

"""
hmmlogo.api
~~~~~~~~~~~

This module implements the HMMLogo API.
"""

from . import plot
from . import hmm

def get_svg(accession, **kwargs):
    """
    Returns a HMM sequence logo in SVG format.

    Parameters
    ----------
    accession : str
        Pfam accession for desired HMM.
    **kwargs : 
        Additional arguments are passed to :class:`LogoPlot`.
    """
    logoplot = plot.LogoPlot(accession, **kwargs)
    svg = logoplot.get_svg()
    return svg

def save_svg(accession, fname, **kwargs):
    """
    Writes an HMM sequence logo to a file in SVG format.

    Parameters
    ----------
    accession : str
        Pfam accession for desired HMM.
    fname : str or file-like object
        A path or a Python file-like object.
    """
    logoplot = plot.LogoPlot(accession, **kwargs)
    logoplot.fig.savefig(fname, format='svg')
