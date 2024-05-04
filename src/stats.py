
import os
import pandas as pd
from scipy.stats import shapiro, mannwhitneyu
from scipy.stats import norm
from math import sqrt
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
import numpy as np


from typing import Optional


class Stats:
    def __init__(self, folder: str) -> None:
        self.folder = folder
        self.all_paths = []
        self.total_paths = None

    def set_file_names(self) -> None:
        for dirname, _, filenames in os.walk(self.folder):
            for filename in filenames:
                path = os.path.join(dirname, filename)
                self.all_paths.append(path)
        self.total_paths = len(self.all_paths)
        self.all_paths.sort()

    def shapiro_test(self) -> None:
        """
        The Shapiro-Wilk test tests the null hypothesis that the data was drawn from a normal distribution.
        """
        print("Total paths analised:", len(self.all_paths))
        for path in self.all_paths:
            df = pd.read_csv(path)
            _, p = shapiro(df[['fitness', 'finished', 'diversity']])
            if p > 0.05:
                # Do not reject the null hypothesis
                print(f"Normal distribution for: {path}")

    def test(self, feature: str, alpha: float) -> Optional[str]:
        p_values = [[0 for _ in range(self.total_paths)] for _ in range(self.total_paths)]
        adjust = alpha / ( self.total_paths * (self.total_paths + 1) / 2 )
        diff_index = set()
        for i in range(self.total_paths):
            for j in range(i + 1, self.total_paths):
                i_csv = pd.read_csv(self.all_paths[i])
                j_csv = pd.read_csv(self.all_paths[j])
                _, p = mannwhitneyu(i_csv[feature], j_csv[feature])
                p_values[i][j] = p #/ (alpha * total_compations)
                p_values[j][i] = p_values[i][j]
                if p < adjust:
                    diff_index.add(i)
                    diff_index.add(j)
        col = [path[26:-4] for path in self.all_paths]
        p_values = pd.DataFrame(p_values, columns=col)

        s = self.folder.replace('/', '_')
        p_values.insert(0, 'Nomes das Colunas', p_values.columns)
        p_values.to_excel(f'./output/stats{s}_{feature}.xlsx', index=False) 

        def cc(path):
            df = pd.read_csv(path)
            return df[feature].mean()

        if len(diff_index) > 0:
            mean = {i: cc(path) for i, path in zip(diff_index, self.all_paths)}
            max_count = max(mean.values())
            return [self.all_paths[i] for i, value in mean.items() if value == max_count]
        return None
    
    def proportions_z_test(self, successes1, nobs1, successes2, nobs2):
        p1 = successes1 / nobs1
        p2 = successes2 / nobs2
        if p1 == p2:
            return 0
        p_combined = (successes1 + successes2) / (nobs1 + nobs2)
        se_combined = sqrt(p_combined * (1 - p_combined) * (1/nobs1 + 1/nobs2))
        z = (p1 - p2) / se_combined
        return z

    def z_to_p(self, z_statistic):
        if z_statistic < 0:
            p_value = norm.cdf(z_statistic)
        else:
            p_value = 1 - norm.cdf(z_statistic)
        return p_value

    def test2(self, feature: str, alpha: float) -> None:
        p_values = [[0 for _ in range(self.total_paths)] for _ in range(self.total_paths)]
        adjust = alpha / ( self.total_paths * (self.total_paths + 1) / 2 )
        diff_index = set()
        for i in range(self.total_paths):
            for j in range(i + 1, self.total_paths):
                i_csv = pd.read_csv(self.all_paths[i])
                j_csv = pd.read_csv(self.all_paths[j])

                i_true = i_csv[i_csv[feature] == True][feature].sum()
                j_true = j_csv[j_csv[feature] == True][feature].sum()
                i_total = len(i_csv[feature])
                j_total = len(j_csv[feature])

                z = self.proportions_z_test(i_true, i_total, j_true, j_total)
                p = self.z_to_p(z)
                p_values[i][j] = round(p, 3)
                p_values[j][i] = p_values[i][j]
                if p < alpha:
                    diff_index.add(i)
                    diff_index.add(j)
        col = [path[26:-4] for path in self.all_paths]

        s = self.folder.replace('/', '_')
        p_values = pd.DataFrame(p_values, columns=col)
        p_values.insert(0, 'Nomes das Colunas', p_values.columns)
        p_values.to_excel(f'./output/stats{s}_{feature}.xlsx', index=False) 

        def cc(path):
            df = pd.read_csv(path)
            return df[df[feature] == True][feature].count()

        if len(diff_index) > 0:
            mean = {i: cc(path) for i, path in zip(diff_index, self.all_paths)}
            max_count = max(mean.values())
            return [value for i, value in mean.items() if value == max_count]
        return None

    def avg_std(self, path: str, feature: str) -> tuple[float, float]:
        df = pd.read_csv(path)
        return df[feature].mean() , df[feature].std()

                
if __name__ == "__main__":
    # folders = ['./output/sea/dim4']
    # for folder in folders:
    #     print("\n", folder, "\n")
    #     stats = Stats(folder)
    #     stats.set_file_names()
    #     print(stats.test('fitness', 0.05))
    # folders = ['./output/aco/dim4', './output/aco/dim8', './output/aco/dim12']
    # for folder in folders:
    #    # print("\n", folder, "\n")
    #    stats = Stats(folder)
    #    stats.set_file_names()
    #    stats.shapiro_test()
    #    # print(stats.test('fitness', 0.05))
    #    # print(stats.test('diversity', 0.05))
    #    # print(stats.test2('finished', 0.05))
    # folders = ['./output/sea/dim4', './output/sea/dim8', './output/sea/dim12']
    # for folder in folders:
    #     # print("\n", folder, "\n")
    #     stats = Stats(folder)
    #     stats.set_file_names()
    #     stats.shapiro_test()
    #     # print(stats.test('fitness', 0.05))
    #     # print(stats.test('diversity', 0.05))
    #     # print(stats.test2('finished', 0.05))
    # folders = ['./output/qtable/dim4', './output/qtable/dim8', './output/qtable/dim12']
    # for folder in folders:
    #     # print("\n", folder, "\n")
    #     stats = Stats(folder)
    #     stats.set_file_names()
    #     stats.shapiro_test()
    #     # print(stats.test('fitness', 0.05))
    #     # print(stats.test('diversity', 0.05))
    #     # print(stats.test2('finished', 0.05))

    folder = ['./output/sea/dim4/map_02_pool_0.15_cross_0.7_mut_0.1.csv', './output/qtable/dim4/map_02_pool_0.2_cross_0.9_mut_0.05.csv', './output/aco/dim4/map_02_alpha_0.8_evap0.8.csv']
    for path in folder:
        print("\n", path, "\n")
        stats = Stats(path)
        print(stats.avg_std(path, "fitness"))
        # print(stats.avg_std(path, "finished"))
        # print(stats.avg_std(path, "diversity"))
