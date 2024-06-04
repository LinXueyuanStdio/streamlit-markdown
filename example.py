import random
import time
import uuid
import streamlit as st
import requests

from streamlit_markdown import st_markdown

markdown_text = """
This is a table:

| Title | Description |
|-----------|-------------|
| text    | hello world |
| math  | $y=f(x)$ |
| reference  | cite[^1][^2] |

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

```latex
F(x) = \\int_{a}^{b} f(x) \\, dx
```

行内数学公式 $y=f(x)$ 自变量为 $x$，因变量为 $y$。

$$y=f(x)$$

# Heading level 1

This is the first paragraph.

This is the second paragraph.

This is the third paragraph.

## Heading level 2

This is an [anchor](https://github.com).

### Heading level 3

This is **bold** and _italics_.

#### Heading level 4

This is `inline` code.

This is a code block:

```tsx
const Message = () => {
  return <div>hi</div>;
};
```

##### Heading level 5

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

###### Heading level 6

> This is a blockquote.

"""

content = st.text_area("Markdown", markdown_text, height=250)
a, b, c = st.columns(3)
streaming = a.checkbox("Streaming", False)
richContent = b.checkbox("Rich Content", True)
theme_color = c.selectbox("Theme Color", ["blue", "orange", "green"])
remote_streaming = a.checkbox("Remote Streaming", False)

if not streaming:
    st_markdown(
        content,
        richContent=richContent,
        theme_color=theme_color,
        key="content",
    )
elif remote_streaming:
    buffer = ""
    for chunk in requests.get("http://localhost:8000", stream=True):
        print(chunk)
        buffer += chunk.decode()
        with st.empty():
            st_markdown(
                buffer,
                richContent=richContent,
                theme_color=theme_color,
            )
    # 1. bind to a socket
    # content_id = uuid.uuid4().hex
    # socket_url = f"ws://localhost:8000/content?id={content_id}"
    # st_markdown(
    #     None,
    #     richContent=richContent,
    #     theme_color=theme_color,
    #     key="content",
    #     socket_url=socket_url + "&server=0",
    # )
    # 2. write to the socket
    # from websocket import create_connection

    # ws = create_connection(socket_url + "&server=1")
    # length = 0
    # while length < len(content):
    #     next_length = length + random.randint(2, 10)
    #     # ws.send({"content": content[length : next_length]})
    #     ws.send_text(content[length : next_length])
    #     length = next_length
    #     time.sleep(0.1)
    # ws.close()
else:
    if "n_chars" not in st.session_state:
        st.session_state.n_chars = 1

    st_markdown(
        content[: st.session_state.n_chars],
        richContent=richContent,
        theme_color=theme_color,
        key="content",
    )

    # Simulate streaming
    if st.session_state.n_chars < len(content):
        st.session_state.n_chars += random.randint(1, 5)
        time.sleep(0.05)
        st.rerun()
    else:
        st.session_state.n_chars = 1
        st.rerun()
