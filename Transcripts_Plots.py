#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
Transcripts_Plots Script
--------------------------------------------------------------------------------
Author:                            Rodolfo Aramayo
Work_Email:                        raramayo@tamu.edu
Personal_Email:                    rodolfo@aramayo.org
--------------------------------------------------------------------------------
Overview:
The Transcripts_Plots script is designed to generate publication‑quality gene
model plots from transcript annotation data found in GTF files. It extracts and
plots the exon structure and/or coding sequence (CDS) of a given transcript,
supporting both single‐transcript and multi‐transcript modes. The script also
accommodates different display modes—either plotting the introns to their full
scale or compressing them for easier viewing.
--------------------------------------------------------------------------------
Copyright:
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.
--------------------------------------------------------------------------------
Version Number:
Version: 1.0.2
--------------------------------------------------------------------------------
"""
#-------------------------------------------------------------------------------
import os
import sys
#-------------------------------------------------------------------------------
# Dependency checking
required_modules = {
    "pip": "python3 -m pip install -U pip",
    "matplotlib": "python3 -m pip install -U matplotlib",
    # If you had other non-standard dependencies, add them here.
}

for module, install_cmd in required_modules.items():
    try:
        __import__(module)
    except ImportError:
        sys.exit(f"Error: The '{module}' module is not installed.\nPlease install it using:\n    {install_cmd}\n")
#-------------------------------------------------------------------------------
# Import dependencies
import argparse
import matplotlib.pyplot as plt
from textwrap import dedent
from packaging import version
#-------------------------------------------------------------------------------
# Defining Script Name
script_name = os.path.basename(sys.argv[0])

# Defining Script Current Version
script_version = "1.0.2"

# Defining_Script_Current_Version (date '+DATE:%Y/%m/%d%tTIME:%R')
current_version_date = "DATE:2025/03/03"
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Helper Functions
#-------------------------------------------------------------------------------

def parse_attributes(attr_str):
    """Parse the attributes field from a GTF entry into a dictionary."""
    attrs = {}
    for attr in attr_str.strip().split(";"):
        if attr.strip():
            key_value = attr.strip().split(" ", 1)
            if len(key_value) == 2:
                key = key_value[0]
                value = key_value[1].replace('"','').strip()
                attrs[key] = value
    return attrs

def parse_gtf(gtf_file, transcript_id):
    """
    Parse the provided GTF file and return a list of entries (as dicts)
    that match the given transcript_id (ignoring version suffix).
    Only entries with exactly 9 columns are processed.
    """
    entries = []
    with open(gtf_file, 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.strip().split("\t")
            if len(parts) != 9:
                sys.exit(f"Error: The GTF file {gtf_file} does not have 9 tab-delimited fields.")
            attr_dict = parse_attributes(parts[8])
            tid = attr_dict.get('transcript_id', '').split('.')[0]
            if tid != transcript_id:
                continue
            entry = {
                'feature': parts[2],
                'start': int(parts[3]),
                'end': int(parts[4]),
                'strand': parts[6],
                'attributes': attr_dict
            }
            entries.append(entry)
    return entries

def process_features(entries):
    """
    Filter entries to only include exons and CDS.
    Sort them by ascending genomic coordinate, then if the strand is '-',
    reverse them so that the 5' end (highest coordinate) is first in the list.
    """
    exons = [e for e in entries if e['feature'] == 'exon']
    cds   = [e for e in entries if e['feature'] == 'CDS']

    # Always sort by ascending genomic coordinate:
    exons.sort(key=lambda x: x['start'])
    cds.sort(key=lambda x: x['start'])

    # Determine the strand (check exons first, else cds)
    strand = None
    if exons:
        strand = exons[0]['strand']
    elif cds:
        strand = cds[0]['strand']
    else:
        strand = '+'  # default if no features found

    # If minus strand, reverse the lists so that the 5' feature is exons[0] or cds[0]
    if strand == '-':
        exons.reverse()
        cds.reverse()

    return exons, cds

def compute_lengths(features):
    """Compute the length of each feature and attach it."""
    for f in features:
        f['length'] = f['end'] - f['start']
    return features

def scale_coordinates(features, full_scale, fixed_intron=20):
    """
    Scale genomic coordinates for plotting.
    If full_scale is True, use real coordinates (shifted so the first feature starts at 0).
    Otherwise, compress introns to a fixed gap.
    """
    scaled = []
    current_pos = 0
    prev_end = None
    for f in features:
        if full_scale:
            scaled_start = f['start'] - features[0]['start']
            scaled_end   = f['end'] - features[0]['start']
        else:
            if prev_end is None:
                scaled_start = 0
            else:
                scaled_start = current_pos + fixed_intron
            width = f['end'] - f['start']
            scaled_end = scaled_start + width
            current_pos = scaled_end
        new_feat = f.copy()
        new_feat['scaled_start'] = scaled_start
        new_feat['scaled_end'] = scaled_end
        scaled.append(new_feat)
        prev_end = f['end']
    return scaled

def create_output_dir(base_name=None):
    """
    Create a new output directory.
    If a base_name is provided and exists, a numeric suffix is appended (e.g., Test01).
    Otherwise, a default name is used.
    """
    if base_name:
        out_dir = base_name
        suffix = 0
        while os.path.exists(out_dir):
            suffix += 1
            out_dir = f"{base_name}_{suffix:02d}"
    else:
        suffix = 1
        out_dir = f"Transcripts_Plots_dir_Run{suffix:02d}"
        while os.path.exists(out_dir):
            suffix += 1
            out_dir = f"Transcripts_Plots_dir_Run{suffix:02d}"
    os.makedirs(out_dir, exist_ok=True)
    return out_dir

#-------------------------------------------------------------------------------
# Plotting Function
#-------------------------------------------------------------------------------

def plot_transcript(features, args, transcript_id, gene_name, plot_feature="exons"):
    """
    Plot the transcript structure for the given features (either exons or CDS),
    always left-to-right from 5' to 3'. At the end, if dynamic_resize is enabled,
    the figure width is adjusted based on the data range so that extra whitespace is minimized.
    """
    # 1) Determine strand and scale coordinates
    #    Because we reversed minus-strand features in process_features,
    #    features[0] is always the 5' end.
    strand = features[0]['strand'] if features else '+'
    scaled_features = []
    if args.full_scale:
        # FULL-SCALE MODE:
        # We want to place features[0] at x=0, then map everything accordingly.
        first_start = features[0]['start']
        for f in features:
            # For plus strand, do: scaled_start = f['start'] - first_start
            # For minus strand, do: scaled_start = first_start - f['end']
            # but we can unify it if we rely on the fact that the list is in 5'→3' order.
            if strand == '+':
                s_start = f['start'] - first_start
                s_end   = f['end']   - first_start
            else:
                # minus-strand features are reversed, so features[0] is the highest coordinate
                s_start = first_start - f['end']
                s_end   = first_start - f['start']
            new_f = f.copy()
            new_f['scaled_start'] = s_start
            new_f['scaled_end']   = s_end
            scaled_features.append(new_f)
    else:
        # INTRON-COMPRESSED MODE:
        # We'll do a simple linear chaining from left to right.
        current_pos = 0
        for i, f in enumerate(features):
            new_f = f.copy()
            width = f['end'] - f['start']
            if i == 0:
                s_start = 0
                s_end   = width
                current_pos = s_end
            else:
                s_start = current_pos + 20  # 20 is the fixed intron gap.
                s_end   = s_start + width
                current_pos = s_end
            new_f['scaled_start'] = s_start
            new_f['scaled_end']   = s_end
            scaled_features.append(new_f)

    # 2) Compute transcript size and prepare transcript label text.
    transcript_size = (max(f['end'] for f in features) - min(f['start'] for f in features)) / 1000.0
    num_features = len(features)
    if plot_feature.lower() == "exons":
        info_text = f"{gene_name} ({transcript_id} [{transcript_size:.1f} kbp - {num_features}-exons])"
    else:
        info_text = f"{gene_name} ({transcript_id} [{transcript_size:.1f} kbp - {num_features}-CDS])"

    # 3) Set uniform rectangle parameters (for both exons and CDS)
    rect_y = 0.5
    #### rect_y = 0.75
    rect_height = 0.3
    #### rect_height = 0.5

    # 4) Create figure and axis using the provided figsize
    fig, ax = plt.subplots(figsize=args.figsize)
    #### plt.subplots_adjust(left=0.08, right=0.98, top=0.90, bottom=0.12)
    plt.subplots_adjust(left=0.08, right=0.98, top=0.60, bottom=0.12)

    # 5) Conditionally place the transcript label (if not suppressed)
    if args.print_transcript_label:
        first_feat = scaled_features[0]
        trans_label_x = first_feat['scaled_start']
        #### trans_label_y = rect_y + rect_height + 0.15
        trans_label_y = rect_y + rect_height + 0.40
        #### ax.text(trans_label_x, trans_label_y, info_text, ha="left", va="bottom", fontsize=10, weight="bold")
        #### ax.text(trans_label_x, trans_label_y, info_text, ha="left", va="bottom", fontsize=18, weight="bold")
        #### ax.text(trans_label_x, trans_label_y, info_text, ha="left", va="bottom", fontsize=args.transcript_fontsize, weight="bold")
        #### ax.text(trans_label_x, trans_label_y, info_text, ha="left", va="bottom", fontsize=args.transcript_fontsize if hasattr(args, 'transcript_fontsize') else 18, weight="bold")
        ax.text(trans_label_x, trans_label_y, info_text, ha="left", va="bottom", fontsize=args.transcript_fontsize, weight="bold")

    # 6) Choose color based on feature type.
    color = args.exon_color if plot_feature.lower() == "exons" else args.CDS_color

    # 7) Draw each feature as a rectangle and label only first and last features if requested.
    for i, feat in enumerate(scaled_features):
        x = feat['scaled_start']
        width = feat['scaled_end'] - feat['scaled_start']
        ax.add_patch(plt.Rectangle((x, rect_y), width, rect_height, color=color, ec='black'))
        # Label only the first and last feature if --labels is set to "full".
        if args.labels == "full" and (i == 0 or i == len(scaled_features) - 1):
            if plot_feature.lower() == "exons":
                label = "E01" if i == 0 else f"E{num_features:02d}"
            else:
                label = "CE01" if i == 0 else f"CE{num_features:02d}"
            #### ax.text(x + width/2, rect_y + rect_height + 0.05, label, ha='center', va='bottom', fontsize=8, color="black")
            ax.text(x + width/2, rect_y + rect_height + 0.05, label, ha='center', va='bottom', fontsize=10, color="black")

    # 8) Draw dashed lines (intron lines) between consecutive features.
    for i in range(1, len(scaled_features)):
        x0 = scaled_features[i-1]['scaled_end']
        x1 = scaled_features[i]['scaled_start']
        y_line = rect_y + rect_height/2
        # You can make the dashes smaller by using a custom dash pattern:
        # linestyle=(0, (1, 1)) or something similar.
        #### ax.plot([x0, x1], [y_line, y_line], linestyle='dashed', color='gray')
        # Custom dash pattern: (offset, (dash_length, gap_length))
        # Custom dash pattern for shorter dashes.
        ax.plot([x0, x1], [y_line, y_line], linestyle=(0, (1, 1)), color='gray')

    # 9) Set x-axis limits based on the data range (with a small padding).
    x_min = min(f['scaled_start'] for f in scaled_features)
    x_max = max(f['scaled_end'] for f in scaled_features)
    ax.set_xlim(x_min - 10, x_max + 10)
    ax.set_ylim(0, 2)

    # 10) Dynamic resizing: adjust the figure width based on the x-range of the drawn content.
    if args.dynamic_resize:
        # Calculate the data width (we already have x_min and x_max)
        data_width = (x_max - x_min) + 20  # Add padding equivalent to the axis limits.
        # Define a conversion factor: in full_scale mode we assume 1000 data units per inch;
        # in compressed mode we assume a 1:1 ratio.
        conversion = 1000.0 if args.full_scale else 1.0
        new_width_inches = data_width / conversion
        # Ensure the new width is at least the original width and cap it to a maximum (e.g., 20 inches)
        new_width_inches = max(new_width_inches, args.figsize[0])
        new_width_inches = min(new_width_inches, 20)
        fig.set_size_inches(new_width_inches, args.figsize[1])

    ax.axis('off')
    return fig

#-------------------------------------------------------------------------------
# Main Function
#-------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
      description="Generate transcript plots from GTF files.",
    formatter_class=argparse.RawTextHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
      "-t",
      "--transcript",
      type=str,
      help="Transcript ID"
    )
    parser.add_argument(
      "-g",
      "--gtf",
      type=str,
      help="GTF file (required with -t)"
    )
    group.add_argument(
      "-f",
      "--file",
      type=str,
      help="File with multiple transcripts and GTF paths (2 tab-delimited columns)"
    )
    parser.add_argument(
      "-s",
      "--select",
      type=str,
      choices=["exons", "CDS", "both"],
      default="exons",
      help="Select feature to be plotted: exons, CDS, or both"
    )
    parser.add_argument(
      "--exon_color",
      type=str,
      default="#305c96",
      help="Color for Exons"
    )
    parser.add_argument(
      "--CDS_color",
      type=str,
      default="#b38d1b",
      help="Color for CDS"
    )
    parser.add_argument(
      "--full_scale",
      action="store_true",
      default=False,
      help="Plot entire region to scale; otherwise introns are compressed uniformly"
    )
    parser.add_argument(
      "--no_transcript_label",
      dest="print_transcript_label",
      action="store_false",
      default=True,
      help="Do not print the transcript label above the plot"
    )
    parser.add_argument(
      "--labels",
      type=str,
      choices=["none", "full"],
      default="none",
      help="Label features with numbers (only the first and last are labeled)"
    )
    parser.add_argument(
      "--format",
      type=str,
      choices=["pdf","png", "svg"],
      default="pdf",
      help="Output file format"
    )
    parser.add_argument(
      "--dpi",
      type=int,
      default=300,
      help="Resolution (dpi) for output file (for png)"
    )
    parser.add_argument(
      "--dynamic_resize",
      action="store_true",
      default=False,
      help="Dynamically adjust figure size to match drawn content (eliminates extra whitespace)"
    )
    parser.add_argument(
      "--figsize",
      nargs=2,
      type=float,
      default=[10, 8],
      help="Figure size in inches (width height)"
    )
    parser.add_argument(
      "--transcript_fontsize",
      type=int,
      default=18,
      help="Font size for the transcript label (default: 18)"
    )
    parser.add_argument(
      "-o",
      "--output",
      type=str,
      help="Output directory name. If provided and exists, a numeric suffix is added (e.g., Test01)."
    )
    parser.add_argument(
      "-v",
      "--version",
      action="version",
      version=f"Transcripts_Plots.py Version: {script_version}",
      help="Show program version and exit"
    )
    args = parser.parse_args()

    if args.dpi > 2000:
      print("Warning: High DPI values may result in extremely large images.")

    # For multi-transcript mode, verify that the file exists before creating any output directory.
    if args.file and not os.path.exists(args.file):
        sys.exit(f"Error: The file '{args.file}' does not exist.")

    # Determine intron display status for file naming:
    introns_status = "Full_Introns" if args.full_scale else "Short_Introns"

    # Single transcript mode:
    if args.transcript:
        if not args.gtf:
            parser.error("The --gtf flag is required when using --transcript.")
        transcript_id = args.transcript.split('.')[0]
        entries = parse_gtf(args.gtf, transcript_id)
        if not entries:
            sys.exit(f"Transcript {transcript_id} not found in {args.gtf}.")
        gene_name = entries[0]['attributes'].get('gene_name', transcript_id)
        exons, cds = process_features(entries)
        exons = compute_lengths(exons)
        if cds:
            cds = compute_lengths(cds)

        # Create output directory only after verifying the transcript exists.
        out_dir = create_output_dir(args.output) if args.output else create_output_dir()

        if args.select in ("exons", "both"):
            fig = plot_transcript(exons, args, transcript_id, gene_name, plot_feature="exons")
            out_path = os.path.join(out_dir, f"{transcript_id}_exons_{introns_status}.{args.format}")
            #### fig.savefig(out_path, format=args.format, dpi=args.dpi, bbox_inches='tight')
            #### fig.savefig(out_path, format=args.format, dpi=args.dpi, bbox_inches='tight', pad_inches=0.1)
            fig.savefig(out_path, format=args.format, dpi=args.dpi, bbox_inches='tight', pad_inches=0.05)
            plt.close(fig)
        if args.select in ("CDS", "both") and cds:
            fig = plot_transcript(cds, args, transcript_id, gene_name, plot_feature="CDS")
            out_path = os.path.join(out_dir, f"{transcript_id}_CDS_{introns_status}.{args.format}")
            #### fig.savefig(out_path, format=args.format, dpi=args.dpi, bbox_inches='tight')
            #### fig.savefig(out_path, format=args.format, dpi=args.dpi, bbox_inches='tight', pad_inches=0.1)
            fig.savefig(out_path, format=args.format, dpi=args.dpi, bbox_inches='tight', pad_inches=0.05)
            plt.close(fig)

    # Multiple transcripts mode:
    elif args.file:
        out_dir = create_output_dir(args.output) if args.output else create_output_dir()
        output_files_created = 0

        with open(args.file) as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) != 2:
                    print(f"Skipping invalid line: {line.strip()}")
                    continue
                transcript_id, gtf_file = parts
                transcript_id = transcript_id.split('.')[0]
                if not os.path.exists(gtf_file) or os.path.getsize(gtf_file) == 0:
                    print(f"GTF file {gtf_file} for transcript {transcript_id} does not exist or is empty. Skipping.")
                    continue
                entries = parse_gtf(gtf_file, transcript_id)
                if not entries:
                    print(f"Transcript {transcript_id} not found in {gtf_file}. Skipping.")
                    continue
                gene_name = entries[0]['attributes'].get('gene_name', transcript_id)
                exons, cds = process_features(entries)
                exons = compute_lengths(exons)
                if cds:
                    cds = compute_lengths(cds)

                if args.select in ("exons", "both"):
                    fig = plot_transcript(exons, args, transcript_id, gene_name, plot_feature="exons")
                    out_path = os.path.join(out_dir, f"{transcript_id}_exons_{introns_status}.{args.format}")
                    #### fig.savefig(out_path, format=args.format, dpi=args.dpi, bbox_inches='tight')
                    #### fig.savefig(out_path, format=args.format, dpi=args.dpi, bbox_inches='tight', pad_inches=0.1)
                    fig.savefig(out_path, format=args.format, dpi=args.dpi, bbox_inches='tight', pad_inches=0.05)
                    plt.close(fig)
                    output_files_created += 1
                if args.select in ("CDS", "both") and cds:
                    fig = plot_transcript(cds, args, transcript_id, gene_name, plot_feature="CDS")
                    out_path = os.path.join(out_dir, f"{transcript_id}_CDS_{introns_status}.{args.format}")
                    #### fig.savefig(out_path, format=args.format, dpi=args.dpi, bbox_inches='tight')
                    #### fig.savefig(out_path, format=args.format, dpi=args.dpi, bbox_inches='tight', pad_inches=0.1)
                    fig.savefig(out_path, format=args.format, dpi=args.dpi, bbox_inches='tight', pad_inches=0.05)
                    plt.close(fig)
                    output_files_created += 1

        # If no valid transcript was processed, remove the output directory.
        if output_files_created == 0:
            import shutil
            shutil.rmtree(out_dir)

if __name__ == "__main__":
    main()
