from pathlib import Path
from setuptools import setup, find_packages

from setupbase import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    get_version,
)

MODULE_DIR = Path(__file__).resolve().parent

with open(MODULE_DIR.joinpath("README.md")) as handle:
    README = handle.read()

with open(MODULE_DIR.joinpath("requirements.txt")) as handle:
    BASE = [f"{_.strip()}" for _ in handle.readlines() if " " not in _]

with open(MODULE_DIR.joinpath("requirements_dev.txt")) as handle:
    DEV = [f"{_.strip()}" for _ in handle.readlines() if " " not in _]


NAME = "ipywidgets_extended"

NB_PATH = MODULE_DIR / NAME / "nbextension/static"
LAB_PATH = MODULE_DIR / NAME / "labextension"

# Representative files that should exist after a successful build
jstargets = [
    NB_PATH / "index.js",
    MODULE_DIR / "lib/plugin.js",
]

package_data_spec = {NAME: ["nbextension/static/*.*js*", "labextension/*.tgz"]}

data_files_spec = [
    (f"share/jupyter/nbextensions/{NAME}", NB_PATH, "*.js*"),
    ("share/jupyter/lab/extensions", LAB_PATH, "*.tgz"),
    ("etc/jupyter/nbconfig/notebook.d", MODULE_DIR, f"{NAME}.json"),
]


cmdclass = create_cmdclass(
    "jsdeps", package_data_spec=package_data_spec, data_files_spec=data_files_spec
)
cmdclass["jsdeps"] = combine_commands(
    install_npm(MODULE_DIR, build_cmd="build:all"),
    ensure_targets(jstargets),
)

setup(
    name="ipywidgets-extended",
    version=get_version(Path(NAME) / "version.py"),
    license="BSD",
    author="Casper Welzel Andersen",
    author_email="casper+github@welzel.nu",
    cmdclass=cmdclass,
    description="Extensions to the Jupyter Widgets in the `ipywidgets` pacakge.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/CasperWA/ipywidgets-extended",
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    install_requires=BASE,
    extras_require={"dev": DEV},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Jupyter",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Widget Sets",
    ],
)
