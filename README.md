# Jupyter Widgets - Extended

This package contains widget extensions to the standard [`ipywidgets`](https://github.com/jupyter-widgets/ipywidgets) package.
The intent is to not produce completely new widgets, but rather _extend_ the widgets already in [`ipywidgets`](https://github.com/jupyter-widgets/ipywidgets) with more possibilities and options.

## Current extended widgets

### Dropdown

The dropdown widget has been extended to include the possibility of:

- disabling options; and
- grouping the options.

#### Disabling

This can be done *via* the `disabled_options` traitlet, which must be a list of option labels.
If an option label is included in the `disabled_options` list traitlet, it will be "grayed out", i.e., disabled (but still visible) in the dropdown widget.

#### Grouping

Using the `grouping` parameter *instead of* the `options` parameter, options can be grouped as desired.
The format is similar to the value for `options`, but each grouping of options should be paired with a header, i.e., you'll the value to be an iterable of (header, `options`)-pairs.

One can introduce un-grouped options by passing an empty header, i.e., an empty string (`""`).

## About

**Author**: Casper Welzel Andersen ([email](casper+github@welzel.nu), [website](https://casper.welzel.nu)).  
**License**: [BSD-3-Clause](LICENSE) and copyright (c) 2020 Casper Welzel Andersen & parts by Jupyter Development Team.
