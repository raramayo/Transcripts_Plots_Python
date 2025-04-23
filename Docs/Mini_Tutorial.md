[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14926215.svg)](https://doi.org/10.5281/zenodo.14926215)

# Transcripts_Plots Mini Tutorial

## Key Capabilities:

+ ### Input Flexibility:

  + Single Transcript:

	+ Use the `--transcript` flag together with a GTF file (`--gtf`) to plot one transcript.

   + Multiple Transcripts:

	 + Use the `--file` flag to supply a tab-delimited file where each line lists a transcript ID and its corresponding GTF file path.

+ ### Feature Selection:

  + `Exons` Only: Plot the exon structures.

  + `CDS` Only: Plot only the coding sequences.

  + `Both`: Generate separate output files for exons and CDS.

+ ### Strand-Specific Plotting:

  + The script automatically rearranges features so that transcripts from both the plus (Watson) and
    minus (Crick) strands are always plotted from `5` to `3` (left to right). This ensures that the
    first feature (i.e., `Exon01` (`E01`) or `Coding Exon01` (`CE01`), always represents the `5′
    end` regardless of genomic orientation.

+ ### Intron Scaling Options:

  + Full Scale (`--full_scale`): Plots introns at their true genomic length.

  + Compressed Introns (default): Introns are replaced with a fixed small gap to produce a more compact view.

	+ The output filenames automatically reflect the intron display mode (e.g., `_Short_Introns` vs.` _Full_Introns`).

+ ### Customizable Appearance:

  + Change the colors of exons (`--exon_color`) and CDS (`--CDS_color`).

  + Adjust the figure size using the `--figsize` flag.

  + Set the output file format (`pdf`, `png`, or `svg`) and resolution (`--dpi`).

+ ### Labeling Options:

  + Print Transcript Label (Default Behavior):

	+ Transcript labels (including gene name, transcript ID, transcript size, and number of features) are automatically placed above the gene model.

  + Disable Transcript Label:

	+ You can disable the transcript label by using the `--no_transcript_label` flag.

   + You can choose not to label features `(--labels none)` or label the first and last feature only `(--labels full)`.

+ ### Output Naming:

  + The produced file names incorporate whether introns are displayed in full scale or compressed, for example:

	```
	ENST00000380152_exons_Short_Introns.pdf
	ENST00000380152_CDS_Full_Introns.pdf
	```

+ ### Version Information:

  + A version flag (`-v`/`--version`) is available to print the script version and exit.

+ ### Dependency Checking:

  + At startup, the script checks for required modules (like `matplotlib`) and provides instructions to install any that are missing.

## How to Use the Script:

### Single Transcript Mode:

+ Run the script by providing a transcript ID and a GTF file:

	```
	python3 Transcripts_Plots.py \
	--format png \
	--transcript ENST00000380152 \
	--gtf Ensembl_Gene_ENSG00000139618.gtf \
	--select exons
	```

	This command will produce s directory called:

	```
	Transcripts_Plots_dir_Run01
	```

	containing an `exons` plot (with compressed introns by default) in a file called:

	```
	ENST00000380152_exons_Short_Introns.pdf
	```

	The plot produced corresponds to the `BRCA2` transcript `ENST00000380152`.
	This transcript is 84.8 kbp long and is composed of 27-exons, with the following structure:

	<p align="center">
	<img src="https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Images/Transcripts_Plots_dir_Run01/ENST00000380152_exons_Short_Introns.png" width="800" height="800" style="display: block; margin: 0 auto">
	<p align="center">
	BRCA2 (ENST00000380152 [84.8 kbp - 27-exons])

+ To generate a `CDS` plot at full scale:

	```
	python3 Transcripts_Plots.py \
	--format png \
	--transcript ENST00000380152 \
	--gtf Ensembl_Gene_ENSG00000139618.gtf \
	--select CDS \
	--full_scale
	```

    This command will produce s directory called:

	```
	Transcripts_Plots_dir_Run02
	```

	containing a `CDS` plot, with `full_scale` introns, in a file called:

	```
	ENST00000380152_CDS_Full_Introns.pdf
	```

    The plot produced corresponds to the `BRCA2` transcript `ENST00000380152`.
    This transcript is 82.3 kbp long and is composed of 26-coding-exons, with the following structure:

	<p align="center">
	<img src="https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Images/Transcripts_Plots_dir_Run02/ENST00000380152_CDS_Full_Introns.png" width="800" height="800" style="display: block; margin: 0 auto">
	<p align="center">
	BRCA2 (ENST00000380152 [82.3 kbp - 26-CDS])

+ To generate a `CDS` plot at full scale with a larger transcript font size:

	```
	python3 Transcripts_Plots.py \
	--format png \
	--transcript ENST00000380152 \
	--gtf Ensembl_Gene_ENSG00000139618.gtf \
	--select CDS \
	--full_scale \
	--transcript_fontsize 24
	```

    This command will produce s directory called:

	```
	Transcripts_Plots_dir_Run03
	```

	containing a `CDS` plot, with `full_scale` introns, in a file called:

	```
	ENST00000380152_CDS_Full_Introns.pdf
	```

    The plot produced is identical to the one generated before, except for the font size of the transcript label.

	<p align="center">
	<img src="https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Images/Transcripts_Plots_dir_Run03/ENST00000380152_CDS_Full_Introns.png" width="800" height="800" style="display: block; margin: 0 auto">
	<p align="center">
	BRCA2 (ENST00000380152 [82.3 kbp - 26-CDS])

### Multiple Transcripts Mode:

+ A powerful feature of this script is its ability to plot different features from many transcripts, from different `GTF` files and with different colors at once.

    To do this, one needs to generate a tab-delimited file where each line contains a transcript ID, the corresponding GTF file, and other desired optional commands.

	For example, if we were to generate a file entitled:

	```
	Ensembl_multiple_genes_transcripts_list.txt
	```

	Containing the following list of transcripts:

	```
	ENST00000526890	Ensembl_Gene_ENSG00000110619.gtf
	ENST00000531387	Ensembl_Gene_ENSG00000110619.gtf
	ENST00000380525	Ensembl_Gene_ENSG00000110619.gtf
	ENST00000524825	Ensembl_Gene_ENSG00000110619.gtf
	ENST00000470094	Ensembl_Gene_ENSG00000139618.gtf
	ENST00000380152	Ensembl_Gene_ENSG00000139618.gtf
	ENST00000700203	Ensembl_Gene_ENSG00000139618.gtf
	```

	Note the `tab` separator between the `Transcript ID` and the `GTF` file.
	This is, for example:

	```
	ENST00000526890 <tab> Ensembl_Gene_ENSG00000110619.gtf
	```

	Also note the different `Biotypes` associated for each one of the transcripts to be plotted.

	For Gene `ENSG00000110619`, coding for `cysteinyl-tRNA synthetase 1`, the transcripts Biotypes are:

	```
	ENST00000526890 ==> Retained intron
	ENST00000531387	==> Nonsense mediated decay
	ENST00000380525	==> Protein coding
	ENST00000524825	==> Protein coding CDS not defined
	```

	For Gene `ENSG00000139618`, coding for `BRCA2 DNA repair associated`, the transcripts Biotypes are:

	```
	ENST00000470094 ==> Nonsense mediated decay
	ENST00000380152	==> Protein coding
	ENST00000700203	==> Retained intron
	```

    The command:

	```
	python3 Transcripts_Plots.py \
	--format png \
	--file Ensembl_multiple_genes_transcripts_list.txt \
	--select CDS \
	--full_scale
	```

	Will generate a directory entitled:

	```
	Transcripts_Plots_dir_Run04
	```

	Containing four plots total, two for Gene `BRCA2` and two for Gene `CARS1`.

	Because we are requesting to plot `CDS`, of the four transcript IDs present in our command list,
    the only transcripts plotted are:

	For `BRAC2`

	```
	ENST00000470094 ==> Nonsense mediated decay
	ENST00000380152	==> Protein coding
	```

	<p align="center">
	<img src="https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Images/Transcripts_Plots_dir_Run04/ENST00000380152_CDS_Full_Introns.png" width="800" height="800" style="display: block; margin: 0 auto">
	<p align="center">
	BRCA2 (ENST00000380152 [82.3 kbp - 26-CDS])

	<p align="center">
	<img src="https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Images/Transcripts_Plots_dir_Run04/ENST00000470094_CDS_Full_Introns.png" width="800" height="800" style="display: block; margin: 0 auto">
	<p align="center">
	BRCA2 (ENST00000470094 [79.6 kbp - 25-CDS])

	For `CARS1`

	```
	ENST00000531387	==> Nonsense mediated decay
	ENST00000380525	==> Protein coding
	```

	<p align="center">
	<img src="https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Images/Transcripts_Plots_dir_Run04/ENST00000380525_CDS_Full_Introns.png" width="800" height="800" style="display: block; margin: 0 auto">
	<p align="center">
	CARS1 (ENST00000380525 [56.2 kbp - 23-CDS])

	<p align="center">
	<img src="https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Images/Transcripts_Plots_dir_Run04/ENST00000531387_CDS_Full_Introns.png" width="800" height="800" style="display: block; margin: 0 auto">
	<p align="center">
	CARS1 (ENST00000531387 [16.4 kbp - 4-CDS])

### Additional Examples:

+ Adjusting the `exons` and `CDS` colors:

    The command:

    ```
	python3 Transcripts_Plots.py \
	--format png \
	--transcript ENST00000380152 \
	--gtf Ensembl_Gene_ENSG00000139618.gtf \
	--select exons \
	--full_scale
	```

	Will generate a directory entitled:

	```
	Transcripts_Plots_dir_Run05
	```

    Containing a plot for the `ENST00000380152` transcript.

	<p align="center">
	<img src="https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Images/Transcripts_Plots_dir_Run05/ENST00000380152_exons_Full_Introns.png" width="800" height="800" style="display: block; margin:0 auto">
	<p align="center">
	BRCA2 (ENST00000380152 [84.8 kbp - 27-exons])

    The color of the exons displayed is `#305c96`

    We can modify this behavior by issuing the following command:

    ```
	python3 Transcripts_Plots.py \
	--format png \
	--transcript ENST00000380152 \
	--gtf Ensembl_Gene_ENSG00000139618.gtf \
	--select exons \
	--full_scale
	--exon_color '#ed0920'
	```

	This will generate a directory entitled:

    ```
	Transcripts_Plots_dir_Run06
    ```

    Containing a plot for the `ENST00000380152` transcript where the exons are depictred using the `#ed0920` color.

    <p align="center">
    <img src="https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Images/Transcripts_Plots_dir_Run06/ENST00000380152_exons_Full_Introns.png" width="800" height="800" style="display: block;margin: 0 auto">
    <p align="center">
	BRCA2 (ENST00000380152 [84.8 kbp - 27-exons])

    Similar effects can be achieved by using the `--select CDS` flag.

+ Adjusting Figure Size:

	The command:

	```
	python3 Transcripts_Plots.py \
	--format png \
	--transcript ENST00000380152 \
	--gtf Ensembl_Gene_ENSG00000139618.gtf \
    --select exons \
	--full_scale \
	--transcript_fontsize 12 \
	--figsize 10 6
	```

	Will generate a directory entitled:

    ```
	Transcripts_Plots_dir_Run07
    ```

    Containing a plot for the `ENST00000380152` transcript where the `transcript_fintsize` and the `figsize` parameners have been modified.

    <p align="center">
    <img src="https://github.com/raramayo/Transcripts_Plots_Python/blob/main/Images/Transcripts_Plots_dir_Run07/ENST00000380152_exons_Full_Introns.png" width="800" height="800" style="display: block;margin: 0 auto">
    <p align="center">
BRCA2 (ENST00000380152 [84.8 kbp - 27-exons])


### Version:

  ```
  python3 Transcripts_Plots.py -v

  or

  python3 Transcripts_Plots.py --version
  ```

### Help:

  ```
  python3 Transcripts_Plots.py -h

  or

  python3 Transcripts_Plots.py --help
  ```

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
