# -*- coding: utf-8 -*-

from subprocess import run
from io import BytesIO

import requests
from pandas import read_csv 

class HiddenMarkovModelLogo:
    """
    Contains logo information for a Hidden Markov Model as DataFrames. 
    These can be found as the heights, and indelinfo attributes. When 
    initializing the object it takes a PFAM accession ID.
    """
    def __init__(self, accession):
        self.accession = accession
        self.hmm = self.get_hmm(self.accession)
        self.heights, self.indelinfo = self.get_hmmlogo(self.hmm)

    def get_hmm(self, accession):
        """
        Return hidden Markov model from Pfam.
        """
        url = f"https://pfam.xfam.org/family/{accession}/hmm"
        response = requests.get(url=url)
        response.raise_for_status()
        hmm = response.content
        return hmm
    
    def get_hmmlogo(self, hmm):
        """
        Return hidden Markov model logo from hidden Markov model.
        """
        arguments = ["hmmlogo", "/dev/stdin"]
        process = run(arguments, input=hmm, capture_output=True)
        heights, indelinfo = self.read_hmmlogo(process.stdout)
        return heights, indelinfo
    
    def read_hmmlogo(self, hmmlogo_output):
        """
        Return heights and indelinfo from hidden Markov model logo.
        """
        column_names = ['profile']+list('ACDEFGHIKLMNPQRSTVWY-')
        seperator = ':?\s+\(?\s?'
        hmmlogo_df = read_csv(
            BytesIO(hmmlogo_output),
            index_col=0,
            skiprows=2,
            header=None,
            sep=seperator,
            names=column_names,
            engine="python",
        )
        hmmlogo_df = hmmlogo_df.drop('-', axis='columns')
        heights = self.clean_df(hmmlogo_df)
        indelinfo = self.get_indelinfo(hmmlogo_df)
        return heights, indelinfo
    
    def clean_df(self, df):
        """
        Remove nan columns and remaining rows containing nan values.
        """
        df = df.dropna(axis='columns', how='all')
        df = df.dropna(axis='rows', how='any')
        df = df.astype('float64')
        df.index = df.index.astype('int64')
        return df
    
    def get_indelinfo(self, hmmlogo_df):
        """
        Return indelinfo for hidden Markov model logo.
        """
        selection = hmmlogo_df['Y'].isna()
        indelinfo = hmmlogo_df[selection].copy()
        indelinfo = self.clean_df(indelinfo) 
        indelinfo = indelinfo.rename(
            columns=dict(
                A='insert probability', 
                C='average insert length', 
                D='occupancy',
            )
        )
        return indelinfo    
