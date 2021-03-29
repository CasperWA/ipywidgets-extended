"""Dropdown Widget Extension"""
from typing import Any, List, Tuple, Union

from ipywidgets.widgets.widget_selection import Dropdown, _make_options
from traitlets import traitlets

from ipywidgets_extended.version import __version__


__all__ = ("DropdownExtended",)


def _make_grouping(
    grouping: List[Tuple[str, List[str]]]
) -> Tuple[Tuple[str, Tuple[Tuple[str, Any]]]]:
    """Utilize `_make_options()` to set inner options in grouping"""
    return tuple([(header, _make_options(options)) for header, options in grouping])


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

    # Additional widget properties used in the TypeScript code
    _disabled_options_labels = traitlets.Tuple(
        trait=traitlets.Unicode(),
        read_only=True,
    ).tag(sync=True)
    _grouping_labels = traitlets.Tuple(
        trait=traitlets.Tuple(
            traitlets.Unicode(),
            traitlets.Tuple(traitlets.Unicode()),  # Similar to `_options_labels`
        ),
        read_only=True,
    ).tag(sync=True)

    # The equivalent Python changeable traits
    disabled_options = traitlets.List(
        traitlets.Unicode(),
        default_value=[],
        help="The labels for the disabled options.",
    )
    grouping = traitlets.Any(  # Similar to `options`
        default_value=(),
        help=(
            "Iterable of values, (header, ((label, value), (label, value), ...)), where the inner "
            "iterable of labels and values can be an iterable of values only, which will result "
            "in labels being auto-generated.\n\nAn empty string header can be used to implement "
            "ungrouped options."
        ),
    )
    _grouping_full: Tuple[Tuple[str, Tuple[Tuple[str, Any]]]] = None

    def __init__(self, *args, **kwargs):
        self._initializing_traits_ = True

        if "options" in kwargs and "grouping" in kwargs:
            raise ValueError(
                "Either `options` or `grouping` must be specified. Not both."
            )

        options = _make_options(kwargs.get("options", ()))
        disabled_options = kwargs.get("disabled_options", [])
        self.set_trait("_disabled_options_labels", tuple(disabled_options))
        grouping = _make_grouping(kwargs.get("grouping", ()))
        self._grouping_full = grouping
        self.set_trait(
            "_grouping_labels",
            tuple(
                [
                    (header, tuple([_[0] for _ in options]))
                    for header, options in grouping
                ]
            ),
        )

        # Ensure initialized 'index' is an enabled option (if possible)
        if (
            "index" not in kwargs
            and "value" not in kwargs
            and "label" not in kwargs
            and "grouping" in kwargs
        ):
            for index, option in enumerate(self._flat_groupings()):
                if option not in disabled_options and option not in self._group_headers:
                    kwargs["index"] = index
                    kwargs["label"], kwargs["value"] = self._get_grouping_label_value(
                        index
                    )
                    break
            else:
                kwargs["index"] = kwargs["label"] = kwargs["value"] = None
        elif (
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

        if "grouping" in kwargs:
            kwargs["options"] = self._create_grouping_options(grouping)
        super().__init__(*args, **kwargs)
        self._initializing_traits_ = True

        if "grouping" in kwargs:
            self._notify_trait(
                "_grouping_labels", self._grouping_labels, self._grouping_labels
            )

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
                if (
                    self.grouping
                    and self._flat_groupings()[self.index] in disabled_options
                ):
                    for index, label in enumerate(self._flat_groupings()):
                        if (
                            label not in disabled_options
                            and label not in self._group_headers
                        ):
                            self.index = index
                            break
                    else:
                        self.index = None
                elif self._options_labels[self.index] in disabled_options:
                    for index, label in enumerate(self._options_labels):
                        if label not in disabled_options:
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
    def _validate_grouping(self, proposal) -> Tuple[Tuple[str, List[str]]]:
        """Ensure all group headers are unique"""
        if proposal.value is None or not proposal.value:
            return ()
        assert len([_ for _ in proposal.value if _[0]]) == len(
            set([_[0] for _ in proposal.value if _[0]])
        ), (
            "Group headers must be unique (ignoring empty un-grouping headers - empty strings). "
            f"Passed group headers: {[_[0] for _ in proposal.value]}"
        )
        self._grouping_full = _make_grouping(proposal.value)
        return proposal.value

    @traitlets.observe("grouping")
    def _set_grouping(self, change) -> None:
        """Put options into desired grouping, updating `options`"""
        grouping = self._grouping_full
        self.options = self._create_grouping_options(grouping)
        self.set_trait(
            "_grouping_labels",
            tuple(
                [
                    (header, tuple([_[0] for _ in options]))
                    for header, options in grouping
                ]
            ),
        )
        if not self._initializing_traits_:
            for index, option in enumerate(self._flat_groupings()):
                if (
                    option not in self.disabled_options
                    and option not in self._group_headers
                ):
                    if self.index == index:
                        self._notify_trait("index", index, index)
                    else:
                        self.index = index
                    break
            else:
                self.index = None

    @property
    def _group_headers(self) -> List[str]:
        """Get group headers from self._grouping_labels"""
        return [_[0] for _ in self._grouping_labels]

    def _flat_groupings(
        self, grouping: Tuple[Tuple[str, Tuple[Any]]] = None
    ) -> List[Union[str, Any]]:
        """Get grouping similar to dropdown - a flat list of entries"""
        grouping = grouping if grouping is not None else self._grouping_labels

        res = []
        for header, options in grouping:
            if header:
                res.append(header)
            res.extend(options)
        return res

    def _get_grouping_label_value(
        self,
        index: int,
        grouping: Tuple[Tuple[str, Tuple[Tuple[str, Any]]]] = None,
    ) -> Tuple[str, Any]:
        """Return label,value-pair of grouping index.

        The index is expected to match `_flat_groupings`, i.e., the actual dropdown.
        """
        grouping = grouping if grouping is not None else self._grouping_full

        res = self._flat_groupings(grouping)[index]
        if len(res) == 1:
            return res, None
        return res

    @staticmethod
    def _create_grouping_options(
        grouping: Tuple[Tuple[str, Tuple[Tuple[str, Any]]]]
    ) -> Tuple[Tuple[str, Any]]:
        """Create and return a standard list of options from a grouping."""
        res = []
        for header, options in grouping:
            if header:
                res.append((header, None))
            res.extend(options)
        return res
