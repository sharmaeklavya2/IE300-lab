#!/usr/bin/env python

import os
import argparse
import math
import numpy as np
from scipy.stats import binom, norm
import matplotlib.pyplot as plt

δ = 0.04

def binomPlot(nList: list[int], p: float, normalize: bool, nRows: int, nCols: int, outFile: str) -> None:
    assert len(nList) == nRows * nCols
    _, axes = plt.subplots(nRows, nCols, figsize=(nCols*2.7, nRows*2.1))
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
            ax.plot(xn, yn, linestyle='--', color='red')
        else:
            ax.set_ylim(-δ, 1+δ)
        ax.vlines(x, 0, y, linewidth=2)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.25, hspace=0.4)
    plt.savefig(outFile)


def gammaPlot(nList: list[int], nRows: int, nCols: int, outFile: str) -> None:
    assert len(nList) == nRows * nCols
    _, axes = plt.subplots(nRows, nCols, figsize=(nCols*2.7, nRows*2.1))
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
        ax.plot(xn, yn, linestyle='--', color='red')
        ax.plot(x, y)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.25, hspace=0.4)
    plt.savefig(outFile)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('out_dir', help='path to output directory')
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    os.chdir(args.out_dir)
    plt.style.use('seaborn-v0_8-whitegrid')
    binomPlot(nList=[1, 2, 3, 10, 20, 50], p=0.3, normalize=False,
        nRows=2, nCols=3, outFile='binom1.pdf')
    binomPlot(nList=[1, 2, 5, 20, 100, 1000], p=0.3, normalize=True,
        nRows=2, nCols=3, outFile='binom2.pdf')
    # gammaPlot(nList=[1, 2, 3, 5, 10, 100], nRows=3, nCols=2, outFile='gamma.pdf')


if __name__ == '__main__':
    main()
