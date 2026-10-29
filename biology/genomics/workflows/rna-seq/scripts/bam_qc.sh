#!/usr/bin/env bash
set -euo pipefail

BAM_DIR=${1:-results/03_star/bam}
OUT_DIR=${2:-results/05_bam_qc}
THREADS=${THREADS:-4}

mkdir -p "${OUT_DIR}/samtools"

for bam in "${BAM_DIR}"/*.bam; do
  sample=$(basename "${bam}" .bam)
  samtools view -H "${bam}" > "${OUT_DIR}/samtools/${sample}.header.sam"
  samtools flagstat -@ "${THREADS}" "${bam}" > "${OUT_DIR}/samtools/${sample}.flagstat.txt"
  samtools stats -@ "${THREADS}" "${bam}" > "${OUT_DIR}/samtools/${sample}.stats.txt"
  samtools idxstats "${bam}" > "${OUT_DIR}/samtools/${sample}.idxstats.txt"
done

multiqc "${OUT_DIR}/samtools" --outdir "${OUT_DIR}/multiqc"

