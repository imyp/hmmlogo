# -*- coding: utf-8 -*-

from json import load
from base64 import b64encode
from io import BytesIO, StringIO
from os.path import dirname, abspath, join

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.path import Path
from matplotlib.patches import PathPatch
from .hmm import HiddenMarkovModel

here = dirname(abspath(__file__))
alph_path = join(here,'alph.json')
cmap_path = join(here,'cmap.json')

class LogoPlot:

    def __init__(self, accession, start=None, end=None, alph=alph_path, cmap=cmap_path):
        self.accession = accession
        self.start = start
        self.end = end
        self.hmm = HiddenMarkovModel(accession)
        self.logo = self.hmm.logo_df
        self.partial_logo = self.logo.loc[start:end]
        self.alph = self.read_json(alph)
        self.cmap = self.read_json(cmap)
        self.get_logoplot()

    def get_logoplot(self):
        self.fig, self.ax = plt.subplots(figsize=(len(self.partial_logo)/4,2), tight_layout=True)
        self.ax = self.plot_logo()

    def plot_logo(self):
        y_max = 0
        for x_offset, (_, series) in enumerate(self.partial_logo.iterrows()):
            self.plot_column(series, x_offset)
            y_max = max(y_max, series.sum())
        self.ax.axis([0, len(self.partial_logo), 0, y_max])
        self.ax.set_xticks(np.arange(len(self.partial_logo)+0.5))
        self.ax.set_xticklabels(self.partial_logo.index)

    def plot_column(self, series, x_offset):
        y_offset = 0
        series = series.sort_values()
        for let, y_scale in series.iteritems():
            patch = self.plot_letter(let, scale=(1, y_scale), offset=(x_offset, y_offset))
            self.ax.add_patch(patch)
            y_offset += y_scale

    def plot_letter(self, let, scale=(1, 1), offset=(0,0)):
        path = Path(*self.alph[let])
        path.vertices *= list(scale)
        path.vertices += list(offset)
        patch = PathPatch(path, color=self.cmap[let])
        return patch

    def read_json(self, path):
        with open(path, 'r') as f:
            obj = load(f)
        return obj

    def get_logofig(self, format='png'):
        if format == 'svg':
            logofig = StringIO()
        elif format == 'png':
            logofig = BytesIO()
        self.fig.savefig(logofig, format=format)
        logofig.seek(0)
        if format == 'svg':
            logofig = ''.join(logofig.readlines()[4:])
        elif format == 'png':
            logofig = b64encode(logofig.read()).decode()
            logofig = f'<img alt="" src="data:image/png;base64,{logofig}">'
        return logofig
