# IE 300 Lab

This repository contains material for the _lab_ component of IE 300 (Analysis of Data),
a course offered at the [ISE department at UIUC](https://ise.illinois.edu/).

This repository is meant for instructors to use as a starting point to design their course materials.
If you are a student, do not use this repository; consult the materials shared by your instructors instead.

## Web access

You can find the case study PDFs at <https://sharmaeklavya2.github.io/IE300-lab/output/>,
and the datasets referenced in them at <https://sharmaeklavya2.github.io/IE300-lab/datasets/>.

## Contents of this repository

The directory `src` contains the LaTeX source for the case studies
and python code to draw plots that would be included in the case studies.
The directory `datasets` contains datasets used by the case studies.

If you are on Linux/macOS, run `make` to create the case study PDFs.
(You can find out which commands it will run using `make --dry-run`. Also try `SILENT=1 make`.)
It will output the case study PDFs in the `output` directory.
The intermediate files (`.aux`, `.log`, the figures as PDFs) can be found in the `build` directory.
