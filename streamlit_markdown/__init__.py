import os
from typing import List, Optional, Union

import streamlit.components.v1 as components

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

_RELEASE = True
COMPONENT_NAME = "streamlit_markdown"

# use the build instead of development if release is true
if _RELEASE:
    root_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(root_dir, "frontend/out")

    _markdown = components.declare_component(COMPONENT_NAME, path=build_dir)
else:
    _markdown = components.declare_component(COMPONENT_NAME, url="http://localhost:35335/component/streamlit_markdown.streamlit_markdown")


def streamlit_markdown(
    content: str,
    partial: bool = False,
    nTokens: Optional[int] = None,
    richContent: bool = True,
    background_color: Literal["blue", "orange", "green"] = "green",
    key=None,
    **kwargs,
):
    """
    Creates a new instance of streamlit-diff-viewer component

    Parameters
    ----------
    content: str
        The markdown content to be displayed
    partial: bool
        Whether to display the content partially
    nTokens: Optional[int]
        The number of tokens to display
    richContent: bool
        Whether to display rich content
    background_color: Literal["blue", "orange", "green"]
        The background color of the component
    key: Optional[str]
        An optional key that makes the component unique
        
    Returns: None
    """
    _markdown(
        background_color=background_color,
        content=content,
        partial=partial,
        nTokens=nTokens,
        richContent=richContent,
        key=key,
        **kwargs,
    )
