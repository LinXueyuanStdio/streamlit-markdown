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
      />
    </div>
  );
}

export default StreamlitMarkdown;
