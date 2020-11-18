# Jupyter Widgets - Extended

This package contains widget extensions to the standard [`ipywidgets`](https://github.com/jupyter-widgets/ipywidgets) package.
The intent is to not produce completely new widgets, but rather _extend_ the widgets already in [`ipywidgets`](https://github.com/jupyter-widgets/ipywidgets) with more possibilities and options.

## Current extended widgets

### Dropdown

The dropdown widget has been extended to include the possibility of disabling options.

This can be done _via_ the `disabled_options` traitlet, which must be a list of option labels.
If an option label is included in the `disabled_options` list traitlet, it will be "grayed out", i.e., disabled (but still visible) in the dropdown widget.

**Author**: Casper Welzel Andersen ([email](casper+github@welzel.nu), [website](https://casper.welzel.nu)).  
**License**: [BSD-3-Clause](LICENSE) and copyright (c) 2020 Casper Welzel Andersen & parts by Jupyter Development Team.
