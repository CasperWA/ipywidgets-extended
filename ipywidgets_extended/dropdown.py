"""Dropdown Widget Extension"""
from typing import List, Tuple

from ipywidgets.widgets.widget_selection import Dropdown, _make_options
from traitlets import traitlets

from ipywidgets_extended.version import __version__


__all__ = ("DropdownExtended",)


class DropdownExtended(Dropdown):
    """Extended Widget of Dropdown

    Extensions:
    - Disable individual options.
    - Create groupings within the dropdown.

    """

    _model_name = traitlets.Unicode("DropdownExtendedModel").tag(sync=True)
    _model_module = traitlets.Unicode("ipywidgets-extended").tag(sync=True)
    _model_module_version = traitlets.Unicode(f"^{__version__}").tag(sync=True)
    _view_name = traitlets.Unicode("DropdownExtendedView").tag(sync=True)
    _view_module = traitlets.Unicode("ipywidgets-extended").tag(sync=True)
    _view_module_version = traitlets.Unicode(f"^{__version__}").tag(sync=True)

    # Additional widget properties used in the TS
    _disabled_options_labels = traitlets.List(
        trait=traitlets.Unicode(),
        read_only=True,
        help="The labels for the disabled options.",
    ).tag(sync=True)
    _grouping_labels = traitlets.List(
        traitlets.Tuple(traitlets.Unicode(), traitlets.List(traitlets.Unicode())),
        read_only=True,
        help=(
            "List of tuples for groupings, where the first value in the tuple is the grouping "
            "header and the second value is a list of the labels in the grouping."
        ),
    ).tag(sync=True)

    # The equivalent Python changeable traits
    disabled_options = traitlets.List(traitlets.Unicode(), default_value=[])
    grouping = traitlets.List(
        traitlets.Tuple(
            traitlets.Unicode(),
            traitlets.List(traitlets.Unicode()),
        ),
        default_value=[],
    )

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
                grouping_entries = range(
                    sum(len(_) + 1 for _ in dict(self._grouping_labels).values())
                )
                if self._options_labels[self.index] in disabled_options:
                    for index, label in enumerate(self._options_labels):
                        if label not in disabled_options:
                            self.index = index
                            break
                    else:
                        self.index = None
                elif grouping_entries[self.index] in disabled_options:
                    for index, label in enumerate(grouping_entries):
                        if (
                            label not in disabled_options
                            and label not in self._group_headers
                        ):
                            self.index = index
                            break
                    else:
                        self.index = None
            elif self._options_labels and not self._grouping_labels:
                if self.index == 0:
                    self._notify_trait("index", 0, 0)
                else:
                    self.index = 0
            else:
                self.index = None

    @traitlets.validate("grouping")
    def _validate_grouping(self, proposal) -> List[Tuple[str, List[str]]]:
        """Ensure all group headers are unique"""
        if proposal.value is None or not proposal.value:
            return []
        assert len(proposal.value) == len(
            dict(proposal.value).keys()
        ), f"Group headers must be unique. Passed group headers: {[_[0] for _ in proposal.value]}"
        return proposal.value

    @traitlets.observe("grouping")
    def _set_grouping(self, change) -> None:
        """Put options into desired grouping, updating `options`"""
        grouping = change.new
        self.set_trait("_grouping_labels", grouping)
        if not self._initializing_traits_:
            if not grouping and self._options_labels:
                if self.index == 0:
                    self._notify_trait("index", 0, 0)
                else:
                    self.index = 0
            else:
                self.index = None

    @property
    def _group_headers(self) -> List[str]:
        """Get group headers from self._grouping_labels"""
        return [_[0] for _ in self._grouping_labels]
