"""Dropdown Widget Extension"""
from typing import List

from ipywidgets.widgets.widget_selection import Dropdown, _make_options
from traitlets import traitlets

from ipywidgets_extended.version import __version__


__all__ = ("DropdownExtended",)


class DropdownExtended(Dropdown):
    """Extended Widget of Dropdown

    Extensions:
    - Disable individual options.

    """

    _model_name = traitlets.Unicode("DropdownExtendedModel").tag(sync=True)
    _model_module = traitlets.Unicode("ipywidgets-extended").tag(sync=True)
    _model_module_version = traitlets.Unicode(__version__).tag(sync=True)
    _view_name = traitlets.Unicode("DropdownExtendedView").tag(sync=True)
    _view_module = traitlets.Unicode("ipywidgets-extended").tag(sync=True)
    _view_module_version = traitlets.Unicode(__version__).tag(sync=True)

    disabled_options = traitlets.List([]).tag(sync=True)

    def __init__(self, *args, **kwargs):
        options = _make_options(kwargs.get("options", ()))

        # Ensure initialized 'index' is an enabled option (if possible)
        if (
            "index" not in kwargs
            and "value" not in kwargs
            and "label" not in kwargs
            and "disabled_options" in kwargs
        ):
            for index, option in enumerate(options):
                if option[0] not in kwargs["disabled_options"]:
                    kwargs["index"] = index
                    kwargs["label"], kwargs["value"] = options[index]
                    break
            else:
                if options:
                    kwargs["index"] = kwargs["label"] = kwargs["value"] = None

        super().__init__(*args, **kwargs)
        self._initializing_traits_ = False

    @traitlets.validate("disabled_options")
    def _validate_disabled_options(self, proposal: dict) -> List[str]:
        """Ensure disabled_options values are part of the list of options"""
        if proposal.value is None:
            return []
        proposal_diff = set(proposal.value).difference_update(set(self._options_labels))
        assert (
            not proposal_diff
        ), f"Invalid passed options for 'disabled_options': {proposal_diff}"
        return proposal.value
