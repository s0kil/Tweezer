from setuptools import setup, find_packages

setup(
    name='Tweezer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'gensim',
        'nltk',
        'scikit-learn',
        'tqdm',
        'tensorflow',
        'tqdm',
        'scipy'
    ],
    entry_points={
        'console_scripts': [
            'tweezer=Tweezer.tweezer:entry',
        ],
    },
)
