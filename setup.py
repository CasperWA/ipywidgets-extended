from pathlib import Path
from setuptools import setup, find_packages

from setupbase import (
    get_data_files,
    wrap_installers,
    npm_builder,
    get_version,
)

MODULE_DIR = Path(__file__).resolve().parent

README = (MODULE_DIR / "README.md").read_text()
BASE = [
    f"{_.strip()}"
    for _ in (MODULE_DIR / "requirements.txt").read_text().splitlines()
    if " " not in _
]
DEV = [
    f"{_.strip()}"
    for _ in (MODULE_DIR / "requirements_dev.txt").read_text().splitlines()
    if " " not in _
]

NAME = "ipywidgets_extended"

NB_PATH = MODULE_DIR / NAME / "nbextension" / "static"
LAB_PATH = MODULE_DIR / NAME / "labextension"

# Representative files that should exist after a successful build
jstargets = [
    NB_PATH / "index.js",
    MODULE_DIR / "lib/plugin.js",
]

data_files_spec = [
    (f"share/jupyter/nbextensions/{NAME}", NB_PATH, "*.js*"),
    ("share/jupyter/lab/extensions", LAB_PATH, "*.tgz"),
    ("etc/jupyter/nbconfig/notebook.d", MODULE_DIR, f"{NAME}.json"),
]

builder = npm_builder(path=MODULE_DIR, build_cmd="build:all")
cmdclass = wrap_installers(
    pre_develop=builder,
    pre_dist=builder,
    ensured_targets=jstargets,
)

setup(
    name=NAME.replace("_", "-"),
    version=get_version(Path(NAME) / "version.py"),
    license="BSD",
    author="Casper Welzel Andersen",
    author_email="casper+github@welzel.nu",
    cmdclass=cmdclass,
    description="Extensions to the Jupyter Widgets in the `ipywidgets` package.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/CasperWA/ipywidgets-extended",
    python_requires=">=3.7",
    packages=find_packages(),
    include_package_data=True,
    install_requires=BASE,
    extras_require={"dev": DEV},
    data_files=get_data_files(data_files_spec),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Jupyter",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Widget Sets",
    ],
)
