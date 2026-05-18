#!/usr/bin/env python3

"""Recursively generate an HTML index page for each directory."""

import os
from os.path import join as pjoin
import argparse
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

IGNORES = set("""
.git
.gitignore
build
__pycache__
index.html
index-style.css
Thumbs.db
Desktop.ini
.DS_Store
""".split())

IGNORE_EXTS = set("""
.swp
.swo
""".split())

HTML_BEGIN = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="color-scheme" content="light dark" />
""".strip()


def generateIndex(root: str, curDir: str, fnames: list[str], dnames: list[str], depth: int) -> None:
    parts = [HTML_BEGIN]
    relCurDir = os.path.relpath(curDir, root).replace(os.sep, '/')
    parts.append('<link rel="stylesheet" href="{}{}" />'.format('../' * depth, 'index-style.css'))
    parts.append(f'<title>Index of {relCurDir}</title>')
    parts.append('</head>\n<body>')
    parts.append(f'<h1>Index of {relCurDir}</h1>')
    parts.append('<ul>')
    for dname in dnames:
        parts.append(f'<li class="dir"><a href="{dname}/">{dname}</a></li>')
    for fname in fnames:
        parts.append(f'<li class="file"><a href="{fname}">{fname}</a></li>')
    parts.append('</ul>\n</body>\n</html>\n')
    with open(os.path.join(curDir, 'index.html'), 'w') as fp:
        fp.write('\n'.join(parts))


def recurseOnDirs(root: str, curDir: str, action, depth: int) -> None:
    fnames, dnames = [], []
    for entry in os.scandir(curDir):
        if entry.name not in IGNORES:
            if entry.is_dir():
                dnames.append(entry.name)
            elif entry.is_file():
                _, ext = os.path.splitext(entry.name)
                if ext not in IGNORE_EXTS:
                    fnames.append(entry.name)
            else:
                raise Exception('Strange file: {}'.format(entry.path))
    action(root, curDir, sorted(fnames), sorted(dnames), depth)
    for dname in dnames:
        newCurDir = os.path.join(curDir, dname)
        recurseOnDirs(root, newCurDir, action, depth+1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dir_path')
    args = parser.parse_args()
    if os.path.realpath(args.dir_path) != os.path.realpath(ROOT_DIR):
        shutil.copyfile(pjoin(ROOT_DIR, 'index-style.css'), pjoin(args.dir_path, 'index-style.css'))
    recurseOnDirs(args.dir_path, args.dir_path, generateIndex, 0)


if __name__ == '__main__':
    main()
