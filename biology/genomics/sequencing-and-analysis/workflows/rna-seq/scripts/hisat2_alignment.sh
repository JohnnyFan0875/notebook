#!/usr/bin/env bash
set -euo pipefail

GENOME_FASTA=${1:?Usage: hisat2_alignment.sh genome.fa annotation.gtf fastq_dir out_dir}
GTF=${2:?Usage: hisat2_alignment.sh genome.fa annotation.gtf fastq_dir out_dir}
FASTQ_DIR=${3:?Usage: hisat2_alignment.sh genome.fa annotation.gtf fastq_dir out_dir}
OUT_DIR=${4:-results/03_hisat2}
THREADS=${THREADS:-8}

mkdir -p "${OUT_DIR}/index" "${OUT_DIR}/bam" "${OUT_DIR}/logs"

hisat2_extract_splice_sites.py "${GTF}" > "${OUT_DIR}/index/splice_sites.txt"
hisat2_extract_exons.py "${GTF}" > "${OUT_DIR}/index/exons.txt"
hisat2-build -p "${THREADS}" \
  --ss "${OUT_DIR}/index/splice_sites.txt" \
  --exon "${OUT_DIR}/index/exons.txt" \
  "${GENOME_FASTA}" "${OUT_DIR}/index/genome"

for r1 in "${FASTQ_DIR}"/*_R1*.fastq.gz; do
  sample=$(basename "${r1}" | sed -E 's/_R1.*\.fastq\.gz//')
  r2=$(echo "${r1}" | sed -E 's/_R1/_R2/')
  hisat2 -p "${THREADS}" --dta \
    -x "${OUT_DIR}/index/genome" \
    -1 "${r1}" -2 "${r2}" \
    2> "${OUT_DIR}/logs/${sample}.hisat2.summary.txt" |
    samtools view -@ "${THREADS}" -bS - |
    samtools sort -@ "${THREADS}" -o "${OUT_DIR}/bam/${sample}.sorted.bam" -
  samtools index "${OUT_DIR}/bam/${sample}.sorted.bam"
done

