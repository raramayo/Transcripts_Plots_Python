# Transcripts_Plots_Pseudocode

```
BEGIN
  # 1. Dependency Checking
  FOR each required module:
      TRY to import the module
      IF ImportError occurs:
          EXIT with an error message (and suggestion to install)

  # 2. Parse Command-Line Arguments (using argparse)
  DEFINE arguments for:
      - Single transcript mode (--transcript) and corresponding GTF file (--gtf)
      - Multiple transcript mode (--file)
      - Feature selection (--select: exons, CDS, or both)
      - Display options (e.g., --full_scale, --labels, --exon_color, --CDS_color)
      - Figure output options (--figsize, --dpi, --format, etc.)
      - Optional transcript label control (--no_transcript_label or similar)
      - Version flag (-v/--version)

  # 3. Pre-checks before processing
  IF multi-transcript mode is selected:
      IF the provided transcripts file does not exist:
          EXIT with an error message
  IF no arguments are provided:
      PRINT usage information and EXIT

  # 4. Process Mode Branching
  IF single transcript mode is active:
      VERIFY that a GTF file is provided
      PARSE the GTF file for the specified transcript ID
      IF transcript not found:
          EXIT with message "Transcript [ID] not found in [GTF file]."
      ELSE:
          EXTRACT gene name, exons, and CDS information
          COMPUTE the lengths of exons and CDS
          (Optionally, adjust ordering for minus-strand transcripts to always plot 5′→3′)
          CREATE output directory (only after successful verification)

          IF feature selection includes exons:
              CALL plot_transcript() with exons data
              SAVE the figure with a filename that includes:
                  transcript ID, "exons", and "Full_Introns" or "Short_Introns"

          IF feature selection includes CDS:
              CALL plot_transcript() with CDS data
              SAVE the figure with a filename that includes:
                  transcript ID, "CDS", and "Full_Introns" or "Short_Introns"

  ELSE IF multi-transcript mode is active:
      CREATE output directory
      SET a counter for the number of files created to zero

      FOR each line in the transcripts list file:
          PARSE transcript ID and its associated GTF file path
          IF the GTF file does not exist or is empty:
              PRINT an error message and CONTINUE to next line
          PARSE the GTF file for the transcript ID
          IF transcript not found:
              PRINT an error message and CONTINUE to next line
          ELSE:
              EXTRACT gene name, exons, and CDS
              COMPUTE feature lengths

              IF feature selection includes exons:
                  CALL plot_transcript() with exons data
                  SAVE the figure with a filename as above
                  INCREMENT output counter

              IF feature selection includes CDS:
                  CALL plot_transcript() with CDS data
                  SAVE the figure with a filename as above
                  INCREMENT output counter

      IF no output files were created (counter is zero):
          REMOVE the output directory

  # 5. Exit
  END
```
