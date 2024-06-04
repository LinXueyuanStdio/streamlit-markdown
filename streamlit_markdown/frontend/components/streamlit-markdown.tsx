import { Streamlit } from "streamlit-component-lib";
import { useRenderData, StreamlitProvider } from "streamlit-component-lib-react-hooks";
import React from 'react';
import { useState, useEffect } from 'react';
import MarkdownContent from '@/components/markdown-content';


function StreamlitMarkdown() {
  const { theme, disabled, args } = useRenderData();
  const [content, setContent] = useState("");
  const [live_socket_url, setSocketUrl] = useState("");

  useEffect(() => {
    const url = args.socket_url;
    if (!url) {
      return;
    }
    if (url === live_socket_url) {
      return;
    }
    // cancel previous socket connection
    if (live_socket_url) {
      const socket = new WebSocket(live_socket_url);
      socket.close();
    }
    setSocketUrl(url);
    const socket = new WebSocket(url);
    let buffer = "";
    socket.onmessage = (event) => {
      console.log(event);
      const data = event.data;
      console.log(data);
      buffer += data;
      setContent(buffer);
      Streamlit.setComponentValue(buffer);
    };
    socket.onerror = (event) => {
      console.error(event);
    }
    socket.onclose = (event) => {
      console.log(event);
      Streamlit.setComponentValue(content);
    }
  }, [live_socket_url, args.socket_url, content]);

  return (
    <div>
      <MarkdownContent
        theme_color={args.theme_color}
        content={args.content ?? content}
        richContent={args.richContent}
      />
    </div>
  );
}

export default StreamlitMarkdown;
