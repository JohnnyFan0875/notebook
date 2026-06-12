# Pipeline Execution

## Pipeline Parameters

e.g.
nextflow run main.nf --project-name projectName
nextflow run main.nf --verbose # params.verbose = true
nextflow run main.nf --files "\*.fasta" # wildcard

## Nextflow Options

e.g. -resume

## Parameter Files

for complex parameters sets

```text
{
  "input": "data.csv",
  "output": "results/",
  "min_quality": 20
}
```

```bash
nextflow run main.nf -params-file params.json
```

## Parameter Precedence

1. Script parameters (params.foo = 'default')
2. Configuration parameters
3. Parameter files (-params-file)
4. Command line parameters (--foo bar)

## Launch Project (`run`)

nextflow run main.nf

nextflow run nextflow-io/hello (from git repositories)
nextflow run https://github.com/nextflow-io/hello

- more information please refer to [Command line interface - Pipeline execution]

# Project Management

nextflow pull nf-core/rnaseq
nextflow list
nextflow info nf-core/rnaseq
nextflow drop nf-core/rnaseq

nextflow view nf-core/rnaseq (main script)
nextflow view nf-core/rnaseq -l (list files)

nextflow clone nf-core/rnaseq test_rnaseq (cache - local repository)

nf-core modules install multiqc

# Configuration and Validation

nextflow.config

```
params.input = 'data/'
executor = 'local'
```

config.conf

```
executor = 'slurm'
```

nextflow -c config.conf main.nf (executor = 'slurm', params.input = 'data/')
nextflow -C config.conf main.nf (only use config.conf)

nextflow config
nextflow config main.nf

nextflow inspect main.nf (analyze process)
nextflow inspect main.nf -format json

> comparison with -dry-run
