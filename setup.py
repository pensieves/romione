"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from pathlib import Path
import romione
import textwrap

description = textwrap.dedent(
    """\
    Named after the duo companion of Harry Potter i.e. Ron and Hermione who were
    the first source of information and help to Harry in the Hogwarts School of 
    Witchcraft and Wizardry. The library is built to function as a knowledge graph
    and computation engine for you (Harry).
    """
)

curr_dir = Path(__file__).parent

with open(curr_dir / "requirements.txt", "r") as f:
    install_requires = [i.strip() for i in f.readlines() if i.strip()]

README = (curr_dir / "README.md").read_text()

setup(
    name="romione",
    version=romione.__version__,
    description=description,
    long_description=README,
    long_description_content_type="text/markdown",
    author="Md Imbesat Hassan Rizvi",
    author_email="imbugene@gmail.com",
    url="https://github.com/pensieves/romione",
    download_url="https://github.com/pensieves/romione/releases",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),  # Required
    package_data={"": ["**/*.yml", "**/*.txt", "**/*.conf"]},
    include_package_data=True,
    install_requires=install_requires,
    # extras_require=extras_require,
    license="MIT",
    keywords=[
        "knowledge graph",
        "computation engine",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Environment :: GPU :: NVIDIA CUDA :: 11.7",
    ],
)
