"""
IPyWidgets Extended

Extensions to the Jupyter Widgets in the `ipywidgets` pacakge.
"""
from .version import __version__, version_info  # noqa: F401
from .nbextension import _jupyter_nbextension_paths  # noqa: F401

from .dropdown import *  # noqa: F403

__all__ = dropdown.__all__  # noqa: F405
