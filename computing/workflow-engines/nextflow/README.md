# Nextflow

Nextflow is a workflow engine for reproducible and portable data pipelines. It is common in bioinformatics because it combines workflow syntax, software environment integration, and execution on local, HPC, or cloud systems.

## Introduction

> nextflow documentation

## Installation

- more information can be found [nextflow documentation - installation](https://www.nextflow.io/docs/latest/install.html)

## Basic script

```groovy
// Default parameter input
params.str = "Hello world!"

// split process
process split {
    publishDir "results/lower"

    input:
    val x

    output:
    path 'chunk_*'

    script:
    """
    printf '${x}' | split -b 6 - chunk_
    """
}

// convert_to_upper process
process convert_to_upper {
    publishDir "results/upper"
    tag "$y"

    input:
    path y

    output:
    path 'upper_*'

    script:
    """
    cat $y | tr '[a-z]' '[A-Z]' > upper_${y}
    """
}

// Workflow block
workflow {
    ch_str = channel.of(params.str)       // Create a channel using parameter input
    ch_chunks = split(ch_str)             // Split string into chunks and create a named channel
    convert_to_upper(ch_chunks.flatten()) // Convert lowercase letters to uppercase letters
}
```

run

```bash
nextflow run main.nf
```

## What to Learn Next

- `running-pipelines/command-line-interface.md`
- `running-pipelines/configuration.md`
- DSL2 concepts such as channels, processes, modules, and workflows
