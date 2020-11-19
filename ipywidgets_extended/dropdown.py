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

    # This being read-only means that it cannot be changed by the user.
    _disabled_options_labels = traitlets.List(
        trait=traitlets.Unicode(),
        read_only=True,
        help="The labels for the disabled options.",
    ).tag(sync=True)

    disabled_options = traitlets.List([]).tag(sync=True)

    def __init__(self, *args, **kwargs):
        self._initializing_traits_ = True

        options = _make_options(kwargs.get("options", ()))
        disabled_options = kwargs.get("disabled_options", [])
        self.set_trait("_disabled_options_labels", disabled_options)

        # Ensure initialized 'index' is an enabled option (if possible)
        if (
            "index" not in kwargs
            and "value" not in kwargs
            and "label" not in kwargs
            and "disabled_options" in kwargs
        ):
            for index, option in enumerate(options):
                if option[0] not in disabled_options:
                    kwargs["index"] = index
                    kwargs["label"], kwargs["value"] = options[index]
                    break
            else:
                kwargs["index"] = kwargs["label"] = kwargs["value"] = None

        super().__init__(*args, **kwargs)
        self._initializing_traits_ = False

    @traitlets.validate("disabled_options")
    def _validate_disabled_options(self, proposal) -> List[str]:
        """Ensure disabled_options values are part of the list of options"""
        if proposal.value is None or not proposal.value:
            return []
        proposal_diff = set(proposal.value).difference_update(set(self._options_labels))
        assert (
            not proposal_diff
        ), f"Invalid passed options for 'disabled_options': {proposal_diff}"
        return proposal.value

    @traitlets.observe("disabled_options")
    def _set_disabled_options(self, change) -> None:
        """Ensure the widget is updated properly."""
        disabled_options = change.new
        self.set_trait("_disabled_options_labels", disabled_options)
        if not self._initializing_traits_:
            if disabled_options:
                if self._options_labels[self.index] in disabled_options:
                    for index, label in enumerate(self._options_labels):
                        if label not in disabled_options:
                            self.index = index
                            break
                    else:
                        self.index = None
            elif self._options_labels:
                if self.index == 0:
                    self._notify_trait("index", 0, 0)
                else:
                    self.index = 0
            else:
                self.index = None
