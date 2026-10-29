#!/usr/bin/env bash
set -euo pipefail

FASTQ_DIR=${1:-data/raw}
OUT_DIR=${2:-results/01_fastq_qc}
THREADS=${THREADS:-4}

mkdir -p "${OUT_DIR}/fastqc" "${OUT_DIR}/multiqc" "${OUT_DIR}/checksums"

find "${FASTQ_DIR}" -name "*.fastq.gz" | sort > "${OUT_DIR}/fastq_files.txt"

while read -r fq; do
  sample=$(basename "${fq}" .fastq.gz)
  zcat "${fq}" | head -n 8 > "${OUT_DIR}/checksums/${sample}.head.txt"
  md5sum "${fq}" >> "${OUT_DIR}/checksums/md5sum.txt"
done < "${OUT_DIR}/fastq_files.txt"

fastqc --threads "${THREADS}" --outdir "${OUT_DIR}/fastqc" $(cat "${OUT_DIR}/fastq_files.txt")
multiqc "${OUT_DIR}/fastqc" --outdir "${OUT_DIR}/multiqc"

