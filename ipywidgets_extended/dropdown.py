from typing import List

from ipywidgets._version import __jupyter_widgets_controls_version__
from ipywidgets.widgets.widget_selection import Dropdown
from traitlets import traitlets

from ipywidget_extended.version import __version__


__all__ = ("DropdownExtended",)


class DropdownExtended(Dropdown):
    """Extended Widget of Dropdown

    Extensions:
    - Disable individual options.

    """

    _model_name = traitlets.Unicode("DropdownModel").tag(sync=True)
    _model_module = traitlets.Unicode("@jupyter-widgets/controls").tag(sync=True)
    _model_module_version = traitlets.Unicode(__jupyter_widgets_controls_version__).tag(
        sync=True
    )
    _view_name = traitlets.Unicode("DropdownExtendedView").tag(sync=True)
    _view_module = traitlets.Unicode("optimade-client").tag(sync=True)
    _view_module_version = traitlets.Unicode(__version__).tag(sync=True)

    disabled_options = traitlets.List([]).tag(sync=True)

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
