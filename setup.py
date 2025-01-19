from setuptools import setup, find_packages

setup(
    name="BasicMLOpsProject",  # The name of the package
    version="0.1",             # The version of the package
    packages=find_packages(where="src"),  # This finds all packages within the 'src' directory
    package_dir={'': 'src'},   # Specifies that all packages are located in the 'src' directory
    install_requires=[         # A list of dependencies that are required to run the package
        "pandas",              # Example dependency: pandas for data manipulation
        "numpy",               # Example dependency: numpy for numerical operations
        "scikit-learn",        # Example dependency: scikit-learn for machine learning models
    ],
)
