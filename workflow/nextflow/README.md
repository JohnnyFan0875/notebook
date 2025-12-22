# Nextflow

## brief introduction

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

