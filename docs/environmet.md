# Environment Configuration Details

## Environment Naming Convention

The Conda environment created by the project script `RUN-ME-FIRST-RUN-ME-ONCE` is named using the
prefix `syntheticDataset` followed by a suffix of
four random uppercase letters, forming a unique identifier like `syntheticDataset-ABCD`. This name is dynamically
generated to ensure each environment setup remains distinct and is stored for later reference.

### Storage of Environment Name

The complete environment name is saved in the `e-name.env` file within the project's root directory. This file is
crucial for subsequent operations that require referencing the environment.

## Python Version Synchronization

The Python version used in the created Conda environment matches the version of the Blender Python interpreter. This
consistency is vital for compatibility between the scripting environment in Blender and the Conda environment.
