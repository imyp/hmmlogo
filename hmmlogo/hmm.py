# -*- coding: utf-8 -*-

from subprocess import run
from io import BytesIO

from requests import get
from pandas import read_csv 
from .exceptions import InvalidAccessionError, ProgramMissingError

class HiddenMarkovModel:
    """Class for a profile Hidden Markov Model."""

    def __init__(self, accession):
        self.accession = accession
        self.hmm = self.get_hmm(accession)
        self.logo = self.get_logo(self.hmm)
        self.logo_df = self.get_logo_df()


    def get_hmm(self, accession):
        url = f'https://pfam.xfam.org/family/{accession}/hmm'
        response = get(url=url)
        if not response.ok:
            raise InvalidAccessionError(accession)
        hmm = response.content
        return hmm

    
    def get_logo(self, hmm):
        args = "hmmlogo --no_indel /dev/stdin".split()
        try:
            proc = run(args, input=hmm, capture_output=True)
        except (FileNotFoundError):
            raise ProgramMissingError(args)
        logo = proc.stdout
        return logo

    
    def get_logo_df(self):
        logo = BytesIO(self.logo)
        df = self.read_logo(logo)
        return df

    
    def read_logo(self, logo):
        names = ['profile']+list('ACDEFGHIKLMNPQRSTVWY-')
        sep = '\s+\(.*|:?\s+'
        df = read_csv(logo, index_col=0, skiprows=2, header=None,
                      sep=sep, engine='python', names=names)
        df = df.dropna(axis='columns')
        return df
        

