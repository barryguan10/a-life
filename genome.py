import numpy as np


class Genome:
    """Genome Class
    This class is for generating and capturing genes of organisms. Each Genome
    contains information that can later be interpreted inside an organism class
    to produce that organisms phenotypes.
    """

    def __init__(self, genes=None, size=6):
        self.genes = genes if genes is not None else np.random.rand(size)

    def mutate(self, rate=0.05, std_dev=0.1):
        '''Mutate Function, can be called to mutate genes
        Args:
            param1: rate (float) between 0 and 1, inclusive. Represents the
            mutation rate percentage for any given gene to mutate.
            default is 0.05 (5%)

            param2: std_dev (float) represents the standard deviation from
            the mean for a normal distribution. Impacts how much more/less
            a genes value changed during mutation. Based on normal
            distribution.

        Returns:
            None. Updates self.genes
        '''
        # determine which, if any, gene mutates with a mask
        mutate_mask = np.random.rand(len(self.genes)) < rate
        # adjust mutated genes based on normal distribution
        self.genes[mutate_mask] += np.random.normal(0, std_dev,
                                                    mutate_mask.sum())
        # clip values to ensure they are within 0 and 1
        np.clip(self.genes, 0, 1, self.genes)

    def get_genes(self):
        '''Return genes for this genome'''
        return self.genes
    
    def copy_genes(self):
        """
        Returns a copy of the genome for editing
        """
        return Genome(genes=self.genes.copy())