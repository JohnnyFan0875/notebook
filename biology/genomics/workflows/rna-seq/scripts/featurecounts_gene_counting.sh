#!/usr/bin/env bash
set -euo pipefail

GTF=${1:?Usage: featurecounts_gene_counting.sh annotation.gtf bam_dir out_dir}
BAM_DIR=${2:?Usage: featurecounts_gene_counting.sh annotation.gtf bam_dir out_dir}
OUT_DIR=${3:-results/06_featurecounts}
THREADS=${THREADS:-8}
STRAND=${STRAND:-0}

mkdir -p "${OUT_DIR}"

featureCounts \
  -T "${THREADS}" \
  -a "${GTF}" \
  -o "${OUT_DIR}/gene_counts.txt" \
  -t exon \
  -g gene_id \
  -p --countReadPairs \
  -s "${STRAND}" \
  "${BAM_DIR}"/*.bam

