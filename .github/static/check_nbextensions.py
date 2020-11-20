#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
from typing import List, Union


def assert_extension(extensions: List[str]) -> None:
    """Assert specific extension exists in the list of installed and enabled notebook extensions.

    "Validating: OK" will go to stderr, while the list of enabled extensions go to stdout.
    """
    extensions_list_call = subprocess.run(
        ["jupyter", "nbextension", "list"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    nbextensions = [
        _ for _ in extensions_list_call.stdout.decode().splitlines() if " " * 6 in _
    ]
    enabled_nbextensions = [_ for _ in nbextensions if "enabled" in _]
    validations = extensions_list_call.stderr.decode().splitlines()

    for extension in extensions:
        assert extension in "".join(
            nbextensions
        ), f"{extension!r} not found in list of installed Jupyter NB extensions: {extensions_list_call.stdout.decode()}"
        assert extension in "".join(
            enabled_nbextensions
        ), f"{extension!r} not found to be an enabled Jupyter NB extension: {extensions_list_call.stdout.decode()}"
        for index, nbextension in enumerate(nbextensions):
            if extension in nbextension:
                assert "OK" in validations[index], (
                    f"{extension!r} not found to be validated. Validations and output: "
                    f"{extensions_list_call.stderr.decode()}\n{extensions_list_call.stdout.decode()}"
                )
                break
        else:
            raise RuntimeError(
                f"By now, the extension {extension!r} should known to be an installed Jupyter NB "
                "extension, but was not found in the list of Jupyter NB extensions: "
                f"{extensions_list_call.stdout.decode()}"
            )


def get_extension_name(json_file: Union[str, Path]) -> List[str]:
    """Retrieve extension name from `json_file`"""
    if not isinstance(json_file, Path):
        json_file = Path(json_file).resolve()
    if not json_file.exists():
        raise RuntimeError(f"Could not find requested extension file at {json_file!r}")

    with open(json_file, "r") as handle:
        extension_file: dict = json.load(handle)

    return [_ for _ in extension_file.get("load_extensions", {})]


if __name__ == "__main__":
    extension_file = (
        Path(__file__)
        .resolve()
        .parent.parent.parent.joinpath("ipywidgets_extended.json")
    )
    extension = get_extension_name(extension_file)
    assert_extension(extension)
