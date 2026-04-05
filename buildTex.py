#!/usr/bin/env python

import os
import sys
import shlex
import shutil
import argparse
import subprocess

DEFAULT_REPS = 2
DEFAULT_TEX_ARGS = ['-cnf-line', 'max_print_line = 10000', '-halt-on-error']


def myMkdir(path: str, dryRun: bool) -> None:
    if dryRun:
        print('$', shlex.join(['mkdir', '-p', path]))
    else:
        os.makedirs(path, exist_ok=True)


def myCmdRun(args: list[str], dryRun: bool) -> None:
    if dryRun:
        print('$', shlex.join(args))
    else:
        subprocess.run(args, check=True)


def buildTex(inPath: str, outPath: str, *, buildDir: str | None, hasBib: bool, reps: int, dryRun: bool) -> bool:
    inDir, inFname = os.path.split(inPath)
    jobName = os.path.splitext(inFname)[0]

    if buildDir is not None:
        myMkdir(buildDir, dryRun)

    os.environ['SOURCE_DATE_EPOCH'] = '0'
    pdflatexCmdLine = ['pdflatex'] + DEFAULT_TEX_ARGS
    if buildDir is not None:
        pdflatexCmdLine.append(f'-output-directory={buildDir}')
    pdflatexCmdLine.append(inPath)

    if buildDir is None:
        buildDir = inDir

    auxPath = os.path.join(buildDir, jobName + '.aux')

    try:
        if hasBib:
            myCmdRun(pdflatexCmdLine, dryRun)
            myCmdRun(['bibtex', auxPath], dryRun)
        for _ in range(reps):
            myCmdRun(pdflatexCmdLine, dryRun)
    except subprocess.CalledProcessError as e:
        print(f'Subprocess exited with return code {e.returncode}.', file=sys.stderr)
        print('Command:', shlex.join(e.cmd), file=sys.stderr)
        return False

    outDir = os.path.dirname(outPath) if outPath.endswith('.pdf') else outPath
    builtPdfPath = os.path.join(buildDir, jobName + '.pdf')

    if outDir != buildDir and outDir != inDir:
        myMkdir(outDir, dryRun)
    if outPath != builtPdfPath:
        if dryRun:
            print('$', shlex.join(['mv', builtPdfPath, outPath]))
        else:
            shutil.move(builtPdfPath, outPath)

    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('in_path',
        help='path to input tex file')
    parser.add_argument('out_path',
        help='path to output pdf path or output directory')
    parser.add_argument('--build-dir', required=True,
        help='path to build directory')
    parser.add_argument('--has-bib', action='store_true', default=False,
        help='use bibtex?')
    parser.add_argument('--reps', type=int, default=DEFAULT_REPS,
        help=f'number of times to run pdflatex (after bibtex, default: {DEFAULT_REPS})')
    parser.add_argument('--dry-run', action='store_true', default=False)
    args = parser.parse_args()

    succeeded = buildTex(args.in_path, args.out_path, buildDir=args.build_dir,
        hasBib=args.has_bib, reps=args.reps, dryRun=args.dry_run)
    sys.exit(1 - succeeded)


if __name__ == '__main__':
    main()
