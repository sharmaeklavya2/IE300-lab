#!/usr/bin/env python

import os
import argparse
import math
import numpy as np
from scipy.stats import binom, norm
import matplotlib.pyplot as plt

δ = 0.04
COLOR1 = None
COLOR2 = 'red'

def binomPlot(nList: list[int], p: float, normalize: bool, nRows: int, nCols: int, outFile: str) -> None:
    assert len(nList) == nRows * nCols
    fig, axes = plt.subplots(nRows, nCols, figsize=(nCols*2.7, nRows*2.1))
    axes = axes.flatten()
    for ax, n in zip(axes, nList):
        x = np.arange(0, n+1)
        y = binom.pmf(x, n, p)
        x = x/n
        if normalize:
            y = y*n
        ax.set_title(f'$n = {n}$')

        mean, stddev = p, np.sqrt(p * (1-p) / n)
        xn = np.linspace(mean - 4 * stddev, mean + 4 * stddev, 101)
        yn = norm.pdf(xn, loc=mean, scale=stddev)
        if normalize:
            ax.set_xlim(mean - 4 * stddev, mean + 4 * stddev)
            ax.plot(xn, yn, linestyle='--', color=COLOR2)
        else:
            ax.set_ylim(-δ, 1+δ)
        ax.vlines(x, 0, y, linewidth=2, color=COLOR1)
    fig.tight_layout()
    fig.subplots_adjust(wspace=0.25, hspace=0.4)
    fig.savefig(outFile)


def gammaPlot(nList: list[int], nRows: int, nCols: int, outFile: str) -> None:
    assert len(nList) == nRows * nCols
    fig, axes = plt.subplots(nRows, nCols, figsize=(nCols*2.7, nRows*2.1))
    axes = axes.flatten()
    xn = np.linspace(-4, 4, 101)
    yn = norm.pdf(xn)
    for ax, n in zip(axes, nList):
        r = np.sqrt(n)
        x = np.linspace(-min(r, 4), 4, 101)
        s = n + x * r
        y = (r/math.gamma(n)) * np.pow(s, n-1) * np.exp(-s)

        ax.set_title(f'$n = {n}$')
        ax.set_xlim(-4, 4)
        ax.set_ylim(-δ, 1+δ)
        ax.plot(xn, yn, linestyle='--', color=COLOR2)
        ax.plot(x, y, color=COLOR1)
    fig.tight_layout()
    fig.subplots_adjust(wspace=0.25, hspace=0.4)
    fig.savefig(outFile)


def comparePlot(x, y, xstd, ystd, outFile: str | None, *,
        xTitle: str | None = None, yTitle: str | None = None,
        label: str | None = None, stdLabel: str | None = None,
        scatter: bool = False, ylims: tuple[float, float] | None = None,
        ) -> None:
    fig, ax = plt.subplots(figsize=(4, 3))
    if xstd is not None and ystd is not None:
        ax.plot(xstd, ystd, linestyle='--', color=COLOR2, label=stdLabel)
    if scatter:
        ax.scatter(x, y, s=1, label=label, color=COLOR1)
    else:
        ax.plot(x, y, label=label, color=COLOR1)
    if xTitle:
        ax.set_xlabel(xTitle)
    if yTitle:
        ax.set_ylabel(yTitle)
    if label and stdLabel:
        ax.legend(loc="upper right")
    if ylims:
        ax.set_ylim(*ylims)
    fig.tight_layout()
    if outFile is None:
        plt.show()
    else:
        fig.savefig(outFile, bbox_inches='tight')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('out_dir', help='path to output directory')
    parser.add_argument('--seed', help='random seed (default: 1)', type=int, default=1)
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    os.chdir(args.out_dir)
    plt.style.use('seaborn-v0_8-whitegrid')
    binomPlot(nList=[1, 2, 3, 10, 20, 50], p=0.3, normalize=False,
        nRows=2, nCols=3, outFile='binom1.pdf')
    binomPlot(nList=[1, 3, 10, 30, 100, 300], p=0.3, normalize=True,
        nRows=2, nCols=3, outFile='binom2.pdf')
    # gammaPlot(nList=[1, 2, 3, 5, 10, 100], nRows=3, nCols=2, outFile='gamma.pdf')

    n = 200
    p = np.arange(n) / n
    x = -np.log(1-p)
    y = norm.ppf(p)
    ystd = x - 1
    comparePlot(x, y, x, ystd, 'expVsNormQQ.pdf',
        xTitle='exponential quantiles', yTitle='normal quantiles')

    xstd = np.linspace(0, 4, 101)
    ystd = np.exp(-xstd)
    xstd = np.concat([[-4, 0], xstd])
    ystd = np.concat([[0, 0], ystd])
    x = np.linspace(-4, 4, 201)
    y = norm.pdf(x)
    comparePlot(x, y, xstd, ystd, 'expVsNorm.pdf',
        stdLabel='Exp(1)', label='N(0, 1)')

    """
    n = 200
    p = np.arange(1, n+1) / n
    x = -np.log(1-p)
    y = p
    ystd = 0.5 + (x - 1)/np.sqrt(12)
    comparePlot(x, y, x, ystd, 'expVsUnifQQ.pdf',
        xTitle='exponential quantiles', yTitle='uniform quantiles')
    """

    rng = np.random.default_rng(seed=args.seed)

    n = 1000
    y = rng.standard_normal(n)
    y.sort()
    p = (np.arange(n) + 0.5)/n
    x = -np.log(1-p)
    xstd = np.array([np.min(x), np.max(x)])
    ystd = xstd - 1
    comparePlot(x, y, xstd, ystd, 'expVsNormQQE.pdf', scatter=True,
        xTitle='exponential quantiles', yTitle='sampled normal quantiles')

    n = 1000
    mat = rng.pareto(a=1.5, size=(1000, n))
    y = mat.mean(axis=0)
    y.sort()
    p = (np.arange(n) + 0.5)/n
    x = norm.ppf(p)
    # comparePlot(x, y, None, None, None, scatter=True,
    comparePlot(x, y, None, None, 'paretoMeanQQE.pdf', scatter=True, ylims=(-δ, 15),
        xTitle='normal quantiles', yTitle='sampled mean-of-pareto quantiles')


if __name__ == '__main__':
    main()
