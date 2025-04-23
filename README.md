[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14926215.svg)](https://doi.org/10.5281/zenodo.14926215)

# Transcripts_Plots

<p align="center">
<img src="https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Images/Transcripts_Plots_Logo.png" width="400" height="400" style="display: block; margin: 0 auto">

## Overview:

	--------------------------------------------------------------------------------
    The Transcripts_Plots script is designed to generate
    publication‑quality gene model plots from transcript annotation data
    found in GTF files. It extracts and plots the exon structure and/or
    coding sequence (CDS) of a given transcript, supporting both
    single‐transcript and multi‐transcript modes. The script also
    accommodates different display modes—either plotting the introns to
    their full scale or compressing them for easier viewing.
    --------------------------------------------------------------------------------

## Motivation:

	--------------------------------------------------------------------------------
    Transcript models are invaluable in computational analyses, as they
    aid in conceptual representation and facilitate comparisons among gene
    models across isoforms, paralogs, and orthologs. However, existing
    tools do not readily support plotting transcript models by
    themselves. To address this gap, we developed a tool that extracts
    transcript model information from a genome annotation file (e.g., GTF)
    and generates a corresponding transcript model plot.
	--------------------------------------------------------------------------------

## Authorship:

    --------------------------------------------------------------------------------
	Author:         Rodolfo Aramayo
    Work_Email:     raramayo@tamu.edu
    Personal_Email: rodolfo@aramayo.org
    --------------------------------------------------------------------------------

## Copyright:

    --------------------------------------------------------------------------------
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or (at
    your option) any later version.

    This program is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
    --------------------------------------------------------------------------------

## Version:

	--------------------------------------------------------------------------------
	v1.0.3
	--------------------------------------------------------------------------------

## Code_Overview:

<pre>
--------------------------------------------------------------------------------
<a href="https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Docs/Code_Overview.md" target="_blank">Code_Overview.md</a>
--------------------------------------------------------------------------------
</pre>


## Usage:

<pre>
--------------------------------------------------------------------------------
<a href="https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Docs/Mini_Tutorial.md" target="_blank">Mini_Tutorial.md</a>
--------------------------------------------------------------------------------
</pre>


## Flags:

	--------------------------------------------------------------------------------
	FLAG:           "--transcript"
    REQUIRED:       Yes
    FORMAT:         Alphanumeric String
    DEFAULT:        No default
    HELP:           Transcript ID
    NOTES:          Script was tested with Ensembl transcripts IDs
	--------------------------------------------------------------------------------
    FLAG:           "--gtf"
    REQUIRED:       Yes
    FORMAT:         Alphanumeric String
    DEFAULT:        No default
    HELP:           GTF file (required with '--transcript')
    NOTES:          Script was tested with Ensembl GTF files
	--------------------------------------------------------------------------------
    FLAG:           "--file"
    REQUIRED:       Yes
    FORMAT:         Text file
    DEFAULT:        No default
    HELP:           Text file with multiple transcripts and GTF paths (2 tab-delimited columns)
    NOTES:          Text file containing multiple transcripts and their associated GTF files paths and names
    Name_Example:   Ensembl_multiple_genes_transcripts_list.txt
    File_Content:   No Header
                    ENST00000278224<tab>Homo_sapiens.GRCh38.113.chr.gtf<$>
                    ENST00000380525<tab>/path/to/other/gtf_file/ENSG00000110619_GTF.gtf<$>
                    ENST00000397111<tab>Homo_sapiens.GRCh38.113.chr.gtf<$>
	--------------------------------------------------------------------------------
    FLAG:           "--select"
    REQUIRED:       No
    FORMAT:         Alphanumeric String
    CHOICES:        'exons', 'CDS', 'both'
    DEFAULT:        'exons'
    HELP:           Select feature to be plotted: 'exons', 'CDS', or 'both'
	--------------------------------------------------------------------------------
    FLAG:           "--exon_color"
    REQUIRED:       No
    FORMAT:         Hexadecimal Color
    CHOICES:        https://g.co/kgs/CNRQC6y
    DEFAULT:        '#305c96'
    HELP:           Color for Exons
	--------------------------------------------------------------------------------
    FLAG:           "--CDS_color"
    REQUIRED:       No
    FORMAT:         Hexadecimal Color
    CHOICES:        https://g.co/kgs/CNRQC6y
    DEFAULT:        '#b38d1b'
    HELP:           Color for Coding Exons
	--------------------------------------------------------------------------------
    FLAG:           "--full_scale"
    REQUIRED:       No
    FORMAT:         Alphanumeric String = '--full_scale'
    CHOICES:        Omitting the flag:  == 'False'
                    Providing the flag: == 'True'
	ACTION:         store_true
    DEFAULT:        'False'
    HELP:           Plot entire region to scale
	                Otherwise introns are compressed uniformly
	--------------------------------------------------------------------------------
	FLAG:           "--no_transcript_label"
	REQUIRED:       No
	FORMAT:         Alphanumeric String = '--no_transcript_label'
	                Omitting the flag:  == 'True'
	                Providing the flag: == 'False'
	ACTION:         store_false
	DEFAULT:        'True'
	HELP:           Do not print the transcript label above the plot
	--------------------------------------------------------------------------------
	FLAG:           "--labels"
    REQUIRED:       No
    FORMAT:         Alphanumeric String
    CHOICES:        'none', 'full'
    DEFAULT:        'none'
    HELP:           Label features with numbers
	                Only the first and last are labeled
	--------------------------------------------------------------------------------
    FLAG:           "--format"
    REQUIRED:       No
    FORMAT:         Alphanumeric String
    CHOICES:        'pdf', 'png', 'svg'
    DEFAULT:        'pdf'
    HELP:           Output file format
	--------------------------------------------------------------------------------
    FLAG:           "--dpi"
    REQUIRED:       No
    FORMAT:         Integer
    DEFAULT:        '300'
    HELP:           Resolution (dpi) for PNG output file
	--------------------------------------------------------------------------------
	FLAG:           "--dynamic_resize"
    REQUIRED:       No
    ACTION:         store_true
    CHOICES:        Omitting the flag:  == 'False'
                    Providing the flag: == 'True'
    DEFAULT:        'False'
    HELP:           Dynamically adjust figure size to match drawn content
	                Eliminates extra whitespace
	--------------------------------------------------------------------------------
    FLAG:           "--figsize"
    REQUIRED:       No
    #_Of_Arguments: 2
    FORMAT:         Float
    DEFAULT:        '10, 8'
    HELP:           Figure size in inches (width height)
	--------------------------------------------------------------------------------
	FLAG:           "--transcript_fontsize"
	REQUIRED:       No
	FORMAT:         Integer
	DEFAULT:        '18'
	HELP:           Font size for the transcript label
	--------------------------------------------------------------------------------
    FLAG:           "--output"
    REQUIRED:       No
    FORMAT:         Alphanumeric
    DEFAULT:        'Transcripts_Plots_dir_Run01'
    HELP:           Output directory name
	                If provided and exists, a numeric suffix is added (e.g., Test01)
	--------------------------------------------------------------------------------
    FLAG:           "-v", "--version"
    REQUIRED:       No
    ACTION:         version
    FORMAT:         Alphanumeric
    HELP:           Show program version's number and exit
	--------------------------------------------------------------------------------
    FLAG:           "-h", "--help"
    REQUIRED:       No
    ACTION:         help
    FORMAT:         Alphanumeric String
    HELP:           show this help message and exit
    --------------------------------------------------------------------------------

## Dependencies:

    --------------------------------------------------------------------------------
    Python3:        Required:
                    https://www.python.org/downloads/
    Matplotlib:     Required:
                    https://matplotlib.org/
                    https://pypi.org/project/matplotlib/
    --------------------------------------------------------------------------------

## Development/Testing Environment:

    --------------------------------------------------------------------------------
    Distributor ID: Apple, Inc.
    Description:    Apple M1 Max
    Release:        15.3.1
    Codename:       Sequoia

    Script was tested with:
                    | Python Version | matplotlib | pandas | seaborn |
                    |----------------|------------|--------|---------|
                    | 3.8.20         | 3.7.5      | 2.0.3  | 0.13.2  |
                    | 3.9.21         | 3.9.4      | 2.2.3  | 0.13.2  |
                    | 3.10.16        | 3.10.1     | 2.2.3  | 0.13.2  |
                    | 3.11.11        | 3.10.1     | 2.2.3  | 0.13.2  |
                    | 3.12.9         | 3.10.1     | 2.2.3  | 0.13.2  |
                    | 3.13.2         | 3.10.1     | 2.2.3  | 0.13.2  |
    --------------------------------------------------------------------------------

## Repository:

<pre>
--------------------------------------------------------------------------------
<a href="https://github.com/raramayo/Transcripts_Plots_Python" target="_blank">Transcripts_Plots_Python</a>
--------------------------------------------------------------------------------
</pre>

## Issues:

<pre>
--------------------------------------------------------------------------------
<a href="https://github.com/raramayo/Transcripts_Plots_Python/issues" target="_blank">Transcripts_Plots_Python_Issues</a>
--------------------------------------------------------------------------------
</pre>
