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
    streaming = st.radio(
        "Streaming",
        [
            "static content",
            "streaming content",
            "streaming from server (built with FastAPI)",
        ],
        index=0,
    )
    richContent = st.checkbox("Rich Content", True)
    theme_color = st.selectbox("Theme Color", ["green", "blue", "orange", "red" , "purple" , "pink" , "indigo" , "yellow" , "teal" , "cyan" , "gray" , "slate" , "dark" , "light" , "null", "custom"])
    mermaid_theme = st.selectbox("Mermaid Theme", ["default", "forest", "dark", "neutral", "null"])
    mermaid_theme_CSS = st.text_area("Mermaid Theme CSS", height=120)
    if theme_color == "custom":
        custom_color = {
            "bg": st.text_input("Background Color", "bg-gray-100"),
            "border": st.text_input("Border Color", "border-gray-300"),
            "text": st.text_input("Text Color", "text-gray-900"),
            "hover:bg": st.text_input("Hover Background Color", "hover:bg-gray-200"),
            "hover:text": st.text_input("Hover Text Color", "hover:text-gray-900"),
        }
    else:
        custom_color = {
            "bg": "bg-gray-100",
            "border": "border-gray-300",
            "text": "text-gray-900",
            "hover:bg": "hover:bg-gray-200",
            "hover:text": "hover:text-gray-900",
        }
    with st.expander("Custom CSS"):
        st.warning("Leave empty to use theme_color system. If not empty, theme_color will be ignored and the customized css will replace **ALL** classNames.")
        custom_css = {
            "a_class": st.text_input("a class", ""),
            "h1_class": st.text_input("h1 class", ""),
            "h2_class": st.text_input("h2 class", ""),
            "h3_class": st.text_input("h3 class", ""),
            "h4_class": st.text_input("h4 class", ""),
            "h5_class": st.text_input("h5 class", ""),
            "h6_class": st.text_input("h6 class", ""),
            "p_class": st.text_input("p class", ""),
            "strong_class": st.text_input("strong class", ""),
            "em_class": st.text_input("em class", ""),
            "code_class": st.text_input("code class", ""),
            "code_button_class": st.text_input("code_button class", ""),
            "code_latex_class": st.text_input("code_latex class", ""),
            "code_mermaid_class": st.text_input("code_mermaid class", ""),
            "pre_class": st.text_input("pre class", ""),
            "ul_class": st.text_input("ul class", ""),
            "ol_class": st.text_input("ol class", ""),
            "li_class": st.text_input("li class", ""),
            "table_class": st.text_input("table class", ""),
            "thead_class": st.text_input("thead class", ""),
            "th_class": st.text_input("th class", ""),
            "td_class": st.text_input("td class", ""),
            "blockquote_class": st.text_input("blockquote class", ""),
        }

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
            mermaid_theme=mermaid_theme,
            mermaid_theme_CSS=mermaid_theme_CSS,
            custom_color=custom_color,
            custom_css=custom_css,
            key="streaming_from_server",
        )
    if streaming == "streaming content":
        token_stream = simulated_token_stream(content)
        final_content = st_streaming_markdown(
            token_stream,
            richContent=richContent,
            theme_color=theme_color,
            mermaid_theme=mermaid_theme,
            mermaid_theme_CSS=mermaid_theme_CSS,
            custom_color=custom_color,
            custom_css=custom_css,
            key="streaming_content",
        )
    else:
        final_content = st_markdown(
            content,
            richContent=richContent,
            theme_color=theme_color,
            mermaid_theme=mermaid_theme,
            mermaid_theme_CSS=mermaid_theme_CSS,
            custom_color=custom_color,
            custom_css=custom_css,
            key="content",
        )

    if final_content:
        st.balloons()
