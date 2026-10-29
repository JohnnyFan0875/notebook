#!/usr/bin/env bash
set -euo pipefail

FASTQ_DIR=${1:-data/raw}
OUT_DIR=${2:-results/01_fastq_qc}
THREADS=${THREADS:-4}

mkdir -p "${OUT_DIR}/fastqc" "${OUT_DIR}/multiqc" "${OUT_DIR}/checksums"

find "${FASTQ_DIR}" -name "*.fastq.gz" | sort > "${OUT_DIR}/fastq_files.txt"
mapfile -t fastqs < "${OUT_DIR}/fastq_files.txt"
: > "${OUT_DIR}/checksums/md5sum.txt"

for fq in "${fastqs[@]}"; do
  sample=$(basename "${fq}" .fastq.gz)
  # head closes the pipe early; zcat's SIGPIPE (141) is expected under pipefail
  zcat "${fq}" | head -n 8 > "${OUT_DIR}/checksums/${sample}.head.txt" || [[ $? -eq 141 ]]
  md5sum "${fq}" >> "${OUT_DIR}/checksums/md5sum.txt"
done

fastqc --threads "${THREADS}" --outdir "${OUT_DIR}/fastqc" "${fastqs[@]}"
multiqc "${OUT_DIR}/fastqc" --outdir "${OUT_DIR}/multiqc"

