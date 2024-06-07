# streamlit-markdown

react-markdown with streaming support for streamlit webapp

![](./docs/head.png)

- [x] streaming rendering of markdown text
- [x] support for latex math
- [x] support for mermaid diagrams
- [x] support for code highlighting
- [x] support for tables
- [x] support for images
- [x] support for links

## Installation

```bash
pip install streamlit-markdown
```

## Usage

static content:

```python
from streamlit_markdown import st_markdown

markdown_text = "$ y = f(x)$"
st_markdown(markdown_text)
```

streaming content:

```python
from streamlit_markdown import st_streaming_markdown

markdown_text = "$ y = f(x)$"
def token_stream():
    for token in markdown_text:
        yeild token
st_streaming_markdown(token_stream, key="token_stream") # key must be set to prevent re-rendering
```

combined streaming content:

```python
from streamlit_markdown import st_streaming_markdown

markdown_text = "$ y = f(x)$"
def token_stream():
    import random
    for token in markdown_text:
        if random.rand() > 0.5:
            yeild token
        else:
            def callable_token():
                return token
            yeild callable_token
st_streaming_markdown(token_stream, key="token_stream") # key must be set to prevent re-rendering
```

run example:

```bash
streamlit run example.py
```

![img.png](./docs/img.png)

## Buiding from source

### Prerequisites

- nodejs >= 18.x
- yarn >= 1.22.x
- poetry >= 1.2.x
- python >= 3.8.x

### Building

```bash
./build.sh
```

### Publishing

```bash
poetry publish
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
