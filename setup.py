from setuptools import setup

setup(
    name="JLC2KiCad Converter",
    version="1.0",
    packages=["src"],
    install_requires=[
        "PyQt6",
        "jlc2kicadlib",
    ],
)
)