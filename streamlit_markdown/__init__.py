import os
import inspect
import time
from typing import Literal, Any, Callable, Generator, Literal, Union

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


def st_markdown(
    content: str,
    richContent: bool = True,
    theme_color: Literal["blue", "orange", "green"] = "green",
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
    theme_color: Literal["blue", "orange", "green"]
        The background color of the component
    key: Optional[str]
        An optional key that makes the component unique

    Returns: current text that already rendered to markdown
    """
    return _markdown(
        theme_color=theme_color,
        content=content,
        richContent=richContent,
        key=key,
        default=default,
        **kwargs,
    )


def st_hack_markdown(
    content: str,
    richContent: bool = True,
    theme_color: Literal["blue", "orange", "green"] = "green",
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
    return st_hack_component(_main, _markdown, key, default, **kwargs)


def st_streaming_markdown(
    token_stream: Union[Generator[str, str, str], Callable[[], str], str],
    richContent: bool = True,
    theme_color: Literal["blue", "orange", "green"] = "green",
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
| reference  | cite[^1][^2] |

# Heading level 1

This is the first paragraph.

This is the second paragraph.

This is the third paragraph.

## Heading level 2

This is an [anchor](https://github.com).

### Heading level 3

This is **bold** and _italics_.

#### Heading level 4

This is an unordered list:

- One
- Two
- Three, and **bold**

This is an ordered list:

1. One
1. Two
1. Three

This is a complex list:

1. **Bold**: One
    - One
    - Two
    - Three

2. **Bold**: Three
    - One
    - Two
    - Three

3. **Bold**: Four
    - One
    - Two
    - Three

##### Heading level 5

> This is a blockquote.

- [ ] This is a task list.
- [x] This is a checked task list.

###### Heading level 6

This is `inline` code.

This is a code block:

```tsx
const Message = () => {
  return <div>hi</div>;
};
```

This is inline latex $y=f(x)$ and latex block:

$$y=f(x)$$

This is latex in code block:

```latex
F(x) = \\int_{a}^{b} f(x) \\, dx
```

This is a mermaid diagram:

```mermaid
sequenceDiagram
   autonumber
   participant 归档标准数据v1
   participant 归档配置planning
   actor 算法侧数据处理
   participant 预标注模型
   participant 工具执行
   participant 归档标准数据v2
   归档标准数据v1 ->> 算法侧数据处理: query, time, nlu
   归档配置planning ->> 算法侧数据处理: tools[develop], time_format
   归档配置planning ->> 算法侧数据处理: planning_prompt[develop]
   算法侧数据处理 ->>+ 预标注模型: planning_instruction[develop]
   loop 直到 ActionList==<Finished>
      预标注模型 ->>+ 工具执行:   Thought, ActionList
      工具执行   ->>- 预标注模型: Action, ActionInput, Observation, ObservationObejct
   end
   预标注模型 ->>- 算法侧数据处理: steps
   算法侧数据处理 ->> 归档标准数据v2: query, time, nlu, steps
```
"""
