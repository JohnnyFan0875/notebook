#!/usr/bin/env bash
set -euo pipefail

GENOME_FASTA=${1:?Usage: star_alignment.sh genome.fa annotation.gtf fastq_dir out_dir}
GTF=${2:?Usage: star_alignment.sh genome.fa annotation.gtf fastq_dir out_dir}
FASTQ_DIR=${3:?Usage: star_alignment.sh genome.fa annotation.gtf fastq_dir out_dir}
OUT_DIR=${4:-results/03_star}
THREADS=${THREADS:-8}
READ_LENGTH=${READ_LENGTH:-101}
SJDB_OVERHANG=$((READ_LENGTH - 1))

mkdir -p "${OUT_DIR}/index" "${OUT_DIR}/bam" "${OUT_DIR}/logs"

STAR --runThreadN "${THREADS}" \
  --runMode genomeGenerate \
  --genomeDir "${OUT_DIR}/index" \
  --genomeFastaFiles "${GENOME_FASTA}" \
  --sjdbGTFfile "${GTF}" \
  --sjdbOverhang "${SJDB_OVERHANG}"

for r1 in "${FASTQ_DIR}"/*_R1*.fastq.gz; do
  sample=$(basename "${r1}" | sed -E 's/_R1.*\.fastq\.gz//')
  r2=$(echo "${r1}" | sed -E 's/_R1/_R2/')
  STAR --runThreadN "${THREADS}" \
    --genomeDir "${OUT_DIR}/index" \
    --readFilesIn "${r1}" "${r2}" \
    --readFilesCommand zcat \
    --outFileNamePrefix "${OUT_DIR}/bam/${sample}." \
    --outSAMtype BAM SortedByCoordinate \
    --quantMode GeneCounts \
    --twopassMode Basic
  mv "${OUT_DIR}/bam/${sample}.Log.final.out" "${OUT_DIR}/logs/${sample}.Log.final.out"
  samtools index "${OUT_DIR}/bam/${sample}.Aligned.sortedByCoord.out.bam"
done

