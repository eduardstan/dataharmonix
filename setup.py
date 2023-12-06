from setuptools import setup, find_packages

setup(
    name='dataharmonix',
    version='0.1.0',
    author='Eduard I. Stan',
    author_email='stan.i.eduard@gmail.com',
    description="A blend of 'data' and 'harmonics', symbolizing the harmonious integration of diverse data types and processing methods.",
    url='https://github.com/eduardstan/dataharmonix',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'dataharmonix': ['operators/schema.json'],
    },
    install_requires=[
        'jsonschema',
        'ipywidgets',
        'ipycytoscape',
    ],
)
