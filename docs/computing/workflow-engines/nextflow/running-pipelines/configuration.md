# Nextflow Configuration

`nextflow.config` controls execution profiles, parameters, resources, and platform-specific settings.

## Common Uses

- Define profiles such as `local`, `slurm`, or `awsbatch`
- Set default CPUs, memory, and time for processes
- Configure container, conda, or executor behavior

## Practical Notes

- Keep reusable settings in profiles.
- Use command-line profile selection to avoid editing the pipeline for each environment.
