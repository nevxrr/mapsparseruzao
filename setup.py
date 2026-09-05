from setuptools import find_packages, setup

setup(
    name="mapsparseruzao",
    version="1.0.0",
    description="Парсер компаний ЮЗАО без сайта → .xlsx",
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.9",
    install_requires=["openpyxl>=3.1.2", "requests>=2.31.0"],
    entry_points={"console_scripts": ["mapsparseruzao=mapsparseruzao.cli:main"]},
)
