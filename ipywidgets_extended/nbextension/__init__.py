"""Related to jupyter nbextensions"""


def _jupyter_nbextension_paths():
    return [
        {
            "section": "notebook",
            "src": "nbextension/static",
            "dest": "ipywidgets_extended",
            "require": "ipywidgets_extended/extension",
        }
    ]
