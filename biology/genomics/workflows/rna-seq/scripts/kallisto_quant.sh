#!/usr/bin/env bash
set -euo pipefail

TRANSCRIPTS_FA=${1:?Usage: kallisto_quant.sh transcripts.fa metadata.csv out_dir}
METADATA=${2:?Usage: kallisto_quant.sh transcripts.fa metadata.csv out_dir}
OUT_DIR=${3:-results/04_kallisto}
THREADS=${THREADS:-8}
BOOTSTRAP=${BOOTSTRAP:-100}

mkdir -p "${OUT_DIR}/index" "${OUT_DIR}/quant"

kallisto index -i "${OUT_DIR}/index/transcripts.idx" "${TRANSCRIPTS_FA}"

tail -n +2 "${METADATA}" | while IFS=, read -r sample fastq1 fastq2 group rest; do
  kallisto quant \
    -i "${OUT_DIR}/index/transcripts.idx" \
    -b "${BOOTSTRAP}" \
    -t "${THREADS}" \
    -o "${OUT_DIR}/quant/${sample}" \
    "${fastq1}" "${fastq2}"
done

