[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14926215.svg)](https://doi.org/10.5281/zenodo.14926215)
# Transcripts_Plots
![alt text](https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Images/Transcripts_Plots_Logo.png)

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

## Motivation

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
	Author:                          Rodolfo Aramayo
    Work_Email:                      raramayo@tamu.edu
    Personal_Email:                  rodolfo@aramayo.org
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

## Script_Version:

	--------------------------------------------------------------------------------
	v1.0.1
	--------------------------------------------------------------------------------

## Script_Usage:
### Key Capabilities
+ ### Input Flexibility:
  + Single Transcript:
	+ Use the ```-t/--transcript``` flag together with a GTF file ```(-g/--gtf)``` to plot one transcript.
   + Multiple Transcripts:
	 + Use the ```-f/--file``` flag to supply a tab-delimited file where each line lists a transcript ID and its corresponding GTF file path.
+ ### Feature Selection:
  + ```Exons``` Only: Plot the exon structures.
  + ```CDS``` Only: Plot only the coding sequences.
  + ```Both```: Generate separate output files for exons and CDS.
+ ### Strand-Specific Plotting:
  + The script automatically rearranges features so that transcripts
    from both the plus (Watson) and minus (Crick) strands are always
    plotted from ```5′ to 3′ (left to right)```. This ensures that the
    first feature (E01 or CE01) always represents the ```5′ end```
    regardless of genomic orientation.
+ ### Intron Scaling Options:
  + Full Scale ```(--full_scale)```: Plots introns at their true genomic length.
  + Compressed Introns (default): Introns are replaced with a fixed small gap to produce a more compact view.
	+ The output filenames automatically reflect the intron display mode ```(e.g., _Short_Introns vs. _Full_Introns)```.
+ ### Customizable Appearance:
  + Change the colors of exons ```(--exon_color)``` and CDS ```(--CDS_color)```.
  + Adjust the figure size using the ```--figsize``` flag.
  + Set the output file format ```(pdf, png, or svg)``` and resolution ```(--dpi)```.

+ ### Labeling Options:
  + Print Transcript Label (Default Behavior):
	+ Transcript labels (including gene name, transcript ID, transcript size, and number of features) are automatically placed above the gene model.
  + Disable Transcript Label:
	+ You can disable the transcript label by using the ```--no_transcript_label``` flag.
   + You can choose not to label features ```(--labels none)``` or label the first and last feature only ```(--labels full)```.
+ ### Output Naming:
  + The produced file names incorporate whether introns are displayed in full scale or compressed, for example:

	```
	ENST00000380152_exons_Short_Introns.pdf
	ENST00000380152_CDS_Full_Introns.pdf
	```
+ ### Version Information:
  + A version flag ```(-v/--version)``` is available to print the script version and exit.

+ ### Dependency Checking:
  + At startup, the script checks for required modules (like ```matplotlib```) and provides instructions to install any that are missing.
## How to Use the Script:
### Single Transcript Mode:
+ Run the script by providing a transcript ID and a GTF file:

	```
	python3 Transcripts_Plots.py \
	--transcript ENST00000380152 \
	--gtf Ensembl_Gene_ENSG00000139618.gtf \
	--select exons
	```
+ This command will produce an exon plot (with compressed introns by default) and output a file named similar to:

	```
	ENST00000380152_exons_Short_Introns.pdf
	```
+ To generate a CDS plot at full scale:

	```
	python3 Transcripts_Plots.py \
	--transcript ENST00000380152 \
	--gtf Ensembl_Gene_ENSG00000139618.gtf \
	--select CDS \
	--full_scale
	```
+ This will produce a file like:

	```
	ENST00000380152_CDS_Full_Introns.pdf
	```
+ To generate a CDS plot at full scale with a larger transcript font size:

	```
	python3 Transcripts_Plots.py \
	--transcript ENST00000380152 \
	--gtf Ensembl_Gene_ENSG00000139618.gtf \
	--select CDS \
	--full_scale \
	--transcript_fontsize 72
	```
+ This will produce a file like:

	```
	ENST00000380152_CDS_Full_Introns.pdf
	```
### Multiple Transcripts Mode:
  + Create a tab-delimited file (e.g., ```Ensembl_multiple_genes_transcripts_list.txt```) where each line contains a transcript ID and the corresponding GTF file:

	```
	ENST00000380152   Ensembl_Gene_ENSG00000139618.gtf
	ENST00000278224   /path/to/other_GTF.gtf
	...
	```
	+ Then run:

	```
	python3 Transcripts_Plots.py \
	--file Ensembl_multiple_genes_transcripts_list.txt \
	--select both \
	--full_scale
	```
	+ This will generate two output files per transcript (one for exons and one for CDS) with file names reflecting the full-scale mode.
+ Additional Examples
  + Adjust Figure Size:

	```
	python3 Transcripts_Plots.py \
	--transcript ENST00000380152 \
	--gtf Ensembl_Gene_ENSG00000139618.gtf \
	--figsize 15 12
	```
+ Show Version:

  ```
  python3 Transcripts_Plots.py --version
  ```

### Example Output:
+ ### Command:

	```
	python3 Transcripts_Plots.py \
	--transcript ENST00000278224 \
	--gtf Ensembl_Gene_ENSG00000110619.gtf \
	--labels full \
	--select exons \
	--format png
	```

+ ### Output:
![alt text](https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Images/ENST00000278224_exons_Short_Introns.png)

## Script_Flags:

	--------------------------------------------------------------------------------
	FLAG:                            "-t", "--transcript"
    REQUIRED:                        "Yes"
    FORMAT:                          "Alphanumeric String"
    DEFAULT:                         "No default"
    HELP:                            "Transcript ID"
    NOTES:                           "Script was tested with Ensembl transcripts IDs"
	--------------------------------------------------------------------------------
    FLAG:                            "-g", "--gtf"
    REQUIRED:                        "Yes"
    FORMAT:                          "Alphanumeric String"
    DEFAULT:                         "No default"
    HELP:                            "GTF file (required with -t)"
    NOTES:                           "Script was tested with Ensembl GTF files"
	--------------------------------------------------------------------------------
    FLAG:                            "-f", "--file"
    REQUIRED:                        "Yes"
    FORMAT:                          "Text file"
    DEFAULT:                         "No default"
    HELP:                            "Text file with multiple transcripts and GTF paths (2 tab-delimited columns)"
    NOTES:                           "Text file containing multiple transcripts and their associated GTF files paths and names"
    File_Name_Example:               "Ensembl_multiple_genes_transcripts_list.txt"
    File_Content:                    "No Header"
                                     ENST00000278224<tab>Homo_sapiens.GRCh38.113.chr.gtf<$>
                                     ENST00000380525<tab>/path/to/other/gtf_file/ENSG00000110619_GTF.gtf<$>
                                     ENST00000397111<tab>Homo_sapiens.GRCh38.113.chr.gtf<$>
	--------------------------------------------------------------------------------
    FLAG:                            "-s", "--select"
    REQUIRED:                        "No"
    FORMAT:                          "Alphanumeric String"
    CHOICES:                         "exons", "CDS", "both"
    DEFAULT:                         "exons"
    HELP:                            "Select feature to be plotted: "exons", "CDS", or "both""
	--------------------------------------------------------------------------------
    FLAG:                            "--exon_color"
    REQUIRED:                        "No"
    FORMAT:                          "Hexadecimal Color"
    CHOICES:                         "https://g.co/kgs/CNRQC6y"
    DEFAULT:                         "#305c96"
    HELP:                            "Color for Exons"
	--------------------------------------------------------------------------------
    FLAG:                            "--CDS_color"
    REQUIRED:                        "No"
    FORMAT:                          "Hexadecimal Color"
    CHOICES:                         "https://g.co/kgs/CNRQC6y"
    DEFAULT:                         "#b38d1b"
    HELP:                            "Color for Exons"
	--------------------------------------------------------------------------------
    FLAG:                            "--full_scale"
    REQUIRED:                        "No"
    FORMAT:                          "Alphanumeric String = "--full_scale""
    CHOICES:                         "Omitting the flag:  == "False""
                                     "Providing the flag: == "True""
	ACTION:                          "store_true"
    DEFAULT:                         "False"
    HELP:                            "Plot entire region to scale; otherwise introns are compressed uniformly"
	--------------------------------------------------------------------------------
	FLAG:                            "--no_transcript_label"
	REQUIRED:                        "No"
	FORMAT:                          "Alphanumeric String = "--print_transcript_label""
	                                 "Omitting the flag:  == "True""
	                                 "Providing the flag: == "False""
	ACTION:                          "store_false"
	DEFAULT:                         "True"
	HELP:                            "Do not print the transcript label above the plot"
	--------------------------------------------------------------------------------
	FLAG:                            "--labels"
    REQUIRED:                        "No"
    FORMAT:                          "Alphanumeric String"
    CHOICES:                         "none", "full"
    DEFAULT:                         "none"
    HELP:                            "Label features with numbers (only the first and last are labeled)"
	--------------------------------------------------------------------------------
    FLAG:                            "--format"
    REQUIRED:                        "No"
    FORMAT:                          "Alphanumeric String"
    CHOICES:                         "pdf", "png", "svg"
    DEFAULT:                         "pdf"
    HELP:                            "Output file format"
	--------------------------------------------------------------------------------
    FLAG:                            "--dpi"
    REQUIRED:                        "No"
    FORMAT:                          "Integer"
    DEFAULT:                         "300"
    HELP:                            "Resolution (dpi) for output file (for png)"
	--------------------------------------------------------------------------------
	FLAG:                            "--dynamic_resize"
    REQUIRED:                        "No"
    ACTION:                          "store_true"
    CHOICES:                         "Omitting the flag:  == "False""
                                     "Providing the flag: == "True""
    DEFAULT:                         "False"
    HELP:                            "Dynamically adjust figure size to match drawn content (eliminates extra whitespace)"
	--------------------------------------------------------------------------------
    FLAG:                            "--figsize"
    REQUIRED:                        "No"
    Number_OF_ARGUMENTS:             "2"
    FORMAT:                          "Float"
    DEFAULT:                         "10, 8"
    HELP:                            "Figure size in inches (width height)"
	--------------------------------------------------------------------------------
	FLAG:                            "--transcript_fontsize"
	REQUIRED:                        "No"
	FORMAT:                          "Integer"
	DEFAULT:                         "18"
	HELP:                            "Font size for the transcript label (default: 18)"
	--------------------------------------------------------------------------------
    FLAG:                            "-o", "--output"
    REQUIRED:                        "No"
    FORMAT:                          "Alphanumeric"
    DEFAULT:                         "Transcripts_Plots_dir_Run01"
    HELP:                            "Output directory name. If provided and exists, a numeric suffix is added (e.g., Test01)"
	--------------------------------------------------------------------------------
    FLAG:                            "-v", "--version"
    REQUIRED:                        "No"
    ACTION:                          "version"
    FORMAT:                          "Alphanumeric"
    HELP:                            "Show program version's number and exit"
	--------------------------------------------------------------------------------

## Dependencies:

	--------------------------------------------------------------------------------
    matplotlib:                      Required (see: https://matplotlib.org/)
	--------------------------------------------------------------------------------

## Development/Testing Environment:

	--------------------------------------------------------------------------------
    Distributor ID:                  Apple, Inc.
    Description:                     Apple M1 Max
    Release:                         15.3.1
    Codename:                        Sequoia
	--------------------------------------------------------------------------------

## Repository:

	--------------------------------------------------------------------------------
    https://github.com/raramayo/Transcripts_Plots_Python
	--------------------------------------------------------------------------------

## Issues:

	--------------------------------------------------------------------------------
    https://github.com/raramayo/Transcripts_Plots_Python/issues
	--------------------------------------------------------------------------------
