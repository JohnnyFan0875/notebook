#!/usr/bin/env bash
set -euo pipefail

METADATA=${1:-data/sample_metadata.csv}
FASTQ_ROOT=${2:-.}
OUT_DIR=${3:-results/02_fastp_trim}
THREADS=${THREADS:-4}

mkdir -p "${OUT_DIR}/fastq" "${OUT_DIR}/reports"

tail -n +2 "${METADATA}" | while IFS=, read -r sample fastq1 fastq2 group rest; do
  fastp \
    --in1 "${FASTQ_ROOT}/${fastq1}" \
    --in2 "${FASTQ_ROOT}/${fastq2}" \
    --out1 "${OUT_DIR}/fastq/${sample}_R1.trimmed.fastq.gz" \
    --out2 "${OUT_DIR}/fastq/${sample}_R2.trimmed.fastq.gz" \
    --detect_adapter_for_pe \
    --cut_front --cut_tail \
    --cut_mean_quality 20 \
    --length_required 30 \
    --trim_poly_g --trim_poly_x \
    --thread "${THREADS}" \
    --html "${OUT_DIR}/reports/${sample}.fastp.html" \
    --json "${OUT_DIR}/reports/${sample}.fastp.json"
done

multiqc "${OUT_DIR}/reports" --outdir "${OUT_DIR}/multiqc"

