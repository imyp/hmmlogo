# -*- coding: utf-8 -*-

import json
import io 
import base64
from os.path import dirname, abspath, join

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.path import Path
from matplotlib.patches import PathPatch
from .hmm import HiddenMarkovModelLogo

# Paths for alphabet and colormap
here = dirname(abspath(__file__))
alph_path = join(here,'alph.json')
cmap_path = join(here,'cmap.json')

class LogoPlot(HiddenMarkovModelLogo):
    """
    Visualization of a profile hidden Markov model.
    """
    def __init__(self, accession, alph=alph_path, cmap=cmap_path):
        super().__init__(accession)
        with open(alph, 'r') as f:
            self.alph = json.load(f)
        with open(cmap, 'r') as f:
            self.cmap = json.load(f)
        self.fig, self.ax = self.initialize_plot()
        self.plot_heights(self.heights)
        self.plot_indelinfo(self.indelinfo)

    def initialize_plot(self):
        length = len(self.heights)
        fig, ax = plt.subplots(figsize=(length/2, 7))
        ax.set_xlim(0, length)
        return fig, ax
    
    def plot_heights(self, heights):
        y_max = 0
        for x_offset, (_, profile_heights) in enumerate(heights.iterrows()):
            self.plot_profile(profile_heights, x_offset)
            y_max = max(y_max, profile_heights.sum())
        self.ax.set_ylim(0, y_max)
    
    def plot_profile(self, profile, x_offset):
        y_offset = 0
        profile = profile.sort_values()
        for aminoacid, height in profile.iteritems():
            patch = self.get_aa_patch(
                aminoacid, 
                [1, height], 
                [x_offset, y_offset],
            )
            self.ax.add_patch(patch)
            y_offset += height
    
    def get_aa_patch(self, aminoacid, scale, offset):
        path = Path(*self.alph[aminoacid])
        path.vertices *= scale
        path.vertices += offset
        patch = PathPatch(path, color=self.cmap[aminoacid])
        return patch
    
    def plot_indelinfo(self, indelinfo):
        self.ax.xaxis.set_visible(False)
        indelinfo = indelinfo.round(decimals=2).T
        self.ax.table(
            cellText=indelinfo.values, 
            rowLabels=indelinfo.index, 
            colLabels=indelinfo.columns,
        )
        self.fig.tight_layout()

    def get_svg(self):
        image = io.StringIO()
        self.fig.savefig(image, format='svg', bbox_inches='tight')
        image.seek(0)
        image = "\n".join(image.readlines()[4:])
        return image

    def get_png(self):
        image = io.BytesIO()
        self.fig.savefig(image, format='png', bbox_inches='tight')
        image.seek(0)
        image = base64.b64encode(logofig.read()).decode()
        return image
