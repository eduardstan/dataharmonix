from setuptools import setup, find_packages

setup(
    name='dataharmonix',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'dataharmonix': ['operators/schema.json'],
    },
    # Add other parameters as needed
)
