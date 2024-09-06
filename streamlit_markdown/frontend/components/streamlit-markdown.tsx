import { useRenderData } from "streamlit-component-lib-react-hooks";
import React from 'react';
import MarkdownContent from '@/components/markdown-content';

function StreamlitMarkdown() {
  const { theme, disabled, args } = useRenderData();

  return (
    <div>
      <MarkdownContent
        theme_color={args.theme_color}
        content={args.content}
        richContent={args.richContent}
        mermaid_theme_CSS={args.mermaid_theme_CSS}
        mermaid_theme={args.mermaid_theme}
      />
    </div>
  );
}

export default StreamlitMarkdown;
