from setuptools import find_packages, setup
# This wil create a wheel file
setup(
    name="truck_model",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "matplotlib",
        "seaborn",
    ],
    python_requires=">=2.7",
)
