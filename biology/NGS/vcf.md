# VCF

## Indexing and Querying VCF Files

```bash
# Download Tabix
sudo apt-get install tabix bcftools

# Compress VCF file (vcf.gz)
bgzip vcf_file.vcf
bcftools sort vcf_file.vcf -Oz -o vcf_file.vcf.gz #optional

# Generate index (vcf.gz.tbi) file
tabix -p vcf vcf_file.vcf.gz
bcftools index -t vcf_file.vcf.gz #optional

# Query variants by genomic region (requires index)
tabix vcf_file.vcf.gz 11                       # Entire chromosome 11
tabix vcf_file.vcf.gz 11:123456                # Specific position
tabix vcf_file.vcf.gz 11:123456-123457         # Range query
```
