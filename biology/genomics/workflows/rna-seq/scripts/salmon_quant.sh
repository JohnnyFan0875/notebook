#!/usr/bin/env bash
set -euo pipefail

TRANSCRIPTS_FA=${1:?Usage: salmon_quant.sh transcripts.fa metadata.csv out_dir}
METADATA=${2:?Usage: salmon_quant.sh transcripts.fa metadata.csv out_dir}
OUT_DIR=${3:-results/04_salmon}
THREADS=${THREADS:-8}

mkdir -p "${OUT_DIR}/index" "${OUT_DIR}/quant"

salmon index -t "${TRANSCRIPTS_FA}" -i "${OUT_DIR}/index" -k 31

tail -n +2 "${METADATA}" | while IFS=, read -r sample fastq1 fastq2 group rest; do
  salmon quant \
    -i "${OUT_DIR}/index" \
    -l A \
    -1 "${fastq1}" \
    -2 "${fastq2}" \
    --validateMappings \
    --seqBias \
    --gcBias \
    -p "${THREADS}" \
    -o "${OUT_DIR}/quant/${sample}"
done

