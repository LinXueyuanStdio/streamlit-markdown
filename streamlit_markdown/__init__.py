import os
import inspect
import time
from typing import Literal, Any, Callable, Generator, Literal, Optional, Union

import streamlit as st
from streamlit import _main
from streamlit_markdown.st_hack import st_hack_component

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
    _markdown = components.declare_component(
        COMPONENT_NAME,
        url="http://localhost:35335/component/streamlit_markdown.streamlit_markdown",
    )

GLOBAL_THEME_COLOR = Literal["blue", "orange", "green"]
MERMAID_THEME = Literal["default", "forest", "dark", "neutral", "base"]

def st_markdown(
    content: str,
    richContent: bool = True,
    theme_color: GLOBAL_THEME_COLOR = "green",
    mermaid_theme: MERMAID_THEME = "forest",
    mermaid_theme_CSS: Optional[str] = None,
    key=None,
    default: Any = None,
    **kwargs,
):
    """
    Creates a new instance of streamlit-markdown component

    Parameters
    ----------
    content: str
        The markdown content to be displayed
    richContent: bool
        Whether to display rich content
    theme_color: GLOBAL_THEME_COLOR
        The background color of the component
    mermaid_theme: MERMAID_THEME
        The theme of the mermaid diagram
    mermaid_theme_CSS: Optional[str]
        The CSS string to style the mermaid diagram. If set, mermaid_theme will be ignored
    key: Optional[str]
        An optional key that makes the component unique

    Returns: current text that already rendered to markdown
    """
    return _markdown(
        theme_color=theme_color,
        content=content,
        richContent=richContent,
        mermaid_theme=mermaid_theme,
        mermaid_theme_CSS=mermaid_theme_CSS,
        key=key,
        default=default,
        **kwargs,
    )


def st_hack_markdown(
    content: str,
    richContent: bool = True,
    theme_color: GLOBAL_THEME_COLOR = "green",
    mermaid_theme: MERMAID_THEME = "forest",
    mermaid_theme_CSS: Optional[str] = None,
    key=None,
    default: Any = None,
    **kwargs,
):
    """hack streamlt to prevent re-rendering or throw DuplicateWidgetID

    Args and Returns:
        same as st_markdown
    """
    kwargs["content"] = content
    kwargs["richContent"] = richContent
    kwargs["theme_color"] = theme_color
    kwargs["mermaid_theme"] = mermaid_theme
    kwargs["mermaid_theme_CSS"] = mermaid_theme_CSS
    return st_hack_component(_main, _markdown, key, default, **kwargs)


def st_streaming_markdown(
    token_stream: Union[Generator[str, str, str], Callable[[], str], str],
    richContent: bool = True,
    theme_color: GLOBAL_THEME_COLOR = "green",
    mermaid_theme: MERMAID_THEME = "forest",
    mermaid_theme_CSS: Optional[str] = None,
    key=None,
    default: Any = None,
    **kwargs,
):
    assert key is not None, "key must be provided to prevent re-rendering"
    placeholder = st.empty()
    # Order matters!
    if callable(token_stream):
        token_stream = token_stream()
    if isinstance(token_stream, str):
        placeholder.empty()
        with placeholder.container():
            st_hack_markdown(
                token_stream,
                richContent,
                theme_color,
                mermaid_theme,
                mermaid_theme_CSS,
                key=key,
                default=default,
                **kwargs,
            )
        return token_stream
    elif inspect.isgenerator(token_stream):
        content = ""
        for token in token_stream:
            if isinstance(token, str):
                content += token
            elif callable(token):
                content += token()
            else:
                raise TypeError(
                    f"token must be str or callable[() -> str], not {type(token)}"
                )
            placeholder.empty()
            with placeholder.container():
                st_hack_markdown(
                    content,
                    richContent,
                    theme_color,
                    mermaid_theme,
                    mermaid_theme_CSS,
                    key=key,
                    default=default,
                    **kwargs,
                )
        return content
    else:
        raise TypeError(
            f"token_stream must be generator or callable, not {type(token_stream)}"
        )


def simulated_token_stream(content):
    import random

    length = 0
    while length < len(content):
        n_chars = random.randint(5, 15)
        yield content[length : length + n_chars]
        length += n_chars
        time.sleep(0.05)


TEST_MARKDOWN_TEXT = """\
This is a table:

| Title | Description |
|-----------|-------------|
| text    | hello world |
| math  | $y=f(x)$ |
| bold  | **bold** |
| italics | _italics_ |
| herf  | [anchor](https://github.com) |

1. **Bold**: One
    - One, and latex $y=f(x)$
    - Two, and **bold**
2. **Bold**: Two
    - [ ] This is a task list.
    - [x] This is a checked task list.

> This is a blockquote.

This is inline latex $y=f(x)$ and below is a latex block:

$$y=f(x)$$

This is `inline` code and below is a code block:

```tsx
const Message = () => {
  return <div>hi</div>;
};
```

This is a mermaid diagram in a code block:

```mermaid
flowchart TD
    A[Christmas] -->|Get money| B(Go shopping)
    B --> C{Let me think}
    C -->|One| D[Laptop]
    C -->|Two| E[iPhone]
    C -->|Three| F[fa:fa-car Car]
```
"""
