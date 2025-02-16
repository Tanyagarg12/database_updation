
from setuptools import setup, find_packages

setup(
    name="update_Package",  # Package name
    version="1.0.0",  # Version number
    author="Manoj Aggrawa;",
    author_email="your.email@example.com",
    description="A package for database updates and file processing",
    packages=find_packages(),  # Automatically finds all modules inside the package
    install_requires=[  # Dependencies (see requirements.txt)
        "pandas",
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "run-update=update_Package.run_all:execute_scripts",  # CLI command
        ]
    },
    python_requires=">=3.7",  # Minimum Python version
)

