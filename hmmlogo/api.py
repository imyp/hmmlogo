# -*- coding: utf-8 -*-

from .plot import LogoPlot

def logofig(accession, start=None, end=None):
    hmmlogoplot = LogoPlot(accession, start=start, end=end)
    hmmlogofig = hmmlogoplot.get_logofig()
    return hmmlogofig



