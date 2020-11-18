from pathlib import Path
import re
import sys
from typing import Tuple

from invoke import task


TOP_DIR = Path(__file__).parent.resolve()


def update_file(filename: str, sub_line: Tuple[str, str], strip: str = None):
    """Utility function for tasks to read, update, and write files"""
    with open(filename, "r") as handle:
        lines = [
            re.sub(sub_line[0], sub_line[1], line.rstrip(strip)) for line in handle
        ]

    with open(filename, "w") as handle:
        handle.write("\n".join(lines))
        handle.write("\n")


@task
def update_version(_, version):
    """Update package version using SemVer"""
    if version.startswith("v"):
        version = version[1:]

    if re.match(r"[0-9]+(\.[0-9]+){2}.*", version) is None:
        sys.exit(
            f"Error: Passed version ({version}) does to match semantic versioning."
        )

    update_file(
        TOP_DIR.joinpath("ipywidgets_extended/version.py"),
        (
            r"version_info = .+",
            f"version_info = {tuple([int(_) for _ in version.split('.')[:3]])}",
        ),
    )
    update_file(
        TOP_DIR.joinpath("package.json"),
        (r'"version": ".+"', f'"version": "{version}"'),
    )

    print(f"Bumped version to {version} !")
