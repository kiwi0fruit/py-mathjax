from setuptools import setup

setup(
    name='mathjax',
    version='2.7.5',

    description='Stub for https://github.com/conda-forge/mathjax-feedstock funtionality. For MathJax see https://github.com/kiwi0fruit/pymathjax',
    url='https://github.com/kiwi0fruit/pypi-mathjax',
    author='kiwi0fruit',
    author_email='peter.zagubisalo@gmail.com',
    license='MIT',
    scripts=[
        'scripts/mathjax-path',
        'scripts/mathjax-path.bat'
    ],
)
