import pipes
import json
import io
import base64

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import requests

def get_hmm(pfam_ac):
    """
    Download hidden Markov model (HMM) using Pfam Accession Number.

    Parameters
    ----------
    pfam_ac : str
        Pfam Accession Number (identifier for protein family).
    
    Returns
    -------
    hmm : str or None
        HMM as string or None if request was unsuccessful.
    """

    url = f'http://pfam.xfam.org/family/{pfam_ac}/hmm'
    r = requests.get(url=url)

    if r.ok:
        return r.text
    else:
        print(f'Could not find Pfam Accession Number: {pfam_id}.')
        return None


def read_logo(logo):
    """
    Read HMM logo as a pandas DataFrame.

    Parameters
    ----------
    logo : file-like object
        Object with a `read()` method which returns the logo.

    Returns
    -------
    df : pandas.core.DataFrame
        DataFrame containing the logo information.
    """
    # Column names of DataFrame.
    names = ['profile']+list('ACDEFGHIKLMNPQRSTVWY-')
    kwargs = dict(index_col=0, skiprows=2, header=None,
                  sep='\s+\(.*|:?\s+', engine='python', names=names)
    df = pd.read_csv(logo, **kwargs)
    df = df.dropna(axis='columns')
    # raise exception if len is 0.
    return df

def get_logo(hmm):
    """
    Get HMM logo from a HMM string using the `hmmlogo` program.
    
    Parameters
    ----------
    hmm : str
        Contents of HMM obtained by running `get_hmm`.

    Returns
    -------
    logo : pandas.core.frame.DataFrame
        The output of `hmmlogo` as a DataFrame.
    """

    # Insert HMM to start of pipe.
    pipe = pipes.Template()
    pipe.prepend(f'echo "{hmm}"', '.-')
    
    # Pipe the HMM to the `hmmlogo` command.
    pipe.append('hmmlogo --no_indel -', '--')

    with pipe.open('', 'r') as logo_obj:
        # Find a way to ensure that the pipe did not fail.
        logo = read_logo(logo_obj)
    return logo

def read_json(path):
    """Convenience function for reading json file."""
    with open(path, 'r') as f:
        obj = json.load(f)
    return obj

def letter(let, alph, cmap, scale=(1,1), offset=(0,0)):
    """
    Create patch for letter with specific scale and and offset.

    Parameters
    ----------
    let : {'A', 'C', 'D', 'E', 'F', 'G', 'H', ..., 'Y'}
        One-letter symbol of an amino acid.
    alph : dict
        Dictionary containing vertices and codes for each letter.
    cmap : dict
        Dictionary containing the color for each type of amino acid.
    scale : tuple, optional
        The scale in x-axis and y-axis, respectively.
    offset : tuple, optional
        Tuple with offset in x-axis and y-axis respectively.

    Returns
    -------
    patch : matplotlib.patches.Patch
        Scaled and translated patch of colored amino acid symbol.
    """
    path = Path(*alph[let])
    path.vertices *= list(scale)
    path.vertices += list(offset)
    patch = PathPatch(path, color=cmap[let])
    return patch

def column(series, x_offset, ax, alph, cmap):
    """
    Plot a column corresponding to a profile in the HMM logo.

    Parameters
    ----------
    series : pandas.Series
        Series corresponding to a profile in of the HMM DataFrame.
    x_offset : float or int
        The x-value where the column will be plotted.
    ax : matplotlib.Axes
        Axes object the column is being plotted to. 
    alph, cmap : dict
        Alphabet and color-mapping dictionary.
    """
    y_offset = 0
    series = series.sort_values()
    for let, y_scale in series.iteritems():
        patch = letter(let, alph, cmap, scale=(1, y_scale),
                       offset=(x_offset, y_offset))
        ax.add_patch(patch)
        y_offset += y_scale

def logo(df, ax, alph, cmap):
    """
    Plot HMM logo to Axes object using specific colormap and alphabet. 
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing HMM logo information for all profiles.
    ax : matplotlib.Axes
        Axes object the HMM logo is going to be plotted to.
    alph, cmap : dict
        Alphabet and colormap information. 
    """
    y_max = 0
    for x_offset, (_, series) in enumerate(df.iterrows()):
        column(series, x_offset, ax, alph, cmap)
        y_max = max(y_max, series.sum())
    ax.axis([0, len(df), 0, y_max])
    ax.set_xticks(np.arange(len(df))+0.5)
    ax.set_xticklabels(df.index)
    return ax

def plot_logo(df, alph, cmap, start=None, end=None):
    df = df.loc[start:end]
    fig, ax = plt.subplots(figsize=(len(df)/4,2))
    ax = logo(df, ax, alph, cmap)
    fig.tight_layout()
    return fig, ax

def hmmlogo(pfam_ac, alph_fname='alph.json',
            cmap_fname='colors.json',
            start=None, end=None):
    hmm = get_hmm(pfam_ac)
    df = get_logo(hmm)
    alph = read_json(alph_fname)
    cmap = read_json(cmap_fname)
    fig, ax = plot_logo(df, alph, cmap, start=start, end=end)
    return fig

def get_fig(fig, format='svg'):
    if format == 'svg':
        logo = io.StringIO()
        fig.savefig(logo, format=format)
        logo.seek(0)
        logo = ''.join(logo.readlines()[4:])
    elif format == 'png':
        logo = io.BytesIO()
        fig.savefig(logo, format=format)
        logo.seek(0)
        logo = base64.b64encode(logo.read()).decode()
        logo = f'<img alt="" src="data:image/png;base64,{logo}">'
    return logo
