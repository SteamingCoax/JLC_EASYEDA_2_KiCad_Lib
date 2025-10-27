from setuptools import setup

setup(
    name="EasyEDA to KiCad Converter",
    version="1.0",
    packages=["src"],
    install_requires=[
        "PyQt6",
        "easyeda2kicad",
    ],
)