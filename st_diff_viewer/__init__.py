import os
from typing import List, Optional, Union

import streamlit.components.v1 as components

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

_RELEASE = True
COMPONENT_NAME = "st_diff_viewer"

# use the build instead of development if release is true
if _RELEASE:
    root_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(root_dir, "frontend/out")

    _diff_viewer = components.declare_component(COMPONENT_NAME, path=build_dir)
else:
    _diff_viewer = components.declare_component(COMPONENT_NAME, url="http://localhost:35335/component/st_diff_viewer.st_diff_viewer")


def diff_viewer(
    old_text: str,
    new_text: str,
    split_view: Optional[bool] = True,
    disabled_word_diff: Optional[bool] = False,
    left_title: Optional[str] = None,
    right_title: Optional[str] = None,
    use_dark_theme: Optional[bool] = False,
    extra_lines_surrounding_diff: Optional[int] = 3,
    hide_line_numbers: Optional[bool] = False,
    highlight_lines: Optional[List[str]] = [],
):
    """
    Creates a new instance of streamlit-diff-viewer component

    Parameters
    ----------
    old_text: str
        The old text to be compared
    new_text: str
        The new text to be compared
    split_view: bool
        If `True` will split the view in two columns, default is `True`.
    disabled_word_diff: bool
        If `True` will disable word diff, default is `False`.
    left_title: str or None
        The title for the left side of the component, default is None.
    right_title: str or None
        The title for the right side of the component, default is None.
    use_dark_theme: bool
        If `True` will use dark theme, default is `False`.
    extra_lines_surrounding_diff: int
        The number of extra lines to show surrounding the diff, default is 3.
    hide_line_numbers: bool
        If `True` will hide line numbers, default is `False`.
    highlight_lines: List[str]
        The lines to be highlighted, default is an empty list.

    Returns: None
    """
    _diff_viewer(
        oldText=old_text,
        newText=new_text,
        splitView=split_view,
        disabledWordDiff=disabled_word_diff,
        leftTitle=left_title,
        rightTitle=right_title,
        useDarkTheme=use_dark_theme,
        extraLinesSurroundingDiff=extra_lines_surrounding_diff,
        hideLineNumbers=hide_line_numbers,
        highlightLines=highlight_lines,
    )
