
import os
import pandas as pd
from scipy.stats import shapiro, mannwhitneyu


class Stats:
    def __init__(self, solver: str) -> None:
        self.solver = solver
        self.dim4 = []
        self.dim8 = []
        self.dim12 = []
        self.all_paths = []

    def set_file_names(self) -> None:
        dir = f'./output/{self.solver}'
        for dirname, _, filenames in os.walk(dir):
            aux = []
            for filename in filenames:
                path = os.path.join(dirname, filename)
                aux.append(path)
            if dirname == f'./output/{self.solver}/dim4':
                self.dim4 = aux.copy()
            elif dirname == f'./output/{self.solver}/dim8':
                self.dim8 = aux.copy()
            elif dirname == f'./output/{self.solver}/dim12':
                self.dim12 = aux.copy()
        self.all_paths.extend(self.dim4)
        self.all_paths.extend(self.dim8)
        self.all_paths.extend(self.dim12)
        
    def shapiro_test(self) -> None:
        """
        The Shapiro-Wilk test tests the null hypothesis that the data was drawn from a normal distribution.
        """
        print(len(self.all_paths))
        for path in self.all_paths:
            df = pd.read_csv(path)
            stat, p = shapiro(df[['fitness', 'finished', 'diversity']])
            if p > 0.05:
                # Do not reject the null hypothesis
                print(f"Normal distribution for: {path}")

    def test(self) -> None:
        ref_sample_path = self.dim12[0]
        ref_sample = pd.read_csv(ref_sample_path)
        #ref_sample = ref_sample[ref_sample['finished'] == True]

        for i in range(len(self.dim12)):
            new_sample_path = self.dim12[i]
            new_sample = pd.read_csv(new_sample_path)
            #new_sample = new_sample[new_sample['finished'] == True]
            if new_sample.shape[0] > 0 and self.mannwhitneyu_test(new_sample, ref_sample):
                ref_sample = new_sample
                ref_sample_path = new_sample_path
        print(ref_sample_path)

    def mannwhitneyu_test(self, sample1, sample2) -> bool:
        _, p_value = mannwhitneyu(sample1['diversity'], sample2['diversity'], alternative="greater") #less
        return p_value < 0.05

                
if __name__ == "__main__":
    stats = Stats('qtable')
    stats.set_file_names()
    stats.shapiro_test()
    stats.test()
