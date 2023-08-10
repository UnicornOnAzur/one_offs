# -*- coding: utf-8 -*-
"""
@author: QtyPython2020

"""
from math import floor, ceil
import matplotlib.pyplot as plt
from numpy import std, mean
from scipy.stats import norm
import seaborn as sns

def normalize_values(sample: list[float]) -> list[float]:
    """


    Parameters
    ----------
    sample : list[float]
        DESCRIPTION.

    Returns
    -------
    list[float]
        DESCRIPTION.

    """
    sample_mean = mean(sample)
    sample_std = std(sample)
    dist = norm(sample_mean, sample_std)
    probabilities = list(map(dist.pdf, sorted(sample)))
    return probabilities

def plot_distribution(values: list[list[float]],
                      labels: list[str]=None,
                      title: str = None,
                      num_bins: int =20) -> plt.Figure:
    """


    Parameters
    ----------
    values : list[list[float]]
        DESCRIPTION.
    labels : list[str], optional
        DESCRIPTION. The default is None.
    num_bins : int, optional
        DESCRIPTION. The default is 20.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    cols = len(values)
    fig, axes = plt.subplots(nrows=3,
                             ncols=cols,
                             figsize=(cols*4, 10),
                             sharex=False,
                             sharey=False)
    fig.suptitle("Distributions" if title is None else f"Distributions of {title}")
    labels = [None]*len(values) if labels is None else labels
    for pos, sample_values in enumerate(zip(values, labels)):
        value, label = sample_values
        sample = sorted(value)
        probabilities = normalize_values(sample)

        for i in range(3):
            axes[i][pos].set_xlim(floor(min(sample)), ceil(max(sample)))

        axes[0][pos].set_title(label)
        axes[0][pos].hist(sample,
                          bins=num_bins,
                          density=True)
        ax_mirror0 = axes[0][pos].twinx()
        ax_mirror0.plot(sample,
                          probabilities,
                          color="orange")
        sns.histplot(sample,
                     bins=num_bins,
                     stat="density",
                     ax=axes[1][pos])
        ax_mirror1 = axes[1][pos].twinx()
        sns.kdeplot(sample,
                    color="red",
                    ax=ax_mirror1)
        sns.lineplot({"x":sample,
                      "y":probabilities},
                     x="x",y="y",
                     color="orange",
                     ax=axes[2][pos])
        ax_mirror2 = axes[2][pos].twinx()
        sns.kdeplot(sample,
                    color="red",
                    ax=ax_mirror2)
    return fig

iris = sns.load_dataset('iris')
cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
data = iris.loc[:, cols].transpose().values
plot_distribution(data, cols, "tips")
plt.show()

tips = sns.load_dataset("tips")
cols = ['total_bill', 'tip', 'size']
data = tips.loc[:, cols].transpose().values
plot_distribution(data, cols, "tips")
plt.show()
