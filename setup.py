from setuptools import setup, find_packages

setup(
    name='bottle-unsign',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'bottle-unsign = bottle_unsign.cookie_encoder_decoder:main',
        ],
    },
)
