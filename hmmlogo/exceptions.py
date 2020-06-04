# -*- coding: utf-8 -*-

class InvalidAccessionError(Exception):
    """Exception raised when using an invalid Pfam accession number"""

    def __init__(self, accession):
        self.accession = accession
        self.message = f'No Hidden Markov Model found with accession number: {accession}.'
        super().__init__(self.message)

class ProgramMissingError(Exception):
    """Exception raised when a returncode different from zero is returned."""

    def __init__(self, args):
        self.args = args
        self.command = ' '.join(args)
        self.message = f"""The following command failed to run on your system:

        {self.command}

        Make sure that {args[0]} is installed."""
        super().__init__(self.message)
