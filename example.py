import streamlit as st
from streamlit_markdown import (
    st_markdown,
    st_streaming_markdown,
    simulated_token_stream,
    TEST_MARKDOWN_TEXT,
)

st.set_page_config(
    layout="wide",
    page_title="streamlit-markdown",
)
st.title("streamlit-markdown")

left, right = st.columns(2)
with left:
    a, b, c = st.columns(3)
    streaming = a.radio(
        "Streaming",
        [
            "static content",
            "streaming content",
            "streaming from server (built with FastAPI)",
        ],
        index=0,
    )
    richContent = b.checkbox("Rich Content", True)
    theme_color = c.selectbox("Theme Color", ["blue", "orange", "green"])
    content = st.text_area("Markdown", TEST_MARKDOWN_TEXT, height=480)
with right:
    if streaming == "streaming from server (built with FastAPI)":
        def remote_token_stream():
            import requests
            response = requests.get(
                "http://localhost:8000/simulated_token_stream",
                params={"text": content},
                headers={"accept": "application/json"},
                stream=True,
            )
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    token = str(chunk, encoding="utf-8")
                    yield token
        final_content = st_streaming_markdown(
            remote_token_stream(),
            richContent=richContent,
            theme_color=theme_color,
            key="streaming_from_server",
        )
    if streaming == "streaming content":
        token_stream = simulated_token_stream(content)
        final_content = st_streaming_markdown(
            token_stream,
            richContent=richContent,
            theme_color=theme_color,
            key="streaming_content",
        )
    else:
        final_content = st_markdown(
            content,
            richContent=richContent,
            theme_color=theme_color,
            key="content",
        )

    if final_content:
        st.balloons()
