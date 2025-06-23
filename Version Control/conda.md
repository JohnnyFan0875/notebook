# Conda

## Install miniconda

- [Tutorial](https://www.anaconda.com/docs/getting-started/miniconda/install)

- Close logging auto-enter (base) (Optional)

    ```bash
    conda config --set auto_activate_base false 
    ```

## Basic instruction

```bash
# View Existing Environments
conda env list

# Create a New Environment
conda create --name {env_name} python={version}

# Activate environment
conda activate {env_name}

# Search for a package
conda search <package>

# Install a package
conda install {package}
conda install {package}={version}
conda install -c conda-forge tmux python-docx openpyxl # specific packages in conda-forge

# Install a package (using pip), better using "which pip" to reconfirm 
pip install {package}

# List installed packages
conda list

# Deactivate Current Environment
conda deactivate

# Remove an Environment
conda env remove -n {env_name}
```

## Import / Export environment

```bash
conda env export > environment.yml # export environment
conda env create -f environment.yml # import environment
```